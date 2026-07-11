from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Disease(Base):
    __tablename__ = "diseases"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    category = Column(String(50))
    description = Column(Text)
    affected_region = Column(String(100))
    prevalence = Column(String(50))
    onset_age = Column(String(50))

    # One disease has many genes
    genes = relationship("Gene", back_populates="disease")
    biomarkers = relationship("Biomarker", back_populates="disease")


class Gene(Base):
    __tablename__ = "genes"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(20), nullable=False)
    full_name = Column(String(200))
    chromosome = Column(String(10))
    role = Column(Text)
    risk_level = Column(String(20))
    disease_id = Column(Integer, ForeignKey("diseases.id"))

    disease = relationship("Disease", back_populates="genes")


class Biomarker(Base):
    __tablename__ = "biomarkers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    type = Column(String(50))
    sample_source = Column(String(50))
    clinical_significance = Column(Text)
    disease_id = Column(Integer, ForeignKey("diseases.id"))

    disease = relationship("Disease", back_populates="biomarkers")