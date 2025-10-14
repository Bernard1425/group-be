# Diabetes Clinic Triage System

A machine learning service that predicts diabetes progression risk to help nurses prioritize patient follow-ups in a virtual diabetes clinic.

## Quick Start

### Pull and Run Docker Image

```bash
# Pull the latest version
docker pull ghcr.io/bernard1425/group-be:latest

# Run the container
docker run -p 8000:8000 ghcr.io/bernard1425/group-be:latest
```

### API Usage

**Health Check:**
```bash
curl http://localhost:8000/health
```

**Response:**
```json
{"status": "ok", "model_version": "v0.1"}
```

**Make Prediction:**
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "age": 0.02,
    "sex": -0.044,
    "bmi": 0.06,
    "bp": -0.03,
    "s1": -0.02,
    "s2": 0.03,
    "s3": -0.02,
    "s4": 0.02,
    "s5": 0.02,
    "s6": -0.001
  }'
```

**Response:**
```json
{"prediction": 152.3}
```

## Local Development

### Prerequisites
- Python 3.11+
- Docker (optional)

### Setup
```bash
git clone https://github.com/YOUR_USERNAME/diabetes-clinic-triage.git
cd diabetes-clinic-triage
pip install -r requirements.txt
```

### Train Models
```bash
# Train v0.1 (LinearRegression baseline)
cd src && python train_v1.py

# Train v0.2 (RandomForest with hyperparameter tuning)
cd src && python train_v2.py
```

### Run API Locally
```bash
cd src && python api.py
```

### Run Tests
```bash
pytest tests/ -v
```

### Build Docker Image
```bash
docker build -t diabetes-clinic-triage .
docker run -p 8000:8000 diabetes-clinic-triage
```

## Model Performance

| Version | Model Type | RMSE | Improvement |
|---------|------------|------|-------------|
| v0.1 | LinearRegression | 54.46 | Baseline |
| v0.2 | RandomForestRegressor | 53.39 | 1.96% better |

## Features

The model uses 10 features from the scikit-learn diabetes dataset:
- `age`: Age in years
- `sex`: Gender 
- `bmi`: Body mass index
- `bp`: Average blood pressure
- `s1`: Total serum cholesterol
- `s2`: Low-density lipoproteins
- `s3`: High-density lipoproteins
- `s4`: Total cholesterol / HDL
- `s5`: Log of serum triglycerides level
- `s6`: Blood sugar level

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  Triage Nurse   │───▶│   Dashboard      │───▶│   ML Service    │
│   Dashboard     │    │  (Frontend)      │    │  (FastAPI)      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                        │
                                                        ▼
                                               ┌─────────────────┐
                                               │  Trained Model  │
                                               │  (Scikit-learn) │
                                               └─────────────────┘
```

## CI/CD Pipeline

- **Push/PR**: Lint, test, train models, upload artifacts
- **Tag Release**: Build Docker image, run container tests, publish to GHCR, create GitHub release

## License

MIT License