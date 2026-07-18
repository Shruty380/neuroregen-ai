from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor, black, white
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.units import inch, cm
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from io import BytesIO
from datetime import datetime

EMERALD = HexColor('#10b981')
DARK_BG = HexColor('#1f2937')
GRAY = HexColor('#6b7280')
LIGHT_GRAY = HexColor('#f3f4f6')
DARK_TEXT = HexColor('#111827')
RED = HexColor('#ef4444')
BLUE = HexColor('#3b82f6')

def generate_disease_report(disease_data: dict, ai_prediction: dict = None) -> bytes:
    """
    Generate a professional PDF research report for a disease.
    
    This is equivalent to the supplementary data section
    you would find in a published bioinformatics paper.
    """
    buffer = BytesIO()
    
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=24,
        fontName='Helvetica-Bold',
        textColor=EMERALD,
        spaceAfter=6,
        alignment=TA_LEFT
    )
    
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=11,
        fontName='Helvetica',
        textColor=GRAY,
        spaceAfter=4,
        alignment=TA_LEFT
    )
    
    heading_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading1'],
        fontSize=14,
        fontName='Helvetica-Bold',
        textColor=DARK_TEXT,
        spaceBefore=16,
        spaceAfter=8,
        borderPad=4
    )
    
    body_style = ParagraphStyle(
        'BodyText',
        parent=styles['Normal'],
        fontSize=10,
        fontName='Helvetica',
        textColor=DARK_TEXT,
        spaceAfter=6,
        leading=16,
        alignment=TA_JUSTIFY
    )
    
    label_style = ParagraphStyle(
        'Label',
        parent=styles['Normal'],
        fontSize=9,
        fontName='Helvetica-Bold',
        textColor=GRAY,
        spaceAfter=2
    )
    
    story = []
    
    story.append(Paragraph("NeuroRegen AI", subtitle_style))
    story.append(Paragraph("Research Report", subtitle_style))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph(disease_data.get('name', 'Unknown Disease'), title_style))
    story.append(HRFlowable(width="100%", thickness=2, color=EMERALD, spaceAfter=12))
    
    meta_data = [
        ['Category:', disease_data.get('category', 'N/A'),
         'Generated:', datetime.now().strftime('%B %d, %Y')],
        ['Prevalence:', disease_data.get('prevalence', 'N/A'),
         'Platform:', 'NeuroRegen AI v1.0'],
        ['Onset Age:', disease_data.get('onset_age', 'N/A'),
         'Report Type:', 'Disease Summary'],
    ]
    
    meta_table = Table(meta_data, colWidths=[3*cm, 6*cm, 3*cm, 5*cm])
    meta_table.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
        ('FONTNAME', (2,0), (2,-1), 'Helvetica-Bold'),
        ('TEXTCOLOR', (0,0), (0,-1), GRAY),
        ('TEXTCOLOR', (2,0), (2,-1), GRAY),
        ('TEXTCOLOR', (1,0), (1,-1), DARK_TEXT),
        ('TEXTCOLOR', (3,0), (3,-1), DARK_TEXT),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("1. Disease Overview", heading_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=LIGHT_GRAY, spaceAfter=8))
    story.append(Paragraph(disease_data.get('description', ''), body_style))
    
    story.append(Paragraph("Affected Brain Region:", label_style))
    story.append(Paragraph(disease_data.get('affected_region', 'N/A'), body_style))
    
    genes = disease_data.get('genes', [])
    if genes:
        story.append(Paragraph("2. Associated Genes", heading_style))
        story.append(HRFlowable(width="100%", thickness=0.5, color=LIGHT_GRAY, spaceAfter=8))
        story.append(Paragraph(
            f"The following {len(genes)} gene(s) have been identified as significant in {disease_data.get('name', 'this disease')}:",
            body_style
        ))
        
        gene_header = [['Gene Symbol', 'Full Name', 'Chromosome', 'Risk Level']]
        gene_rows = []
        for gene in genes:
            gene_rows.append([
                gene.get('symbol', 'N/A'),
                gene.get('full_name', 'N/A')[:40],
                gene.get('chromosome', 'N/A'),
                gene.get('risk_level', 'N/A')
            ])
        
        gene_table = Table(
            gene_header + gene_rows,
            colWidths=[3*cm, 8*cm, 3*cm, 3*cm]
        )
        gene_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), DARK_BG),
            ('TEXTCOLOR', (0,0), (-1,0), white),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 9),
            ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [white, LIGHT_GRAY]),
            ('TEXTCOLOR', (0,1), (-1,-1), DARK_TEXT),
            ('GRID', (0,0), (-1,-1), 0.5, HexColor('#e5e7eb')),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
        ]))
        story.append(gene_table)
        story.append(Spacer(1, 0.1*inch))
        
        for gene in genes:
            if gene.get('role'):
                story.append(Paragraph(
                    f"<b>{gene.get('symbol')}</b> — {gene.get('role')}",
                    body_style
                ))
    
    biomarkers = disease_data.get('biomarkers', [])
    if biomarkers:
        story.append(Paragraph("3. Clinical Biomarkers", heading_style))
        story.append(HRFlowable(width="100%", thickness=0.5, color=LIGHT_GRAY, spaceAfter=8))
        
        bm_header = [['Biomarker', 'Type', 'Sample Source']]
        bm_rows = [[
            bm.get('name', 'N/A'),
            bm.get('type', 'N/A'),
            bm.get('sample_source', 'N/A')
        ] for bm in biomarkers]
        
        bm_table = Table(
            bm_header + bm_rows,
            colWidths=[6*cm, 4*cm, 7*cm]
        )
        bm_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), DARK_BG),
            ('TEXTCOLOR', (0,0), (-1,0), white),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 9),
            ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [white, LIGHT_GRAY]),
            ('TEXTCOLOR', (0,1), (-1,-1), DARK_TEXT),
            ('GRID', (0,0), (-1,-1), 0.5, HexColor('#e5e7eb')),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
        ]))
        story.append(bm_table)
        story.append(Spacer(1, 0.1*inch))
        
        for bm in biomarkers:
            if bm.get('clinical_significance'):
                story.append(Paragraph(
                    f"<b>{bm.get('name')}</b> — {bm.get('clinical_significance')}",
                    body_style
                ))
    
    if ai_prediction:
        story.append(Paragraph("4. AI Analysis", heading_style))
        story.append(HRFlowable(width="100%", thickness=0.5, color=LIGHT_GRAY, spaceAfter=8))
        
        story.append(Paragraph(
            f"<b>Predicted Disease:</b> {ai_prediction.get('prediction', 'N/A')} "
            f"(Confidence: {ai_prediction.get('confidence_percent', 0)}%)",
            body_style
        ))
        story.append(Paragraph(
            ai_prediction.get('explanation', ''),
            body_style
        ))
        
        top_features = ai_prediction.get('top_features', {})
        if top_features:
            story.append(Paragraph("Top Predictive Biomarkers (Feature Importance):", label_style))
            for feature, importance in list(top_features.items())[:5]:
                story.append(Paragraph(
                    f"• {feature.replace('_', ' ').title()}: {importance}% importance",
                    body_style
                ))
    
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("5. Methods", heading_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=LIGHT_GRAY, spaceAfter=8))
    story.append(Paragraph(
        "Disease data was curated from published literature and stored in a SQLite database "
        "managed via SQLAlchemy ORM. Gene and biomarker information was cross-referenced "
        "with NCBI Gene and UniProt databases using the Biopython Entrez interface.",
        body_style
    ))
    story.append(Paragraph(
        "The AI disease classifier was implemented as a Random Forest ensemble (n=100 trees, "
        "max_depth=10) trained on synthetic biomarker data generated to reflect known "
        "biological patterns for each disease class. Features were standardized using "
        "StandardScaler prior to training. Model performance was evaluated on a held-out "
        "test set (80/20 split). Feature importance was extracted from the trained ensemble "
        "to provide explainable predictions.",
        body_style
    ))
    story.append(Paragraph(
        "The platform was built using FastAPI (Python) for the backend REST API, "
        "Next.js and React for the frontend interface, and SQLite for local data storage. "
        "All source code is available at github.com/Shruty380/neuroregen-ai.",
        body_style
    ))
    
    story.append(Spacer(1, 0.2*inch))
    story.append(HRFlowable(width="100%", thickness=0.5, color=LIGHT_GRAY, spaceAfter=8))
    story.append(Paragraph(
        f"Generated by NeuroRegen AI Platform · {datetime.now().strftime('%B %d, %Y')} · "
        "For research purposes only · Not for clinical use",
        ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8,
                      textColor=GRAY, alignment=TA_CENTER)
    ))
    
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()


def generate_csv_export(diseases: list) -> str:
    """
    Generate a CSV export of all disease data.
    CSV is the standard format for sharing biological data
    between researchers and for loading into R or Python for analysis.
    """
    lines = []
    lines.append("disease_name,category,prevalence,onset_age,gene_symbol,gene_full_name,chromosome,risk_level,biomarker_name,biomarker_type,sample_source")
    
    for disease in diseases:
        genes = disease.get('genes', [{}])
        biomarkers = disease.get('biomarkers', [{}])
        
        max_rows = max(len(genes), len(biomarkers), 1)
        
        for i in range(max_rows):
            gene = genes[i] if i < len(genes) else {}
            bm = biomarkers[i] if i < len(biomarkers) else {}
            
            row = [
                disease.get('name', ''),
                disease.get('category', ''),
                disease.get('prevalence', ''),
                disease.get('onset_age', ''),
                gene.get('symbol', ''),
                gene.get('full_name', ''),
                gene.get('chromosome', ''),
                gene.get('risk_level', ''),
                bm.get('name', ''),
                bm.get('type', ''),
                bm.get('sample_source', ''),
            ]
            lines.append(','.join(f'"{str(v)}"' for v in row))
    
    return '\n'.join(lines)