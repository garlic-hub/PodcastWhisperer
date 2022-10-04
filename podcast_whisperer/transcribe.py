import whisper
from typing import Dict


def transcribe_file(file: str) -> Dict:
    model = whisper.load_model('tiny.en')
    result = model.transcribe(file, language='english')
    return result
