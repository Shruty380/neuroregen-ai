from fastapi import APIRouter
from app.bio.ncbi_fetch import fetch_gene_info, fetch_protein_sequence, search_pubmed
from app.bio.blast_search import analyze_sequence, run_blast_search
from pydantic import BaseModel

router = APIRouter(prefix="/bio", tags=["bioinformatics"])

class SequenceRequest(BaseModel):
    sequence: str

class BlastRequest(BaseModel):
    sequence: str
    program: str = "blastp"
    database: str = "nr"

@router.get("/gene/{gene_symbol}")
def get_gene_from_ncbi(gene_symbol: str):
    """Fetch gene information from NCBI Gene database"""
    return fetch_gene_info(gene_symbol)

@router.get("/protein/{protein_id}")
def get_protein_sequence(protein_id: str):
    """Fetch protein sequence from NCBI Protein database"""
    return fetch_protein_sequence(protein_id)

@router.get("/pubmed/{query}")
def search_papers(query: str, max_results: int = 5):
    """Search PubMed research papers"""
    return search_pubmed(query, max_results)

@router.post("/analyze")
def analyze_bio_sequence(request: SequenceRequest):
    """Analyze a DNA or protein sequence"""
    return analyze_sequence(request.sequence)

@router.post("/blast")
def blast_search(request: BlastRequest):
    """
    Run BLAST sequence similarity search.
    Warning: This takes 30-60 seconds as it queries NCBI servers.
    """
    return run_blast_search(
        request.sequence,
        request.program,
        request.database
    )

@router.get("/demo/alzheimers")
def alzheimers_demo():
    """
    Demo endpoint showing APOE protein analysis.
    APOE is the major genetic risk factor for Alzheimer's disease.
    """
    apoe_sequence_fragment = "MKVLWAALLVTFLAGCQAKVEQAVETEPEPELRQQTEWQSGQRWELALGRFWDYLRWVQTLSEQVQEELLSSQVTQELRALMDETMKELKAYKSELEEQLTPVAEETRARLSKELQAAQARLGADMEDVCGRLVQYRGEVQAMLGQSTEELRVRLASHLRKLRKRLLRDADDLQKRLAVYQAGAREGAERGLSAIRERLGPLVEQGRVRAATVGSLAGQPLQERAQAWGERLRARMEEMGSRTRDRLDEVKEQVAEVRAKLEEQAQQIRLQAEAFQARLKSWFEPLVEDMQRQWAGLVEKVQAAVGTSAAPVPSDNH"
    
    analysis = analyze_sequence(apoe_sequence_fragment)
    
    return {
        "demo": "APOE Protein Fragment Analysis",
        "biological_context": "APOE4 variant increases Alzheimer's risk by 3-4x (heterozygous) or 8-12x (homozygous)",
        "protein_id": "P02649",
        "ncbi_url": "https://www.ncbi.nlm.nih.gov/protein/P02649",
        "sequence_analysis": analysis
    }