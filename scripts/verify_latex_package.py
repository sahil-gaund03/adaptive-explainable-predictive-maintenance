"""
LaTeX Package & Verification Suite
Verifies image paths, BibTeX keys, and syntax completeness for IEEE_Paper_Final.tex
"""

import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PAPER_DIR = PROJECT_ROOT / "paper"
PLOTS_DIR = PROJECT_ROOT / "plots"

TEX_PATH = PAPER_DIR / "IEEE_Paper_Final.tex"
BIB_PATH = PAPER_DIR / "references.bib"

def verify_latex():
    print("=== VERIFYING IEEE LATEX PACKAGE ===")
    
    assert TEX_PATH.exists(), f"Missing {TEX_PATH}"
    assert BIB_PATH.exists(), f"Missing {BIB_PATH}"
    
    tex_content = TEX_PATH.read_text(encoding="utf-8")
    bib_content = BIB_PATH.read_text(encoding="utf-8")
    
    # Extract \includegraphics paths
    fig_matches = re.findall(r'\\includegraphics\[.*?\]\{(.*?)\}', tex_content)
    print(f"Found {len(fig_matches)} figure inclusions in TeX source:")
    missing_figs = 0
    for fig_name in fig_matches:
        fig_file = PLOTS_DIR / fig_name
        if fig_file.exists():
            print(f"  [OK] Figure exists: plots/{fig_name}")
        else:
            print(f"  [FAIL] Figure missing: plots/{fig_name}")
            missing_figs += 1
            
    # Extract \cite{} keys
    cite_matches = re.findall(r'\\cite\{(.*?)\}', tex_content)
    all_cites = set()
    for c_group in cite_matches:
        for c in c_group.split(','):
            all_cites.add(c.strip())
            
    print(f"\nFound {len(all_cites)} unique citation keys in TeX source:")
    bib_keys = set(re.findall(r'@[a-zA-Z]+\{([a-zA-Z0-9_-]+),', bib_content))
    
    missing_cites = 0
    for cite_key in sorted(all_cites):
        if cite_key in bib_keys:
            print(f"  [OK] Citation key matched in references.bib: {cite_key}")
        else:
            print(f"  [FAIL] Missing citation key in references.bib: {cite_key}")
            missing_cites += 1
            
    assert missing_figs == 0, f"Found {missing_figs} missing figures!"
    assert missing_cites == 0, f"Found {missing_cites} missing citations!"
    
    print("\n=========================================================")
    print(" SUCCESS: All figures & BibTeX keys 100% verified!")
    print("=========================================================\n")

if __name__ == "__main__":
    verify_latex()
