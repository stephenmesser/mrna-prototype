#!/usr/bin/env python3
"""
IVT RNA QC Pipeline CLI
Command-line interface for automated IVT RNA quality control.
"""

import argparse
import json
import sys
import os
from pathlib import Path
from typing import Dict, Any, List

from ivt_rna_qc import IVTRNAQCPipeline, RNASequence, QCStatus


def load_sample_data(file_path: str) -> Dict[str, Any]:
    """Load sample data from JSON file."""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Sample data file '{file_path}' not found")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in file '{file_path}': {e}")
        sys.exit(1)


def save_results(results: Dict[str, Any], output_file: str) -> None:
    """Save QC results to JSON file."""
    # Convert enum values to strings for JSON serialization
    def convert_enums(obj):
        if isinstance(obj, dict):
            return {k: convert_enums(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_enums(item) for item in obj]
        elif hasattr(obj, 'value'):  # Enum object
            return obj.value
        else:
            return obj
    
    results_serializable = convert_enums(results)
    
    try:
        with open(output_file, 'w') as f:
            json.dump(results_serializable, f, indent=2, default=str)
        print(f"Results saved to: {output_file}")
    except Exception as e:
        print(f"Error saving results: {e}")
        sys.exit(1)


def create_sample_template(output_file: str) -> None:
    """Create a sample template file for user input."""
    template = {
        "name": "Sample_001",
        "description": "IVT mRNA sample for QC analysis",
        "sequence": "AUGGCCACCAUGGAGAAAGUAAAGGGCUUUAUAGGGGAGAUAAGGUUUUGACUUUGUAG",
        "expected_sequence": "AUGGCCACCAUGGAGAAAGUAAAGGGCUUUAUAGGGGAGAUAAGGUUUUGACUUUGUAG",
        "analytical_data": {
            "absorbance": {
                "a260": 1.8,
                "a280": 0.9,
                "a230": 0.8
            },
            "concentration": 185.0,
            "volume_ul": 200.0,
            "integrity": {
                "rin_score": 8.2,
                "degradation_ratio": 0.04
            },
            "capping": {
                "efficiency": 87.5,
                "cap_detected": True
            },
            "poly_a": {
                "length": 125
            },
            "dna_contamination": 0.3,
            "protein_content": 1.8,
            "endotoxin": 0.8
        }
    }
    
    try:
        with open(output_file, 'w') as f:
            json.dump(template, f, indent=2)
        print(f"Sample template created: {output_file}")
        print("Edit this file with your sample data and run QC analysis")
    except Exception as e:
        print(f"Error creating template: {e}")
        sys.exit(1)


def create_batch_template(output_file: str) -> None:
    """Create a batch template file for multiple samples."""
    batch_template = {
        "samples": [
            {
                "name": "Sample_001",
                "description": "First IVT mRNA sample",
                "sequence": "AUGGCCACCAUGGAGAAAGUAAAGGGCUUUAUAGGGGAGAUAAGGUUUUGACUUUGUAG",
                "expected_sequence": "AUGGCCACCAUGGAGAAAGUAAAGGGCUUUAUAGGGGAGAUAAGGUUUUGACUUUGUAG",
                "analytical_data": {
                    "absorbance": {"a260": 1.8, "a280": 0.9, "a230": 0.8},
                    "concentration": 185.0,
                    "volume_ul": 200.0,
                    "integrity": {"rin_score": 8.2, "degradation_ratio": 0.04},
                    "capping": {"efficiency": 87.5, "cap_detected": True},
                    "poly_a": {"length": 125},
                    "dna_contamination": 0.3,
                    "protein_content": 1.8,
                    "endotoxin": 0.8
                }
            },
            {
                "name": "Sample_002", 
                "description": "Second IVT mRNA sample",
                "sequence": "AUGGCCACCAUGGAGAAAGUAAAGGGCUUUAUAGGGGAGAUAAGGUUUUGACUUUGUAG",
                "analytical_data": {
                    "absorbance": {"a260": 1.6, "a280": 0.8, "a230": 0.7},
                    "concentration": 165.0,
                    "volume_ul": 150.0,
                    "integrity": {"rin_score": 7.8, "degradation_ratio": 0.06},
                    "capping": {"efficiency": 82.0, "cap_detected": True},
                    "poly_a": {"length": 110},
                    "dna_contamination": 0.5,
                    "protein_content": 2.2,
                    "endotoxin": 1.2
                }
            }
        ]
    }
    
    try:
        with open(output_file, 'w') as f:
            json.dump(batch_template, f, indent=2)
        print(f"Batch template created: {output_file}")
        print("Edit this file with your sample data and run batch QC analysis")
    except Exception as e:
        print(f"Error creating batch template: {e}")
        sys.exit(1)


def print_summary_report(results: List[Dict[str, Any]]) -> None:
    """Print a summary report of QC results."""
    print("\n" + "="*60)
    print("IVT RNA QC PIPELINE SUMMARY REPORT")
    print("="*60)
    
    total_samples = len(results)
    passed_samples = 0
    failed_samples = 0
    warning_samples = 0
    
    for result in results:
        if 'error' in result:
            failed_samples += 1
            continue
            
        status = result.get('qc_report', {}).get('qc_assessment', {}).get('overall_status')
        if hasattr(status, 'value'):
            status_value = status.value
        else:
            status_value = str(status)
            
        if status_value == 'PASS':
            passed_samples += 1
        elif status_value == 'FAIL':
            failed_samples += 1
        elif status_value == 'WARNING':
            warning_samples += 1
    
    print(f"Total Samples Analyzed: {total_samples}")
    print(f"Passed: {passed_samples}")
    print(f"Warnings: {warning_samples}")
    print(f"Failed: {failed_samples}")
    print(f"Success Rate: {(passed_samples/total_samples)*100:.1f}%")
    
    print("\nDETAILED RESULTS:")
    print("-"*60)
    
    for result in results:
        sample_name = result.get('sample_name', 'Unknown')
        
        if 'error' in result:
            print(f"{sample_name:20} | ERROR: {result['error']}")
            continue
            
        status = result.get('qc_report', {}).get('qc_assessment', {}).get('overall_status')
        status_value = status.value if hasattr(status, 'value') else str(status)
        
        metrics = result.get('metrics')
        if metrics:
            quality_score = result.get('qc_report', {}).get('detailed_analysis', {}).get('quality_score', 0)
            concentration = getattr(metrics, 'concentration_ng_ul', 0)
            rin_score = getattr(metrics, 'rin_score', 0)
            
            print(f"{sample_name:20} | {status_value:8} | Quality: {quality_score:5.1f} | "
                  f"Conc: {concentration:6.1f} ng/μL | RIN: {rin_score:4.1f}")
        else:
            print(f"{sample_name:20} | {status_value:8} | No metrics available")


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="IVT RNA Quality Control Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze single sample
  python qc_cli.py --input sample.json --output results.json
  
  # Analyze batch of samples  
  python qc_cli.py --batch samples.json --output batch_results.json
  
  # Create sample template
  python qc_cli.py --create-template sample_template.json
  
  # Create batch template
  python qc_cli.py --create-batch-template batch_template.json
  
  # Run with verbose output
  python qc_cli.py --input sample.json --verbose
        """
    )
    
    # Input options
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('--input', '-i', 
                           help='Input JSON file with sample data')
    input_group.add_argument('--batch', '-b',
                           help='Input JSON file with batch sample data')
    input_group.add_argument('--create-template', '-t',
                           help='Create sample template file')
    input_group.add_argument('--create-batch-template', '-bt',
                           help='Create batch template file')
    
    # Output options
    parser.add_argument('--output', '-o',
                       help='Output JSON file for results (default: auto-generated)')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Verbose output')
    parser.add_argument('--summary-only', '-s', action='store_true',
                       help='Show only summary report (no detailed output)')
    
    args = parser.parse_args()
    
    # Handle template creation
    if args.create_template:
        create_sample_template(args.create_template)
        return
        
    if args.create_batch_template:
        create_batch_template(args.create_batch_template)
        return
    
    # Initialize pipeline
    pipeline = IVTRNAQCPipeline()
    
    # Process single sample
    if args.input:
        sample_data = load_sample_data(args.input)
        
        try:
            rna_seq = RNASequence(
                sequence=sample_data['sequence'],
                name=sample_data['name'],
                description=sample_data.get('description', '')
            )
            
            results = pipeline.run_complete_qc(
                sample_name=sample_data['name'],
                rna_sequence=rna_seq,
                analytical_data=sample_data.get('analytical_data', {}),
                expected_sequence=sample_data.get('expected_sequence')
            )
            
            # Generate output filename if not provided
            if not args.output:
                base_name = Path(args.input).stem
                args.output = f"{base_name}_qc_results.json"
            
            # Save results
            save_results(results, args.output)
            
            # Print summary
            if not args.summary_only:
                print_summary_report([results])
                
        except Exception as e:
            print(f"Error processing sample: {e}")
            sys.exit(1)
    
    # Process batch
    elif args.batch:
        batch_data = load_sample_data(args.batch)
        samples = batch_data.get('samples', [])
        
        if not samples:
            print("Error: No samples found in batch file")
            sys.exit(1)
        
        try:
            results = pipeline.run_batch_qc(samples)
            
            # Generate output filename if not provided
            if not args.output:
                base_name = Path(args.batch).stem
                args.output = f"{base_name}_batch_qc_results.json"
            
            # Save results
            batch_results = {
                'batch_info': {
                    'total_samples': len(samples),
                    'analysis_timestamp': results[0].get('analysis_timestamp') if results else None,
                    'pipeline_version': results[0].get('pipeline_version') if results else None
                },
                'results': results
            }
            save_results(batch_results, args.output)
            
            # Print summary
            if not args.summary_only:
                print_summary_report(results)
                
        except Exception as e:
            print(f"Error processing batch: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()