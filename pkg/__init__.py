import os
from flask import Flask
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail  # Import Flask-Mail
mail = Mail()
#instantiate the object of Flask
csrf =CSRFProtect()




def create_app():
    from pkg.models import db
    app=Flask(__name__)
    
    # Use Docker config if running in container, otherwise use local config
    if os.getenv('FLASK_ENV') == 'production':
        from pkg import docker_config
        app.config.from_object(docker_config)
    else:
        app.config.from_pyfile("config.py", silent=True)
        # Flask-Mail configuration for local development
        app.config['MAIL_SERVER'] = 'smtp.gmail.com'
        app.config['MAIL_PORT'] = 587
        app.config['MAIL_USE_TLS'] = True
        app.config['MAIL_USERNAME'] = 'hello@tosineniolorundafoundation.com'
        app.config['MAIL_PASSWORD'] = 'ocku watq dkpz xkpf'
        app.config['MAIL_DEFAULT_SENDER'] = 'hello@tosineniolorundafoundation.com'

    db.init_app(app)
    migrate= Migrate(app,db)
    csrf.init_app(app)

     # Initialize the Mail object with the app
    mail.init_app(app)
    return app

app=create_app()

#load routes from here 
from pkg import admin_routes, user_routes
from pkg.forms import*