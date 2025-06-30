#!/usr/bin/env python3
"""
Plasmid Vector Builder for mRNA Vaccine Prototype
Designed for neoantigen X expression with optimized features.
"""

import json
import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum


class ElementType(Enum):
    """Types of plasmid elements"""
    PROMOTER = "promoter"
    GENE = "gene"
    TAG = "tag"
    ENHANCER = "enhancer"
    UTR = "utr"
    ORIGIN = "origin"
    RESISTANCE = "resistance"


@dataclass
class PlasmidElement:
    """Represents a single element in the plasmid"""
    name: str
    sequence: str
    element_type: ElementType
    position: int = 0
    length: int = 0
    description: str = ""
    
    def __post_init__(self):
        if self.length == 0:
            self.length = len(self.sequence)


class CodonOptimizer:
    """Optimizes codons for mammalian expression"""
    
    # Mammalian codon usage table (relative frequencies)
    MAMMALIAN_CODON_TABLE = {
        'A': {'GCT': 0.26, 'GCC': 0.40, 'GCA': 0.23, 'GCG': 0.11},
        'C': {'TGT': 0.46, 'TGC': 0.54},
        'D': {'GAT': 0.46, 'GAC': 0.54},
        'E': {'GAA': 0.42, 'GAG': 0.58},
        'F': {'TTT': 0.46, 'TTC': 0.54},
        'G': {'GGT': 0.16, 'GGC': 0.34, 'GGA': 0.25, 'GGG': 0.25},
        'H': {'CAT': 0.42, 'CAC': 0.58},
        'I': {'ATT': 0.36, 'ATC': 0.48, 'ATA': 0.16},
        'K': {'AAA': 0.43, 'AAG': 0.57},
        'L': {'TTA': 0.08, 'TTG': 0.13, 'CTT': 0.13, 'CTC': 0.20, 'CTA': 0.07, 'CTG': 0.39},
        'M': {'ATG': 1.00},
        'N': {'AAT': 0.47, 'AAC': 0.53},
        'P': {'CCT': 0.28, 'CCC': 0.32, 'CCA': 0.27, 'CCG': 0.13},
        'Q': {'CAA': 0.26, 'CAG': 0.74},
        'R': {'CGT': 0.08, 'CGC': 0.18, 'CGA': 0.11, 'CGG': 0.20, 'AGA': 0.21, 'AGG': 0.22},
        'S': {'TCT': 0.19, 'TCC': 0.22, 'TCA': 0.15, 'TCG': 0.05, 'AGT': 0.15, 'AGC': 0.24},
        'T': {'ACT': 0.25, 'ACC': 0.36, 'ACA': 0.28, 'ACG': 0.11},
        'V': {'GTT': 0.18, 'GTC': 0.24, 'GTA': 0.11, 'GTG': 0.47},
        'W': {'TGG': 1.00},
        'Y': {'TAT': 0.44, 'TAC': 0.56},
        '*': {'TAA': 0.30, 'TAG': 0.24, 'TGA': 0.46}
    }
    
    @classmethod
    def optimize_sequence(cls, protein_sequence: str) -> str:
        """Optimize a protein sequence for mammalian expression"""
        optimized_codons = []
        
        for amino_acid in protein_sequence.upper():
            if amino_acid in cls.MAMMALIAN_CODON_TABLE:
                # Get the most frequent codon for this amino acid
                codon_options = cls.MAMMALIAN_CODON_TABLE[amino_acid]
                best_codon = max(codon_options, key=codon_options.get)
                optimized_codons.append(best_codon)
            else:
                raise ValueError(f"Unknown amino acid: {amino_acid}")
        
        return ''.join(optimized_codons)
    
    @classmethod
    def calculate_optimization_score(cls, dna_sequence: str) -> float:
        """Calculate optimization score for a DNA sequence"""
        if len(dna_sequence) % 3 != 0:
            raise ValueError("DNA sequence length must be divisible by 3")
        
        score = 0.0
        codon_count = 0
        
        for i in range(0, len(dna_sequence), 3):
            codon = dna_sequence[i:i+3]
            # Find which amino acid this codon codes for
            for aa, codons in cls.MAMMALIAN_CODON_TABLE.items():
                if codon in codons:
                    score += codons[codon]
                    codon_count += 1
                    break
        
        return score / codon_count if codon_count > 0 else 0.0


class PlasmidBuilder:
    """Main class for building plasmid vectors for mRNA vaccines"""
    
    def __init__(self, name: str = "neoantigen_x_vector"):
        self.name = name
        self.elements: List[PlasmidElement] = []
        self.total_length = 0
        
        # Pre-defined regulatory elements for mRNA vaccine applications
        self.regulatory_library = self._initialize_regulatory_library()
    
    def _initialize_regulatory_library(self) -> Dict[str, PlasmidElement]:
        """Initialize library of common regulatory elements"""
        return {
            "cmv_promoter": PlasmidElement(
                name="CMV Promoter",
                sequence="GTTGACATTGATTATTGACTAGTTATTAATAGTAATCAATTACGGGGTCATTAGTTCATAGCCCATATATGGAGTTCCGCGTTACATAACTTACGGTAAATGGCCCGCCTGGCTGACCGCCCAACGACCCCCGCCCATTGACGTCAATAATGACGTATGTTCCCATAGTAACGCCAATAGGGACTTTCCATTGACGTCAATGGGTGGAGTATTTACGGTAAACTGCCCACTTGGCAGTACATCAAGTGTATCATATGCCAAGTACGCCCCCTATTGACGTCAATGACGGTAAATGGCCCGCCTGGCATTATGCCCAGTACATGACCTTATGGGACTTTCCTACTTGGCAGTACATCTACGTATTAGTCATCGCTATTACCATGGTGATGCGGTTTTGGCAGTACATCAATGGGCGTGGATAGCGGTTTGACTCACGGGGATTTCCAAGTCTCCACCCCATTGACGTCAATGGGAGTTTGTTTTGGCACCAAAATCAACGGGACTTTCCAAAATGTCGTAACAACTCCGCCCCATTGACGCAAATGGGCGGTAGGCGTGTACGGTGGGAGGTCTATATAAGCAGAGCTCGTTTAGTGAACCGTCAGATCGCCTGGAGACGCCATCCACGCTGTTTTGACCTCCATAGAAGACACCGGGACCGATCCAGCCTCCGCGGCCGGGAACGGTGCATTGGAACGCGGATTCCCCGTGCCAAGAGTGACGTAAGTACCGCCTATAGAGTCTATAGGCCCACCCCCTTGGCTTCGAGGAA",
                element_type=ElementType.PROMOTER,
                description="Strong CMV immediate early promoter for high expression"
            ),
            "t7_promoter": PlasmidElement(
                name="T7 Promoter",
                sequence="TAATACGACTCACTATAGGG",
                element_type=ElementType.PROMOTER,
                description="T7 RNA polymerase promoter for in vitro transcription"
            ),
            "his_tag": PlasmidElement(
                name="6xHis Tag",
                sequence="CATCATCATCATCATCAT",
                element_type=ElementType.TAG,
                description="Hexahistidine tag for protein purification"
            ),
            "flag_tag": PlasmidElement(
                name="FLAG Tag",
                sequence="GACTACAAAGACCATGACGGTGATTATAAAGATCATGACATCGATTACAAGGATGACGATGACAAG",
                element_type=ElementType.TAG,
                description="FLAG epitope tag for detection and purification"
            ),
            "kozak_sequence": PlasmidElement(
                name="Kozak Sequence",
                sequence="GCCACC",
                element_type=ElementType.ENHANCER,
                description="Kozak consensus sequence for enhanced translation initiation"
            ),
            "bgh_polya": PlasmidElement(
                name="BGH polyA",
                sequence="CTCGAGACATGATAAGATACATTGATGAGTTTGGACAAACCACAACTAGAATGCAGTGAAAAAAATGCTTTATTTGTGAAATTTGTGATGCTATTGCTTTATTTGTAACCATTATAAGCTGCAATAAACAAGTTAACAACAACAATTGCATTCATTTTATGTTTCAGGTTCAGGGGGAGATGTGGGAGGTTTTTTAAAGCAAGTAAAACCTCTACAAATGTGGTAAAATCGATAAG",
                element_type=ElementType.UTR,
                description="BGH polyadenylation signal for mRNA stability"
            ),
            "amp_resistance": PlasmidElement(
                name="Ampicillin Resistance",
                sequence="ATGAGTATTCAACATTTCCGTGTCGCCCTTATTCCCTTTTTTGCGGCATTTTGCCTTCCTGTTTTTGCTCACCCAGAAACGCTGGTGAAAGTAAAAGATGCTGAAGATCAGTTGGGTGCACGAGTGGGTTACATCGAACTGGATCTCAACAGCGGTAAGATCCTTGAGAGTTTTCGCCCCGAAGAACGTTTTCCAATGATGAGCACTTTTAAAGTTCTGCTATGTGGCGCGGTATTATCCCGTATTGACGCCGGGCAAGAGCAACTCGGTCGCCGCATACACTATTCTCAGAATGACTTGGTTGAGTACTCACCAGTCACAGAAAAGCATCTTACGGATGGCATGACAGTAAGAGAATTATGCAGTGCTGCCATAACCATGAGTGATAACACTGCGGCCAACTTACTTCTGACAACGATCGGAGGACCGAAGGAGCTAACCGCTTTTTTGCACAACATGGGGGATCATGTAACTCGCCTTGATCGTTGGGAACCGGAGCTGAATGAAGCCATACCAAACGACGAGCGTGACACCACGATGCCTGTAGCAATGGCAACAACGTTGCGCAAACTATTAACTGGCGAACTACTTACTCTAGCTTCCCGGCAACAATTAATAGACTGGATGGAGGCGGATAAAGTTGCAGGACCACTTCTGCGCTCGGCCCTTCCGGCTGGCTGGTTTATTGCTGATAAATCTGGAGCCGGTGAGCGTGGGTCTCGCGGTATCATTGCAGCACTGGGGCCAGATGGTAAGCCCTCCCGTATCGTAGTTATCTACACGACGGGGAGTCAGGCAACTATGGATGAACGAAATAGACAGATCGCTGAGATAGGTGCCTCACTGATTAAGCATTGGTAACTGTCAGACCAAGTTTACTCATATATACTTTAGATTGATTTAAAACTTCATTTTTAATTTAAAAGGATCTAGGTGAAGATCCTTTTTGATAATCTCATGACCAAAATCCCTTAACGTGAGTTTTCGTTCCACTGAGCGTCAGACCCCGTAGAAAAGATCAAAGGATCTTCTTGAGATCCTTTTTTTCTGCGCGTAATCTGCTGCTTGCAAACAAAAAAACCACCGCTACCAGCGGTGGTTTGTTTGCCGGATCAAGAGCTACCAACTCTTTTTCCGAAGGTAACTGGCTTCAGCAGAGCGCAGATACCAAATACTGTCCTTCTAGTGTAGCCGTAGTTAGGCCACCACTTCAAGAACTCTGTAGCACCGCCTACATACCTCGCTCTGCTAATCCTGTTACCAGTGGCTGCTGCCAGTGGCGATAAGTCGTGTCTTACCGGGTTGGACTCAAGACGATAGTTACCGGATAAGGCGCAGCGGTCGGGCTGAACGGGGGGTTCGTGCACACAGCCCAGCTTGGAGCGAACGACCTACACCGAACTGAGATACCTACAGCGTGAGCTATGAGAAAGCGCCACGCTTCCCGAAGGGAGAAAGGCGGACAGGTATCCGGTAAGCGGCAGGGTCGGAACAGGAGAGCGCACGAGGGAGCTTCCAGGGGGAAACGCCTGGTATCTTTATAGTCCTGTCGGGTTTCGCCACCTCTGACTTGAGCGTCGATTTTTGTGATGCTCGTCAGGGGGGCGGAGCCTATGGAAAAACGCCAGCAACGCGGCCTTTTTACGGTTCCTGGCCTTTTGCTGGCCTTTTGCTCACATGTTCTTTCCTGCGTTATCCCCTGATTCTGTGGATAACCGTATTACCGCCTTTGAGTGAGCTGATACCGCTCGCCGCAGCCGAACGACCGAGCGCAGCGAGTCAGTGAGCGAGGAAGCGGAAGAGCGCCCAATACGCAAACCGCCTCTCCCCGCGCGTTGGCCGATTCATTAATGCAGCTG",
                element_type=ElementType.RESISTANCE,
                description="Ampicillin resistance gene for selection"
            )
        }
    
    def add_element(self, element: PlasmidElement, position: Optional[int] = None) -> None:
        """Add an element to the plasmid"""
        if position is not None:
            element.position = position
        else:
            element.position = self.total_length
        
        self.elements.append(element)
        self.total_length += element.length
    
    def add_neoantigen_x(self, protein_sequence: str, optimize_codons: bool = True) -> None:
        """Add neoantigen X gene with optional codon optimization"""
        if optimize_codons:
            dna_sequence = CodonOptimizer.optimize_sequence(protein_sequence)
            optimization_score = CodonOptimizer.calculate_optimization_score(dna_sequence)
            description = f"Codon-optimized neoantigen X (optimization score: {optimization_score:.3f})"
        else:
            # Convert protein to DNA using standard genetic code (simplified)
            dna_sequence = protein_sequence  # This would need proper translation
            description = "Neoantigen X (not codon optimized)"
        
        neoantigen_element = PlasmidElement(
            name="Neoantigen X",
            sequence=dna_sequence,
            element_type=ElementType.GENE,
            description=description
        )
        
        self.add_element(neoantigen_element)
    
    def add_from_library(self, element_name: str) -> None:
        """Add a pre-defined element from the regulatory library"""
        if element_name in self.regulatory_library:
            element = self.regulatory_library[element_name]
            self.add_element(element)
        else:
            raise ValueError(f"Element '{element_name}' not found in library")
    
    def build_mrna_compatible_vector(self, neoantigen_sequence: str) -> None:
        """Build a complete mRNA-compatible vector for neoantigen X"""
        # Add T7 promoter for in vitro transcription
        self.add_from_library("t7_promoter")
        
        # Add Kozak sequence for enhanced translation
        self.add_from_library("kozak_sequence")
        
        # Add start codon
        start_codon = PlasmidElement(
            name="Start Codon",
            sequence="ATG",
            element_type=ElementType.GENE,
            description="Translation start codon"
        )
        self.add_element(start_codon)
        
        # Add FLAG tag for detection
        self.add_from_library("flag_tag")
        
        # Add optimized neoantigen X
        self.add_neoantigen_x(neoantigen_sequence, optimize_codons=True)
        
        # Add His tag for purification
        self.add_from_library("his_tag")
        
        # Add stop codon
        stop_codon = PlasmidElement(
            name="Stop Codon",
            sequence="TAA",
            element_type=ElementType.GENE,
            description="Translation stop codon"
        )
        self.add_element(stop_codon)
        
        # Add polyA tail for mRNA stability
        self.add_from_library("bgh_polya")
        
        # For plasmid maintenance (not in final mRNA)
        self.add_from_library("amp_resistance")
    
    def get_full_sequence(self) -> str:
        """Get the complete plasmid sequence"""
        return ''.join([element.sequence for element in self.elements])
    
    def get_mrna_sequence(self) -> str:
        """Get the mRNA sequence (excluding plasmid maintenance elements)"""
        mrna_elements = [
            element for element in self.elements 
            if element.element_type != ElementType.RESISTANCE
        ]
        return ''.join([element.sequence for element in mrna_elements])
    
    def validate_design(self) -> Dict[str, any]:
        """Perform in silico validation of the plasmid design"""
        validation_results = {
            "total_length": self.total_length,
            "element_count": len(self.elements),
            "has_promoter": any(e.element_type == ElementType.PROMOTER for e in self.elements),
            "has_gene": any(e.element_type == ElementType.GENE for e in self.elements),
            "has_tags": any(e.element_type == ElementType.TAG for e in self.elements),
            "mrna_compatible": any(e.name == "T7 Promoter" for e in self.elements),
            "elements": [{"name": e.name, "type": e.element_type.value, "length": e.length} for e in self.elements]
        }
        
        # Check for proper start/stop codons
        full_seq = self.get_full_sequence()
        validation_results["has_start_codon"] = "ATG" in full_seq
        validation_results["has_stop_codon"] = any(stop in full_seq for stop in ["TAA", "TAG", "TGA"])
        
        return validation_results
    
    def export_design(self) -> Dict[str, any]:
        """Export the complete plasmid design as JSON"""
        # Convert elements to dict format with proper enum handling
        elements_data = []
        for element in self.elements:
            element_dict = asdict(element)
            element_dict['element_type'] = element.element_type.value  # Convert enum to string
            elements_data.append(element_dict)
        
        return {
            "name": self.name,
            "total_length": self.total_length,
            "elements": elements_data,
            "full_sequence": self.get_full_sequence(),
            "mrna_sequence": self.get_mrna_sequence(),
            "validation": self.validate_design()
        }


def main():
    """Example usage of the plasmid builder"""
    # Example neoantigen X sequence (simplified)
    neoantigen_x_sequence = "MQLVESGGGLVKPGGSLRLSCAASGFTFSSYAMSWVRQAPGKGLEWVSAISGSGGSTYYADSVKGRFTISRDNSKNTLYLQMNSLRAEDTAVYYCAKVSYLSTASSLDYWGQGTLVTVSS"
    
    # Create plasmid builder
    builder = PlasmidBuilder("neoantigen_x_mrna_vector")
    
    # Build mRNA-compatible vector
    builder.build_mrna_compatible_vector(neoantigen_x_sequence)
    
    # Validate design
    validation = builder.validate_design()
    print("Plasmid Design Validation:")
    for key, value in validation.items():
        if key != "elements":
            print(f"  {key}: {value}")
    
    print(f"\nTotal plasmid length: {builder.total_length} bp")
    print(f"Number of elements: {len(builder.elements)}")
    
    # Export design
    design = builder.export_design()
    
    return builder, design


if __name__ == "__main__":
    builder, design = main()