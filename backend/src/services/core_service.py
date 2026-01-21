import PIL.Image as pil
import io
from fastapi import UploadFile
from models.model import model_engine
from schemas.model import ModelResponse
from database.result_db import db_session_maker, save_detection_result_info

def validate_image_upload(image: UploadFile) -> pil.Image:
    if image.content_type not in ["image/jpeg", "image/png"]:
        raise ValueError("Invalid image format. Only JPEG and PNG are supported.")
    return pil.open(image.file).convert("RGB")

def _prepare_save_data(
        results: ModelResponse
) -> dict:
    det_box_count = len(results.bboxes)
    vis_image_path = results.image_path
    data = {
        "det_box_count": det_box_count,
        "vis_image_path": vis_image_path,
    }
    return data

async def save_data(
        results: ModelResponse
):
    data = _prepare_save_data(results)
    await save_detection_result_info(
        session_maker=db_session_maker,
        data=data
    )
    return

async def detect_save_image(image: UploadFile, is_visualized: bool)->io.BytesIO:
    validated_image = validate_image_upload(image)
    results = model_engine.detect(validated_image, is_visualized)
    await save_data(results)
    return results.image_buffer