# mRNA Prototype - Neoantigen X Plasmid Vector Design

A comprehensive plasmid vector design system for neoantigen X expression in mRNA vaccine applications, now with an integrated CLI tool for task list generation.

## Overview

This repository contains a complete plasmid design system for developing mRNA vaccines targeting neoantigen X. The system provides automated design, optimization, validation, and documentation capabilities for creating therapeutic vaccine templates.

**New Feature**: The repository now includes a CLI tool for generating structured task lists to help manage project workflows and research tasks.

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

5. **Generate task lists:**
   ```bash
   # Interactive mode
   python3 task_list_generator.py --interactive
   
   # Command line mode
   python3 task_list_generator.py --title "Research Tasks" --add "Design experiment" --add "Analyze data:Statistical analysis required" --export markdown
   ```

## Features

### Plasmid Design System
- **Automated Plasmid Design**: Complete vector construction with all essential components
- **Codon Optimization**: Human-optimized sequences for maximum expression
- **Quality Validation**: Comprehensive in silico validation checks
- **Schematic Generation**: Visual representations of plasmid structure
- **Comprehensive Documentation**: Detailed design rationale and specifications

### Task List Generator CLI Tool
- **Interactive Mode**: User-friendly interface for creating task lists
- **Command Line Interface**: Batch operations with command line arguments
- **Multiple Export Formats**: Markdown, plain text, and JSON export options
- **Task Management**: Add, remove, and toggle task completion status
- **Persistent Storage**: Save and load task lists from JSON files

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

### Plasmid Design System
- `plasmid_builder.py` - Main design system
- `generate_schematics.py` - Diagram generator
- `PLASMID_DESIGN_DOCUMENTATION.md` - Complete documentation

### Task List Generator
- `task_list_generator.py` - CLI tool for task list generation
- `test_task_list_generator.py` - Test suite for task list functionality

### Testing and Configuration
- `test_plasmid_design.py` - Comprehensive test suite
- `requirements.txt` - Python dependencies

## Design Results

- **Plasmid Name**: pNeoantigenX-mRNA
- **Total Length**: 2,251 bp
- **Expression System**: Mammalian (Human)
- **Quality Status**: All validations passed

## Task List Generator Usage

### Interactive Mode
```bash
python3 task_list_generator.py --interactive
```

### Command Line Mode
```bash
# Create a simple task list
python3 task_list_generator.py --title "Project Tasks" --add "Setup environment" --add "Write tests" --export markdown

# Add tasks with descriptions
python3 task_list_generator.py --title "Research Tasks" --add "Literature review:Survey recent papers on mRNA vaccines" --add "Data analysis" --export text --output tasks.txt

# Load and modify existing task lists
python3 task_list_generator.py --load existing_tasks.json --add "New task" --export markdown --output updated_tasks.md
```

### Export Formats
- **Markdown**: Checkbox format compatible with GitHub and other Markdown renderers
- **Plain Text**: Simple text format with completion status indicators
- **JSON**: Machine-readable format for integration with other tools

## Next Steps

1. **Experimental Validation**: Transform into competent cells
2. **Expression Testing**: Validate protein expression in mammalian cells
3. **mRNA Synthesis**: Use as template for in vitro transcription
4. **Immunogenicity Testing**: Assess T cell activation

## License

This project is designed for research and educational purposes in vaccine development.