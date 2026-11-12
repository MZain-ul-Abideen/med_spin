
import json
from pathlib import Path

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Disease

DATASET = Path("../dataset/diseases_100_france_learning.json")

with open(DATASET, encoding="utf-8") as file:
    data = json.load(file)

db: Session = SessionLocal()

try:
    for name in data["diseases"]:
        exists = db.query(Disease).filter_by(name=name).first()

        if not exists:
            db.add(Disease(name=name))

    db.commit()
    print("Disease dataset uploaded successfully!")

except Exception:
    db.rollback()
    raise

finally:
    db.close()
