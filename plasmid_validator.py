#!/usr/bin/env python3
"""
Enhanced Validation Module for Plasmid Vector Design
Performs comprehensive in silico validation for mRNA vaccine applications.
"""

import json
import re
from typing import Dict, List, Tuple, Optional, Any
from plasmid_builder import PlasmidBuilder, PlasmidElement, ElementType, CodonOptimizer


class PlasmidValidator:
    """Comprehensive validation tools for plasmid design"""
    
    # Restriction enzyme recognition sites to avoid
    RESTRICTION_SITES = {
        'EcoRI': 'GAATTC',
        'BamHI': 'GGATCC',
        'HindIII': 'AAGCTT',
        'XhoI': 'CTCGAG',
        'NotI': 'GCGGCCGC',
        'KpnI': 'GGTACC'
    }
    
    # Illegal sequences that can cause problems
    ILLEGAL_SEQUENCES = {
        'poly_A': 'AAAAAA',  # Can cause premature termination
        'poly_T': 'TTTTTT',  # Can cause transcription termination
        'chi_site': 'GCTGGTGG',  # Recombination hotspot
        'direct_repeats': r'(.{8,})\1',  # Direct repeats > 8bp
    }
    
    @classmethod
    def validate_comprehensive(cls, builder: PlasmidBuilder, config_file: str = "plasmid_config.json") -> Dict[str, Any]:
        """Perform comprehensive validation of plasmid design"""
        
        # Load configuration
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
        except FileNotFoundError:
            config = cls._get_default_config()
        
        validation_results = {
            "overall_status": "PENDING",
            "timestamp": "",
            "basic_validation": cls._validate_basic_structure(builder, config),
            "sequence_validation": cls._validate_sequences(builder, config),
            "mrna_validation": cls._validate_mrna_compatibility(builder, config),
            "expression_validation": cls._validate_expression_potential(builder, config),
            "safety_validation": cls._validate_safety(builder, config),
            "optimization_validation": cls._validate_optimization(builder, config),
            "recommendations": []
        }
        
        # Determine overall status
        all_passed = all([
            validation_results["basic_validation"]["passed"],
            validation_results["sequence_validation"]["passed"],
            validation_results["mrna_validation"]["passed"],
            validation_results["expression_validation"]["passed"],
            validation_results["safety_validation"]["passed"]
        ])
        
        validation_results["overall_status"] = "PASSED" if all_passed else "FAILED"
        
        # Generate recommendations
        validation_results["recommendations"] = cls._generate_recommendations(validation_results)
        
        return validation_results
    
    @classmethod
    def _validate_basic_structure(cls, builder: PlasmidBuilder, config: Dict) -> Dict[str, Any]:
        """Validate basic plasmid structure"""
        validation = {
            "passed": True,
            "issues": [],
            "warnings": []
        }
        
        # Check length requirements
        min_length = config.get("validation_criteria", {}).get("min_total_length", 1000)
        max_length = config.get("validation_criteria", {}).get("max_total_length", 10000)
        
        if builder.total_length < min_length:
            validation["issues"].append(f"Plasmid too short: {builder.total_length} bp < {min_length} bp")
            validation["passed"] = False
        elif builder.total_length > max_length:
            validation["issues"].append(f"Plasmid too long: {builder.total_length} bp > {max_length} bp")
            validation["passed"] = False
        
        # Check required elements
        required_elements = config.get("validation_criteria", {}).get("required_elements", [])
        element_types_present = {e.element_type.value for e in builder.elements}
        
        for required in required_elements:
            if required not in element_types_present:
                validation["issues"].append(f"Missing required element type: {required}")
                validation["passed"] = False
        
        # Check element count
        if len(builder.elements) < 3:
            validation["warnings"].append("Very few elements in plasmid - consider adding more regulatory elements")
        
        validation["total_length"] = builder.total_length
        validation["element_count"] = len(builder.elements)
        validation["element_types"] = list(element_types_present)
        
        return validation
    
    @classmethod
    def _validate_sequences(cls, builder: PlasmidBuilder, config: Dict) -> Dict[str, Any]:
        """Validate DNA sequences for common issues"""
        validation = {
            "passed": True,
            "issues": [],
            "warnings": []
        }
        
        full_sequence = builder.get_full_sequence().upper()
        
        # Check for restriction sites
        restriction_sites_found = []
        for enzyme, site in cls.RESTRICTION_SITES.items():
            if site in full_sequence:
                restriction_sites_found.append(f"{enzyme} ({site})")
        
        if restriction_sites_found:
            validation["warnings"].append(f"Restriction sites found: {', '.join(restriction_sites_found)}")
        
        # Check for illegal sequences
        illegal_found = []
        for name, pattern in cls.ILLEGAL_SEQUENCES.items():
            if name == 'direct_repeats':
                matches = re.finditer(pattern, full_sequence)
                if any(matches):
                    illegal_found.append(name)
            else:
                if pattern in full_sequence:
                    illegal_found.append(name)
        
        if illegal_found:
            validation["issues"].append(f"Problematic sequences found: {', '.join(illegal_found)}")
            validation["passed"] = False
        
        # Check GC content
        gc_count = full_sequence.count('G') + full_sequence.count('C')
        gc_content = (gc_count / len(full_sequence)) * 100 if full_sequence else 0
        
        gc_range = config.get("codon_optimization", {}).get("gc_content_range", [40, 60])
        if not (gc_range[0] <= gc_content <= gc_range[1]):
            validation["warnings"].append(f"GC content {gc_content:.1f}% outside optimal range {gc_range[0]}-{gc_range[1]}%")
        
        validation["gc_content"] = round(gc_content, 2)
        validation["restriction_sites"] = restriction_sites_found
        validation["sequence_length"] = len(full_sequence)
        
        return validation
    
    @classmethod
    def _validate_mrna_compatibility(cls, builder: PlasmidBuilder, config: Dict) -> Dict[str, Any]:
        """Validate mRNA synthesis and stability requirements"""
        validation = {
            "passed": True,
            "issues": [],
            "warnings": []
        }
        
        mrna_requirements = config.get("validation_criteria", {}).get("mrna_requirements", {})
        
        # Check for T7 promoter (required for in vitro transcription)
        has_t7 = any(e.name == "T7 Promoter" for e in builder.elements)
        if not has_t7:
            validation["issues"].append("Missing T7 promoter for in vitro transcription")
            validation["passed"] = False
        
        # Check for start codon
        if mrna_requirements.get("has_start_codon", True):
            has_start = any("ATG" in e.sequence for e in builder.elements)
            if not has_start:
                validation["issues"].append("Missing start codon (ATG)")
                validation["passed"] = False
        
        # Check for stop codon
        if mrna_requirements.get("has_stop_codon", True):
            has_stop = any(stop in builder.get_full_sequence() for stop in ["TAA", "TAG", "TGA"])
            if not has_stop:
                validation["issues"].append("Missing stop codon")
                validation["passed"] = False
        
        # Check for polyadenylation signal
        if mrna_requirements.get("has_polya_signal", True):
            has_polya = any(e.element_type == ElementType.UTR for e in builder.elements)
            if not has_polya:
                validation["issues"].append("Missing polyadenylation signal")
                validation["passed"] = False
        
        # Check Kozak sequence for enhanced translation
        has_kozak = any("kozak" in e.name.lower() for e in builder.elements)
        if not has_kozak:
            validation["warnings"].append("Consider adding Kozak sequence for enhanced translation")
        
        # Get mRNA sequence (without plasmid maintenance elements)
        mrna_sequence = builder.get_mrna_sequence()
        validation["mrna_length"] = len(mrna_sequence)
        validation["has_t7_promoter"] = has_t7
        validation["has_kozak_sequence"] = has_kozak
        
        return validation
    
    @classmethod
    def _validate_expression_potential(cls, builder: PlasmidBuilder, config: Dict) -> Dict[str, Any]:
        """Validate potential for high expression levels"""
        validation = {
            "passed": True,
            "issues": [],
            "warnings": []
        }
        
        # Check for strong promoter
        promoter_elements = [e for e in builder.elements if e.element_type == ElementType.PROMOTER]
        if not promoter_elements:
            validation["issues"].append("No promoter found")
            validation["passed"] = False
        else:
            strong_promoters = ["CMV", "T7", "EF1A"]
            has_strong_promoter = any(any(sp in p.name for sp in strong_promoters) for p in promoter_elements)
            if not has_strong_promoter:
                validation["warnings"].append("Consider using a stronger promoter (CMV, T7, EF1A)")
        
        # Check codon optimization
        neoantigen_elements = [e for e in builder.elements if "neoantigen" in e.name.lower()]
        optimization_scores = []
        
        for element in neoantigen_elements:
            if "optimization score" in element.description:
                # Extract score from description
                import re
                match = re.search(r'optimization score: ([\d.]+)', element.description)
                if match:
                    score = float(match.group(1))
                    optimization_scores.append(score)
        
        if optimization_scores:
            avg_score = sum(optimization_scores) / len(optimization_scores)
            if avg_score < 0.7:
                validation["warnings"].append(f"Low codon optimization score: {avg_score:.3f}")
            validation["codon_optimization_score"] = round(avg_score, 3)
        
        # Check for expression tags
        tag_elements = [e for e in builder.elements if e.element_type == ElementType.TAG]
        if not tag_elements:
            validation["warnings"].append("No expression tags found for detection/purification")
        
        validation["promoter_count"] = len(promoter_elements)
        validation["tag_count"] = len(tag_elements)
        
        return validation
    
    @classmethod
    def _validate_safety(cls, builder: PlasmidBuilder, config: Dict) -> Dict[str, Any]:
        """Validate biosafety aspects of the design"""
        validation = {
            "passed": True,
            "issues": [],
            "warnings": []
        }
        
        # Check for antibiotic resistance markers
        resistance_elements = [e for e in builder.elements if e.element_type == ElementType.RESISTANCE]
        if resistance_elements:
            validation["warnings"].append("Contains antibiotic resistance genes - ensure proper containment")
        
        # Check for origin of replication
        origin_elements = [e for e in builder.elements if e.element_type == ElementType.ORIGIN]
        if not origin_elements:
            validation["warnings"].append("No origin of replication found - may affect plasmid maintenance")
        
        # Check sequence length for mRNA delivery
        mrna_sequence = builder.get_mrna_sequence()
        if len(mrna_sequence) > 4000:
            validation["warnings"].append("Long mRNA sequence may have reduced delivery efficiency")
        
        validation["resistance_markers"] = len(resistance_elements)
        validation["origin_count"] = len(origin_elements)
        validation["biosafety_level"] = "BSL-1"  # Default for vaccine vectors
        
        return validation
    
    @classmethod
    def _validate_optimization(cls, builder: PlasmidBuilder, config: Dict) -> Dict[str, Any]:
        """Validate optimization for manufacturing and efficacy"""
        validation = {
            "passed": True,
            "issues": [],
            "warnings": []
        }
        
        # Check for manufacturing considerations
        total_length = builder.total_length
        if total_length > 8000:
            validation["warnings"].append("Large plasmid may be challenging to manufacture at scale")
        
        # Check element organization
        promoter_positions = [e.position for e in builder.elements if e.element_type == ElementType.PROMOTER]
        gene_positions = [e.position for e in builder.elements if e.element_type == ElementType.GENE]
        
        if promoter_positions and gene_positions:
            # Check if promoter comes before gene (simplified check)
            if min(promoter_positions) > min(gene_positions):
                validation["warnings"].append("Promoter should typically precede the gene")
        
        # Calculate complexity score
        element_types = len(set(e.element_type for e in builder.elements))
        complexity_score = element_types / 7  # 7 possible element types
        
        validation["complexity_score"] = round(complexity_score, 3)
        validation["manufacturing_suitability"] = "High" if total_length < 6000 else "Medium" if total_length < 8000 else "Low"
        
        return validation
    
    @classmethod
    def _generate_recommendations(cls, validation_results: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on validation results"""
        recommendations = []
        
        # Basic structure recommendations
        if not validation_results["basic_validation"]["passed"]:
            recommendations.append("Address basic structural issues before proceeding")
        
        # mRNA compatibility recommendations
        mrna_val = validation_results["mrna_validation"]
        if not mrna_val["passed"]:
            recommendations.append("Fix mRNA compatibility issues for successful transcription")
        
        # Expression optimization recommendations
        expr_val = validation_results["expression_validation"]
        if "codon_optimization_score" in expr_val and expr_val["codon_optimization_score"] < 0.8:
            recommendations.append("Consider further codon optimization for higher expression")
        
        # Safety recommendations
        safety_val = validation_results["safety_validation"]
        if safety_val["resistance_markers"] > 0:
            recommendations.append("Follow biosafety protocols for antibiotic resistance genes")
        
        # Sequence recommendations
        seq_val = validation_results["sequence_validation"]
        if seq_val["restriction_sites"]:
            recommendations.append("Consider removing restriction sites if they interfere with cloning")
        
        if not recommendations:
            recommendations.append("Plasmid design meets all validation criteria - ready for experimental testing")
        
        return recommendations
    
    @classmethod
    def _get_default_config(cls) -> Dict[str, Any]:
        """Get default configuration if config file is not found"""
        return {
            "validation_criteria": {
                "min_total_length": 1000,
                "max_total_length": 10000,
                "required_elements": ["promoter", "gene"],
                "mrna_requirements": {
                    "has_start_codon": True,
                    "has_stop_codon": True,
                    "has_polya_signal": True
                }
            },
            "codon_optimization": {
                "gc_content_range": [40, 60]
            }
        }
    
    @classmethod
    def export_validation_report(cls, validation_results: Dict[str, Any], filename: str = "validation_report.json") -> None:
        """Export validation results to a file"""
        with open(filename, 'w') as f:
            json.dump(validation_results, f, indent=2)
        print(f"Validation report exported to {filename}")


def main():
    """Demonstration of plasmid validation"""
    from plasmid_builder import main as build_plasmid
    
    # Get a plasmid design
    builder, design = build_plasmid()
    
    print("Performing comprehensive validation...")
    print("=" * 50)
    
    # Run validation
    validation_results = PlasmidValidator.validate_comprehensive(builder)
    
    # Display results
    print(f"Overall Status: {validation_results['overall_status']}")
    print()
    
    for category, results in validation_results.items():
        if category in ["overall_status", "timestamp", "recommendations"]:
            continue
        
        print(f"{category.replace('_', ' ').title()}:")
        print(f"  Passed: {results.get('passed', 'N/A')}")
        
        if results.get("issues"):
            print("  Issues:")
            for issue in results["issues"]:
                print(f"    - {issue}")
        
        if results.get("warnings"):
            print("  Warnings:")
            for warning in results["warnings"]:
                print(f"    - {warning}")
        
        print()
    
    print("Recommendations:")
    for i, rec in enumerate(validation_results["recommendations"], 1):
        print(f"  {i}. {rec}")
    
    # Export report
    PlasmidValidator.export_validation_report(validation_results)


if __name__ == "__main__":
    main()