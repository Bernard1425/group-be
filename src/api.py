from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
import json
import os
from typing import Dict

app = FastAPI(title="Diabetes Clinic Triage API", version="0.1.0")

# Load model and scaler at startup
MODEL_VERSION = os.getenv("MODEL_VERSION", "v0.2")
model = joblib.load(f'/app/models/model_{MODEL_VERSION}.pkl')
scaler = joblib.load(f'/app/models/scaler_{MODEL_VERSION}.pkl')

# Load metrics for version info
with open(f'/app/models/metrics_{MODEL_VERSION}.json', 'r') as f:
    metrics = json.load(f)

class PredictionRequest(BaseModel):
    age: float
    sex: float
    bmi: float
    bp: float
    s1: float
    s2: float
    s3: float
    s4: float
    s5: float
    s6: float

class PredictionResponse(BaseModel):
    prediction: float

class HealthResponse(BaseModel):
    status: str
    model_version: str

@app.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(status="ok", model_version=MODEL_VERSION)

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    try:
        # Convert request to array
        features = np.array([[
            request.age, request.sex, request.bmi, request.bp,
            request.s1, request.s2, request.s3, request.s4,
            request.s5, request.s6
        ]])
        
        # Scale features
        features_scaled = scaler.transform(features)
        
        # Make prediction
        prediction = model.predict(features_scaled)[0]
        
        return PredictionResponse(prediction=float(prediction))
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)