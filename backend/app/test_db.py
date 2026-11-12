from app.database import engine

with engine.connect() as connection:
    print("Supabase connected successfully!")