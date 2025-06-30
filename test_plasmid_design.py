#!/usr/bin/env python3
"""
Test suite for the plasmid design system.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from plasmid_builder import PlasmidDesigner, NeoantiogenX


def test_neoantigen_creation():
    """Test neoantigen X creation and optimization."""
    print("Testing neoantigen creation...")
    
    neoantigen = NeoantiogenX()
    
    # Test basic properties
    assert neoantigen.raw_peptide == "KTVNMRLGL", "Incorrect raw peptide sequence"
    assert len(neoantigen.extended_sequence) > len(neoantigen.raw_peptide), "Extended sequence should be longer"
    
    # Test codon optimization
    optimized_dna = neoantigen.optimize_codons()
    assert len(optimized_dna) % 3 == 0, "Optimized DNA should be divisible by 3"
    assert len(optimized_dna) == len(neoantigen.extended_sequence) * 3, "DNA length should be 3x protein length"
    
    print("✅ Neoantigen tests passed")


def test_plasmid_design():
    """Test complete plasmid design."""
    print("Testing plasmid design...")
    
    designer = PlasmidDesigner()
    design_summary = designer.design_vector()
    
    # Test design summary structure
    required_keys = ["plasmid_name", "total_length", "neoantigen_sequence", "components"]
    for key in required_keys:
        assert key in design_summary, f"Missing key: {key}"
    
    # Test components
    assert len(designer.components) == 8, "Should have 8 components"
    
    # Test essential component types
    component_types = [comp.feature_type for comp in designer.components]
    essential_types = ["promoter", "CDS", "terminator", "selection", "origin"]
    for comp_type in essential_types:
        assert comp_type in component_types, f"Missing essential component: {comp_type}"
    
    # Test sequence integrity
    total_length = sum(len(comp.sequence) for comp in designer.components)
    assert total_length == designer.total_length, "Total length mismatch"
    
    print("✅ Plasmid design tests passed")


def test_validation():
    """Test design validation."""
    print("Testing design validation...")
    
    designer = PlasmidDesigner()
    designer.design_vector()
    
    validation_results = designer.validate_design()
    
    # All essential validations should pass
    essential_validations = [
        "has_promoter", "has_CDS", "has_terminator", 
        "has_selection", "has_origin", "sequence_integrity"
    ]
    
    for validation in essential_validations:
        assert validation_results.get(validation, False), f"Validation failed: {validation}"
    
    print("✅ Validation tests passed")


def test_export_functionality():
    """Test sequence export functionality."""
    print("Testing export functionality...")
    
    designer = PlasmidDesigner()
    designer.design_vector()
    
    sequences = designer.export_sequences()
    
    # Test that key sequences are exported
    assert "complete_plasmid" in sequences, "Complete plasmid sequence missing"
    assert "expression_cassette" in sequences, "Expression cassette missing"
    assert "Neoantigen_X" in sequences, "Neoantigen sequence missing"
    
    # Test sequence integrity
    complete_seq = sequences["complete_plasmid"]
    assert len(complete_seq) == designer.total_length, "Complete sequence length mismatch"
    
    print("✅ Export tests passed")


def test_plasmid_map_generation():
    """Test plasmid map generation."""
    print("Testing plasmid map generation...")
    
    designer = PlasmidDesigner()
    designer.design_vector()
    
    plasmid_map = designer.generate_plasmid_map()
    
    # Test that map contains essential information
    assert "pNeoantigenX-mRNA" in plasmid_map, "Plasmid name missing from map"
    assert "Total Length:" in plasmid_map, "Total length missing from map"
    assert "CMV_Promoter" in plasmid_map, "CMV promoter missing from map"
    assert "Neoantigen_X" in plasmid_map, "Neoantigen missing from map"
    
    print("✅ Plasmid map tests passed")


def run_all_tests():
    """Run all tests."""
    print("Starting plasmid design system tests...\n")
    
    tests = [
        test_neoantigen_creation,
        test_plasmid_design,
        test_validation,
        test_export_functionality,
        test_plasmid_map_generation
    ]
    
    for test in tests:
        try:
            test()
        except Exception as e:
            print(f"❌ Test failed: {test.__name__}")
            print(f"Error: {e}")
            return False
    
    print("\n🎉 All tests passed! Plasmid design system is working correctly.")
    return True


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)