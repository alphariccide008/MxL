import os
import random,string,os
import json,requests
from functools import wraps

from flask import render_template,request,abort,redirect,flash,make_response,session,url_for,jsonify
from sqlalchemy.sql import text
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import desc
from flask_mail import Message

# Import mail instance from your create_app setup


from pkg import app,csrf,mail
from pkg.models import db,User,Admin,Information
from pkg.forms import *




UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'upload')





#This is a decoratoer to help check if there is a user logged in
def login_required(f):
    @wraps(f)
    def login_check(*args,**kwargs):
        if session.get('admin') !=None:
            return f(*args,**kwargs)
        else:
            flash('Access Denied')
            flash('You must be logged in first')
            return redirect('/admin/')
    return login_check




@app.route("/admin/", methods=["GET", "POST"])
def admin():
    if request.method == "GET":
        return render_template("admin/adminlog.html")

    email = request.form.get("email")
    pwd = request.form.get("pwd")

    # Look up admin by email
    deets = db.session.query(Admin).filter(Admin.email == email).first()

    if deets and deets.password:  # ensure password exists
        if check_password_hash(deets.password, pwd):
            session["admin"] = deets.id
            flash("Login successful!", "success")
            return redirect(url_for("all_users"))
        else:
            flash("Invalid credentials, try again", "danger")
            return redirect(url_for("admin"))
    else:
        flash("Invalid credentials, try again", "danger")
        return redirect(url_for("admin"))




@app.route("/send-email", methods=["GET", "POST"])
def send_email():
    try:
        msg = Message(subject, recipients=[recipient])
        msg.html = f"""
        <html>
            <body>
                <h2 style='color:#2d6cdf;'>{subject}</h2>
                    <p>{message_body}</p>
                <hr>
                <small>Sent from Gold Capital Investment</small>
            </body>
        </html>
            """

        mail.send(msg)
        flash("✅ Email sent successfully!", "success")
        return redirect(url_for("send_email"))
    except Exception as e:
        flash(f"❌ Failed to send email: {str(e)}", "danger")

    return render_template("send_email.html")



  # Make sure this import is present

@app.route("/all_users/")
@login_required
def all_users():
    id = session.get("admin")
    admindeets = Admin.query.get_or_404(id)

    page = request.args.get("page", 1, type=int)

    pagination = (
        db.session.query(User, Information)
        .join(Information, User.id == Information.user_id)
        .order_by(desc(User.id)).filter(User.approved=='pending')   # 👈 Sort by newest first (change to created_at if needed)
        .paginate(page=page, per_page=5, error_out=False)
    )

    deet = pagination.items

    return render_template(
        "admin/all_user.html",
        deet=deet,
        admindeets=admindeets,
        pagination=pagination,
    )



@app.route("/approved_applicants/")
@login_required
def approved():
    id = session.get("admin")
    admindeets = Admin.query.get_or_404(id)

    # Get current page number from query string (default = 1)
    page = request.args.get("page", 1, type=int)

    # Join User and Information, paginate with 10 per page
    pagination = (
        db.session.query(User, Information)
        .join(Information, User.id == Information.user_id).filter(User.approved=='approved')
        .paginate(page=page, per_page=5, error_out=False)
    )

    # pagination.items contains the actual records for this pageds
    deet = pagination.items

    return render_template(
        "admin/approved.html",
        deet=deet,
        admindeets=admindeets,
        pagination=pagination,
    )


# declined Applicant

@app.route("/declined_applicants/")
@login_required
def declined():
    id = session.get("admin")
    admindeets = Admin.query.get_or_404(id)

    # Get current page number from query string (default = 1)
    page = request.args.get("page", 1, type=int)

    # Join User and Information, paginate with 10 per page
    pagination = (
        db.session.query(User, Information)
        .join(Information, User.id == Information.user_id).filter(User.approved=='decline')
        .paginate(page=page, per_page=5, error_out=False)
    )

    # pagination.items contains the actual records for this pageds
    deet = pagination.items

    return render_template(
        "admin/declined.html",
        deet=deet,
        admindeets=admindeets,
        pagination=pagination,
    )


@app.route('/user/<int:user_id>')
@login_required
def user_detail(user_id):
    # Correct way to get user or 404
    user = User.query.get_or_404(user_id)
    if user.status:
        user.status='clicked'
        db.session.commit()

    # Fetch related Information record
    information = Information.query.filter_by(user_id=user.id).first()


    return render_template('admin/user_detail.html', user=user, information=information)





@app.route('/approved/<int:user_id>')
@login_required
def approve_user(user_id):
    user = User.query.get_or_404(user_id)

    if user.status:
        user.approved = 'approved'
        db.session.commit()

        # ✅ Send email after approval
        

            # ✅ Log actions to the console instead of flashing
        print(f"✅ User {user.fullname} (ID: {user.id}) approved successfully.")
        print(f"✅ Approval email sent to {user.email}")
        return redirect(url_for('all_users'))



    else:
        print(f"⚠️ Approval succeeded but email failed to send: {str(e)}")

        return redirect(url_for('all_users'))

    


@app.route('/decline/<int:user_id>')
@login_required
def decline_user(user_id):
    user = User.query.get_or_404(user_id)

    if user.status:
        user.approved = 'decline'
        db.session.commit()

        # try:
        #     msg = Message(
        #         subject="Scholarship Application Update - ",
        #         recipients=[user.email]
        #     )
        #     msg.html = f"""
        #     <html>
        #         <body style="font-family: Arial, sans-serif; background-color:#f4f4f4; padding:20px;">
        #             <div style="max-width:700px; margin:auto; background:#fff; padding:20px; border-radius:8px; ">
                    
        #                 <h2 style='color:#000000;'>Dear {user.fullname},</h2>
        #                 <b>

        #                 <p>Thank you for taking the time to apply for the Tosin Eniolorunda Future Builders STEM Scholarship. We were deeply inspired by your story, your aspirations, and the passion you poured into your application.</p>

        #                 <p>This year, we received an overwhelming number of applications from brilliant and driven individuals like you. After careful consideration, we regret to inform you that you were not selected for this cycle. Please know that this decision was not a reflection of your potential, but rather the limited number of awards available.</p>

        #                 <p>We want you to remember your dreams remain valid, your journey is important, and the resilience you’ve shown in reaching this stage is remarkable. Many great leaders and changemakers have faced setbacks along the way, but what set them apart was their ability to keep moving forward.</p>

        #                 <p>We truly believe in your future, and we encourage you to continue pursuing opportunities that bring you closer to your goals.

        #                 .</p>
        #                 <p>Stay Winning,<br>
        #                 <b>Tosin Eniolorunda Foundation</b></p>
                        
                        
        #             </div>
        #         </body>
        #     </html>
        #     """

        #     mail.send(msg)
        #     print(f"❌ User {user.fullname} was declined. Email sent to {user.email}")

        # except Exception as e:
        #     print(f"⚠️ Decline succeeded but email failed to send: {str(e)}")

        return redirect(url_for('all_users'))

    


@app.route('/view-file/<filename>')
def view_file(filename):
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    # Detect extension for preview logic
    ext = filename.lower().split('.')[-1]

    return render_template('admin/view_file.html', filename=filename, ext=ext)








@app.route("/admin/logout")
def admin_logout():
    if session.get('admin')!= None:
        session.pop('admin',None)
        flash('you\'ve logged out successfully',"success")
    return redirect(url_for('admin'))