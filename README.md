# mRNA Vaccine Plasmid Vector Design for Neoantigen X

## Overview

This repository contains a comprehensive plasmid vector design system specifically developed for neoantigen X expression in mRNA vaccine applications. The system provides tools for designing, optimizing, validating, and visualizing plasmid vectors that are compatible with mRNA synthesis and optimized for mammalian expression systems.

## Features

### Core Functionality
- **Codon Optimization**: Mammalian-optimized codon usage for enhanced expression
- **Regulatory Elements**: Comprehensive library of promoters, enhancers, and control sequences
- **Expression Tags**: Built-in purification and detection tags (FLAG, His-tag)
- **mRNA Compatibility**: Designed for in vitro transcription and mRNA vaccine applications
- **In Silico Validation**: Comprehensive quality control and safety checks
- **Visualization**: ASCII and SVG plasmid diagrams

### Key Components

1. **PlasmidBuilder** (`plasmid_builder.py`)
   - Main class for constructing plasmid vectors
   - Regulatory element library
   - Codon optimization engine
   - mRNA-compatible vector assembly

2. **PlasmidVisualizer** (`plasmid_visualizer.py`)
   - ASCII art plasmid diagrams
   - Linear and circular map generation
   - mRNA transcript visualization
   - SVG export functionality

3. **PlasmidValidator** (`plasmid_validator.py`)
   - Comprehensive validation suite
   - Sequence analysis and safety checks
   - mRNA compatibility verification
   - Expression potential assessment

4. **Configuration** (`plasmid_config.json`)
   - Customizable design parameters
   - Validation criteria
   - Element preferences

## Design Rationale

### Neoantigen X Expression System

The plasmid vector is specifically optimized for neoantigen X with the following design choices:

1. **T7 Promoter**: Enables efficient in vitro transcription for mRNA synthesis
2. **Kozak Sequence**: Enhances translation initiation in mammalian cells
3. **Codon Optimization**: Uses mammalian-preferred codons for higher expression
4. **Dual Tags**: FLAG tag for detection, His-tag for purification
5. **BGH PolyA**: Provides mRNA stability and efficient translation termination
6. **Ampicillin Resistance**: Enables plasmid selection and maintenance

### mRNA Vaccine Compatibility

The design ensures compatibility with mRNA vaccine manufacturing:
- T7 promoter for in vitro transcription
- Optimized sequences for mRNA stability
- Minimal secondary structure formation
- Compatible with lipid nanoparticle formulation

## Usage

### Basic Plasmid Construction

```python
from plasmid_builder import PlasmidBuilder

# Create plasmid builder
builder = PlasmidBuilder("neoantigen_x_vector")

# Build mRNA-compatible vector
neoantigen_sequence = "MQLVESGGGLVKPGGSLRLSCAASGFTFSSYAMSWVRQAPGKGLEWVSAISGSGGSTYYADSVKGRFTISRDNSKNTLYLQMNSLRAEDTAVYYCAKVSYLSTASSLDYWGQGTLVTVSS"
builder.build_mrna_compatible_vector(neoantigen_sequence)

# Validate design
validation = builder.validate_design()
print(f"Total length: {builder.total_length} bp")
```

### Comprehensive Validation

```python
from plasmid_validator import PlasmidValidator

# Perform full validation
validation_results = PlasmidValidator.validate_comprehensive(builder)
print(f"Status: {validation_results['overall_status']}")

# Export validation report
PlasmidValidator.export_validation_report(validation_results)
```

### Visualization

```python
from plasmid_visualizer import PlasmidVisualizer

# Generate ASCII diagram
ascii_diagram = PlasmidVisualizer.generate_ascii_diagram(builder)
print(ascii_diagram)

# Export SVG diagram
PlasmidVisualizer.export_svg_diagram(builder, "neoantigen_x_plasmid.svg")
```

## File Structure

```
mrna-prototype/
├── plasmid_builder.py       # Core plasmid construction
├── plasmid_visualizer.py    # Visualization tools
├── plasmid_validator.py     # Validation suite
├── plasmid_config.json      # Configuration file
├── README.md                # This documentation
└── outputs/                 # Generated files
    ├── neoantigen_x_plasmid.svg
    └── validation_report.json
```

## Validation Results

The current neoantigen X vector design achieves:

- **Total Length**: 2,571 bp (suitable for mRNA synthesis)
- **Elements**: 9 functional elements
- **mRNA Compatibility**: ✅ Full T7/mRNA compatibility
- **Expression Tags**: ✅ FLAG and His tags included
- **Codon Optimization**: 0.436 score (acceptable, room for improvement)

### Quality Metrics
- ✅ Contains required promoter, gene, and tag elements
- ✅ Proper start/stop codons present
- ✅ mRNA synthesis compatible
- ⚠️ Contains some restriction sites (manageable)
- ⚠️ Codon optimization could be enhanced

## Design Specifications

### Vector Elements (5' to 3')
1. **T7 Promoter** (20 bp) - In vitro transcription
2. **Kozak Sequence** (6 bp) - Translation enhancement
3. **Start Codon** (3 bp) - ATG
4. **FLAG Tag** (66 bp) - Detection/immunoprecipitation
5. **Neoantigen X** (360 bp) - Codon-optimized target gene
6. **His Tag** (18 bp) - Purification
7. **Stop Codon** (3 bp) - TAA
8. **BGH PolyA** (236 bp) - mRNA stability
9. **Ampicillin Resistance** (1,859 bp) - Selection marker

### Technical Specifications
- **Expression System**: Mammalian cells
- **Transcription**: T7 RNA polymerase
- **Translation**: Kozak-enhanced initiation
- **Purification**: Nickel affinity (His-tag)
- **Detection**: Anti-FLAG antibodies
- **Selection**: Ampicillin resistance

## Manufacturing Considerations

### For mRNA Production
1. Linearize plasmid downstream of polyA signal
2. Use T7 RNA polymerase for in vitro transcription
3. Add 5' cap and optimize 3' polyA tail
4. Purify mRNA for lipid nanoparticle formulation

### Quality Control
- Sequence verification by DNA sequencing
- Functional testing in mammalian cell culture
- mRNA integrity analysis
- Protein expression confirmation

## Safety and Regulatory

- Contains ampicillin resistance gene (requires BSL-1 containment)
- No oncogenes or pathogenic sequences
- Suitable for research and vaccine development
- Follow institutional biosafety guidelines

## Future Enhancements

1. **Enhanced Codon Optimization**: Improve optimization score above 0.7
2. **Alternative Promoters**: Test CMV or EF1A for different applications
3. **Additional Tags**: Consider Strep-tag or other purification systems
4. **Restriction Site Removal**: Eliminate problematic enzyme sites
5. **Origin of Replication**: Add ColE1 origin for plasmid maintenance

## Dependencies

- Python 3.12+
- Standard library modules: `json`, `re`, `typing`, `dataclasses`, `enum`, `math`
- No external packages required

## Contributing

When modifying the plasmid design:
1. Run comprehensive validation after changes
2. Update configuration file as needed
3. Test mRNA compatibility
4. Document design rationale
5. Validate experimental functionality

## License

This project is designed for research and educational purposes in vaccine development.

---

**Contact**: For questions about this plasmid design system, please refer to the project documentation or submit an issue.

**Version**: 1.0  
**Last Updated**: Current date  
**Status**: Ready for experimental validation