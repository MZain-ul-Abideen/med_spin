
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Disease, ExploredDisease

app = FastAPI(title="MedSpin API")

# Allow Vue frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://med-spin-gh4zxilyo-zain-ul-abideens-projects-4c66e3a7.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/diseases")
def get_diseases(db: Session = Depends(get_db)):
    diseases = db.query(Disease).order_by(Disease.id).all()

    return [
        {"id": d.id, "name": d.name}
        for d in diseases
    ]


@app.get("/explored")
def get_explored(db: Session = Depends(get_db)):
    records = (
        db.query(ExploredDisease, Disease)
        .join(Disease)
        .order_by(ExploredDisease.explored_at.desc())
        .all()
    )

    return [
        {
            "id": disease.id,
            "name": disease.name,
            "explored_at": record.explored_at
        }
        for record, disease in records
    ]


@app.post("/explored/{disease_id}")
def mark_explored(
    disease_id: int,
    db: Session = Depends(get_db)
):
    disease = db.query(Disease).filter_by(id=disease_id).first()

    if not disease:
        raise HTTPException(status_code=404, detail="Disease not found")

    existing = db.query(ExploredDisease).filter_by(
        disease_id=disease_id
    ).first()

    if existing:
        return {"message": "Already explored"}

    db.add(ExploredDisease(disease_id=disease_id))
    db.commit()

    return {"message": "Disease marked as explored"}


@app.delete("/explored")
def reset_explored(db: Session = Depends(get_db)):
    db.query(ExploredDisease).delete()
    db.commit()

    return {"message": "Exploration progress reset"}
