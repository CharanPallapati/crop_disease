# AgriShield AI v1.0

Production-oriented hackathon application architecture for:
**field image → disease analysis → live weather → risk engine → actionable timing.**

## Current status

This package is deployable as a web service, with:
- Flask API
- PostgreSQL/SQLite-compatible SQLAlchemy models
- JWT authentication
- scan history
- upload validation
- weather integration
- advisory/risk engine
- Docker/Gunicorn
- responsive frontend
- model loading pipeline
- training script

### Critical distinction

The included repository intentionally does **NOT** ship a fake trained disease model.

If `model/disease_model.keras` is absent, the API returns `model-missing` with 0 confidence. This is deliberate: a production app must never pretend a hard-coded demo prediction is a real ML result.

## Run

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt
copy .env.example .env   # Windows
# cp .env.example .env   # Linux/macOS

python init_db.py
python app.py
```

Open the API root at `http://localhost:5000`.
For the included frontend, serve `frontend/` through your preferred static server or configure your reverse proxy to serve it.

## Real model

Put your trained file at:

`model/disease_model.keras`

and class names, in exact output order, at:

`model/labels.json`

Then install a platform-compatible TensorFlow package and restart the service.

### Training

Organize data as:

```text
dataset/
  Tomato___Early_Blight/
  Tomato___Late_Blight/
  Tomato___healthy/
```

Run:

```bash
pip install -r requirements-ml.txt
python train.py --data dataset --epochs 12
```

**For the hackathon, do not rely only on clean benchmark images.** Evaluate on separate real field photographs and report that performance separately.

## Deployment

Docker:

```bash
docker compose up --build
```

 
