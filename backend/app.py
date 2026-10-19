from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

import cv2
import numpy as np
import joblib

from color_utils import extract_features
from recommendation import get_recommendations


app = FastAPI(
    title="Personal Color API",
    description="API untuk klasifikasi skin tone dan rekomendasi warna",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3002",
        "http://127.0.0.1:3002",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


model_data = joblib.load(
    "model/skin_tone_model.pkl"
)

model = model_data["model"]


@app.get("/")
def root():
    return {
        "message": "Personal Color API berjalan"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


@app.post("/predict")
async def predict(
    file: UploadFile = File(...)
):

    contents = await file.read()

    image_array = np.frombuffer(
        contents,
        np.uint8
    )

    image = cv2.imdecode(
        image_array,
        cv2.IMREAD_COLOR
    )

    if image is None:
        return {
            "success": False,
            "message": "Gambar tidak dapat dibaca"
        }

    try:
        features = extract_features(image)

        X = np.array([
            [
                features["rgb_r"],
                features["rgb_g"],
                features["rgb_b"],
                features["lab_l"],
                features["lab_a"],
                features["lab_b"],
            ]
        ])

        prediction = model.predict(X)[0]

        probabilities = model.predict_proba(X)[0]

        classes = model.classes_

        class_index = list(classes).index(prediction)

        confidence = float(
            probabilities[class_index]
        )

        recommendations = get_recommendations(
            prediction
        )

        return {
            "success": True,
            "prediction": prediction,
            "confidence": round(confidence, 4),
            "features": {
                "rgb_r": features["rgb_r"],
                "rgb_g": features["rgb_g"],
                "rgb_b": features["rgb_b"],
                "lab_l": features["lab_l"],
                "lab_a": features["lab_a"],
                "lab_b": features["lab_b"],
            },
            "recommendations": recommendations,
        }

    except ValueError as e:

        return {
            "success": False,
            "message": str(e)
        }

    except Exception as e:

        return {
            "success": False,
            "message": str(e)
        }