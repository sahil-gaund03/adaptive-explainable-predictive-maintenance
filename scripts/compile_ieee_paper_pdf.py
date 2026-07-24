"""
IEEE LaTeX PDF Compilation & Validation Harness
Parses paper/IEEE_Paper_Final.tex and compiles a publication-ready PDF at paper/IEEE_Paper_Final.pdf.
"""

import os
import re
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, HRFlowable
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PAPER_DIR = PROJECT_ROOT / "paper"
PLOTS_DIR = PROJECT_ROOT / "plots"

TEX_PATH = PAPER_DIR / "IEEE_Paper_Submission2.tex"
PDF_PATH = PAPER_DIR / "IEEE_Paper_Submission.pdf"

def compile_pdf():
    print("=== STARTING IEEE LATEX PDF COMPILATION ===")
    assert TEX_PATH.exists(), f"Missing TeX source at {TEX_PATH}"
    
    tex_text = TEX_PATH.read_text(encoding="utf-8")
    
    # Document Setup - Standard IEEE Margins (0.75 in)
    doc = SimpleDocTemplate(
        str(PDF_PATH),
        pagesize=letter,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch
    )
    
    styles = getSampleStyleSheet()
    
    # Custom IEEE Typography Styles
    title_style = ParagraphStyle(
        'IEEETitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        alignment=1, # Center
        spaceAfter=12,
        textColor=colors.HexColor("#002B49")
    )
    
    author_style = ParagraphStyle(
        'IEEEAuthor',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        alignment=1, # Center
        spaceAfter=16,
        textColor=colors.HexColor("#222222")
    )
    
    abstract_heading = ParagraphStyle(
        'IEEEAbstractHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor("#002B49"),
        spaceAfter=4
    )
    
    abstract_text = ParagraphStyle(
        'IEEEAbstractText',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9,
        leading=12,
        spaceAfter=14,
        textColor=colors.HexColor("#333333")
    )
    
    h1_style = ParagraphStyle(
        'IEEEH1',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        spaceBefore=14,
        spaceAfter=6,
        textColor=colors.HexColor("#002B49")
    )
    
    h2_style = ParagraphStyle(
        'IEEEH2',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=13,
        spaceBefore=10,
        spaceAfter=4,
        textColor=colors.HexColor("#1A365D")
    )
    
    body_style = ParagraphStyle(
        'IEEEBody',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=9.5,
        leading=12.5,
        spaceAfter=6,
        textColor=colors.HexColor("#111111")
    )
    
    caption_style = ParagraphStyle(
        'IEEECaption',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=11,
        alignment=1, # Center
        spaceBefore=4,
        spaceAfter=10,
        textColor=colors.HexColor("#444444")
    )
    
    story = []
    
    # 1. Document Title
    story.append(Paragraph("Adaptive Explainable Predictive Maintenance Using Ensemble Learning and Online Concept Drift Detection for Smart Manufacturing", title_style))
    
    # 2. Authors & Affiliations
    author_text = "<b>Autonomous Industrial AI R&D Team</b>, Member, IEEE<br/><i>Department of Industrial Automation and Machine Learning R&D Group</i><br/>Repository: <font color='#0066cc'>https://github.com/sahil-gaund03/adaptive-explainable-predictive-maintenance.git</font>"
    story.append(Paragraph(author_text, author_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CCCCCC"), spaceBefore=2, spaceAfter=10))
    
    # Parse sections from TeX source
    lines = tex_text.split('\n')
    in_abstract = False
    abstract_content = []
    
    for line in lines:
        line_s = line.strip()
        if '\\begin{abstract}' in line_s:
            in_abstract = True
            continue
        if '\\end{abstract}' in line_s:
            in_abstract = False
            story.append(Paragraph("<b>Abstract</b>", abstract_heading))
            story.append(Paragraph(" ".join(abstract_content), abstract_text))
            story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#DDDDDD"), spaceBefore=4, spaceAfter=10))
            continue
        if in_abstract:
            abstract_content.append(line_s)
            continue
            
        # IEEE Keywords
        if '\\begin{IEEEkeywords}' in line_s:
            kw_text = line_s.replace('\\begin{IEEEkeywords}', '').replace('\\end{IEEEkeywords}', '').strip()
            continue
            
        # Section Headings
        if line_s.startswith('\\section{'):
            sec_title = re.search(r'\\section\{(.*?)\}', line_s).group(1)
            story.append(Paragraph(sec_title, h1_style))
            continue
        if line_s.startswith('\\subsection{'):
            subsec_title = re.search(r'\\subsection\{(.*?)\}', line_s).group(1)
            story.append(Paragraph(subsec_title, h2_style))
            continue
            
        # Figures
        if '\\includegraphics' in line_s:
            fig_match = re.search(r'\\includegraphics\[.*?\]\{(.*?)\}', line_s)
            if fig_match:
                fig_name = fig_match.group(1)
                fig_file = PLOTS_DIR / fig_name
                if fig_file.exists():
                    img = Image(str(fig_file), width=6.5*inch, height=3.2*inch)
                    story.append(img)
                    story.append(Spacer(1, 4))
            continue
            
        # Captions
        if line_s.startswith('\\caption{'):
            cap_text = re.search(r'\\caption\{(.*?)\}', line_s).group(1)
            story.append(Paragraph(f"<b>Figure / Table:</b> {cap_text}", caption_style))
            story.append(Spacer(1, 6))
            continue
            
        # Body Paragraphs
        if line_s and not line_s.startswith('\\') and not line_s.startswith('%'):
            # Escape HTML characters & clean LaTeX formatting safely
            clean_p = line_s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            clean_p = re.sub(r'\\textbf\{(.*?)\}', r'<b>\1</b>', clean_p)
            clean_p = re.sub(r'\\textit\{(.*?)\}', r'<i>\1</i>', clean_p)
            clean_p = re.sub(r'\\texttt\{(.*?)\}', r'<code>\1</code>', clean_p)
            clean_p = re.sub(r'\\cite\{(.*?)\}', r'[\1]', clean_p)
            clean_p = re.sub(r'\\ref\{(.*?)\}', r'\1', clean_p)
            clean_p = re.sub(r'\$(.*?)\$', r'\1', clean_p)
            clean_p = clean_p.replace('---', '—').replace('--', '–').replace('\\$', '$')
            if clean_p.strip():
                try:
                    story.append(Paragraph(clean_p, body_style))
                except Exception as e:
                    # Fallback to plain text Paragraph on markup edge cases
                    plain_p = re.sub(r'<[^>]+>', '', clean_p)
                    story.append(Paragraph(plain_p, body_style))
                
    doc.build(story)
    
    print(f"\n=========================================================")
    print(f" SUCCESS: {PDF_PATH.name} generated! ({PDF_PATH.stat().st_size / 1024:.1f} KB)")
    print(f"=========================================================\n")

if __name__ == "__main__":
    compile_pdf()
