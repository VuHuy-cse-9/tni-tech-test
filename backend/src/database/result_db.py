from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy import text
from configs.config import settings
from urllib.parse import quote
from common.logging import logger


INSERT_DET_RESULT = f"""
INSERT INTO public.{settings.postgresql_detection_results_table} (
    det_box_count,
    vis_image_path
) VALUES (
    :det_box_count,
    :vis_image_path
);
"""

GET_DET_RESULTS = f"""
    SELECT created_at, det_box_count, vis_image_path
    FROM public.{settings.postgresql_detection_results_table}
    ORDER BY created_at ASC
    LIMIT :limit OFFSET :offset;
"""

GET_DET_RESULTS_WITH_IMAGE_PATTERN = f"""
    SELECT created_at, det_box_count, vis_image_path
    FROM public.{settings.postgresql_detection_results_table}
    WHERE vis_image_path ILIKE :image_path
    ORDER BY created_at ASC
    LIMIT :limit OFFSET :offset;
"""

def initialize_zoopla_db_engine():
    """
    Initialize Zoopla database engine and session maker.

    Returns:
        tuple: (engine, session_maker)
    """
    db_url = (
        f"postgresql+asyncpg://{settings.postgres_user}:{quote(settings.postgres_password)}"
        f"@{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db}"
    )
    engine = create_async_engine(
        db_url,
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,
        echo=False,
    )
    session_maker = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    return engine, session_maker

db_engine, db_session_maker = initialize_zoopla_db_engine()


async def save_detection_result_info(
    session_maker: async_sessionmaker[AsyncSession],
    data: dict
):
    try:
        params = {
            "det_box_count": data.get("det_box_count"),
            "vis_image_path": data.get("vis_image_path"),
        }
        async with session_maker() as session:
            query = text(INSERT_DET_RESULT)
            await session.execute(query, params)
            await session.commit()
    except Exception as e:
        logger.error(f"Error saving detection result info: {str(e)}")
        return None  # Don't raise, just log error
    

async def fetch_detection_results(
    session_maker: async_sessionmaker[AsyncSession],
    limit: int,
    offset: int,
    image_path: str
) -> list[dict]:
    results = []
    try:
        async with session_maker() as session:
            query = text(GET_DET_RESULTS)
            result_proxy = await session.execute(query, {"limit": limit, "offset": offset})
            rows = result_proxy.fetchall()
            for row in rows:
                results.append({
                    "created_at": row.created_at.isoformat(),
                    "det_box_count": row.det_box_count,
                    "vis_image_path": row.vis_image_path
                })
    except Exception as e:
        logger.error(f"Error fetching detection results: {str(e)}")
    return results