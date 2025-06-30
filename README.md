# Neoantigen X Plasmid Vector Design

## Overview

This repository contains a comprehensive plasmid vector design system for neoantigen X, specifically optimized for mRNA vaccine applications. The design addresses all key requirements for therapeutic mRNA vaccine development including codon optimization, expression tracking, purification capabilities, and compatibility with mRNA synthesis processes.

## Features

### ✅ Completed Objectives

- **Neoantigen X Sequence Definition**: Synthetic 65 amino acid neoantigen sequence with human codon optimization
- **Promoter Selection**: Multiple promoter options including T7, CMV, EF1A, and SV40 for different expression systems
- **Expression Tags**: 6xHis and FLAG tags for protein tracking and purification
- **mRNA Synthesis Compatibility**: Optimized design for in vitro transcription and mRNA vaccine production
- **In Silico Validation**: Comprehensive validation system checking sequence quality, GC content, and potential synthesis issues
- **Schematic Generation**: Data structure for creating plasmid maps and visual representations

## Plasmid Design Details

### Neoantigen X Specifications

```
Name: Neoantigen_X
Amino Acid Sequence: MKTVRQERLKSIVRILERSKEPVSGAQLAEELSVSRQVIVQDIAYLRSLGYNIVATPRGYVLAGG
Length: 65 amino acids
Description: Synthetic neoantigen X designed for therapeutic mRNA vaccine
Source: Synthetic design optimized for immunogenicity
```

### Vector Components (pNeoX_T7)

1. **T7 Promoter** (20 bp) - Enables in vitro transcription for mRNA synthesis
2. **Kozak Sequence + Start Codon** (9 bp) - Optimal translation initiation
3. **N-terminal Tags** (42 bp) - 6xHis + FLAG tags for purification and detection
4. **Neoantigen X CDS** (195 bp) - Codon-optimized coding sequence for human expression
5. **Stop Codon** (3 bp) - Translation termination
6. **Poly(A) Signal** (49 bp) - mRNA stability and translation efficiency
7. **T7 Terminator** (19 bp) - Transcription termination
8. **Ampicillin Resistance** (861 bp) - Bacterial selection marker

**Total Vector Length**: 1,198 bp  
**GC Content**: 51.7% (within optimal range)

## Design Rationale

### Promoter Selection
- **T7 Promoter**: Chosen for optimal compatibility with in vitro transcription systems used in mRNA vaccine production
- High expression levels and well-characterized performance in mRNA synthesis

### Codon Optimization
- Optimized for human codon usage to maximize expression in mammalian cells
- Uses most frequently used codons for each amino acid to enhance translation efficiency

### Expression Tags
- **6xHis Tag**: Enables efficient protein purification using metal affinity chromatography
- **FLAG Tag**: Allows for protein detection and immunoprecipitation assays
- N-terminal placement preserves neoantigen structure and immunogenicity

### mRNA Compatibility Features
- **Kozak Sequence**: Optimizes translation initiation efficiency
- **Poly(A) Signal**: Enhances mRNA stability and translation in target cells
- **T7 System**: Standard for pharmaceutical mRNA production

## Usage

### Basic Usage

```python
from plasmid_builder import PlasmidVectorDesigner, PromoterType

# Initialize designer
designer = PlasmidVectorDesigner()

# Design complete vector
design = designer.design_complete_vector(
    promoter=PromoterType.T7,
    include_his_tag=True,
    include_flag_tag=True
)

# Print summary
designer.print_design_summary()

# Export design
designer.export_design("my_plasmid_design.json")
```

### Advanced Configuration

```python
# Design with different promoter
cmv_design = designer.design_complete_vector(
    promoter=PromoterType.CMV,
    include_his_tag=True,
    include_flag_tag=False
)

# Generate schematic data for visualization
schematic_data = designer.generate_schematic_data()
```

## Validation Results

The design system performs comprehensive validation:

### Quality Checks
- ✅ Sequence length validation
- ✅ GC content analysis (51.7% - within optimal range)
- ✅ Promoter and regulatory element presence
- ✅ Translation signals validation

### Potential Issues Identified
- ⚠️ Multiple start codons detected (expected due to resistance gene)
- ⚠️ Contains TTTT sequence (potential T7 termination - monitoring required)
- ⚠️ Homopolymer runs present (may require synthesis optimization)

## Files Generated

1. **`plasmid_builder.py`** - Main design system implementation
2. **`neoantigen_x_plasmid_design.json`** - Complete design specification
3. **`README.md`** - This documentation file

## mRNA Vaccine Workflow Integration

This plasmid design is optimized for the following mRNA vaccine production workflow:

1. **Plasmid Production**: Clone and amplify plasmid in bacterial systems
2. **Linearization**: Cut plasmid downstream of poly(A) signal
3. **In Vitro Transcription**: Use T7 RNA polymerase for mRNA synthesis
4. **mRNA Processing**: Cap and purify mRNA for vaccine formulation
5. **Quality Control**: Validate neoantigen expression using included tags

## Experimental Validation Recommendations

### Next Steps for Laboratory Validation

1. **Plasmid Construction**
   - Synthesize and clone into suitable vector backbone
   - Validate sequence by Sanger sequencing
   - Confirm plasmid integrity by restriction analysis

2. **Expression Testing**
   - Transfect mammalian cells (HEK293T, CHO)
   - Western blot analysis using FLAG antibody
   - Protein purification via 6xHis tag

3. **mRNA Synthesis**
   - In vitro transcription using T7 RNA polymerase
   - mRNA quality assessment (gel electrophoresis, bioanalyzer)
   - Cap efficiency and stability testing

4. **Immunogenicity Assessment**
   - Neoantigen presentation analysis
   - T-cell activation assays
   - Vaccine efficacy studies in appropriate models

## Technical Specifications

- **Python Version**: 3.6+
- **Dependencies**: Standard library only (json, dataclasses, enum, typing)
- **Design Philosophy**: Minimal dependencies, maximum functionality
- **Validation**: Built-in quality control and issue detection

## Research and Design References

This design incorporates best practices from:
- Current mRNA vaccine development protocols
- Optimized codon usage tables for mammalian expression
- Standard molecular cloning and expression strategies
- Regulatory guidelines for therapeutic nucleic acids

## Future Enhancements

Potential improvements for future versions:
- Integration with visualization tools for plasmid maps
- Expanded codon optimization for different species
- Additional promoter and regulatory element options
- Enhanced validation including secondary structure prediction
- Automated primer design for cloning

---

**Status**: Design Complete ✅  
**Ready for**: Experimental validation and mRNA synthesis  
**Last Updated**: June 2024