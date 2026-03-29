from fastapi import FastAPI
import joblib
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# load trained model (single XGB)
model = joblib.load("model.pkl")

@app.get("/")
def home():
    return {"message": "Credit Card Fraud Detection API"}

@app.post("/predict")
def predict(data: dict):
    # convert to DataFrame
    features = pd.DataFrame([data])

    prediction = model.predict(features)

    if(int(prediction[0] == 0)):
        return {"result": "Not Fraud"}
    else:
        return {"result": "Fraud"}