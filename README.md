# mRNA Prototype - Neoantigen X Plasmid Vector Design & IVT RNA QC

A comprehensive system for developing mRNA vaccines targeting neoantigen X, including automated plasmid design, optimization, validation, and IVT RNA quality control capabilities.

## Overview

This repository contains a complete development pipeline for mRNA vaccine production:

1. **Plasmid Design System**: Automated design, optimization, validation, and documentation capabilities for creating therapeutic vaccine templates
2. **IVT RNA QC Pipeline**: Automated quality control analysis for In Vitro Transcribed RNA samples with regulatory compliance

## Quick Start

### Plasmid Design System

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the plasmid design system:**
   ```bash
   python3 plasmid_builder.py
   ```

3. **Generate schematic diagrams:**
   ```bash
   python3 generate_schematics.py
   ```

### IVT RNA QC Pipeline

1. **Run QC analysis on NanoDrop data:**
   ```bash
   python3 ivt_qc_pipeline.py data/example_nanodrop.csv
   ```

2. **Generate markdown report:**
   ```bash
   python3 ivt_qc_pipeline.py data/example_nanodrop.csv --markdown
   ```

3. **Automated QC via GitHub Actions:**
   - Push to branch `qc/ivt-run-*` or use workflow dispatch
   - Results automatically posted to GitHub issue

### Run All Tests

4. **Run tests:**
   ```bash
   python3 test_plasmid_design.py
   python3 test_ivt_qc_pipeline.py
   ```

## Features

### Plasmid Design System

- **Automated Plasmid Design**: Complete vector construction with all essential components
- **Codon Optimization**: Human-optimized sequences for maximum expression
- **Quality Validation**: Comprehensive in silico validation checks
- **Schematic Generation**: Visual representations of plasmid structure
- **Comprehensive Documentation**: Detailed design rationale and specifications

### IVT RNA QC Pipeline

- **Automated QC Analysis**: Process NanoDrop CSV exports for concentration and purity
- **Regulatory Compliance**: Meet FDA/EMA standards for RNA therapeutics
- **Real-time Results**: Generate JSON reports and markdown summaries
- **GitHub Integration**: Automated workflow with issue commenting
- **Performance Optimized**: < 5s processing time for 100 samples
- **Quality Flagging**: Automatic identification of samples outside acceptance limits

### QC Acceptance Criteria

- **Minimum Concentration**: ≥ 1.0 µg/µL
- **A260/A280 Ratio**: 1.8 - 2.2 (RNA purity indicator)
- **A260/A230 Ratio**: 1.8 - 2.5 (Contamination indicator)

## Plasmid Components

- **CMV Promoter**: Strong mammalian expression
- **Kozak Sequence**: Optimized translation initiation
- **Signal Peptide**: ER targeting for MHC presentation
- **Neoantigen X**: Codon-optimized target antigen (KTVNMRLGL)
- **Expression Tags**: His-tag and FLAG tag for validation
- **BGH polyA**: mRNA stability and termination
- **Selection Marker**: Ampicillin resistance
- **Origin of Replication**: ColE1 for bacterial propagation

## Files

### Core System
- `plasmid_builder.py` - Main design system
- `test_plasmid_design.py` - Plasmid design test suite
- `generate_schematics.py` - Diagram generator
- `requirements.txt` - Python dependencies

### IVT RNA QC Pipeline
- `ivt_qc_pipeline.py` - Automated QC analysis system
- `test_ivt_qc_pipeline.py` - QC pipeline test suite
- `data/example_nanodrop.csv` - Example NanoDrop data
- `.github/workflows/qc-pipeline.yml` - GitHub Actions automation

### Documentation
- `PLASMID_DESIGN_DOCUMENTATION.md` - Complete plasmid documentation
- `README.md` - System overview and usage guide

## Design Results

- **Plasmid Name**: pNeoantigenX-mRNA
- **Total Length**: 2,251 bp
- **Expression System**: Mammalian (Human)
- **Quality Status**: All validations passed

## Next Steps

1. **Experimental Validation**: Transform into competent cells
2. **Expression Testing**: Validate protein expression in mammalian cells
3. **mRNA Synthesis**: Use as template for in vitro transcription
4. **Immunogenicity Testing**: Assess T cell activation

## License

This project is designed for research and educational purposes in vaccine development.