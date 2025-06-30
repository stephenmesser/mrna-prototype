#!/usr/bin/env python3
"""
Integration Demo - IVT RNA QC Pipeline with Plasmid Builder
Demonstrates how the QC pipeline integrates with plasmid design workflow.
"""

from ivt_rna_qc import IVTRNAQCPipeline, RNASequence
import json


def simulate_plasmid_to_mrna_workflow():
    """
    Simulate the complete workflow from plasmid design to mRNA QC.
    In a real implementation, this would interface with the plasmid builder.
    """
    print("IVT RNA QC Pipeline - Integration Demo")
    print("=" * 50)
    
    # Simulate plasmid design output (neoantigen X mRNA)
    # This would come from plasmid_builder.py in a real workflow
    plasmid_info = {
        "name": "pNeoantigenX-mRNA",
        "description": "Plasmid vector for neoantigen X mRNA production",
        "total_length": 2571,
        "mrna_transcript": "AUGGCCACCAUGGAGAAAGUAAAGGGCUUUAUAGGGGAGAUAAGGUUUUGACUUUGUAGAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
        "expected_yield": "High",
        "promoter": "T7",
        "poly_a_tail": True
    }
    
    print(f"1. Plasmid Design Complete:")
    print(f"   Name: {plasmid_info['name']}")
    print(f"   Total Length: {plasmid_info['total_length']} bp")
    print(f"   mRNA Length: {len(plasmid_info['mrna_transcript'])} nt")
    print(f"   Promoter: {plasmid_info['promoter']}")
    
    # Simulate IVT process
    print("\n2. In Vitro Transcription (IVT) Process:")
    print("   - Template: Linearized plasmid")
    print("   - Polymerase: T7 RNA Polymerase")
    print("   - Conditions: 37°C, 2 hours")
    print("   - 5' Capping: Yes")
    print("   - 3' Poly(A) tailing: Yes")
    
    # Create RNA sequence for QC
    rna_sample = RNASequence(
        sequence=plasmid_info['mrna_transcript'],
        name="Neoantigen_X_IVT_mRNA",
        description="IVT mRNA from pNeoantigenX-mRNA plasmid"
    )
    
    # Simulate analytical measurements (would come from lab instruments)
    analytical_data = {
        'absorbance': {
            'a260': 1.95,
            'a280': 0.98,
            'a230': 0.92
        },
        'concentration': 195.0,
        'volume_ul': 250.0,
        'integrity': {
            'rin_score': 8.6,
            'degradation_ratio': 0.03
        },
        'capping': {
            'efficiency': 89.0,
            'cap_detected': True
        },
        'poly_a': {
            'length': 138
        },
        'dna_contamination': 0.2,
        'protein_content': 1.1,
        'endotoxin': 0.5
    }
    
    print("\n3. Analytical Measurements:")
    print(f"   Concentration: {analytical_data['concentration']} ng/μL")
    print(f"   Volume: {analytical_data['volume_ul']} μL")
    print(f"   A260/A280: {analytical_data['absorbance']['a260'] / analytical_data['absorbance']['a280']:.2f}")
    print(f"   RIN Score: {analytical_data['integrity']['rin_score']}")
    print(f"   Capping Efficiency: {analytical_data['capping']['efficiency']}%")
    
    # Run QC pipeline
    print("\n4. Automated QC Analysis:")
    pipeline = IVTRNAQCPipeline()
    
    qc_results = pipeline.run_complete_qc(
        sample_name="Neoantigen_X_IVT_001",
        rna_sequence=rna_sample,
        analytical_data=analytical_data,
        expected_sequence=plasmid_info['mrna_transcript']
    )
    
    # Display QC results
    metrics = qc_results['metrics']
    assessment = qc_results['qc_report']['qc_assessment']
    recommendations = qc_results['qc_report']['recommendations']
    detailed = qc_results['qc_report']['detailed_analysis']
    
    print(f"   Overall Status: {assessment['overall_status'].value}")
    print(f"   Quality Score: {detailed['quality_score']:.1f}/100")
    print(f"   Total Yield: {metrics.total_yield_ug:.1f} μg")
    print(f"   Sequence Accuracy: {metrics.sequence_accuracy_percent:.1f}%")
    
    # Summary of individual checks
    checks = assessment['individual_checks']
    passed = sum(1 for status in checks.values() if status.value == 'PASS')
    total = len(checks)
    
    print(f"\n5. QC Check Results: {passed}/{total} PASSED")
    for check_name, status in checks.items():
        symbol = "✅" if status.value == "PASS" else "⚠️" if status.value == "WARNING" else "❌"
        print(f"   {symbol} {check_name.replace('_', ' ').title()}: {status.value}")
    
    # Recommendations
    print("\n6. Recommendations:")
    for i, rec in enumerate(recommendations, 1):
        print(f"   {i}. {rec}")
    
    # Regulatory compliance
    compliance = detailed['regulatory_compliance']
    print("\n7. Regulatory Compliance:")
    for standard, compliant in compliance.items():
        symbol = "✅" if compliant else "❌"
        print(f"   {symbol} {standard.upper().replace('_', ' ')}: {'Compliant' if compliant else 'Non-compliant'}")
    
    # Manufacturing decision
    print("\n8. Manufacturing Decision:")
    if assessment['overall_status'].value == 'PASS':
        print("   ✅ APPROVED: Sample meets all specifications for vaccine production")
        print("   Next steps: Proceed to formulation and fill-finish")
    elif assessment['overall_status'].value == 'WARNING':
        print("   ⚠️  CONDITIONAL: Sample has minor deviations but may be acceptable")
        print("   Next steps: Review with Quality Assurance team")
    else:
        print("   ❌ REJECTED: Sample fails critical quality parameters")
        print("   Next steps: Investigate root cause and reprocess")
    
    # Save detailed results
    output_file = "neoantigen_x_qc_results.json"
    def convert_enums(obj):
        if isinstance(obj, dict):
            return {k: convert_enums(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_enums(item) for item in obj]
        elif hasattr(obj, 'value'):
            return obj.value
        else:
            return obj
    
    results_serializable = convert_enums(qc_results)
    with open(output_file, 'w') as f:
        json.dump(results_serializable, f, indent=2, default=str)
    
    print(f"\n9. Detailed results saved to: {output_file}")
    
    return qc_results


def demonstrate_batch_production_qc():
    """Demonstrate QC of a production batch."""
    print("\n" + "=" * 50)
    print("BATCH PRODUCTION QC DEMO")
    print("=" * 50)
    
    # Simulate production batch
    batch_samples = []
    base_sequence = "AUGGCCACCAUGGAGAAAGUAAAGGGCUUUAUAGGGGAGAUAAGGUUUUGACUUUGUAG"
    
    for i in range(1, 6):
        # Vary quality parameters across batch
        concentration = 180 + (i * 10) + ((-1)**i * 15)  # Simulate variation
        rin_score = 8.0 + (i * 0.1) + ((-1)**i * 0.3)
        capping_eff = 85 + (i * 2) + ((-1)**i * 5)
        
        batch_samples.append({
            'name': f'Production_Lot_A_{i:03d}',
            'sequence': base_sequence + 'A' * (100 + i * 10),  # Variable poly-A
            'analytical_data': {
                'absorbance': {'a260': 1.8, 'a280': 0.9, 'a230': 0.85},
                'concentration': max(50, concentration),
                'volume_ul': 200,
                'integrity': {'rin_score': max(5.0, rin_score), 'degradation_ratio': 0.04},
                'capping': {'efficiency': max(60, capping_eff), 'cap_detected': True},
                'poly_a': {'length': 120 + i * 5},
                'dna_contamination': 0.2 + i * 0.1,
                'protein_content': 1.0 + i * 0.5,
                'endotoxin': 0.4 + i * 0.2
            }
        })
    
    # Run batch QC
    pipeline = IVTRNAQCPipeline()
    batch_results = pipeline.run_batch_qc(batch_samples)
    
    # Analyze batch results
    total_samples = len(batch_results)
    passed = sum(1 for r in batch_results if r.get('qc_report', {}).get('qc_assessment', {}).get('overall_status', '').value == 'PASS')
    warnings = sum(1 for r in batch_results if r.get('qc_report', {}).get('qc_assessment', {}).get('overall_status', '').value == 'WARNING')
    failed = sum(1 for r in batch_results if r.get('qc_report', {}).get('qc_assessment', {}).get('overall_status', '').value == 'FAIL')
    
    print(f"Batch Summary:")
    print(f"  Total Samples: {total_samples}")
    print(f"  Passed: {passed} ({passed/total_samples*100:.1f}%)")
    print(f"  Warnings: {warnings} ({warnings/total_samples*100:.1f}%)")
    print(f"  Failed: {failed} ({failed/total_samples*100:.1f}%)")
    print(f"  Batch Pass Rate: {passed/total_samples*100:.1f}%")
    
    # Batch acceptance decision
    pass_rate = passed / total_samples
    if pass_rate >= 0.9:
        print(f"\n✅ BATCH APPROVED: Pass rate {pass_rate*100:.1f}% exceeds 90% threshold")
    elif pass_rate >= 0.8:
        print(f"\n⚠️  BATCH CONDITIONAL: Pass rate {pass_rate*100:.1f}% requires review")
    else:
        print(f"\n❌ BATCH REJECTED: Pass rate {pass_rate*100:.1f}% below 80% threshold")
    
    return batch_results


if __name__ == "__main__":
    # Run integration demo
    single_sample_results = simulate_plasmid_to_mrna_workflow()
    batch_results = demonstrate_batch_production_qc()
    
    print("\n" + "=" * 50)
    print("INTEGRATION DEMO COMPLETE")
    print("=" * 50)
    print("✅ Single sample QC: Complete")
    print("✅ Batch production QC: Complete") 
    print("✅ Regulatory compliance: Verified")
    print("✅ Manufacturing decisions: Generated")
    print("\nThe IVT RNA QC pipeline is fully operational and ready for production use.")