from fastapi import APIRouter, Depends
from fastapi.responses import Response
from pkg_resources import safe_name
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor, black, white
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.units import inch, cm
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from io import BytesIO

def generate_disease_report(disease_data: dict, ai_prediction: dict = None) -> bytes:
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
    styles = getSampleStyleSheet()
    story = []
    story.append(Paragraph("NeuroRegen AI — Research Report", styles['Title']))
    story.append(Paragraph(disease_data.get('name', ''), styles['Heading1']))
    story.append(Paragraph(disease_data.get('description', ''), styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("Genes", styles['Heading2']))
    for gene in disease_data.get('genes', []):
        story.append(Paragraph(f"{gene.get('symbol')} — {gene.get('full_name')} (Chr {gene.get('chromosome')}, {gene.get('risk_level')} risk)", styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("Biomarkers", styles['Heading2']))
    for bm in disease_data.get('biomarkers', []):
        story.append(Paragraph(f"{bm.get('name')} — {bm.get('clinical_significance', '')}", styles['Normal']))
    if ai_prediction:
        story.append(Spacer(1, 0.2*inch))
        story.append(Paragraph("AI Analysis", styles['Heading2']))
        story.append(Paragraph(f"Prediction: {ai_prediction.get('prediction')} ({ai_prediction.get('confidence_percent')}% confidence)", styles['Normal']))
        story.append(Paragraph(ai_prediction.get('explanation', ''), styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("Methods", styles['Heading2']))
    story.append(Paragraph("Random Forest classifier (n=100) trained on synthetic biomarker data. FastAPI backend, Next.js frontend, SQLite database. Source: github.com/Shruty380/neuroregen-ai", styles['Normal']))
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()

def generate_csv_export(diseases: list) -> str:
    lines = ["disease_name,category,prevalence,gene_symbol,biomarker_name"]
    for disease in diseases:
        genes = disease.get('genes', [{}])
        biomarkers = disease.get('biomarkers', [{}])
        max_rows = max(len(genes), len(biomarkers), 1)
        for i in range(max_rows):
            gene = genes[i] if i < len(genes) else {}
            bm = biomarkers[i] if i < len(biomarkers) else {}
            name = disease.get('name','')
            cat = disease.get('category','')
            prev = disease.get('prevalence','')
            gsym = gene.get('symbol','')
            bname = bm.get('name','')
            lines.append(f'"{name}","{cat}","{prev}","{gsym}","{bname}"')
    return '\n'.join(lines)

from app.ai.biomarker_model import biomarker_classifier
from datetime import datetime

router = APIRouter(prefix="/export", tags=["Export & Reports"])

@router.get("/disease/{disease_id}/pdf")
def export_disease_pdf(disease_id: int, db: Session = Depends(get_db)):
    """
    Generate and download a PDF research report for a disease.
    Includes disease overview, genes, biomarkers, AI analysis, and methods section.
    """
    disease = db.query(models.Disease).filter(
        models.Disease.id == disease_id
    ).first()

    if not disease:
        return {"error": "Disease not found"}

    disease_dict = {
        "name": disease.name,
        "category": disease.category,
        "description": disease.description,
        "affected_region": disease.affected_region,
        "prevalence": disease.prevalence,
        "onset_age": disease.onset_age,
        "genes": [
            {
                "symbol": g.symbol,
                "full_name": g.full_name,
                "chromosome": g.chromosome,
                "role": g.role,
                "risk_level": g.risk_level
            }
            for g in disease.genes
        ],
        "biomarkers": [
            {
                "name": b.name,
                "type": b.type,
                "sample_source": b.sample_source,
                "clinical_significance": b.clinical_significance
            }
            for b in disease.biomarkers
        ]
    }

    demo_profiles = {
        1: {"amyloid_beta_42": 450.0, "phospho_tau_181": 420.0,
            "neurofilament_light": 1900.0, "alpha_synuclein": 1150.0,
            "dopamine_transporter": 72.0, "sod1_activity": 88.0,
            "huntingtin_mutant": 48.0, "glial_fibrillary_acidic_protein": 210.0,
            "brain_derived_neurotrophic_factor": 13.0, "inflammatory_index": 7.5},
        2: {"amyloid_beta_42": 1250.0, "phospho_tau_181": 175.0,
            "neurofilament_light": 1450.0, "alpha_synuclein": 2900.0,
            "dopamine_transporter": 32.0, "sod1_activity": 92.0,
            "huntingtin_mutant": 44.0, "glial_fibrillary_acidic_protein": 155.0,
            "brain_derived_neurotrophic_factor": 19.0, "inflammatory_index": 5.2},
        3: {"amyloid_beta_42": 1100.0, "phospho_tau_181": 170.0,
            "neurofilament_light": 4500.0, "alpha_synuclein": 1100.0,
            "dopamine_transporter": 75.0, "sod1_activity": 30.0,
            "huntingtin_mutant": 48.0, "glial_fibrillary_acidic_protein": 350.0,
            "brain_derived_neurotrophic_factor": 12.0, "inflammatory_index": 8.0},
        4: {"amyloid_beta_42": 1150.0, "phospho_tau_181": 175.0,
            "neurofilament_light": 2200.0, "alpha_synuclein": 1300.0,
            "dopamine_transporter": 68.0, "sod1_activity": 88.0,
            "huntingtin_mutant": 850.0, "glial_fibrillary_acidic_protein": 180.0,
            "brain_derived_neurotrophic_factor": 14.0, "inflammatory_index": 9.0},
    }

    ai_result = None
    if disease_id in demo_profiles:
        ai_result = biomarker_classifier.predict(demo_profiles[disease_id])

    pdf_bytes = generate_disease_report(disease_dict, ai_result)

    safe_name = disease.name.lower().replace(' ', '_').replace("'", '')
    filename = f"neuroregen_{safe_name}_{datetime.now().strftime('%Y%m%d')}.pdf"

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@router.get("/diseases/csv")
def export_all_diseases_csv(db: Session = Depends(get_db)):
    """
    Export all disease data as CSV.
    Standard format for bioinformatics data sharing and analysis in R/Python.
    """
    diseases = db.query(models.Disease).all()

    diseases_list = []
    for disease in diseases:
        diseases_list.append({
            "name": disease.name,
            "category": disease.category,
            "prevalence": disease.prevalence,
            "onset_age": disease.onset_age,
            "genes": [{"symbol": g.symbol, "full_name": g.full_name,
                       "chromosome": g.chromosome, "risk_level": g.risk_level}
                      for g in disease.genes],
            "biomarkers": [{"name": b.name, "type": b.type,
                           "sample_source": b.sample_source}
                          for b in disease.biomarkers]
        })

    csv_content = generate_csv_export(diseases_list)

    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=neuroregen_diseases.csv"}
    )


@router.get("/methods")
def get_methods_section():
    """
    Return the platform methods section in JSON format.
    This is the text you would include in a research paper's methods section.
    """
    return {
        "platform": "NeuroRegen AI",
        "version": "1.0.0",
        "methods": {
            "data_collection": {
                "description": "Disease data curated from published literature",
                "sources": ["NCBI Gene", "UniProt", "PubMed", "OMIM"],
                "storage": "SQLite via SQLAlchemy ORM"
            },
            "bioinformatics_pipeline": {
                "description": "Gene and sequence analysis pipeline",
                "tools": ["Biopython", "NCBI Entrez API", "NCBI BLAST"],
                "operations": ["Gene fetching", "Protein sequence retrieval",
                              "Sequence analysis", "PubMed search"]
            },
            "ai_model": {
                "algorithm": "Random Forest Classifier",
                "library": "scikit-learn",
                "n_estimators": 100,
                "max_depth": 10,
                "train_test_split": "80/20",
                "features": 10,
                "feature_scaling": "StandardScaler",
                "training_samples": 1000,
                "classes": 4,
                "explainability": "Feature importance from ensemble"
            },
            "tech_stack": {
                "backend": "FastAPI (Python 3.9)",
                "frontend": "Next.js 15, React, TailwindCSS",
                "database": "SQLite (development), PostgreSQL (production)",
                "ml_libraries": ["scikit-learn", "numpy", "pandas"],
                "bio_libraries": ["biopython"],
                "deployment": "Docker (Phase 8)"
            },
            "limitations": [
                "AI model trained on synthetic data, not real patient data",
                "Requires validation on clinical datasets before any medical use",
                "BLAST searches depend on NCBI server availability",
                "Current database contains representative gene subset only"
            ],
            "citation": "NeuroRegen AI Platform. github.com/Shruty380/neuroregen-ai"
        }
    }