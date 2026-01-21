from database.result_db import db_session_maker, fetch_detection_results
from schemas.data import DetResult, DataRequestSchema
from marshmallow import ValidationError
from common.logging import logger
from fastapi import HTTPException

def format_det_results(results: list[dict]) -> list[DetResult]:
    return [DetResult(**res) for res in results]

def validate_schema_data(limit: int, offset: int, image_pattern: str) -> DataRequestSchema:
    try:
        DataRequestSchema().dump({
            "limit": limit,
            "offset": offset,
            "image_pattern": image_pattern
        })
    except ValidationError as ve:
        raise HTTPException(status_code=400, detail=ve.messages)

async def fetch_det_results(
    limit: int = 10,
    offset: int = 0,
    image_pattern: str = ""
):
    validate_schema_data(limit=limit, offset=offset, image_pattern=image_pattern)
    results = await fetch_detection_results(
        session_maker=db_session_maker,
        limit=limit,
        offset=offset,
        image_path=image_pattern
    )
    logger.info(results)
    return format_det_results(results)