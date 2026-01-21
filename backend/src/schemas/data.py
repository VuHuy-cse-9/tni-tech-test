from pydantic import BaseModel

class DetResult(BaseModel):
    created_at: str
    det_box_count: int
    vis_image_path: str