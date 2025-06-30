#!/usr/bin/env python3
"""
Plasmid Vector Designer for Neoantigen X mRNA Vaccine
====================================================

This module provides comprehensive functionality for designing plasmid vectors
optimized for neoantigen X expression in mRNA vaccine applications.

Features:
- Codon optimization for mammalian expression systems
- Promoter and regulatory element selection
- Expression tracking and purification tags
- mRNA synthesis compatibility validation
- In silico design validation
"""

import re
import json
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
from enum import Enum


class ExpressionSystem(Enum):
    """Supported expression systems for codon optimization."""
    HUMAN = "human"
    MOUSE = "mouse"
    MAMMALIAN_GENERAL = "mammalian_general"


class PromoterType(Enum):
    """Available promoter types for expression."""
    T7 = "T7"
    CMV = "CMV"
    EF1A = "EF1A"
    SV40 = "SV40"


@dataclass
class PlasmidComponent:
    """Represents a single component of the plasmid vector."""
    name: str
    sequence: str
    component_type: str
    description: str
    start_pos: int = 0
    end_pos: int = 0


@dataclass
class NeoantigenX:
    """Definition and properties of neoantigen X."""
    name: str = "Neoantigen_X"
    amino_acid_sequence: str = "MKTVRQERLKSIVRILERSKEPVSGAQLAEELSVSRQVIVQDIAYLRSLGYNIVATPRGYVLAGG"
    description: str = "Synthetic neoantigen X designed for therapeutic mRNA vaccine"
    source_organism: str = "Synthetic"
    
    def get_codon_optimized_sequence(self, system: ExpressionSystem = ExpressionSystem.HUMAN) -> str:
        """Generate codon-optimized DNA sequence for the neoantigen."""
        # Human codon usage table (simplified - using most frequent codons)
        codon_table = {
            'A': 'GCC', 'R': 'CGC', 'N': 'AAC', 'D': 'GAC', 'C': 'TGC',
            'Q': 'CAG', 'E': 'GAG', 'G': 'GGC', 'H': 'CAC', 'I': 'ATC',
            'L': 'CTG', 'K': 'AAG', 'M': 'ATG', 'F': 'TTC', 'P': 'CCC',
            'S': 'AGC', 'T': 'ACC', 'W': 'TGG', 'Y': 'TAC', 'V': 'GTG',
            '*': 'TAG'  # Stop codon
        }
        
        # Convert amino acid sequence to codon-optimized DNA
        dna_sequence = ""
        for aa in self.amino_acid_sequence:
            if aa in codon_table:
                dna_sequence += codon_table[aa]
            else:
                raise ValueError(f"Unknown amino acid: {aa}")
        
        return dna_sequence


class PlasmidVectorDesigner:
    """Main class for designing plasmid vectors for neoantigen X."""
    
    def __init__(self):
        self.components: List[PlasmidComponent] = []
        self.total_length: int = 0
        self.neoantigen = NeoantigenX()
        
        # Define standard sequences for common elements
        self.standard_sequences = {
            "T7_promoter": "TAATACGACTCACTATAGGG",
            "CMV_promoter": "GTTGACATTGATTATTGACTAGTTATTAATAGTAATCAATTACGGGGTCATTAGTTCATAGCCCATATATGGAGTTCCGCGTTACATAACTTACGGTAAATGGCCCGCCTGGCTGACCGCCCAACGACCCCCGCCCATTGACGTCAATAATGACGTATGTTCCCATAGTAACGCCAATAGGGACTTTCCATTGACGTCAATGGGTGGAGTATTTACGGTAAACTGCCCACTTGGCAGTACATCAAGTGTATCATATGCCAAGTACGCCCCCTATTGACGTCAATGACGGTAAATGGCCCGCCTGGCATTATGCCCAGTACATGACCTTATGGGACTTTCCTACTTGGCAGTACATCTACGTATTAGTCATCGCTATTACCATGGTGATGCGGTTTTGGCAGTACATCAATGGGCGTGGATAGCGGTTTGACTCACGGGGATTTCCAAGTCTCCACCCCATTGACGTCAATGGGAGTTTGTTTTGGCACCAAAATCAACGGGACTTTCCAAAATGTCGTAACAACTCCGCCCCATTGACGCAAATGGGCGGTAGGCGTGTACGGTGGGAGGTCTATATAAGCAGAGCT",
            "EF1A_promoter": "GGCTCCGGTGCCCGTCAGTGGGCAGAGCGCACATCGCCCACAGTCCCCGAGAAGTTGGGGGGAGGGGTCGGCAATTGAACCGGTGCCTAGAGAAGGTGGCGCGGGGTAAACTGGGAAAGTGATGTCGTGTACTGGCTCCGCCTTTTTCCCGAGGGTGGGGGAGAACCGTATATAAGTGCAGTAGTCGCCGTGAACGTTCTTTTTCGCAACGGGTTTGCCGCCAGAACACAGCTG",
            "SV40_promoter": "GACATTGATTATTGACTAGTTATTAATAGTAATCAATTACGGGGTCATTAGTTCATAGCCCATATATGGAGTTCCGCGTTACATAACTTACGGTAAATGGCCCGCCTGGCTGACCGCCCAACGACCCCCGCCCATTGACGTCAATAATGACGTATGTTCCCATAGTAACGCCAATAGGGACTTTCCATTGACGTCAATGGGTGGAGTATTTACGGTAAACTGCCCACTTGGCAGTACATCAAGTGTATCATATGCCAAGTACGCCCCCTATTGACGTCAATGACGGTAAATGGCCCGCCTGGCATTATGCCCAGTACATGACCTTATGGGACTTTCCTACTTGGCAGTACATCTACGTATTAGTCATCGCTATTACCATGGTGATGCGGTTTTGGCAGTACATCAATGGGCGTGGATAGCGGTTTGACTCACGGGGATTTCCAAGTCTCCACCCCATTGACGTCAATGGGAGTTTGTTTTGGCACCAAAATCAACGGGACTTTCCAAAATGTCGTAACAACTGCCGCCCCATTGACGCAAATGGGCGGTAGGCGTGTACGGTGGGAGGTCTATATAAGCAGAGCTCGTTTAGTGAACCGTCAGATCGCCTGGAGACGCCATCCACGCTGTTTTGACCTCCATAGAAGACACCGGGACCGATCCAGCCTCCGCGGCTCGCATCTCTCCTTCACGCGCCCGCCGCCCTACCTGAGGCCGCCATCCACGCCGGTTGAGTCGCGTTCTGCCGCCTCCCGCCTGTGGTGCCTCCTGAACTGCGTCCGCCGTCTAGGTAAGTTTAAAGCTCAGGTCGAGACCGGGCCTTTGTCCGGCGCTCCCTTGGAGCCTACCTAGACTCAGCCGGCTCTCCACGCTTTGCCTGACCCTGCTTGCTCAACTCTACGTCTTTGTTTCGTTTTCTGTTCTGCGCCGTTACAGATCC",
            "kozak_sequence": "GCCACC",
            "start_codon": "ATG",
            "his_tag": "CATCACCATCACCATCAC",  # 6xHis
            "flag_tag": "GACTACAAGGACGACGATGACAAG",  # FLAG
            "stop_codon": "TAG",
            "polya_signal": "AATAAAAGATCTTTATTTTCATTAGATCTGTGTGTTGGTTTTTTGTGTG",
            "t7_terminator": "GCTAGTTATTGCTCAGCGG",
            "ampicillin_resistance": "ATGAGTATTCAACATTTCCGTGTCGCCCTTATTCCCTTTTTTGCGGCATTTTGCCTTCCTGTTTTTGCTCACCCAGAAACGCTGGTGAAAGTAAAAGATGCTGAAGATCAGTTGGGTGCACGAGTGGGTTACATCGAACTGGATCTCAACAGCGGTAAGATCCTTGAGAGTTTTCGCCCCGAAGAACGTTTTCCAATGATGAGCACTTTTAAAGTTCTGCTATGTGGCGCGGTATTATCCCGTGTTGACGCCGGGCAAGAGCAACTCGGTCGCCGCATACACTATTCTCAGAATGACTTGGTTGAGTACTCACCAGTCACAGAAAAGCATCTTACGGATGGCATGACAGTAAGAGAATTATGCAGTGCTGCCATAACCATGAGTGATAACACTGCGGCCAACTTACTTCTGACAACGATCGGAGGACCGAAGGAGCTAACCGCTTTTTTGCACAACATGGGGGATCATGTAACTCGCCTTGATCGTTGGGAACCGGAGCTGAATGAAGCCATACCAAACGACGAGCGTGACACCACGATGCCTGTAGCAATGGCAACAACGTTGCGCAAACTATTAACTGGCGAACTACTTACTCTAGCTTCCCGGCAACAATTAATAGACTGGATGGAGGCGGATAAAGTTGCAGGACCACTTCTGCGCTCGGCCCTTCCGGCTGGCTGGTTTATTGCTGATAAATCTGGAGCCGGTGAGCGTGGGTCTCGCGGTATCATTGCAGCACTGGGGCCAGATGGTAAGCCCTCCCGTATCGTAGTTATCTACACGACGGGGAGTCAGGCAACTATGGATGAACGAAATAGACAGATCGCTGAGATAGGTGCCTCACTGATTAAGCATTGGTAA"
        }
    
    def add_component(self, component: PlasmidComponent) -> None:
        """Add a component to the plasmid design."""
        component.start_pos = self.total_length
        component.end_pos = self.total_length + len(component.sequence)
        self.components.append(component)
        self.total_length = component.end_pos
    
    def create_neoantigen_expression_cassette(self, 
                                            promoter: PromoterType = PromoterType.T7,
                                            include_his_tag: bool = True,
                                            include_flag_tag: bool = True) -> List[PlasmidComponent]:
        """Create a complete expression cassette for neoantigen X."""
        cassette_components = []
        
        # 1. Promoter
        promoter_seq = self.standard_sequences.get(f"{promoter.value}_promoter", 
                                                  self.standard_sequences["T7_promoter"])
        cassette_components.append(PlasmidComponent(
            name=f"{promoter.value}_promoter",
            sequence=promoter_seq,
            component_type="promoter",
            description=f"{promoter.value} promoter for high-level expression"
        ))
        
        # 2. Kozak sequence + Start codon
        kozak_start = self.standard_sequences["kozak_sequence"] + self.standard_sequences["start_codon"]
        cassette_components.append(PlasmidComponent(
            name="kozak_start",
            sequence=kozak_start,
            component_type="translation_start",
            description="Kozak sequence and start codon for optimal translation initiation"
        ))
        
        # 3. Optional N-terminal tags
        tag_sequence = ""
        tag_description = []
        if include_his_tag:
            tag_sequence += self.standard_sequences["his_tag"]
            tag_description.append("6xHis tag for purification")
        if include_flag_tag:
            tag_sequence += self.standard_sequences["flag_tag"]
            tag_description.append("FLAG tag for detection")
            
        if tag_sequence:
            cassette_components.append(PlasmidComponent(
                name="n_terminal_tags",
                sequence=tag_sequence,
                component_type="tag",
                description="; ".join(tag_description)
            ))
        
        # 4. Neoantigen X coding sequence
        neoantigen_seq = self.neoantigen.get_codon_optimized_sequence()
        cassette_components.append(PlasmidComponent(
            name="neoantigen_x_cds",
            sequence=neoantigen_seq,
            component_type="coding_sequence",
            description=f"Codon-optimized coding sequence for {self.neoantigen.name}"
        ))
        
        # 5. Stop codon
        cassette_components.append(PlasmidComponent(
            name="stop_codon",
            sequence=self.standard_sequences["stop_codon"],
            component_type="translation_stop",
            description="Stop codon for translation termination"
        ))
        
        # 6. Poly(A) signal for mRNA stability
        cassette_components.append(PlasmidComponent(
            name="polya_signal",
            sequence=self.standard_sequences["polya_signal"],
            component_type="polya_signal",
            description="Polyadenylation signal for mRNA stability"
        ))
        
        # 7. Terminator
        cassette_components.append(PlasmidComponent(
            name="t7_terminator",
            sequence=self.standard_sequences["t7_terminator"],
            component_type="terminator",
            description="T7 terminator for transcription termination"
        ))
        
        return cassette_components
    
    def add_antibiotic_resistance(self, antibiotic: str = "ampicillin") -> None:
        """Add antibiotic resistance marker for selection."""
        if antibiotic.lower() == "ampicillin":
            self.add_component(PlasmidComponent(
                name="amp_resistance",
                sequence=self.standard_sequences["ampicillin_resistance"],
                component_type="resistance_marker",
                description="Ampicillin resistance gene for bacterial selection"
            ))
    
    def design_complete_vector(self, 
                             promoter: PromoterType = PromoterType.T7,
                             include_his_tag: bool = True,
                             include_flag_tag: bool = True) -> Dict:
        """Design a complete plasmid vector for neoantigen X."""
        # Clear existing components
        self.components = []
        self.total_length = 0
        
        # Add expression cassette
        expression_components = self.create_neoantigen_expression_cassette(
            promoter, include_his_tag, include_flag_tag
        )
        
        for component in expression_components:
            self.add_component(component)
        
        # Add antibiotic resistance
        self.add_antibiotic_resistance("ampicillin")
        
        # Generate complete sequence
        complete_sequence = "".join([comp.sequence for comp in self.components])
        
        # Create design summary
        design_summary = {
            "plasmid_name": f"pNeoX_{promoter.value}",
            "total_length": self.total_length,
            "neoantigen": asdict(self.neoantigen),
            "components": [asdict(comp) for comp in self.components],
            "complete_sequence": complete_sequence,
            "design_rationale": self._generate_design_rationale(promoter, include_his_tag, include_flag_tag),
            "mRNA_compatibility": self._assess_mRNA_compatibility(),
            "validation_results": self._perform_in_silico_validation(complete_sequence)
        }
        
        return design_summary
    
    def _generate_design_rationale(self, promoter: PromoterType, 
                                 include_his_tag: bool, include_flag_tag: bool) -> Dict[str, str]:
        """Generate rationale for each design decision."""
        rationale = {
            "promoter_choice": f"{promoter.value} promoter selected for {'high expression in mammalian cells' if promoter != PromoterType.T7 else 'in vitro transcription compatibility'}",
            "codon_optimization": "Human codon usage optimized to maximize expression in mammalian systems",
            "kozak_sequence": "Optimal Kozak sequence included for efficient translation initiation",
            "tag_selection": f"Tags included: {', '.join([tag for tag, include in [('6xHis', include_his_tag), ('FLAG', include_flag_tag)] if include])} for protein tracking and purification",
            "polya_signal": "Polyadenylation signal included for mRNA stability and efficient translation",
            "resistance_marker": "Ampicillin resistance for bacterial selection and plasmid maintenance",
            "mRNA_compatibility": "Design optimized for in vitro transcription and mRNA vaccine applications"
        }
        return rationale
    
    def _assess_mRNA_compatibility(self) -> Dict[str, any]:
        """Assess compatibility with mRNA synthesis process."""
        compatibility = {
            "t7_promoter_present": any(comp.name.startswith("T7") for comp in self.components),
            "polya_signal_present": any(comp.component_type == "polya_signal" for comp in self.components),
            "kozak_optimized": any(comp.name == "kozak_start" for comp in self.components),
            "codon_optimized": True,  # Our neoantigen is codon optimized
            "gc_content_optimal": self._calculate_gc_content(),
            "predicted_issues": []
        }
        
        # Check for potential issues
        complete_seq = "".join([comp.sequence for comp in self.components])
        if "TTTT" in complete_seq:
            compatibility["predicted_issues"].append("Contains TTTT sequence (potential T7 termination)")
        
        return compatibility
    
    def _calculate_gc_content(self) -> float:
        """Calculate GC content of the complete sequence."""
        complete_seq = "".join([comp.sequence for comp in self.components])
        gc_count = complete_seq.count('G') + complete_seq.count('C')
        return (gc_count / len(complete_seq)) * 100 if complete_seq else 0
    
    def _perform_in_silico_validation(self, sequence: str) -> Dict[str, any]:
        """Perform basic in silico validation of the plasmid design."""
        validation = {
            "sequence_length": len(sequence),
            "gc_content": self._calculate_gc_content(),
            "start_codons": sequence.count("ATG"),
            "stop_codons": sequence.count("TAG") + sequence.count("TAA") + sequence.count("TGA"),
            "potential_issues": [],
            "validation_passed": True
        }
        
        # Check for common issues
        if validation["gc_content"] < 40 or validation["gc_content"] > 60:
            validation["potential_issues"].append(f"GC content ({validation['gc_content']:.1f}%) outside optimal range (40-60%)")
        
        if validation["start_codons"] > 2:
            validation["potential_issues"].append(f"Multiple start codons detected ({validation['start_codons']})")
        
        if "GGGG" in sequence or "CCCC" in sequence:
            validation["potential_issues"].append("Contains homopolymer runs that may cause synthesis issues")
        
        validation["validation_passed"] = len(validation["potential_issues"]) == 0
        
        return validation
    
    def generate_schematic_data(self) -> Dict[str, any]:
        """Generate data for creating schematic diagrams."""
        schematic_data = {
            "plasmid_map": [],
            "component_colors": {
                "promoter": "#FF6B6B",
                "coding_sequence": "#4ECDC4", 
                "tag": "#45B7D1",
                "resistance_marker": "#96CEB4",
                "terminator": "#FECA57",
                "polya_signal": "#FF9FF3",
                "translation_start": "#54A0FF",
                "translation_stop": "#5F27CD"
            }
        }
        
        total_length = self.total_length
        for component in self.components:
            start_angle = (component.start_pos / total_length) * 360
            end_angle = (component.end_pos / total_length) * 360
            
            schematic_data["plasmid_map"].append({
                "name": component.name,
                "type": component.component_type,
                "start_angle": start_angle,
                "end_angle": end_angle,
                "start_pos": component.start_pos,
                "end_pos": component.end_pos,
                "length": len(component.sequence),
                "color": schematic_data["component_colors"].get(component.component_type, "#CCCCCC")
            })
        
        return schematic_data
    
    def export_design(self, filename: str = "neoantigen_x_plasmid_design.json") -> None:
        """Export the complete design to a JSON file."""
        design_data = self.design_complete_vector()
        
        with open(filename, 'w') as f:
            json.dump(design_data, f, indent=2)
        
        print(f"Plasmid design exported to {filename}")
    
    def print_design_summary(self) -> None:
        """Print a formatted summary of the plasmid design."""
        design = self.design_complete_vector()
        
        print("=" * 80)
        print(f"PLASMID VECTOR DESIGN: {design['plasmid_name']}")
        print("=" * 80)
        print(f"Total Length: {design['total_length']} bp")
        print(f"GC Content: {design['validation_results']['gc_content']:.1f}%")
        print()
        
        print("NEOANTIGEN X DETAILS:")
        print(f"  Name: {design['neoantigen']['name']}")
        print(f"  Amino Acid Sequence: {design['neoantigen']['amino_acid_sequence']}")
        print(f"  Description: {design['neoantigen']['description']}")
        print()
        
        print("PLASMID COMPONENTS:")
        for i, comp in enumerate(design['components'], 1):
            print(f"  {i}. {comp['name']} ({comp['component_type']})")
            print(f"     Position: {comp['start_pos']}-{comp['end_pos']} bp")
            print(f"     Description: {comp['description']}")
            print()
        
        print("DESIGN RATIONALE:")
        for key, value in design['design_rationale'].items():
            print(f"  {key.replace('_', ' ').title()}: {value}")
        print()
        
        print("mRNA COMPATIBILITY ASSESSMENT:")
        compatibility = design['mRNA_compatibility']
        print(f"  T7 Promoter Present: {compatibility['t7_promoter_present']}")
        print(f"  Poly(A) Signal Present: {compatibility['polya_signal_present']}")
        print(f"  Kozak Optimized: {compatibility['kozak_optimized']}")
        print(f"  Codon Optimized: {compatibility['codon_optimized']}")
        if compatibility['predicted_issues']:
            print(f"  Potential Issues: {', '.join(compatibility['predicted_issues'])}")
        else:
            print("  No compatibility issues detected")
        print()
        
        print("VALIDATION RESULTS:")
        validation = design['validation_results']
        print(f"  Validation Status: {'PASSED' if validation['validation_passed'] else 'FAILED'}")
        if validation['potential_issues']:
            print("  Issues Found:")
            for issue in validation['potential_issues']:
                print(f"    - {issue}")
        else:
            print("  No validation issues detected")
        print("=" * 80)


def main():
    """Main function to demonstrate the plasmid design process."""
    print("Neoantigen X Plasmid Vector Designer")
    print("====================================")
    
    # Initialize the designer
    designer = PlasmidVectorDesigner()
    
    # Design plasmid with T7 promoter (optimal for mRNA synthesis)
    print("Designing plasmid vector for neoantigen X...")
    designer.design_complete_vector(
        promoter=PromoterType.T7,
        include_his_tag=True,
        include_flag_tag=True
    )
    
    # Print design summary
    designer.print_design_summary()
    
    # Export design
    designer.export_design("neoantigen_x_plasmid_design.json")
    
    # Generate schematic data
    schematic_data = designer.generate_schematic_data()
    print(f"\nSchematic data generated with {len(schematic_data['plasmid_map'])} components")
    
    print("\nPlasmid design completed successfully!")
    print("Ready for experimental validation and mRNA synthesis.")


if __name__ == "__main__":
    main()