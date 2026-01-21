from fastapi import FastAPI, UploadFile, HTTPException
from services.core_service import detect_save_image
from services.data_service import fetch_det_results
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from common.logging import logger

app = FastAPI(title="House price evaluation gateway")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/v1/detect", tags=["Root"])
async def detect_image(image: UploadFile):  # noqa: D103
    try:
        response =  await detect_save_image(image=image, is_visualized=True)
        return StreamingResponse(response, media_type="image/jpeg")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


@app.get("/results/", tags=["Root"])
async def get_det_results(limit: int = 10, offset: int = 0, image_pattern: str = ""):  # noqa: D103
    try:
        return await fetch_det_results(limit=limit, offset=offset, image_pattern=image_pattern)
    except Exception as e:
        logger.error(f"Error in get_det_results: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    