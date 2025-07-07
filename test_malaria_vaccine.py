#!/usr/bin/env python3
"""
Test suite for malaria vaccine design system.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from malaria_vaccine_builder import MalariaVaccineDesigner, MalariaAntigen


def test_malaria_antigen():
    """Test malaria antigen creation."""
    print("Testing malaria antigen creation...")
    
    antigen = MalariaAntigen("NANPNANPNANP")
    assert antigen.epitope_sequence == "NANPNANPNANP"
    assert antigen.pathogen == "Plasmodium falciparum"
    assert "CSP" in antigen.protein_source
    
    extended_seq = antigen.get_extended_sequence()
    assert "NANPNANPNANP" in extended_seq
    assert len(extended_seq) > len("NANPNANPNANP")
    
    dna_seq = antigen.get_codon_optimized_sequence()
    assert len(dna_seq) > 0
    assert len(dna_seq) % 3 == 0  # Should be divisible by 3
    
    print("✅ Malaria antigen tests passed")


def test_malaria_vaccine_design():
    """Test malaria vaccine design."""
    print("Testing malaria vaccine design...")
    
    designer = MalariaVaccineDesigner("NANPNANPNANP")
    design_summary = designer.design_malaria_vector()
    
    # Test design summary structure
    required_keys = ["plasmid_name", "total_length", "target_antigen", "pathogen"]
    for key in required_keys:
        assert key in design_summary, f"Missing key: {key}"
    
    # Test components
    assert len(designer.components) >= 6, "Should have at least 6 components"
    
    # Test malaria-specific components
    component_names = [comp.name for comp in designer.components]
    assert "CSP_Epitope" in component_names, "Missing CSP epitope component"
    
    print("✅ Malaria vaccine design tests passed")


def test_malaria_vaccine_validation():
    """Test malaria vaccine validation."""
    print("Testing malaria vaccine validation...")
    
    designer = MalariaVaccineDesigner("NANPNANPNANP")
    designer.design_malaria_vector()
    
    validation = designer.validate_design()
    
    # Test essential validations
    essential_checks = ["has_promoter", "has_CDS", "has_terminator", "sequence_integrity"]
    for check in essential_checks:
        assert validation.get(check, False), f"Failed validation: {check}"
    
    print("✅ Malaria vaccine validation tests passed")


def test_malaria_vaccine_map():
    """Test malaria vaccine map generation."""
    print("Testing malaria vaccine map generation...")
    
    designer = MalariaVaccineDesigner("NANPNANPNANP")
    designer.design_malaria_vector()
    
    vaccine_map = designer.generate_malaria_vaccine_map()
    
    # Test map contents
    assert "MALARIA VACCINE PLASMID MAP" in vaccine_map
    assert "Plasmodium falciparum" in vaccine_map
    assert "NANPNANPNANP" in vaccine_map
    assert "CSP_Epitope" in vaccine_map
    
    print("✅ Malaria vaccine map tests passed")


def run_all_tests():
    """Run all malaria vaccine tests."""
    print("Starting malaria vaccine tests...\n")
    
    try:
        test_malaria_antigen()
        test_malaria_vaccine_design()
        test_malaria_vaccine_validation()
        test_malaria_vaccine_map()
        
        print("\n🎉 All malaria vaccine tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)