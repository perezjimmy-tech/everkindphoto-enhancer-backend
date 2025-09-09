from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from enhancer import PhotoEnhancer
from utils import ensure_weights_folder, download_weights
import io
from PIL import Image

app = FastAPI(title="EverKindPhoto Enhancer")

# Inicialización al arrancar el servidor
ensure_weights_folder()
download_weights()
enhancer = PhotoEnhancer()

@app.post("/enhance")
async def enhance_image(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(400, "Archivo debe ser imagen")

    try:
        input_img = Image.open(file.file).convert("RGB")
        output_img = enhancer.enhance_pil(input_img)

        buffer = io.BytesIO()
        output_img.save(buffer, format="JPEG", quality=95)
        buffer.seek(0)

        return StreamingResponse(buffer, media_type="image/jpeg")
    except ValueError as e:
        raise HTTPException(400, str(e))
    except Exception as e:
        raise HTTPException(500, "Error interno: " + str(e))