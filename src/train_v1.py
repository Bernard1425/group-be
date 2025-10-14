import numpy as np
import pandas as pd
import joblib
import json
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

seed = 7

def train_model():
    # Load data
    Xy = load_diabetes(as_frame=True)
    X = Xy.frame.drop(columns=["target"])
    y = Xy.frame["target"]
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=seed
    )
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train model
    model = LinearRegression()
    model.fit(X_train_scaled, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test_scaled)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    
    # Save model and scaler
    joblib.dump(model, '../models/model_v0.1.pkl')
    joblib.dump(scaler, '../models/scaler_v0.1.pkl')
    
    # Save metrics
    metrics = {
        "version": "v0.1",
        "model_type": "LinearRegression",
        "rmse": float(rmse),
        "test_size": len(y_test),
        "features": list(X.columns)
    }
    
    with open('../models/metrics_v0.1.json', 'w') as f:
        json.dump(metrics, f, indent=2)
    
    print(f"RMSE for Linear Regression model: {rmse}")
    return rmse

if __name__ == "__main__":
    train_model()