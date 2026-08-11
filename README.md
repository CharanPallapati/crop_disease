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

For a real production deployment:
- use PostgreSQL instead of SQLite
- store uploads in object storage (S3-compatible)
- set strong secrets
- restrict CORS
- terminate HTTPS at a reverse proxy/load balancer
- enable application monitoring
- use background jobs for expensive inference if required
- back up the database
- never expose `.env`
- add rate limiting/WAF

## Safety

The advisory layer intentionally avoids inventing pesticide doses. Treatment details must come from trusted, locally approved agricultural sources and product labels.

The application is decision support, not a substitute for a qualified agronomist.

## Next winning upgrades

1. Real field-validated model
2. Grad-CAM explanation
3. Crop/leaf image quality + OOD model
4. Telugu localization + text-to-speech
5. 7-day disease-risk model
6. Field history/trend graphs
7. Trusted-source citations per recommendation
8. Offline/PWA support for weak connectivity


## v2 winning features

- bilingual farmer-facing output (English/Telugu)
- browser speech synthesis for Telugu advisory
- source-linked agronomic guidance
- explicit uncertainty/quality gate
- Grad-CAM integration point that refuses to fake explanations
- field-validation scaffold
- judge demo script

The source layer follows FAO's integrated pest-management emphasis on monitoring, forecasting,
non-chemical options and careful intervention, while Indian references can be mapped into
crop-specific guidance. See the source cards in the app.
