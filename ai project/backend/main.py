import cv2
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import numpy as np
import tensorflow as tf
import os

os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
MODEL_DIR = "ssd_mobilenet_v2_coco/saved_model"
model = tf.saved_model.load(str(MODEL_DIR))
infer = model.signatures['serving_default']

def run_inference(image: np.ndarray) -> Dict[str, Any]:
    input_tenso = tf.convert_to_tensor(image)
    input_tenso = input_tenso[tf.newaxis, ...] 

    detection = infer(input_tenso)

    return detection

app = FastAPI()

@app.post
async def prediction(file: UploadFile = File(...)) -> JSONResponse:
    contents = await file.read()
    image = np.array(cv2.imdecode(np.frombuffer(contents, np.uint8), cv2.IMREAD_COLOR))
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    detections = run_inference(image_rgb)

    num_detection = int(detections.pop('num_detection'))
    detections = {key: value[0, :num_detection].numpy() for key, value in detections.items()}

@app.get('/')
async def get_zapros():
    return {"hellow: world"}
