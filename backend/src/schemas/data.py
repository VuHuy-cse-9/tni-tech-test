from pydantic import BaseModel
from marshmallow import Schema, fields

class DetResult(BaseModel):
    created_at: str
    det_box_count: int
    vis_image_path: str


class DataRequestSchema(Schema):
    image_pattern: str = fields.Str(required=False)
    limit: int = fields.Int(required=True)
    offset: int = fields.Int(required=True)