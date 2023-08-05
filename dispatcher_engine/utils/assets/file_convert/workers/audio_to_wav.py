import io
import secrets
from pathlib import Path

from fastapi import UploadFile
from pydub import AudioSegment


async def convert_audio_to_wav(file: UploadFile) -> bytes:
    file_raw = file.file.read()
    audio_segment = AudioSegment.from_file(io.BytesIO(file_raw))
    temp_path = Path.cwd() / f"{secrets.token_hex(8)}.wav"
    audio_segment.export(temp_path, format="wav")
    with open(temp_path, "rb") as f:
        wav_raw = f.read()
    temp_path.unlink()
    return wav_raw
