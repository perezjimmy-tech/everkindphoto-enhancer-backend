import io
import numpy as np
from PIL import Image, ImageEnhance
from realesrgan import RealESRGAN
from insightface.app import FaceAnalysis
import torch

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

class PhotoEnhancer:
    def __init__(self) -> None:
        self.model = RealESRGAN(DEVICE, scale=4)
        self.model.load_weights("weights/RealESRGAN_x4.pth")
        self.face_app = FaceAnalysis(name="buffalo_l")
        self.face_app.prepare(ctx_id=0 if DEVICE == "cuda" else -1, det_size=(640, 640))

    def enhance_pil(self, img: Image.Image) -> Image.Image:
        faces_before = self._get_faces(img)
        sr_img = self.model.predict(img)
        sr_img = self._post_process(sr_img)
        faces_after = self._get_faces(sr_img)

        if not self._faces_match(faces_before, faces_after):
            raise ValueError("Rostros alterados: proceso abortado.")
        return sr_img

    def _get_faces(self, img: Image.Image):
        return [face.bbox for face in self.face_app.get(np.array(img))]

    def _faces_match(self, fb, fa, tol=10):
        return len(fb) == len(fa) and all(abs(b[0]-a[0]) < tol and abs(b[1]-a[1]) < tol for b, a in zip(fb, fa))

    def _post_process(self, img: Image.Image) -> Image.Image:
        img = ImageEnhance.Color(img).enhance(1.15)
        img = ImageEnhance.Contrast(img).enhance(1.08)
        img = ImageEnhance.Sharpness(img).enhance(1.08)
        return img