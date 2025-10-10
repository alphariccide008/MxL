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
        # Step 1: User details
        fullname = request.form.get("fullname")
        email = request.form.get("email")
        age = request.form.get("age")
        level = request.form.get("level")
        school = request.form.get("school")
        phone = request.form.get("phone")
        guardian = request.form.get("guardian")
        occupation = request.form.get("occupation")

        # Save user
        new_user = User(
            fullname=fullname,
            email=email,
            age=age,
            level=level,
            school=school,
            phone=phone,
            guardian=guardian,
            occupation=occupation,
            status='new',
            approved='pending'
        )
        db.session.add(new_user)
        db.session.commit()

        # Step 2–5: Information
        financial = request.form.get("financial")
        intelligence = request.form.get("intelligence")
        grit = request.form.get("grit")
        growth = request.form.get("growth")
        giving_back = request.form.get("giving")

        # --------------------------------------------------------
        # ✅ Handle File Uploads — upload directly to Cloudinary
        # --------------------------------------------------------
        filesobj = request.files.get('waec')
        filesobj1 = request.files.get('jamb')
        filesobj2 = request.files.get('transcript')

        if not filesobj or not filesobj1 or not filesobj2:
            flash('Please upload all required files', category='error')
            return

        allowed_ext = {'jpg', 'jpeg', 'png', 'pdf'}
        for f in [filesobj, filesobj1, filesobj2]:
            if f.filename == '' or f.filename.rsplit('.', 1)[-1].lower() not in allowed_ext:
                flash('Invalid or missing files', category='error')
                return

        # ✅ Upload to Cloudinary
        upload_waec = cloudinary.uploader.upload(filesobj, folder="scholarship_uploads", resource_type="raw")
        upload_jamb = cloudinary.uploader.upload(filesobj1, folder="scholarship_uploads", resource_type="raw")
        upload_transcript = cloudinary.uploader.upload(filesobj2, folder="scholarship_uploads", resource_type="raw")

        waec_url = upload_waec["secure_url"]
        jamb_url = upload_jamb["secure_url"]
        transcript_url = upload_transcript["secure_url"]

        # ✅ Save info to database
        new_info = Information(
            financial=financial,
            intelligence=intelligence,
            grit=grit,
            growth=growth,
            giving_back=giving_back,
            waec_file=waec_url,
            jamb_file=jamb_url,
            transcript=transcript_url,
            user_id=new_user.id,
        )
        db.session.add(new_info)
        db.session.commit()

        # ✅ Optional CSV backup
        import csv
        from datetime import datetime
        BACKUP_FOLDER = "backups"
        os.makedirs(BACKUP_FOLDER, exist_ok=True)
        csv_file = os.path.join(BACKUP_FOLDER, "form_backup.csv")
        file_exists = os.path.isfile(csv_file)

        with open(csv_file, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow([
                    "timestamp", "user_id", "fullname", "email", "age", "level", "school", "phone",
                    "guardian", "occupation", "financial", "intelligence", "grit", "growth",
                    "giving_back", "waec_file", "jamb_file", "transcript"
                ])
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                new_user.id, fullname, email, age, level, school, phone, guardian, occupation,
                financial, intelligence, grit, growth, giving_back, waec_url, jamb_url, transcript_url
            ])

        print(f"✅ User created: {new_user.fullname} ({new_user.school})")
        print(f"✅ Uploaded Files: WAEC={waec_url}, JAMB={jamb_url}, TRANSCRIPT={transcript_url}")

        return ("", 204)

    return render_template('users/index.html')


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
