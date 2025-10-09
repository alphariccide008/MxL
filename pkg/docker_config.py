from os import getenv

SECRET_KEY = getenv("SECRET_KEY", "R5T6Y7UHJIKOLO987EROELFKGWASDDJNRFTGHVN")
ADMIN_EMAIL = getenv("ADMIN_EMAIL", "godspowerlawrence008@gmail.com")
USER_PROFILE_PATH = "pkg/static/profiles/"

# Use environment variable for database URL, fallback to PostgreSQL default
DATABASE_URL = getenv("DATABASE_URL", "postgresql://moniepoint_user:fywokEqHfMiMguQwq2ynmB3nSZ5tdQlK@dpg-d3jnsrl6ubrc73d02nsg-a.oregon-postgres.render.com:5432/moniepoint")
SQLALCHEMY_DATABASE_URI = DATABASE_URL

# Mail configuration
MAIL_SERVER = getenv("MAIL_SERVER", "smtp.gmail.com")
MAIL_PORT = int(getenv("MAIL_PORT", "587"))
MAIL_USE_TLS = getenv("MAIL_USE_TLS", "True").lower() == "true"
MAIL_USERNAME = getenv("MAIL_USERNAME", "hello@tosineniolorundafoundation.com")
MAIL_PASSWORD = getenv("MAIL_PASSWORD", "ocku watq dkpz xkpf")
MAIL_DEFAULT_SENDER = getenv("MAIL_DEFAULT_SENDER", "hello@tosineniolorundafoundation.com")