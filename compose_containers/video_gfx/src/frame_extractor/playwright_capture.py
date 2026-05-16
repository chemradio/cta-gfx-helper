"""Playwright-based frame capture with image2pipe streaming.

The selenium backend (``png_capture.py``) writes every animation frame to disk
as a PNG and lets ffmpeg glob the folder afterwards. This backend instead
renders the animation in a headless Chromium page and streams each frame's PNG
bytes straight into a per-segment ffmpeg encoder over ``image2pipe`` — so no PNG
sequence ever touches disk.

The timeline is split into ``worker_count`` contiguous frame ranges; each range
is captured by its own process and encoded into a standalone ``.mp4`` segment.
``segment_stitcher.concat_segments`` later stitches the segments losslessly.

Used when ``config.FRAME_CAPTURE_BACKEND == "playwright"``.
"""

import json
import multiprocessing
import subprocess
import sys
import time
import traceback
from pathlib import Path

from playwright.sync_api import sync_playwright

from src.helpers import linear_interpolation, split_timeline_segments

# Hard ceiling on a single capture run. Past this the workers are killed and
# the order fails loudly instead of hanging the queue forever.
CAPTURE_TIMEOUT_SECONDS = 600


def _log(tag: str, message: str) -> None:
    """Timestamped, flushed log line — flushing matters because capture workers
    are separate processes and docker compose only shows flushed stdout."""
    print(f"[playwright {tag}] {time.strftime('%H:%M:%S')} {message}", flush=True)


def build_video_encode_args(width: int, height: int) -> list[str]:
    """ffmpeg video-encode flags, kept identical to the selenium/PNG path
    (see ``frames_to_video/png_stitcher.py``) so a segment is byte-compatible
    with that pipeline's output and segments concat without re-encoding."""
    return [
        "-s", f"{width}x{height}",
        "-crf", "13",
        "-vcodec", "libx264",
        "-pix_fmt", "yuv420p",
        "-color_range", "1",
        "-movflags", "+write_colr",
        "-vf", "scale=out_color_matrix=bt709:out_range=limited",
        "-bsf:v", "h264_metadata=video_full_range_flag=0",
    ]


def _capture_segment(
    worker_index: int,
    total_frames: int,
    range_tuple: tuple[int, int],
    segment_path: Path,
    target_url: str,
    frame_width: int,
    frame_height: int,
    framerate: int | float,
) -> None:
    """Worker process: render frames ``[start, end]`` and pipe each one into a
    dedicated ffmpeg encoder, producing a single video-only segment ``.mp4``."""
    tag = f"w{worker_index}"
    start_frame, end_frame = range_tuple
    frame_count = end_frame - start_frame + 1
    interpolation_data = [[0, 0], [total_frames, 1]]
    started_at = time.perf_counter()

    try:
        _log(tag, f"worker start | frames {start_frame}-{end_frame} ({frame_count})")
        _log(tag, f"viewport {frame_width}x{frame_height} | target {target_url}")

        ffmpeg_cmd = [
            "ffmpeg", "-y", "-loglevel", "info",
            "-f", "image2pipe",
            "-framerate", str(framerate),
            "-i", "pipe:0",
            *build_video_encode_args(frame_width, frame_height),
            str(segment_path),
        ]
        _log(tag, f"launching ffmpeg: {' '.join(ffmpeg_cmd)}")
        ffmpeg_proc = subprocess.Popen(
            ffmpeg_cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            # stderr inherited -> ffmpeg's own logs show up in docker compose
            stderr=None,
        )
        _log(tag, f"ffmpeg started (pid {ffmpeg_proc.pid})")

        with sync_playwright() as playwright:
            _log(tag, "launching chromium...")
            browser = playwright.chromium.launch(
                headless=True,
                args=[
                    "--no-sandbox",
                    "--disable-gpu",
                    # plain containers have a tiny /dev/shm; without this
                    # Chromium can hang or crash mid-render
                    "--disable-dev-shm-usage",
                ],
            )
            _log(tag, "chromium launched, opening page")
            page = browser.new_page(
                viewport={"width": frame_width, "height": frame_height},
                device_scale_factor=1,
            )

            _log(tag, f"page.goto({target_url})")
            page.goto(target_url)
            _log(tag, "goto returned, waiting 2000ms")
            page.wait_for_timeout(2000)

            _log(tag, "pressing Enter")
            page.keyboard.press("Enter")
            page.wait_for_timeout(3000)

            # sanity-check the animation timeline the page is expected to expose
            timeline_type = page.evaluate("typeof timeline")
            _log(tag, f"typeof timeline == {timeline_type!r}")
            if timeline_type == "undefined":
                raise RuntimeError(
                    "page global `timeline` is undefined - animation not ready"
                )

            # seek to the start of this segment's range and let it settle.
            # NB: the evaluate body is a *statement* block (no return) - GSAP's
            # timeline.progress() returns the timeline object, and letting
            # Playwright serialize that circular structure back to Python hangs.
            start_progress = linear_interpolation(interpolation_data, start_frame)
            _log(tag, f"seeking to start progress {start_progress}")
            page.evaluate("(p) => { timeline.progress(p); }", start_progress)
            page.wait_for_timeout(1000)

            _log(tag, "begin frame capture loop")
            for frame in range(start_frame, end_frame + 1):
                progress = linear_interpolation(interpolation_data, frame)
                page.evaluate("(p) => { timeline.progress(p); }", progress)
                png_bytes = page.screenshot(type="png")
                ffmpeg_proc.stdin.write(png_bytes)
                done = frame - start_frame + 1
                if done == 1 or done % 25 == 0 or frame == end_frame:
                    _log(
                        tag,
                        f"frame {frame} ({done}/{frame_count}) "
                        f"{len(png_bytes)} bytes",
                    )

            _log(tag, "capture loop done, closing browser")
            browser.close()

        _log(tag, "closing ffmpeg stdin, waiting for encode to finish")
        ffmpeg_proc.stdin.close()
        return_code = ffmpeg_proc.wait()
        elapsed = time.perf_counter() - started_at
        _log(tag, f"ffmpeg exited code {return_code} after {elapsed:.1f}s")
        if return_code != 0:
            raise RuntimeError(
                f"ffmpeg segment encode failed (code {return_code}) for "
                f"{segment_path.name}"
            )
        _log(tag, f"worker done -> {segment_path}")
    except Exception:
        _log(tag, "WORKER FAILED:\n" + traceback.format_exc())
        # non-zero exit so the parent can detect the failure
        sys.exit(1)


def capture_segments(
    html_assembly_path: Path,
    framerate: int | float,
    assembly_server_url: str,
    worker_count: int,
) -> list[Path]:
    """Render the whole HTML/GSAP animation as ``worker_count`` video segments
    in parallel. Returns the segment paths in playback order."""
    _log("main", f"capture_segments start | assembly {html_assembly_path.name}")
    target_url = f"{assembly_server_url}/storage/{html_assembly_path.name}/main.html"

    with open(html_assembly_path / "config.json", "rt") as config_file:
        animation_config = json.load(config_file)
    timeline_duration = animation_config["animationDuration"]
    vertical_resolution = int(animation_config["verticalResolution"])

    frame_width = int(vertical_resolution / 9 * 16)
    frame_height = vertical_resolution

    total_frames = int(timeline_duration * framerate)
    ranges = split_timeline_segments(total_frames, pieces=worker_count)
    _log(
        "main",
        f"duration {timeline_duration}s @ {framerate}fps = {total_frames} frames | "
        f"{worker_count} workers | ranges {ranges}",
    )

    segments_dir = html_assembly_path / "segments"
    segments_dir.mkdir(exist_ok=True)

    workers: list[multiprocessing.Process] = []
    segment_paths: list[Path] = []
    for index, frame_range in enumerate(ranges):
        segment_path = segments_dir / f"segment_{index:02}.mp4"
        segment_paths.append(segment_path)
        workers.append(
            multiprocessing.Process(
                target=_capture_segment,
                args=(
                    index,
                    total_frames,
                    frame_range,
                    segment_path,
                    target_url,
                    frame_width,
                    frame_height,
                    framerate,
                ),
            )
        )

    for index, worker in enumerate(workers):
        worker.start()
        _log("main", f"started worker w{index} (pid {worker.pid})")

    deadline = time.monotonic() + CAPTURE_TIMEOUT_SECONDS
    for index, worker in enumerate(workers):
        remaining = deadline - time.monotonic()
        worker.join(timeout=max(remaining, 0))
        if worker.is_alive():
            _log(
                "main",
                f"TIMEOUT after {CAPTURE_TIMEOUT_SECONDS}s - killing all workers",
            )
            for alive in workers:
                if alive.is_alive():
                    alive.terminate()
            for alive in workers:
                alive.join()
            raise RuntimeError(
                f"Playwright capture timed out after {CAPTURE_TIMEOUT_SECONDS}s"
            )
        _log("main", f"worker w{index} joined (exitcode {worker.exitcode})")

    failed = [
        index
        for index, worker in enumerate(workers)
        if worker.exitcode != 0 or not segment_paths[index].exists()
    ]
    if failed:
        raise RuntimeError(f"Playwright capture failed for segment(s): {failed}")

    _log("main", "capture_segments done")
    return segment_paths
