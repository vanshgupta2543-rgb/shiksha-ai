import tempfile
import os
from faster_whisper import WhisperModel

model = None

def load_model():
    global model
    if model is None:
        model = WhisperModel("base", device="cpu", compute_type="int8")
    return model

def transcribe(audio_bytes: bytes) -> str:
    m = load_model()
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        f.write(audio_bytes)
        tmp_path = f.name
    try:
        segments, _ = m.transcribe(tmp_path, language="hi")
        text = " ".join(seg.text for seg in segments).strip()
    finally:
        os.unlink(tmp_path)
    return text