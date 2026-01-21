from pydantic import BaseModel, ConfigDict
from io import BytesIO

class Box(BaseModel):
    x1: int
    y1: int
    x2: int
    y2: int

class ModelResponse(BaseModel):
    image_buffer: BytesIO
    image_path: str | None = None
    bboxes: list[Box] = []
    model_config = ConfigDict(arbitrary_types_allowed=True)