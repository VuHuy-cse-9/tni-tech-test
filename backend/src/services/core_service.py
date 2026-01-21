import PIL.Image as pil
import io
from fastapi import UploadFile
from models.model import model_engine

def validate_image_upload(image: UploadFile) -> pil.Image:
    if image.content_type not in ["image/jpeg", "image/png"]:
        raise ValueError("Invalid image format. Only JPEG and PNG are supported.")
    return pil.open(image.file).convert("RGB")

async def detect_save_image(image: UploadFile, is_visualized: bool)->io.BytesIO:
    validated_image = validate_image_upload(image)
    results = model_engine.detect(validated_image, is_visualized)
    return results.image_buffer