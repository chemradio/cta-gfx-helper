from io import BytesIO
import secrets
from pathlib import Path

from pydub import AudioSegment


async def convert_audio_to_wav(file_bytesio: BytesIO) -> BytesIO:
    audio_segment = AudioSegment.from_file(file_bytesio)
    temp_path = Path.cwd() / f"{secrets.token_hex(8)}.wav"
    audio_segment.export(temp_path, format="wav")
    with open(temp_path, "rb") as f:
        wav_raw = f.read()
    temp_path.unlink()
    return BytesIO(wav_raw)
