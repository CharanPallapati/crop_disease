import os
import uuid

from flask import Blueprint, request, jsonify, current_app, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename

from models import db, Scan
from services.detector import DiseaseDetector
from services.weather import WeatherService
from services.advisory import AdvisoryEngine


analysis_bp = Blueprint("analysis", __name__)

detector = DiseaseDetector()
weather = WeatherService()
advisory = AdvisoryEngine()

ALLOWED = {"jpg", "jpeg", "png", "webp"}


def valid_file(f):
    return (
        f
        and f.filename
        and "." in f.filename
        and f.filename.rsplit(".", 1)[1].lower() in ALLOWED
    )


@analysis_bp.post("/analyze")
def analyze():

    f = request.files.get("image")

    if not valid_file(f):
        return jsonify(
            error="Upload JPG, PNG or WEBP."
        ), 400

    lat = request.form.get("lat", type=float)
    lon = request.form.get("lon", type=float)

    crop = (
        request.form.get("crop") or "auto"
    ).lower()

    folder = current_app.config["UPLOAD_FOLDER"]

    name = (
        f"{uuid.uuid4().hex}_"
        f"{secure_filename(f.filename)}"
    )

    path = os.path.join(folder, name)

    f.save(path)

    # Run the AI disease model
    prediction = detector.predict(
        path,
        crop
    )

    # Get weather information
    wx = (
        weather.get(lat, lon)
        if lat is not None and lon is not None
        else weather.demo()
    )

    # Build advisory information
    result = advisory.build(
        prediction,
        wx
    )

    # IMPORTANT:
    # The frontend expects the model prediction
    # under result["prediction"].
    result["prediction"] = prediction

    user_id = None

    try:
        user_id = int(
            get_jwt_identity()
        )
    except Exception:
        pass

    scan = Scan(
        user_id=user_id,
        image_path=name,
        crop=prediction["crop"],
        disease=prediction["disease"],
        confidence=prediction["confidence"],
        latitude=lat,
        longitude=lon,
        decision=result["decision"]["action"],
        weather_score=result["decision"]["score"],
        result_json=result
    )

    db.session.add(scan)

    db.session.commit()

    result["scan_id"] = scan.id

    result["image_url"] = (
        "/api/uploads/" + name
    )

    return jsonify(result)


@analysis_bp.get("/uploads/<path:name>")
def uploaded(name):

    return send_from_directory(
        current_app.config["UPLOAD_FOLDER"],
        name
    )


@analysis_bp.get("/history")
@jwt_required()
def history():

    uid = int(
        get_jwt_identity()
    )

    rows = (
        Scan.query
        .filter_by(user_id=uid)
        .order_by(Scan.created_at.desc())
        .limit(50)
        .all()
    )

    return jsonify(
        items=[
            {
                "id": r.id,
                "crop": r.crop,
                "disease": r.disease,
                "confidence": r.confidence,
                "decision": r.decision,
                "score": r.weather_score,
                "created_at":
                    r.created_at.isoformat()
                    if r.created_at
                    else None
            }
            for r in rows
        ]
    )


@analysis_bp.get("/weather")
def weather_endpoint():

    lat = request.args.get(
        "lat",
        type=float
    )

    lon = request.args.get(
        "lon",
        type=float
    )

    if lat is None or lon is None:
        return jsonify(
            weather.demo()
        )

    return jsonify(
        weather.get(lat, lon)
    )


@analysis_bp.post("/explain")
def explain():

    # Grad-CAM requires a model-specific
    # convolution layer. This endpoint deliberately
    # refuses to fabricate a heatmap when the model
    # architecture has not been configured.

    return jsonify(
        error=(
            "Grad-CAM layer is model-specific. "
            "Configure the target convolution layer "
            "in services/gradcam.py."
        )
    ), 501