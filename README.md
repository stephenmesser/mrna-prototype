# mRNA Prototype - Neoantigen X Plasmid Vector Design

A comprehensive plasmid vector design system for neoantigen X expression in mRNA vaccine applications.

## Overview

This repository contains a complete plasmid design system for developing mRNA vaccines targeting neoantigen X. The system provides automated design, optimization, validation, and documentation capabilities for creating therapeutic vaccine templates.

## Quick Start

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

4. **Run tests:**
   ```bash
   python3 test_plasmid_design.py
   ```

## Features

- **Automated Plasmid Design**: Complete vector construction with all essential components
- **Codon Optimization**: Human-optimized sequences for maximum expression
- **Quality Validation**: Comprehensive in silico validation checks
- **Schematic Generation**: Visual representations of plasmid structure
- **Comprehensive Documentation**: Detailed design rationale and specifications

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

- `plasmid_builder.py` - Main design system
- `test_plasmid_design.py` - Test suite
- `generate_schematics.py` - Diagram generator
- `PLASMID_DESIGN_DOCUMENTATION.md` - Complete documentation
- `requirements.txt` - Python dependencies

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