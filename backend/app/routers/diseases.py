from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/diseases", tags=["diseases"])

@router.get("/", response_model=list[schemas.Disease])
def get_all_diseases(db: Session = Depends(get_db)):
    return db.query(models.Disease).all()

@router.get("/{disease_id}", response_model=schemas.Disease)
def get_disease(disease_id: int, db: Session = Depends(get_db)):
    disease = db.query(models.Disease).filter(
        models.Disease.id == disease_id
    ).first()
    if not disease:
        raise HTTPException(status_code=404, detail="Disease not found")
    return disease

@router.get("/{disease_id}/genes", response_model=list[schemas.Gene])
def get_disease_genes(disease_id: int, db: Session = Depends(get_db)):
    disease = db.query(models.Disease).filter(
        models.Disease.id == disease_id
    ).first()
    if not disease:
        raise HTTPException(status_code=404, detail="Disease not found")
    return disease.genes

@router.get("/{disease_id}/biomarkers", response_model=list[schemas.Biomarker])
def get_disease_biomarkers(disease_id: int, db: Session = Depends(get_db)):
    disease = db.query(models.Disease).filter(
        models.Disease.id == disease_id
    ).first()
    if not disease:
        raise HTTPException(status_code=404, detail="Disease not found")
    return disease.biomarkers