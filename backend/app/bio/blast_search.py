from Bio.Blast import NCBIWWW, NCBIXML
from Bio import SeqIO
import time

def run_blast_search(sequence: str, program: str = "blastp", database: str = "nr") -> dict:
    """
    Run a BLAST search against NCBI databases.
    
    What BLAST does biologically:
    - Takes your sequence (DNA or protein)
    - Compares it against billions of known sequences
    - Returns the most similar sequences with alignment scores
    
    Parameters:
    - sequence: your DNA or protein sequence
    - program: 
        'blastp' = protein vs protein database
        'blastn' = nucleotide vs nucleotide database
        'blastx' = nucleotide vs protein database
    - database:
        'nr' = non-redundant protein sequences (all known proteins)
        'nt' = nucleotide collection
        'swissprot' = manually curated proteins only
    
    The score tells you how similar two sequences are.
    E-value (expect value) tells you how likely the match is by chance.
    E-value < 0.05 = significant match
    E-value < 0.001 = very significant match
    """
    try:
        if len(sequence) < 10:
            return {"error": "Sequence too short. Minimum 10 characters."}
        
        if len(sequence) > 1000:
            sequence = sequence[:1000]
        
        print(f"Running BLAST search... this takes 30-60 seconds")
        
        result_handle = NCBIWWW.qblast(
            program=program,
            database=database,
            sequence=sequence,
            hitlist_size=5
        )
        
        blast_records = NCBIXML.parse(result_handle)
        blast_record = next(blast_records)
        
        hits = []
        for alignment in blast_record.alignments[:5]:
            for hsp in alignment.hsps[:1]:
                hits.append({
                    "title": alignment.title[:100],
                    "length": alignment.length,
                    "score": hsp.score,
                    "e_value": hsp.expect,
                    "identity_percent": round((hsp.identities / hsp.align_length) * 100, 1),
                    "query_coverage": round((hsp.align_length / len(sequence)) * 100, 1),
                    "alignment_preview": str(hsp.query[:50])
                })
        
        return {
            "program": program,
            "database": database,
            "query_length": len(sequence),
            "hits_found": len(hits),
            "hits": hits,
            "status": "success",
            "note": "E-value < 0.001 indicates a highly significant match"
        }
        
    except Exception as e:
        return {"error": str(e), "program": program, "database": database}


def analyze_sequence(sequence: str) -> dict:
    """
    Analyze basic properties of a biological sequence.
    
    For DNA sequences this calculates:
    - GC content: percentage of G and C bases
      (important because GC pairs are stronger than AT pairs)
    - Base composition
    - Sequence length
    
    For protein sequences this calculates:
    - Amino acid composition
    - Molecular weight estimate
    """
    sequence = sequence.upper().strip()
    
    dna_bases = set('ATCGN')
    protein_aa = set('ACDEFGHIKLMNPQRSTVWY')
    
    is_dna = all(c in dna_bases for c in sequence if c.isalpha())
    
    if is_dna:
        g_count = sequence.count('G')
        c_count = sequence.count('C')
        a_count = sequence.count('A')
        t_count = sequence.count('T')
        total = len(sequence)
        
        gc_content = round(((g_count + c_count) / total) * 100, 2) if total > 0 else 0
        
        return {
            "sequence_type": "DNA",
            "length": total,
            "gc_content_percent": gc_content,
            "base_composition": {
                "A": a_count, "T": t_count,
                "G": g_count, "C": c_count
            },
            "gc_interpretation": (
                "High GC content - thermally stable region" if gc_content > 60
                else "Low GC content - AT-rich region" if gc_content < 40
                else "Typical GC content"
            ),
            "status": "success"
        }
    else:
        return {
            "sequence_type": "Protein",
            "length": len(sequence),
            "amino_acid_composition": {
                aa: sequence.count(aa) for aa in set(sequence)
            },
            "status": "success"
        }