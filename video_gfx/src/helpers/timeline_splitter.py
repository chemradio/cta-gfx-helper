def split_timeline_segments(
    total_frames: int, pieces: int = 3
) -> list[tuple[int, int]]:
    """Given a total number of frames, split them into pieces
    and return a list of tuples representing the ranges
    of frames for each piece. The last piece will have the
    remaining frames if the total number of frames is not
    divisible by the number of pieces."""

    if pieces == 1:
        return [(0, total_frames - 1)]

    ranges = list()
    block_length = int(total_frames / pieces)

    start_index = 0

    for _ in range(pieces):
        end_index = start_index + block_length - 1
        ranges.append((start_index, end_index))
        start_index = end_index + 1
    else:
        if start_index < total_frames:
            ranges[-1] = (ranges[-1][0], total_frames - 1)

    return ranges
