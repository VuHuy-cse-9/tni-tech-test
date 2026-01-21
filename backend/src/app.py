from fastapi import FastAPI, UploadFile, HTTPException
from services.core_service import detect_save_image
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

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
    