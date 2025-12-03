import random, string, os
import json, requests
from functools import wraps

from flask import render_template, request, abort, redirect, flash, make_response, session, url_for, jsonify
from sqlalchemy.sql import text
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from pkg import app, csrf
from pkg.models import db, User, Information
from pkg.forms import *

import cloudinary
import cloudinary.uploader

# ✅ Cloudinary Configuration
cloudinary.config(
    cloud_name="djetqdl9e",           # your Cloudinary cloud name
    api_key="574177562338279",        # your Cloudinary API key
    api_secret="93ONTpDhLBvWcpxWz3dV6cenFC8",  # your Cloudinary API secret (use full secret)
    secure=True
)

# ------------------------------------------------------------
# Decorator to check if there is a user logged in
# ------------------------------------------------------------
def login_required(f):
    @wraps(f)
    def login_check(*args, **kwargs):
        if session.get('user') is not None:
            return f(*args, **kwargs)
        else:
            flash("Access denied. Please login.", "danger")
            return redirect('/login')
    return login_check


def generate_string(howmany):
    x = random.sample(string.digits, howmany)
    return ''.join(x)


ALLOWED_EXTENSIONS = {"pdf", "jpg", "jpeg", "png"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def home():
    return redirect(url_for('scholarship'))


@app.route("/scholarshipapplication")
def scholarship():
    return render_template('users/index.html')


# ------------------------------------------------------------
# MAIN FORM ROUTE
# ------------------------------------------------------------
@app.route("/form", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        try:
            # -------------------------
            # STEP 1 – USER DETAILS
            # -------------------------
            fullname = request.form.get("fullname")
            gender = request.form.get("gender")
            dob = request.form.get("dob")
            phone = request.form.get("phone")
            email = request.form.get("email")
            state = request.form.get("state")
            geo = request.form.get("geo")
            type = request.form.get("type")
            media = request.form.get("media")
            role = request.form.get("role")
            journalism = request.form.get("journalism")
            finance = request.form.get("finance")
            supervisor = request.form.get("supervisor")

            # Create User
            new_user = User(
                fullname=fullname,
                gender=gender,
                dob=dob,
                phone=phone,
                email=email,
                state=state,
                geo=geo,
                media=media,
                role=role,
                type=type,
                finance=finance,
                supervisor=supervisor,
                journalism=journalism,
                approved='pending',
                status ='new'
            )
            db.session.add(new_user)
            db.session.flush()  # Get the ID without committing yet

            # -------------------------
            # STEP 2 – INFORMATION
            # -------------------------
            leadership = request.form.get("leadership")
            leadership_desc = request.form.get("leadership_desc")
            motivation = request.form.get("motivation")
            knowledge_use = request.form.get("knowledge_use")
            commitment = request.form.get("commitment")
            signature = request.form.get("signature")
            sign_date = request.form.get("sign_date")

            # -------------------------
            # FILE UPLOADS (Cloudinary)
            # -------------------------
            article1 = request.files.get("article1")
            article2 = request.files.get("article2")

            if not article1 or not article2:
                db.session.rollback()
                flash("Both article files are required", "error")
                return redirect(url_for("scholarship"))

            allowed_ext = {"jpg", "jpeg", "png", "pdf"}
            for f in [article1, article2]:
                if f.filename == "" or f.filename.rsplit(".", 1)[1].lower() not in allowed_ext:
                    db.session.rollback()
                    flash("Invalid image/document upload", "error")
                    return redirect(url_for("scholarship"))

            # Upload to Cloudinary
            upload_article1 = cloudinary.uploader.upload(
                article1, folder="scholarship_uploads", resource_type="auto"
            )
            upload_article2 = cloudinary.uploader.upload(
                article2, folder="scholarship_uploads", resource_type="auto"
            )

            article1_url = upload_article1["secure_url"]
            article2_url = upload_article2["secure_url"]

            # -------------------------
            # SAVE INFORMATION
            # -------------------------
            new_info = Information(
                leadership=leadership,
                leadership_desc=leadership_desc,
                motivation=motivation,
                knowledge_use=knowledge_use,
                commitment=commitment,
                signature=signature,
                sign_date=sign_date,
                article1=article1_url,
                article2=article2_url,
                user_id=new_user.id,
            )

            db.session.add(new_info)
            db.session.commit()

            # Console log
            print(f"[SUCCESS] User created: {new_user.fullname} (ID: {new_user.id})")

            return ("", 204)

        except Exception as e:
            db.session.rollback()
            print(f"[ERROR] Form submission failed: {str(e)}")
            import traceback
            traceback.print_exc()
            flash("An error occurred while submitting your application. Please try again.", "error")
            return redirect(url_for("scholarship"))

    return render_template("users/index.html")


# ------------------------------------------------------------
# ERROR HANDLERS
# ------------------------------------------------------------
@app.errorhandler(404)
def error_page(errors):
    return render_template("users/error.html")

@app.errorhandler(500)
def server_error_page(errors):
    return render_template("users/error.html")

@app.errorhandler(403)
def forbidden_page(errors):
    return render_template("users/badrequest.html")
