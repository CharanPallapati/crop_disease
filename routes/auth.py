from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db, User

auth_bp=Blueprint("auth", __name__)

@auth_bp.post("/register")
def register():
    data=request.get_json() or {}
    name=(data.get("name") or "").strip()
    email=(data.get("email") or "").strip().lower()
    password=data.get("password") or ""
    if not name or not email or len(password)<8:
        return jsonify(error="Name, valid email and password of at least 8 characters are required."),400
    if User.query.filter_by(email=email).first():
        return jsonify(error="Email already registered."),409
    user=User(name=name,email=email)
    user.set_password(password)
    db.session.add(user); db.session.commit()
    return jsonify(token=create_access_token(identity=str(user.id)), user={"id":user.id,"name":name,"email":email}),201

@auth_bp.post("/login")
def login():
    data=request.get_json() or {}
    user=User.query.filter_by(email=(data.get("email") or "").lower().strip()).first()
    if not user or not user.check_password(data.get("password") or ""):
        return jsonify(error="Invalid email or password."),401
    return jsonify(token=create_access_token(identity=str(user.id)), user={"id":user.id,"name":user.name,"email":user.email})

@auth_bp.get("/me")
@jwt_required()
def me():
    user=User.query.get(int(get_jwt_identity()))
    if not user: return jsonify(error="User not found."),404
    return jsonify(id=user.id,name=user.name,email=user.email,language=user.language)
