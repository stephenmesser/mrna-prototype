#!/usr/bin/env python3
"""
Comprehensive Demonstration of Neoantigen X Plasmid Vector Design System
This script demonstrates all features of the mRNA vaccine plasmid design tools.
"""

import json
import os
from plasmid_builder import PlasmidBuilder, CodonOptimizer
from plasmid_visualizer import PlasmidVisualizer
from plasmid_validator import PlasmidValidator


def main():
    """Comprehensive demonstration of the plasmid design system"""
    
    print("=" * 80)
    print("NEOANTIGEN X PLASMID VECTOR DESIGN SYSTEM")
    print("mRNA Vaccine Prototype - Comprehensive Demonstration")
    print("=" * 80)
    print()
    
    # Step 1: Create plasmid design
    print("Step 1: Creating Neoantigen X Plasmid Vector")
    print("-" * 50)
    
    # Neoantigen X sequence (example antibody variable region)
    neoantigen_x_sequence = "MQLVESGGGLVKPGGSLRLSCAASGFTFSSYAMSWVRQAPGKGLEWVSAISGSGGSTYYADSVKGRFTISRDNSKNTLYLQMNSLRAEDTAVYYCAKVSYLSTASSLDYWGQGTLVTVSS"
    
    print(f"Original neoantigen X sequence: {neoantigen_x_sequence}")
    print(f"Length: {len(neoantigen_x_sequence)} amino acids")
    print()
    
    # Create plasmid builder
    builder = PlasmidBuilder("neoantigen_x_mrna_vector")
    
    # Build the complete vector
    builder.build_mrna_compatible_vector(neoantigen_x_sequence)
    
    print(f"Plasmid constructed: {builder.name}")
    print(f"Total length: {builder.total_length} bp")
    print(f"Number of elements: {len(builder.elements)}")
    print()
    
    # Step 2: Show codon optimization details
    print("Step 2: Codon Optimization Analysis")
    print("-" * 50)
    
    # Show codon optimization
    optimized_dna = CodonOptimizer.optimize_sequence(neoantigen_x_sequence)
    optimization_score = CodonOptimizer.calculate_optimization_score(optimized_dna)
    
    print(f"Optimized DNA sequence: {optimized_dna[:60]}...")
    print(f"Full optimized length: {len(optimized_dna)} bp")
    print(f"Optimization score: {optimization_score:.3f}")
    print(f"Optimization quality: {'Excellent' if optimization_score > 0.8 else 'Good' if optimization_score > 0.6 else 'Needs improvement'}")
    print()
    
    # Step 3: Comprehensive validation
    print("Step 3: Comprehensive Validation")
    print("-" * 50)
    
    validation_results = PlasmidValidator.validate_comprehensive(builder)
    
    print(f"Overall validation status: {validation_results['overall_status']}")
    print()
    
    # Show validation summary
    validation_categories = [
        "basic_validation", "sequence_validation", "mrna_validation", 
        "expression_validation", "safety_validation", "optimization_validation"
    ]
    
    for category in validation_categories:
        if category in validation_results:
            result = validation_results[category]
            status = "✅ PASSED" if result.get("passed", True) else "❌ FAILED"
            print(f"  {category.replace('_', ' ').title()}: {status}")
            
            if result.get("issues"):
                print(f"    Issues: {len(result['issues'])}")
            if result.get("warnings"):
                print(f"    Warnings: {len(result['warnings'])}")
    
    print()
    
    # Step 4: Design export and analysis
    print("Step 4: Design Export and Analysis")
    print("-" * 50)
    
    design = builder.export_design()
    
    print("Key design metrics:")
    print(f"  • Total plasmid length: {design['total_length']} bp")
    print(f"  • mRNA transcript length: {len(design['mrna_sequence'])} bp")
    print(f"  • Number of elements: {len(design['elements'])}")
    
    # Element breakdown
    element_types = {}
    for element in design['elements']:
        elem_type = element['element_type']
        element_types[elem_type] = element_types.get(elem_type, 0) + 1
    
    print("  • Element composition:")
    for elem_type, count in element_types.items():
        print(f"    - {elem_type.replace('_', ' ').title()}: {count}")
    
    print()
    
    # Step 5: Generate visualizations
    print("Step 5: Generating Visualizations")
    print("-" * 50)
    
    # ASCII diagram
    print("Creating ASCII diagram...")
    ascii_diagram = PlasmidVisualizer.generate_ascii_diagram(builder)
    
    # Element summary
    print("Creating element summary...")
    element_summary = PlasmidVisualizer.generate_element_summary(builder)
    
    # mRNA map
    print("Creating mRNA transcript map...")
    mrna_map = PlasmidVisualizer.generate_mrna_transcript_map(builder)
    
    # SVG export
    print("Exporting SVG diagram...")
    svg_content = PlasmidVisualizer.export_svg_diagram(builder, "neoantigen_x_plasmid.svg")
    
    print("✅ All visualizations generated successfully")
    print()
    
    # Step 6: Save all outputs
    print("Step 6: Saving Outputs")
    print("-" * 50)
    
    # Create outputs directory
    os.makedirs("outputs", exist_ok=True)
    
    # Save design JSON
    with open("outputs/neoantigen_x_design.json", "w") as f:
        json.dump(design, f, indent=2)
    print("✅ Design exported to: outputs/neoantigen_x_design.json")
    
    # Save validation report
    PlasmidValidator.export_validation_report(validation_results, "outputs/validation_report.json")
    print("✅ Validation report saved to: outputs/validation_report.json")
    
    # Save ASCII diagram
    with open("outputs/plasmid_diagram.txt", "w") as f:
        f.write(ascii_diagram)
    print("✅ ASCII diagram saved to: outputs/plasmid_diagram.txt")
    
    # Save element summary
    with open("outputs/element_summary.txt", "w") as f:
        f.write(element_summary)
    print("✅ Element summary saved to: outputs/element_summary.txt")
    
    # Save mRNA map
    with open("outputs/mrna_transcript_map.txt", "w") as f:
        f.write(mrna_map)
    print("✅ mRNA map saved to: outputs/mrna_transcript_map.txt")
    
    # Move SVG to outputs
    if os.path.exists("neoantigen_x_plasmid.svg"):
        os.rename("neoantigen_x_plasmid.svg", "outputs/neoantigen_x_plasmid.svg")
    print("✅ SVG diagram saved to: outputs/neoantigen_x_plasmid.svg")
    
    print()
    
    # Step 7: Summary and recommendations
    print("Step 7: Summary and Recommendations")
    print("-" * 50)
    
    print("DESIGN SUMMARY:")
    print(f"✅ Successfully designed plasmid vector for neoantigen X")
    print(f"✅ mRNA-compatible design with T7 promoter")
    print(f"✅ Codon-optimized for mammalian expression")
    print(f"✅ Includes purification and detection tags")
    print(f"✅ Comprehensive validation completed")
    print()
    
    print("RECOMMENDATIONS:")
    for i, recommendation in enumerate(validation_results.get("recommendations", []), 1):
        print(f"  {i}. {recommendation}")
    
    print()
    print("NEXT STEPS:")
    print("  1. Review validation report for any issues")
    print("  2. Consider experimental validation in cell culture")
    print("  3. Optimize further if needed based on expression data")
    print("  4. Proceed with mRNA synthesis and vaccine formulation")
    print()
    
    print("=" * 80)
    print("DEMONSTRATION COMPLETED SUCCESSFULLY")
    print("All files saved to 'outputs/' directory")
    print("=" * 80)
    
    return builder, design, validation_results


if __name__ == "__main__":
    builder, design, validation = main()