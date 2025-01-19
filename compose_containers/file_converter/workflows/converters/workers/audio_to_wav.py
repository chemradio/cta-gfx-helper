from io import BytesIO
from pydub import AudioSegment


async def convert_audio_to_wav(file_bytesio: BytesIO) -> BytesIO:
    audio_segment = AudioSegment.from_file(file_bytesio)
    audio_bytesio = BytesIO()
    audio_segment.export(audio_bytesio, format="wav")
    return audio_bytesio
