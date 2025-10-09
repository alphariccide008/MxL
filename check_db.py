from pkg.models import db, Admin, User
from pkg import app

with app.app_context():
    print(f"Admins: {Admin.query.count()}")
    print(f"Users: {User.query.count()}")
    
    for admin in Admin.query.all():
        print(f"Admin: {admin.email}")
    
    for user in User.query.all():
        print(f"User: {user.fullname} ({user.email})")