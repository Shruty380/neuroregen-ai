from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from app.ai.biomarker_model import biomarker_classifier

router = APIRouter(prefix="/ai", tags=["AI Models"])

class BiomarkerInput(BaseModel):
    amyloid_beta_42: Optional[float] = 1200.0
    phospho_tau_181: Optional[float] = 180.0
    neurofilament_light: Optional[float] = 1500.0
    alpha_synuclein: Optional[float] = 1200.0
    dopamine_transporter: Optional[float] = 70.0
    sod1_activity: Optional[float] = 85.0
    huntingtin_mutant: Optional[float] = 50.0
    glial_fibrillary_acidic_protein: Optional[float] = 150.0
    brain_derived_neurotrophic_factor: Optional[float] = 18.0
    inflammatory_index: Optional[float] = 4.0

@router.post("/predict/disease")
def predict_disease(biomarkers: BiomarkerInput):
    """
    Predict neurodegenerative disease from biomarker levels.
    Uses a Random Forest classifier trained on synthetic biological data.
    """
    biomarker_dict = biomarkers.dict()
    result = biomarker_classifier.predict(biomarker_dict)
    return result

@router.get("/demo/alzheimers")
def demo_alzheimers_prediction():
    """Demo prediction using typical Alzheimer's biomarker profile"""
    alzheimers_profile = {
        "amyloid_beta_42": 450.0,
        "phospho_tau_181": 420.0,
        "neurofilament_light": 1900.0,
        "alpha_synuclein": 1150.0,
        "dopamine_transporter": 72.0,
        "sod1_activity": 88.0,
        "huntingtin_mutant": 48.0,
        "glial_fibrillary_acidic_protein": 210.0,
        "brain_derived_neurotrophic_factor": 13.0,
        "inflammatory_index": 7.5
    }
    result = biomarker_classifier.predict(alzheimers_profile)
    result["demo_profile"] = "Typical Alzheimer's Disease biomarker pattern"
    return result

@router.get("/demo/parkinsons")
def demo_parkinsons_prediction():
    """Demo prediction using typical Parkinson's biomarker profile"""
    parkinsons_profile = {
        "amyloid_beta_42": 1250.0,
        "phospho_tau_181": 175.0,
        "neurofilament_light": 1450.0,
        "alpha_synuclein": 2900.0,
        "dopamine_transporter": 32.0,
        "sod1_activity": 92.0,
        "huntingtin_mutant": 44.0,
        "glial_fibrillary_acidic_protein": 155.0,
        "brain_derived_neurotrophic_factor": 19.0,
        "inflammatory_index": 5.2
    }
    result = biomarker_classifier.predict(parkinsons_profile)
    result["demo_profile"] = "Typical Parkinson's Disease biomarker pattern"
    return result

@router.get("/model/info")
def get_model_info():
    """Get information about the AI model"""
    return {
        "model_type": "Random Forest Classifier",
        "algorithm": "Ensemble of 100 decision trees",
        "features": biomarker_classifier.feature_names,
        "diseases_classified": biomarker_classifier.disease_labels,
        "training_samples": 1000,
        "model_accuracy_percent": round(biomarker_classifier.accuracy * 100, 1),
        "explainable_ai": True,
        "feature_importance_available": True,
        "biological_context": "Model trained on synthetic data following known biomarker patterns for each disease",
        "real_world_equivalent": "Models like this are trained on ADNI, PPMI, and other clinical biomarker databases"
    }