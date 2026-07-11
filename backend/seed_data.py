from app.database import SessionLocal, engine, Base
from app import models

Base.metadata.create_all(bind=engine)

def seed():
    db = SessionLocal()
    db.query(models.Biomarker).delete()
    db.query(models.Gene).delete()
    db.query(models.Disease).delete()
    a = models.Disease(name="Alzheimer's Disease", category="Neurodegenerative", description="Progressive memory loss from amyloid plaques and tau tangles.", affected_region="Hippocampus, Cortex", prevalence="55 million worldwide", onset_age="65+")
    p = models.Disease(name="Parkinson's Disease", category="Neurodegenerative", description="Loss of dopaminergic neurons causing motor dysfunction.", affected_region="Substantia Nigra", prevalence="10 million worldwide", onset_age="60+")
    s = models.Disease(name="ALS", category="Motor Neuron Disease", description="Progressive motor neuron degeneration causing paralysis.", affected_region="Motor Cortex, Spinal Cord", prevalence="300,000 worldwide", onset_age="40-70")
    h = models.Disease(name="Huntington's Disease", category="Neurodegenerative", description="CAG repeat expansion destroys striatal neurons.", affected_region="Striatum, Cortex", prevalence="30,000 in USA", onset_age="30-50")
    db.add_all([a, p, s, h])
    db.commit()
    db.refresh(a)
    db.refresh(p)
    db.refresh(s)
    db.refresh(h)
    db.add_all([
        models.Gene(symbol="APOE4", full_name="Apolipoprotein E4", chromosome="19", role="Impairs amyloid-beta clearance", risk_level="High", disease_id=a.id),
        models.Gene(symbol="SNCA", full_name="Alpha-Synuclein", chromosome="4", role="Forms Lewy bodies", risk_level="High", disease_id=p.id),
        models.Gene(symbol="SOD1", full_name="Superoxide Dismutase 1", chromosome="21", role="Toxic free radical generation", risk_level="High", disease_id=s.id),
        models.Gene(symbol="HTT", full_name="Huntingtin", chromosome="4", role="CAG repeat expansion causes toxicity", risk_level="High", disease_id=h.id),
    ])
    db.add_all([
        models.Biomarker(name="Amyloid-beta 42", type="Protein", sample_source="CSF", clinical_significance="Reduced levels indicate plaque accumulation", disease_id=a.id),
        models.Biomarker(name="Alpha-synuclein", type="Protein", sample_source="CSF", clinical_significance="Aggregated forms indicate Lewy body pathology", disease_id=p.id),
        models.Biomarker(name="Neurofilament Light Chain", type="Protein", sample_source="Blood", clinical_significance="Elevated NfL reflects motor neuron damage", disease_id=s.id),
        models.Biomarker(name="Mutant Huntingtin", type="Protein", sample_source="CSF", clinical_significance="Tracks disease burden", disease_id=h.id),
    ])
    db.commit()
    db.close()
    print("Done: 4 diseases, 4 genes, 4 biomarkers seeded")

if __name__ == "__main__":
    seed()
