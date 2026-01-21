from PIL import Image
from ultralytics import YOLO
import numpy as np
from uuid import uuid4
import os
from configs.config import settings
import cv2
from schemas.model import Box, ModelResponse
from io import BytesIO

PERSON_CLASS_ID = 0

class PersonDetectorEngine:
    def __init__(self, save_dir: str) -> None:
        # Load yolov model.
        self.save_dir = save_dir
        # Validate save directory
        self.__setup()

    def detect(self, image: Image, is_visualized: bool) -> ModelResponse:
        results = self.__process(image)
        bboxes = self.__postprocess(results)
        vis_image, vis_image_path = self.__save_visualize_image(image, bboxes, is_visualized)
        buffer = self.serialize_image(vis_image)
        return ModelResponse(image_buffer=buffer, image_path=vis_image_path, bboxes=bboxes)

    def __setup(self):
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

        self.model = YOLO("yolo11n.pt")
        

    def __process(self, image: Image) -> Image:
        results = self.model(image)
        return results
    
    def __postprocess(self, results) -> list[Box]:
        bboxes = []
        for result in results:
            for box in result.boxes:
                cls_id = int(box.cls[0])
                # Assuming class ID 0 corresponds to 'person' in the model
                if cls_id == PERSON_CLASS_ID:
                    x1, y1, x2, y2 = box.xyxy[0]
                    bboxes.append(Box(
                        x1=int(x1),
                        y1=int(y1),
                        x2=int(x2),
                        y2=int(y2)
                    ))
        return bboxes
    
    def serialize_image(self, image: Image) -> BytesIO:
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        buffered.seek(0)
        return buffered
    
    def __visualize_results(self, image: Image, results: list[Box]) -> Image:
        img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        for box in results:
            cv2.rectangle(img_cv, (box.x1, box.y1), (box.x2, box.y2), (0, 255, 0), 2)
        return Image.fromarray(cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB))
    
    def __generate_new_image_path(self) -> str:
        return os.path.join(self.save_dir, f"{uuid4()}.jpg")

    def __save_visualize_image(self, image: Image, results: list[Box], is_visualized: bool) -> None:
        # Generate id for image_name:
        if not is_visualized or len(results) == 0:
            return None
        
        image_path = self.__generate_new_image_path()
        vis_image = self.__visualize_results(image, results)
        vis_image.save(image_path)
        return vis_image, image_path
    
model_engine = PersonDetectorEngine(settings.save_dir)