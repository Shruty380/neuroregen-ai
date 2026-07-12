from Bio import Entrez, SeqIO
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Your email is required by NCBI - they contact you if you overuse their API
Entrez.email = os.getenv("NCBI_EMAIL", "shruty1522@gmail.com")
Entrez.api_key = os.getenv("NCBI_API_KEY", "")

def fetch_gene_info(gene_symbol: str, organism: str = "Homo sapiens") -> dict:
    """
    Fetch gene information from NCBI Gene database.
    
    What this does biologically:
    - Searches NCBI's Gene database for a specific gene symbol
    - Returns the official gene name, description, chromosome location
    - This is the same data researchers use when studying disease genes
    """
    try:
        # Search NCBI Gene database
        search_term = f"{gene_symbol}[Gene Name] AND {organism}[Organism]"
        
        search_handle = Entrez.esearch(db="gene", term=search_term, retmax=1)
        search_results = Entrez.read(search_handle)
        search_handle.close()
        
        if not search_results["IdList"]:
            return {"error": f"Gene {gene_symbol} not found in NCBI"}
        
        gene_id = search_results["IdList"][0]
        
        # Fetch detailed gene information
        fetch_handle = Entrez.efetch(
            db="gene",
            id=gene_id,
            rettype="gene_table",
            retmode="text"
        )
        gene_data = fetch_handle.read()
        fetch_handle.close()
        
        return {
            "gene_symbol": gene_symbol,
            "organism": organism,
            "ncbi_gene_id": gene_id,
            "ncbi_url": f"https://www.ncbi.nlm.nih.gov/gene/{gene_id}",
            "data_preview": str(gene_data)[:500],
            "status": "success"
        }
        
    except Exception as e:
        return {"error": str(e), "gene_symbol": gene_symbol}


def fetch_protein_sequence(protein_id: str) -> dict:
    """
    Fetch a protein sequence from NCBI Protein database.
    
    What this does biologically:
    - Downloads the actual amino acid sequence of a protein
    - Amino acids are the building blocks of proteins
    - Each protein has a unique accession number in NCBI
    
    Example protein IDs for neurodegenerative diseases:
    - P02649 = APOE (Alzheimer's risk gene protein)
    - P37840 = Alpha-synuclein (Parkinson's protein)
    - P00441 = SOD1 (ALS protein)
    """
    try:
        handle = Entrez.efetch(
            db="protein",
            id=protein_id,
            rettype="fasta",
            retmode="text"
        )
        record = SeqIO.read(handle, "fasta")
        handle.close()
        
        sequence = str(record.seq)
        
        return {
            "protein_id": protein_id,
            "name": record.description,
            "length": len(sequence),
            "sequence": sequence,
            "sequence_preview": sequence[:50] + "..." if len(sequence) > 50 else sequence,
            "amino_acid_composition": {
                aa: sequence.count(aa) 
                for aa in set(sequence)
            },
            "status": "success"
        }
        
    except Exception as e:
        return {"error": str(e), "protein_id": protein_id}


def search_pubmed(query: str, max_results: int = 5) -> dict:
    """
    Search PubMed for research papers.
    
    PubMed contains 35 million biomedical research papers.
    This function lets us find papers about specific genes or diseases.
    
    Example queries:
    - "APOE4 Alzheimer's disease"
    - "alpha-synuclein Parkinson aggregation"
    - "neurogenesis stem cells"
    """
    try:
        search_handle = Entrez.esearch(
            db="pubmed",
            term=query,
            retmax=max_results,
            sort="relevance"
        )
        search_results = Entrez.read(search_handle)
        search_handle.close()
        
        ids = search_results["IdList"]
        
        if not ids:
            return {"query": query, "results": [], "count": 0}
        
        fetch_handle = Entrez.efetch(
            db="pubmed",
            id=",".join(ids),
            rettype="abstract",
            retmode="text"
        )
        abstracts_raw = fetch_handle.read()
        fetch_handle.close()
        
        return {
            "query": query,
            "total_found": search_results["Count"],
            "returned": len(ids),
            "pubmed_ids": ids,
            "abstracts_preview": str(abstracts_raw)[:1000],
            "pubmed_search_url": f"https://pubmed.ncbi.nlm.nih.gov/?term={query.replace(' ', '+')}",
            "status": "success"
        }
        
    except Exception as e:
        return {"error": str(e), "query": query}