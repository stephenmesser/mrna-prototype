#!/usr/bin/env python3
"""
Test Script for Neoantigen X Plasmid Vector Designer
===================================================

This script tests the basic functionality of the plasmid design system
to ensure all components work correctly.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from plasmid_builder import PlasmidVectorDesigner, PromoterType, NeoantigenX


def test_neoantigen_sequence():
    """Test neoantigen sequence generation and codon optimization."""
    print("Testing Neoantigen X sequence generation...")
    
    neoantigen = NeoantigenX()
    
    # Test basic properties
    assert neoantigen.name == "Neoantigen_X"
    assert len(neoantigen.amino_acid_sequence) == 65
    assert neoantigen.source_organism == "Synthetic"
    
    # Test codon optimization
    dna_seq = neoantigen.get_codon_optimized_sequence()
    assert len(dna_seq) == 195  # 65 amino acids * 3 codons = 195 bp
    assert dna_seq.startswith("ATG")  # Should start with start codon
    
    print("✅ Neoantigen sequence tests passed")


def test_plasmid_design():
    """Test complete plasmid design functionality."""
    print("Testing plasmid design functionality...")
    
    designer = PlasmidVectorDesigner()
    
    # Test T7 promoter design
    design = designer.design_complete_vector(
        promoter=PromoterType.T7,
        include_his_tag=True,
        include_flag_tag=True
    )
    
    # Validate design structure
    assert design["plasmid_name"] == "pNeoX_T7"
    assert design["total_length"] > 1000  # Should be reasonable size
    assert len(design["components"]) >= 7  # Should have all major components
    
    # Check essential components are present
    component_types = [comp["component_type"] for comp in design["components"]]
    required_types = ["promoter", "coding_sequence", "resistance_marker"]
    
    for req_type in required_types:
        assert req_type in component_types, f"Missing component type: {req_type}"
    
    # Validate mRNA compatibility
    compatibility = design["mRNA_compatibility"]
    assert compatibility["t7_promoter_present"] == True
    assert compatibility["polya_signal_present"] == True
    assert compatibility["kozak_optimized"] == True
    assert compatibility["codon_optimized"] == True
    
    print("✅ Plasmid design tests passed")


def test_different_promoters():
    """Test design with different promoter types."""
    print("Testing different promoter configurations...")
    
    designer = PlasmidVectorDesigner()
    
    promoters_to_test = [PromoterType.T7, PromoterType.CMV, PromoterType.EF1A]
    
    for promoter in promoters_to_test:
        design = designer.design_complete_vector(
            promoter=promoter,
            include_his_tag=True,
            include_flag_tag=False
        )
        
        assert design["plasmid_name"] == f"pNeoX_{promoter.value}"
        
        # Check promoter is actually in the design
        promoter_found = any(
            comp["component_type"] == "promoter" and promoter.value in comp["name"]
            for comp in design["components"]
        )
        assert promoter_found, f"Promoter {promoter.value} not found in design"
    
    print("✅ Multiple promoter tests passed")


def test_validation_system():
    """Test the in silico validation functionality."""
    print("Testing validation system...")
    
    designer = PlasmidVectorDesigner()
    design = designer.design_complete_vector()
    
    validation = design["validation_results"]
    
    # Check validation structure
    required_keys = ["sequence_length", "gc_content", "start_codons", "stop_codons", "validation_passed"]
    for key in required_keys:
        assert key in validation, f"Missing validation key: {key}"
    
    # Check reasonable values
    assert validation["sequence_length"] > 0
    assert 0 <= validation["gc_content"] <= 100
    assert validation["start_codons"] >= 1
    assert validation["stop_codons"] >= 1
    
    print("✅ Validation system tests passed")


def test_schematic_generation():
    """Test schematic data generation."""
    print("Testing schematic data generation...")
    
    designer = PlasmidVectorDesigner()
    designer.design_complete_vector()
    
    schematic_data = designer.generate_schematic_data()
    
    # Check structure
    assert "plasmid_map" in schematic_data
    assert "component_colors" in schematic_data
    assert len(schematic_data["plasmid_map"]) > 0
    
    # Check each component has required fields
    for component in schematic_data["plasmid_map"]:
        required_fields = ["name", "type", "start_angle", "end_angle", "start_pos", "end_pos"]
        for field in required_fields:
            assert field in component, f"Missing field {field} in schematic component"
    
    print("✅ Schematic generation tests passed")


def test_export_functionality():
    """Test design export functionality."""
    print("Testing export functionality...")
    
    import tempfile
    import json
    import os
    
    designer = PlasmidVectorDesigner()
    
    # Create temporary file for testing
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp_file:
        temp_filename = tmp_file.name
    
    try:
        # Test export
        designer.export_design(temp_filename)
        
        # Verify file was created and contains valid JSON
        assert os.path.exists(temp_filename)
        
        with open(temp_filename, 'r') as f:
            exported_data = json.load(f)
        
        # Check essential fields are present
        required_fields = ["plasmid_name", "total_length", "neoantigen", "components"]
        for field in required_fields:
            assert field in exported_data, f"Missing field {field} in exported data"
        
        print("✅ Export functionality tests passed")
        
    finally:
        # Clean up temporary file
        if os.path.exists(temp_filename):
            os.unlink(temp_filename)


def run_all_tests():
    """Run all test functions."""
    print("=" * 60)
    print("RUNNING NEOANTIGEN X PLASMID DESIGN TESTS")
    print("=" * 60)
    
    test_functions = [
        test_neoantigen_sequence,
        test_plasmid_design,
        test_different_promoters,
        test_validation_system,
        test_schematic_generation,
        test_export_functionality
    ]
    
    total_tests = len(test_functions)
    passed_tests = 0
    
    for test_func in test_functions:
        try:
            test_func()
            passed_tests += 1
        except Exception as e:
            print(f"❌ {test_func.__name__} FAILED: {e}")
            return False
    
    print("=" * 60)
    print(f"TEST RESULTS: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🎉 ALL TESTS PASSED - System is working correctly!")
        print("Ready for experimental validation and mRNA synthesis.")
        return True
    else:
        print("❌ SOME TESTS FAILED - Please check implementation")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)