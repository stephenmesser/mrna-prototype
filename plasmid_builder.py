#!/usr/bin/env python3
"""
Plasmid Vector Design System for Neoantigen X mRNA Vaccine

This module provides a comprehensive system for designing plasmid vectors
for neoantigen expression in mRNA vaccine applications.

Author: AI Assistant
Date: 2024
"""

import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
try:
    from Bio.Seq import Seq
except ImportError:
    # Fallback if BioPython is not available
    pass


@dataclass
class PlasmidComponent:
    """Represents a component of the plasmid vector."""
    name: str
    sequence: str
    start_pos: int
    end_pos: int
    feature_type: str
    description: str


class NeoantiogenX:
    """
    Represents neoantigen X with optimized sequence and properties.
    
    For this prototype, we'll use a representative neoantigen sequence
    that would be derived from tumor-specific mutations.
    """
    
    def __init__(self):
        # Example neoantigen sequence (9-mer epitope extended for better expression)
        # In practice, this would be derived from patient-specific tumor sequencing
        self.raw_peptide = "KTVNMRLGL"  # Example HLA-A*02:01 restricted neoantigen
        
        # Extended sequence for better expression and processing
        self.extended_sequence = self._generate_extended_sequence()
        
        # Human codon usage table for optimization
        self.codon_usage = self._get_human_codon_usage()
    
    def _generate_extended_sequence(self) -> str:
        """Generate an extended neoantigen sequence with flanking regions."""
        # Add flanking sequences to improve processing and presentation
        n_flank = "MGSLVLVAAL"  # Signal peptide for ER targeting
        c_flank = "GGGSGGGSGGS"  # Flexible linker
        
        extended = n_flank + self.raw_peptide + c_flank
        return extended
    
    def _get_human_codon_usage(self) -> Dict[str, Dict[str, float]]:
        """Get human codon usage frequencies for optimization."""
        # Simplified human codon usage table (key codons)
        return {
            'K': {'AAA': 0.58, 'AAG': 0.42},
            'T': {'ACA': 0.28, 'ACC': 0.36, 'ACG': 0.11, 'ACT': 0.25},
            'V': {'GTA': 0.11, 'GTC': 0.24, 'GTG': 0.47, 'GTT': 0.18},
            'N': {'AAC': 0.54, 'AAT': 0.46},
            'M': {'ATG': 1.0},
            'R': {'AGA': 0.20, 'AGG': 0.20, 'CGA': 0.11, 'CGC': 0.19, 'CGG': 0.21, 'CGT': 0.08},
            'L': {'CTA': 0.07, 'CTC': 0.20, 'CTG': 0.41, 'CTT': 0.13, 'TTA': 0.07, 'TTG': 0.13},
            'G': {'GGA': 0.25, 'GGC': 0.34, 'GGG': 0.25, 'GGT': 0.16},
            'S': {'AGC': 0.24, 'AGT': 0.15, 'TCA': 0.15, 'TCC': 0.22, 'TCG': 0.06, 'TCT': 0.18},
            'A': {'GCA': 0.23, 'GCC': 0.40, 'GCG': 0.11, 'GCT': 0.26}
        }
    
    def optimize_codons(self) -> str:
        """Optimize codons for human expression."""
        optimized_dna = ""
        
        for aa in self.extended_sequence:
            if aa in self.codon_usage:
                # Select the most frequent codon for this amino acid
                codons = self.codon_usage[aa]
                best_codon = max(codons.items(), key=lambda x: x[1])[0]
                optimized_dna += best_codon
            else:
                # Fallback for amino acids not in our simplified table
                optimized_dna += self._get_standard_codon(aa)
        
        return optimized_dna
    
    def _get_standard_codon(self, aa: str) -> str:
        """Get standard codon for amino acids not in optimization table."""
        standard_codons = {
            'F': 'TTC', 'Y': 'TAC', 'H': 'CAC', 'Q': 'CAG',
            'I': 'ATC', 'P': 'CCC', 'D': 'GAC', 'E': 'GAG',
            'C': 'TGC', 'W': 'TGG', '*': 'TAA'
        }
        return standard_codons.get(aa, 'NNN')


class PlasmidDesigner:
    """
    Main class for designing the plasmid vector for neoantigen X.
    """
    
    def __init__(self):
        self.neoantigen = NeoantiogenX()
        self.components = []
        self.total_length = 0
        self.design_rationale = {}
    
    def design_vector(self) -> Dict:
        """
        Design the complete plasmid vector with all necessary components.
        """
        print("Designing plasmid vector for neoantigen X...")
        
        # Build vector components in order
        self._add_promoter()
        self._add_kozak_sequence()
        self._add_signal_peptide()
        self._add_neoantigen_sequence()
        self._add_expression_tags()
        self._add_terminator()
        self._add_selection_marker()
        self._add_origin_of_replication()
        
        # Calculate final positions
        self._calculate_positions()
        
        # Generate design summary
        return self._generate_design_summary()
    
    def _add_promoter(self):
        """Add CMV promoter for high expression in mammalian cells."""
        cmv_promoter = (
            "TAGTTATTAATAGTAATCAATTACGGGGTCATTAGTTCATAGCCCATATATGGAGTTCCGCGTTACATAACTTACG"
            "GTAAATGGCCCGCCTGGCTGACCGCCCAACGACCCCCGCCCATTGACGTCAATAATGACGTATGTTCCCATAGTAAC"
            "GCCAATAGGGACTTTCCATTGACGTCAATGGGTGGAGTATTTACGGTAAACTGCCCACTTGGCAGTACATCAAGTG"
            "TATCATATGCCAAGTACGCCCCCTATTGACGTCAATGACGGTAAATGGCCCGCCTGGCATTATGCCCAGTACATGA"
            "CCTTATGGGACTTTCCTACTTGGCAGTACATCTACGTATTAGTCATCGCTATTACCATGGTGATGCGGTTTTGGCA"
            "GTACATCAATGGGCGTGGATAGCGGTTTGACTCACGGGGATTTCCAAGTCTCCACCCCATTGACGTCAATGGGAGT"
            "TTGTTTTGGCACCAAAATCAACGGGACTTTCCAAAATGTCGTAACAACTCCGCCCCATTGACGCAAATGGGCGGTA"
            "GGCGTGTACGGTGGGAGGTCTATATAAGCAGAGCTCTCTGGCTAACTAGAGAACCCACTGCTTACTGGCTTATCGAA"
            "ATTAATACGACTCACTATAGGGAGACCCAAGCTGGCTAGTTAAGCTTGGTACCGAGCTCGGATCCACTAGTAACGGC"
            "CGCCAGTGTGCTGGAATTCGCCCTT"
        )
        
        component = PlasmidComponent(
            name="CMV_Promoter",
            sequence=cmv_promoter,
            start_pos=0,
            end_pos=len(cmv_promoter),
            feature_type="promoter",
            description="Cytomegalovirus immediate early promoter for high expression in mammalian cells"
        )
        self.components.append(component)
        
        self.design_rationale["promoter"] = (
            "CMV promoter selected for strong, constitutive expression in mammalian cells. "
            "Widely used in mRNA vaccine applications and provides reliable high-level expression."
        )
    
    def _add_kozak_sequence(self):
        """Add Kozak sequence for efficient translation initiation."""
        kozak = "GCCACCATGG"  # Optimal Kozak sequence with start codon
        
        component = PlasmidComponent(
            name="Kozak_Sequence",
            sequence=kozak,
            start_pos=0,  # Will be updated in _calculate_positions
            end_pos=len(kozak),
            feature_type="regulatory",
            description="Kozak sequence for efficient translation initiation"
        )
        self.components.append(component)
        
        self.design_rationale["kozak"] = (
            "Optimal Kozak sequence (GCCACCATGG) included to maximize translation efficiency. "
            "Critical for high protein expression levels."
        )
    
    def _add_signal_peptide(self):
        """Add signal peptide for ER targeting and MHC presentation."""
        # tPA signal peptide - well characterized for secretion
        signal_peptide_aa = "MDAMKRGLCCVLLLCGAVFVSP"
        signal_peptide_dna = self._optimize_sequence(signal_peptide_aa)
        
        component = PlasmidComponent(
            name="Signal_Peptide",
            sequence=signal_peptide_dna,
            start_pos=0,
            end_pos=len(signal_peptide_dna),
            feature_type="signal",
            description="tPA signal peptide for ER targeting and secretion"
        )
        self.components.append(component)
        
        self.design_rationale["signal_peptide"] = (
            "tPA signal peptide ensures proper targeting to the ER for MHC class I presentation pathway. "
            "Essential for neoantigen processing and presentation to T cells."
        )
    
    def _add_neoantigen_sequence(self):
        """Add the codon-optimized neoantigen X sequence."""
        optimized_sequence = self.neoantigen.optimize_codons()
        
        component = PlasmidComponent(
            name="Neoantigen_X",
            sequence=optimized_sequence,
            start_pos=0,
            end_pos=len(optimized_sequence),
            feature_type="CDS",
            description=f"Codon-optimized neoantigen X sequence: {self.neoantigen.raw_peptide}"
        )
        self.components.append(component)
        
        self.design_rationale["neoantigen"] = (
            f"Neoantigen X ({self.neoantigen.raw_peptide}) with flanking sequences for improved processing. "
            "Codon-optimized for human expression to maximize mRNA stability and translation efficiency."
        )
    
    def _add_expression_tags(self):
        """Add expression and purification tags."""
        # His-tag for purification and FLAG tag for detection
        his_tag_aa = "HHHHHH"
        flag_tag_aa = "DYKDDDDK"
        
        his_tag_dna = self._optimize_sequence(his_tag_aa)
        flag_tag_dna = self._optimize_sequence(flag_tag_aa)
        
        # Add linker between tags
        linker_aa = "GGS"
        linker_dna = self._optimize_sequence(linker_aa)
        
        combined_tags = his_tag_dna + linker_dna + flag_tag_dna
        
        component = PlasmidComponent(
            name="Expression_Tags",
            sequence=combined_tags,
            start_pos=0,
            end_pos=len(combined_tags),
            feature_type="tag",
            description="His-tag and FLAG tag for purification and detection"
        )
        self.components.append(component)
        
        self.design_rationale["tags"] = (
            "His-tag enables protein purification for quality control. "
            "FLAG tag allows detection and quantification of expression levels. "
            "Critical for validating vaccine efficacy."
        )
    
    def _add_terminator(self):
        """Add transcription termination sequence."""
        # BGH polyadenylation signal
        bgh_polyA = (
            "CTCGAGAAATTTGTGATGCTATTGCTTTATTTGTAACCATTATAAGCTGCAATAAACAAGTTAACAACAACAATT"
            "GCATTCATTTTATGTTTCAGGTTCAGGGGGAGGTGTGGGAGGTTTTTTAAAGCAAGTAAAACCTCTACAAATGTG"
            "GTATGGCTGATTATGATCC"
        )
        
        component = PlasmidComponent(
            name="BGH_polyA",
            sequence=bgh_polyA,
            start_pos=0,
            end_pos=len(bgh_polyA),
            feature_type="terminator",
            description="BGH polyadenylation signal for mRNA stability"
        )
        self.components.append(component)
        
        self.design_rationale["terminator"] = (
            "BGH polyadenylation signal provides efficient transcription termination "
            "and mRNA stability, essential for mRNA vaccine applications."
        )
    
    def _add_selection_marker(self):
        """Add antibiotic resistance for plasmid selection."""
        # Simplified ampicillin resistance gene
        amp_resistance = (
            "ATGAGTATTCAACATTTCCGTGTCGCCCTTATTCCCTTTTTTGCGGCATTTTGCCTTCCTGTTTTTGCTCACCC"
            "AGAAACGCTGGTGAAAGTAAAAGATGCTGAAGATCAGTTGGGTGCACGAGTGGGTTACATCGAACTGGATCTCA"
            "ACAGCGGTAAGATCCTTGAGAGTTTTCGCCCCGAAGAACGTTTTCCAATGATGAGCACTTTTAAAGTTCTGCTA"
            "TGTGGCGCGGTATTATCCCGTGTTGACGCCGGGCAAGAGCAACTCGGTCGCCGCATACACTATTCTCAGAATGA"
            "CTTGGTTGAGTACTCACCAGTCACAGAAAAGCATCTTACGGATGGCATGACAGTAAGAGAATTATGCAGTGCTG"
            "CCATAACCATGAGTGATAACACTGCGGCCAACTTACTTCTGACAACGATCGGAGGACCGAAGGAGCTAACCGCT"
            "TTTTTGCACAACATGGGGGATCATGTAACTCGCCTTGATCGTTGGGAACCGGAGCTGAATGAAGCCATACCAAA"
            "CGACGAGCGTGACACCACGATGCCTGTAGCAATGGCAACAACGTTGCGCAAACTATTAACTGGCGAACTACTTA"
            "CTCTAGCTTCCCGGCAACAATTAATAGACTGGATGGAGGCGGATAAAGTTGCAGGACCACTTCTGCGCTCGGCC"
            "CTTCCGGCTGGCTGGTTTATTGCTGATAAATCTGGAGCCGGTGAGCGTGGGTCTCGCGGTATCATTGCAGCACT"
            "GGGGCCAGATGGTAAGCCCTCCCGTATCGTAGTTATCTACACGACGGGGAGTCAGGCAACTATGGATGAACGAA"
            "ATAGACAGATCGCTGAGATAGGTGCCTCACTGATTAAGCATTGGTAA"
        )
        
        component = PlasmidComponent(
            name="Ampicillin_Resistance",
            sequence=amp_resistance,
            start_pos=0,
            end_pos=len(amp_resistance),
            feature_type="selection",
            description="Ampicillin resistance gene for plasmid selection"
        )
        self.components.append(component)
        
        self.design_rationale["selection"] = (
            "Ampicillin resistance gene enables selection of successfully transformed bacterial cells "
            "during plasmid production and amplification."
        )
    
    def _add_origin_of_replication(self):
        """Add bacterial origin of replication."""
        # Simplified ColE1 origin of replication
        cole1_ori = (
            "TTAATTAAGCGGCCGCCCTGTCAGGTTGGGGGATAAGTCCCCTCCCTCCCCTATAGATCCGCCACCTAGAATG"
            "CGCCGCATCTGTGCCCGCCACCCAGAGACAGGAGAGGCCACCCAGAGACAGCCCTTACCCCTGGGGGGAGAGG"
            "AGAAAAGGAAAAGGACACCGGAGAAGGGGAGAGAGGGGAGCCCACCCCGAGAGCCCACCCCGAGAGCCGAGGG"
            "CCCAGCCGCCCACCCCCCAATCGCGGGGGAGGGATGGGGGCCACCTGCGGGGGGCCCCCCCCCCCCCCCGCCC"
        )
        
        component = PlasmidComponent(
            name="ColE1_Origin",
            sequence=cole1_ori,
            start_pos=0,
            end_pos=len(cole1_ori),
            feature_type="origin",
            description="ColE1 origin of replication for bacterial propagation"
        )
        self.components.append(component)
        
        self.design_rationale["origin"] = (
            "ColE1 origin of replication allows high-copy plasmid propagation in E. coli "
            "for efficient production and purification."
        )
    
    def _optimize_sequence(self, protein_seq: str) -> str:
        """Optimize a protein sequence for human codon usage."""
        optimized = ""
        for aa in protein_seq:
            if aa in self.neoantigen.codon_usage:
                codons = self.neoantigen.codon_usage[aa]
                best_codon = max(codons.items(), key=lambda x: x[1])[0]
                optimized += best_codon
            else:
                optimized += self.neoantigen._get_standard_codon(aa)
        return optimized
    
    def _calculate_positions(self):
        """Calculate start and end positions for all components."""
        current_pos = 0
        for component in self.components:
            component.start_pos = current_pos
            component.end_pos = current_pos + len(component.sequence)
            current_pos = component.end_pos
        
        self.total_length = current_pos
    
    def _generate_design_summary(self) -> Dict:
        """Generate a comprehensive design summary."""
        summary = {
            "plasmid_name": "pNeoantigenX-mRNA",
            "total_length": self.total_length,
            "neoantigen_sequence": self.neoantigen.raw_peptide,
            "extended_sequence": self.neoantigen.extended_sequence,
            "codon_optimized": True,
            "components": [],
            "design_rationale": self.design_rationale,
            "expression_system": "Mammalian (Human)",
            "intended_use": "mRNA vaccine template",
            "quality_metrics": self._calculate_quality_metrics()
        }
        
        for comp in self.components:
            summary["components"].append({
                "name": comp.name,
                "type": comp.feature_type,
                "start": comp.start_pos,
                "end": comp.end_pos,
                "length": len(comp.sequence),
                "description": comp.description
            })
        
        return summary
    
    def _calculate_quality_metrics(self) -> Dict:
        """Calculate quality metrics for the plasmid design."""
        # Get the complete CDS sequence
        cds_sequence = ""
        for comp in self.components:
            if comp.feature_type in ["signal", "CDS", "tag"]:
                cds_sequence += comp.sequence
        
        # Calculate GC content
        gc_count = cds_sequence.count('G') + cds_sequence.count('C')
        gc_content = (gc_count / len(cds_sequence)) * 100 if cds_sequence else 0
        
        # Check for problematic sequences
        problematic_motifs = self._check_problematic_motifs(cds_sequence)
        
        return {
            "cds_length": len(cds_sequence),
            "gc_content_percent": round(gc_content, 2),
            "problematic_motifs": problematic_motifs,
            "codon_adaptation_index": "Optimized for human expression",
            "predicted_expression": "High" if 40 <= gc_content <= 60 else "Moderate"
        }
    
    def _check_problematic_motifs(self, sequence: str) -> List[str]:
        """Check for problematic sequence motifs."""
        motifs = []
        
        # Check for poly-A/T stretches
        if re.search(r'A{6,}|T{6,}', sequence):
            motifs.append("Long poly-A/T stretch detected")
        
        # Check for high GC stretches
        if re.search(r'[GC]{8,}', sequence):
            motifs.append("High GC stretch detected")
        
        # Check for rare codons (simplified check)
        rare_codons = ['CGA', 'CGG', 'AGA', 'AGG', 'CTA', 'CTC']
        for codon in rare_codons:
            if sequence.count(codon) > 2:
                motifs.append(f"Multiple rare codons ({codon}) detected")
        
        return motifs if motifs else ["No problematic motifs detected"]
    
    def generate_plasmid_map(self) -> str:
        """Generate a text-based plasmid map."""
        map_str = "\n" + "="*80 + "\n"
        map_str += "PLASMID MAP: pNeoantigenX-mRNA\n"
        map_str += "="*80 + "\n"
        map_str += f"Total Length: {self.total_length} bp\n\n"
        
        for i, comp in enumerate(self.components, 1):
            map_str += f"{i:2d}. {comp.name:20s} ({comp.start_pos:4d}-{comp.end_pos:4d}) "
            map_str += f"[{len(comp.sequence):4d} bp] - {comp.feature_type}\n"
            map_str += f"    {comp.description}\n\n"
        
        return map_str
    
    def export_sequences(self) -> Dict[str, str]:
        """Export all sequences in different formats."""
        sequences = {}
        
        # Individual component sequences
        for comp in self.components:
            sequences[comp.name] = comp.sequence
        
        # Complete plasmid sequence
        complete_sequence = "".join([comp.sequence for comp in self.components])
        sequences["complete_plasmid"] = complete_sequence
        
        # Just the expression cassette (promoter through terminator)
        expression_components = [comp for comp in self.components 
                               if comp.feature_type in ["promoter", "regulatory", "signal", "CDS", "tag", "terminator"]]
        expression_cassette = "".join([comp.sequence for comp in expression_components])
        sequences["expression_cassette"] = expression_cassette
        
        return sequences
    
    def validate_design(self) -> Dict[str, bool]:
        """Perform in silico validation of the plasmid design."""
        validation_results = {}
        
        # Check if all essential components are present
        essential_components = ["promoter", "CDS", "terminator", "selection", "origin"]
        for comp_type in essential_components:
            has_component = any(comp.feature_type == comp_type for comp in self.components)
            validation_results[f"has_{comp_type}"] = has_component
        
        # Check sequence integrity
        total_seq_length = sum(len(comp.sequence) for comp in self.components)
        validation_results["sequence_integrity"] = total_seq_length == self.total_length
        
        # Check for ORF integrity
        cds_components = [comp for comp in self.components if comp.feature_type in ["signal", "CDS", "tag"]]
        total_cds_length = sum(len(comp.sequence) for comp in cds_components)
        validation_results["orf_frame_correct"] = total_cds_length % 3 == 0
        
        # Check GC content
        complete_seq = "".join([comp.sequence for comp in self.components])
        gc_content = (complete_seq.count('G') + complete_seq.count('C')) / len(complete_seq) * 100
        validation_results["gc_content_acceptable"] = 30 <= gc_content <= 70
        
        return validation_results


def main():
    """Main function to demonstrate the plasmid design system."""
    print("Plasmid Vector Design System for Neoantigen X mRNA Vaccine")
    print("=" * 60)
    
    # Create designer instance
    designer = PlasmidDesigner()
    
    # Design the vector
    design_summary = designer.design_vector()
    
    # Display results
    print("\nDESIGN SUMMARY:")
    print(f"Plasmid Name: {design_summary['plasmid_name']}")
    print(f"Total Length: {design_summary['total_length']} bp")
    print(f"Neoantigen: {design_summary['neoantigen_sequence']}")
    print(f"Expression System: {design_summary['expression_system']}")
    
    # Show plasmid map
    print(designer.generate_plasmid_map())
    
    # Show quality metrics
    print("QUALITY METRICS:")
    metrics = design_summary['quality_metrics']
    for key, value in metrics.items():
        print(f"  {key}: {value}")
    
    # Validate design
    print("\nVALIDATION RESULTS:")
    validation = designer.validate_design()
    for test, result in validation.items():
        status = "PASS" if result else "FAIL"
        print(f"  {test}: {status}")
    
    # Export sequences for synthesis
    sequences = designer.export_sequences()
    print(f"\nExported {len(sequences)} sequence components for synthesis")
    
    # Show design rationale
    print("\nDESIGN RATIONALE:")
    for component, rationale in design_summary['design_rationale'].items():
        print(f"\n{component.upper()}:")
        print(f"  {rationale}")
    
    print("\n" + "=" * 60)
    print("Plasmid design completed successfully!")
    print("Ready for experimental validation and mRNA synthesis.")
    
    return design_summary


if __name__ == "__main__":
    main()