from pkg import app
from pkg.models import db, User, Information

with app.app_context():
    try:
        # Test database connection
        result = db.session.execute(db.text("SELECT 1"))
        print("[SUCCESS] Database connection successful!")

        # Check tables exist
        print("\n[TABLES] Checking tables...")
        tables = db.session.execute(db.text("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")).fetchall()
        print(f"Found {len(tables)} tables:")
        for table in tables:
            print(f"  - {table[0]}")

        # Check User table structure
        print("\n[USER TABLE] User table columns:")
        user_cols = db.session.execute(db.text("SELECT column_name, data_type FROM information_schema.columns WHERE table_name='user'")).fetchall()
        for col in user_cols:
            print(f"  - {col[0]}: {col[1]}")

        # Check Information table structure
        print("\n[INFO TABLE] Information table columns:")
        info_cols = db.session.execute(db.text("SELECT column_name, data_type FROM information_schema.columns WHERE table_name='information'")).fetchall()
        for col in info_cols:
            print(f"  - {col[0]}: {col[1]}")

        # Count existing records
        user_count = db.session.query(User).count()
        info_count = db.session.query(Information).count()
        print(f"\n[RECORDS] Current records:")
        print(f"  - Users: {user_count}")
        print(f"  - Information: {info_count}")

    except Exception as e:
        print(f"[ERROR] Error: {e}")
        import traceback
        traceback.print_exc()
