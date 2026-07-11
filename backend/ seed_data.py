from app.database import SessionLocal, engine, Base
from app import models

Base.metadata.create_all(bind=engine)

def seed():
    db = SessionLocal()

    db.query(models.Biomarker).delete()
    db.query(models.Gene).delete()
    db.query(models.Disease).delete()

    alzheimers = models.Disease(name="Alzheimer's Disease", category="Neurodegenerative", description="Progressive neurodegenerative disorder characterized by amyloid-beta plaques and neurofibrillary tau tangles, leading to synaptic loss and neuronal death primarily in the hippocampus and cortex.", affected_region="Hippocampus, Entorhinal Cortex, Prefrontal Cortex", prevalence="55 million worldwide", onset_age="65+ (late onset), 40-65 (early onset)")
    parkinsons = models.Disease(name="Parkinson's Disease", category="Neurodegenerative", description="Progressive loss of dopaminergic neurons in the substantia nigra pars compacta, leading to motor symptoms. Characterized by Lewy bodies composed of misfolded alpha-synuclein protein.", affected_region="Substantia Nigra, Basal Ganglia, Brainstem", prevalence="10 million worldwide", onset_age="60+ (typical), under 50 (young onset)")
    als = models.Disease(name="ALS", category="Motor Neuron Disease", description="Amyotrophic Lateral Sclerosis causes progressive degeneration of both upper and lower motor neurons leading to muscle weakness, paralysis, and eventually respiratory failure.", affected_region="Motor Cortex, Brainstem, Spinal Cord", prevalence="300,000 worldwide", onset_age="40-70")
    huntingtons = models.Disease(name="Huntington's Disease", category="Neurodegenerative", description="Autosomal dominant disorder caused by CAG trinucleotide repeat expansion in the HTT gene. Produces toxic mutant huntingtin protein that destroys striatal and cortical neurons.", affected_region="Striatum, Caudate Nucleus, Putamen, Cortex", prevalence="30,000 in USA, 200,000 at risk", onset_age="30-50")

    db.add_all([alzheimers, parkinsons, als, huntingtons])
    db.commit()
    db.refresh(alzheimers)
    db.refresh(parkinsons)
    db.refresh(als)
    db.refresh(huntingtons)

    db.add_all([
        models.Gene(symbol="APOE4", full_name="Apolipoprotein E4", chromosome="19", role="Major genetic risk factor. Impairs amyloid-beta clearance and promotes plaque formation.", risk_level="High", disease_id=alzheimers.id),
        models.Gene(symbol="APP", full_name="Amyloid Precursor Protein", chromosome="21", role="Mutations cause overproduction of amyloid-beta peptides leading to early-onset Alzheimer's.", risk_level="High", disease_id=alzheimers.id),
        models.Gene(symbol="PSEN1", full_name="Presenilin 1", chromosome="14", role="Most common cause of familial early-onset Alzheimer's. Affects gamma-secretase processing of APP.", risk_level="High", disease_id=alzheimers.id),
        models.Gene(symbol="SNCA", full_name="Alpha-Synuclein", chromosome="4", role="Mutations lead to toxic protein aggregation and Lewy body formation.", risk_level="High", disease_id=parkinsons.id),
        models.Gene(symbol="LRRK2", full_name="Leucine Rich Repeat Kinase 2", chromosome="12", role="Most common genetic cause of familial Parkinson's. Mutations increase kinase activity causing neuronal death.", risk_level="High", disease_id=parkinsons.id),
        models.Gene(symbol="PINK1", full_name="PTEN-induced Kinase 1", chromosome="1", role="Regulates mitochondrial quality control. Loss of function impairs mitophagy.", risk_level="Medium", disease_id=parkinsons.id),
        models.Gene(symbol="SOD1", full_name="Superoxide Dismutase 1", chromosome="21", role="First ALS gene discovered. Mutations cause toxic free radical generation in motor neurons.", risk_level="High", disease_id=als.id),
        models.Gene(symbol="C9orf72", full_name="Chromosome 9 Open Reading Frame 72", chromosome="9", role="Most common genetic cause of ALS. GGGGCC repeat expansion causes RNA toxicity.", risk_level="High", disease_id=als.id),
        models.Gene(symbol="FUS", full_name="Fused in Sarcoma", chromosome="16", role="RNA-binding protein mutations cause cytoplasmic mislocalization and toxic aggregation.", risk_level="Medium", disease_id=als.id),
        models.Gene(symbol="HTT", full_name="Huntingtin", chromosome="4", role="CAG repeat expansion beyond 36 repeats produces mutant huntingtin protein. Longer repeats mean earlier onset.", risk_level="High", disease_id=huntingtons.id),
    ])

    db.add_all([
        models.Biomarker(name="Amyloid-beta 42", type="Protein", sample_source="CSF, PET scan", clinical_significance="Reduced CSF levels indicate amyloid plaque accumulation. Primary diagnostic biomarker for Alzheimer's.", disease_id=alzheimers.id),
        models.Biomarker(name="Phospho-tau 181", type="Protein", sample_source="CSF, Blood", clinical_significance="Elevated levels indicate neurofibrillary tangle formation. Correlates with disease progression.", disease_id=alzheimers.id),
        models.Biomarker(name="Alpha-synuclein aggregates", type="Protein", sample_source="CSF, Blood, Skin biopsy", clinical_significance="Aggregated forms indicate Lewy body pathology. Seed amplification assays show high sensitivity.", disease_id=parkinsons.id),
        models.Biomarker(name="Dopamine transporter", type="Imaging", sample_source="DaTscan SPECT imaging", clinical_significance="Reduced striatal binding confirms dopaminergic neuron loss in Parkinson's.", disease_id=parkinsons.id),
        models.Biomarker(name="Neurofilament Light Chain", type="Protein", sample_source="CSF, Blood", clinical_significance="Elevated NfL reflects axonal damage. Correlates with ALS progression rate.", disease_id=als.id),
        models.Biomarker(name="Mutant Huntingtin protein", type="Protein", sample_source="CSF, Blood", clinical_significance="Quantification tracks disease burden. Levels correlate with CAG repeat length.", disease_id=huntingtons.id),
    ])

    db.commit()
    db.close()
    print("Database seeded: 4 diseases, 10 genes, 6 biomarkers")

if __name__ == "__main__":
    seed()