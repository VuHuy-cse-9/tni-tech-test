from database.result_db import db_session_maker, fetch_detection_results
from schemas.data import DetResult
from common.logging import logger

def format_det_results(results: list[dict]) -> list[DetResult]:
    return [DetResult(**res) for res in results]

async def fetch_det_results(
    limit: int,
    offset: int
):
    results = await fetch_detection_results(
        session_maker=db_session_maker,
        limit=limit,
        offset=offset
    )
    logger.info(results)
    return format_det_results(results)