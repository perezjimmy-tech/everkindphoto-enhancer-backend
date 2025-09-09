import os
import urllib.request
from pathlib import Path

WEIGHTS_DIR = Path("weights")
WEIGHTS_FILE = WEIGHTS_DIR / "RealESRGAN_x4.pth"
DOWNLOAD_URL = (
    "https://github.com/xinntao/Real-ESRGAN/"
    "releases/download/v0.1.0/RealESRGAN_x4.pth"
)

def ensure_weights_folder() -> None:
    WEIGHTS_DIR.mkdir(exist_ok=True)

def download_weights() -> None:
    if WEIGHTS_FILE.exists():
        return
    print("Descargando modelo RealESRGAN_x4.pth (~67 MB)...")
    urllib.request.urlretrieve(DOWNLOAD_URL, WEIGHTS_FILE)
    print("Descarga completada.")