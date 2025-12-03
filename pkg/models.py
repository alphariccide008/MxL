from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(120), nullable=False)
    gender = db.Column(db.String(120), nullable=False)
    dob = db.Column(db.String(120))  
    phone = db.Column(db.String(225))
    email = db.Column(db.String(225))
    state = db.Column(db.String(200))
    geo = db.Column(db.String(120))

    media = db.Column(db.String(200))
    type = db.Column(db.String(200))         # NEW (from form)
    role = db.Column(db.String(200))

    journalism = db.Column(db.String(200))   # NEW + CORRECT SPELLING
    finance = db.Column(db.String(200))      # NEW
    supervisor = db.Column(db.String(300))   # NEW

    approved = db.Column(db.String(120), default="pending")
    status = db.Column(db.String(120), default="pending")

    info = db.relationship("Information", backref="user", uselist=False)



class Information(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    article1 = db.Column(db.String(255))
    article2 = db.Column(db.String(255))

    leadership = db.Column(db.String(120))
    leadership_desc = db.Column(db.Text)

    motivation = db.Column(db.Text)
    knowledge_use = db.Column(db.Text)
    commitment = db.Column(db.String(50))

    signature = db.Column(db.String(200))
    sign_date = db.Column(db.String(120))

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)



class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(300), nullable=False)
