from pydantic import BaseModel
from typing import List, Optional

class GeneBase(BaseModel):
    symbol: str
    full_name: Optional[str] = None
    chromosome: Optional[str] = None
    role: Optional[str] = None
    risk_level: Optional[str] = None

class Gene(GeneBase):
    id: int
    disease_id: int
    class Config:
        from_attributes = True

class BiomarkerBase(BaseModel):
    name: str
    type: Optional[str] = None
    sample_source: Optional[str] = None
    clinical_significance: Optional[str] = None

class Biomarker(BiomarkerBase):
    id: int
    disease_id: int
    class Config:
        from_attributes = True

class DiseaseBase(BaseModel):
    name: str
    category: Optional[str] = None
    description: Optional[str] = None
    affected_region: Optional[str] = None
    prevalence: Optional[str] = None
    onset_age: Optional[str] = None

class Disease(DiseaseBase):
    id: int
    genes: List[Gene] = []
    biomarkers: List[Biomarker] = []
    class Config:
        from_attributes = True