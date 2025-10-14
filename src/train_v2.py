import numpy as np
import pandas as pd
import joblib
import json
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
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
    
    # Train model with hyperparameter tuning
    rf = RandomForestRegressor(random_state=seed, n_jobs=-1)
    
    param_grid = {
        "n_estimators": [100, 200, 500],
        "max_depth": [None, 5, 10, 20],
        "min_samples_split": [2, 5, 10],
        "min_samples_leaf": [1, 2, 4],
        "max_features": ["sqrt", "log2"],
    }
    
    grid_search = GridSearchCV(
        estimator=rf,
        param_grid=param_grid,
        cv=5,
        scoring="neg_root_mean_squared_error",
        n_jobs=-1,
        verbose=1,
    )
    
    grid_search.fit(X_train_scaled, y_train)
    best_model = grid_search.best_estimator_
    
    # Evaluate
    y_pred = best_model.predict(X_test_scaled)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    
    # Save model and scaler
    joblib.dump(best_model, '../models/model_v0.2.pkl')
    joblib.dump(scaler, '../models/scaler_v0.2.pkl')
    
    # Save metrics
    metrics = {
        "version": "v0.2",
        "model_type": "RandomForestRegressor",
        "rmse": float(rmse),
        "test_size": len(y_test),
        "features": list(X.columns),
        "best_params": grid_search.best_params_
    }
    
    with open('../models/metrics_v0.2.json', 'w') as f:
        json.dump(metrics, f, indent=2)
    
    print(f"RMSE for Random Forest Regressor model: {rmse}")
    return rmse

if __name__ == "__main__":
    train_model()