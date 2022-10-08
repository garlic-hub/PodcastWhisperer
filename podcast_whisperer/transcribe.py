import whisper
from typing import Dict


def transcribe_file(file: str) -> Dict:
    model = whisper.load_model('small')
    result = model.transcribe(file)
    return result
