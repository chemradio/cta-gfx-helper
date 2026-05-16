"""Stitch the per-segment video files produced by the Playwright capture
pipeline into the final video.

All segments are encoded with identical parameters (see
``frame_extractor/playwright_capture.build_video_encode_args``), so the ffmpeg
``concat`` demuxer joins them with ``-c copy`` — no video re-encode, no quality
loss at the seams. Audio, if present, is muxed in afterwards without touching
the video stream.

Counterpart of ``png_stitcher.stitch_images`` for the playwright backend.
"""

import subprocess
import time
from pathlib import Path

from py_gfxhelper_lib.files import AssetFile


def _log(message: str) -> None:
    print(f"[playwright concat] {time.strftime('%H:%M:%S')} {message}", flush=True)


def _run_ffmpeg(args: list[str]) -> None:
    """Run ffmpeg with stderr inherited so its logs surface in docker compose."""
    _log("running: " + " ".join(args))
    started_at = time.perf_counter()
    subprocess.run(args, check=True)
    _log(f"ffmpeg ok ({time.perf_counter() - started_at:.1f}s)")


def concat_segments(
    segment_paths: list[Path],
    audio_file: AssetFile | None,
    output_path: Path,
    audio_delay: float = 0.3,
) -> Path:
    """Concatenate ``segment_paths`` (in playback order) into ``output_path``,
    muxing ``audio_file`` in when supplied. Returns ``output_path``."""
    work_dir = output_path.parent
    _log(f"concat {len(segment_paths)} segment(s) | audio={audio_file is not None}")
    for segment_path in segment_paths:
        size = segment_path.stat().st_size if segment_path.exists() else "MISSING"
        _log(f"  segment {segment_path.name}: {size} bytes")

    # concat demuxer input list: one `file '...'` line per segment
    concat_list_path = work_dir / "segments.txt"
    with open(concat_list_path, "wt") as concat_list:
        for segment_path in segment_paths:
            concat_list.write(f"file '{segment_path.resolve()}'\n")

    if not audio_file:
        _run_ffmpeg(
            [
                "ffmpeg", "-y", "-loglevel", "info",
                "-f", "concat", "-safe", "0",
                "-i", str(concat_list_path),
                "-c", "copy",
                str(output_path),
            ]
        )
        _log(f"done -> {output_path}")
        return output_path

    # stitch the video first, then mux audio in a copy-only pass
    concat_video_path = work_dir / "concat.mp4"
    _run_ffmpeg(
        [
            "ffmpeg", "-y", "-loglevel", "info",
            "-f", "concat", "-safe", "0",
            "-i", str(concat_list_path),
            "-c", "copy",
            str(concat_video_path),
        ]
    )

    audio_extension = audio_file.filename.split(".")[-1].lower()
    audio_path = work_dir / f"audio_file.{audio_extension}"
    with open(audio_path, "wb") as audio_out:
        audio_out.write(audio_file.bytesio.read())
    _log(f"wrote audio {audio_path} ({audio_path.stat().st_size} bytes)")

    _run_ffmpeg(
        [
            "ffmpeg", "-y", "-loglevel", "info",
            "-i", str(concat_video_path),
            "-itsoffset", str(audio_delay), "-i", str(audio_path),
            "-c:v", "copy",
            "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "1",
            str(output_path),
        ]
    )
    _log(f"done -> {output_path}")
    return output_path
