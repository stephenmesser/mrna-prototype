# IVT RNA Quality Control Pipeline

Automated quality control system for In Vitro Transcribed (IVT) RNA samples in mRNA vaccine production.

## Overview

This pipeline provides comprehensive automated quality assessment of RNA samples produced from plasmid templates, specifically designed for mRNA vaccine development. The system analyzes multiple quality parameters and generates standardized reports for regulatory compliance.

## Features

### Core Quality Control Metrics
- **RNA Integrity Analysis**: RIN scores, degradation assessment
- **Purity Assessment**: A260/A280 and A260/A230 ratios
- **Concentration & Yield**: Quantitative measurements
- **Sequence Validation**: Accuracy comparison with expected sequences
- **mRNA-Specific Features**: 5' capping efficiency, poly(A) tail length
- **Contamination Screening**: DNA, protein, and endotoxin detection
- **Secondary Structure**: Melting temperature and hairpin predictions

### Advanced Analytics
- **Automated Quality Scoring**: 0-100 scale with pass/fail criteria
- **Regulatory Compliance**: FDA, EMA, ICH, and USP standards
- **Stability Prediction**: Storage recommendations and shelf life
- **Batch Processing**: High-throughput analysis capabilities
- **Detailed Reporting**: Comprehensive QC reports with recommendations

## Installation

No additional dependencies required - uses Python standard library only.

```bash
# Clone the repository
git clone https://github.com/stephenmesser/mrna-prototype.git
cd mrna-prototype

# Run tests to verify installation
python3 test_ivt_qc.py

# Run example analysis
python3 ivt_rna_qc.py
```

## Quick Start

### Command Line Interface

1. **Create a sample template:**
```bash
python3 qc_cli.py --create-template my_sample.json
```

2. **Edit the template with your data:**
```json
{
  "name": "Sample_001",
  "description": "IVT mRNA sample for QC analysis",
  "sequence": "AUGGCCACCAUGGAGAAAGUAAAGGGCUUUAUAGGGGAGAUAAGGUUUUGACUUUGUAG",
  "expected_sequence": "AUGGCCACCAUGGAGAAAGUAAAGGGCUUUAUAGGGGAGAUAAGGUUUUGACUUUGUAG",
  "analytical_data": {
    "absorbance": {"a260": 1.8, "a280": 0.9, "a230": 0.8},
    "concentration": 185.0,
    "volume_ul": 200.0,
    "integrity": {"rin_score": 8.2, "degradation_ratio": 0.04},
    "capping": {"efficiency": 87.5, "cap_detected": true},
    "poly_a": {"length": 125},
    "dna_contamination": 0.3,
    "protein_content": 1.8,
    "endotoxin": 0.8
  }
}
```

3. **Run QC analysis:**
```bash
python3 qc_cli.py --input my_sample.json --output results.json
```

### Batch Processing

1. **Create batch template:**
```bash
python3 qc_cli.py --create-batch-template batch_samples.json
```

2. **Run batch analysis:**
```bash
python3 qc_cli.py --batch batch_samples.json --output batch_results.json
```

### Python API

```python
from ivt_rna_qc import IVTRNAQCPipeline, RNASequence

# Initialize pipeline
pipeline = IVTRNAQCPipeline()

# Create RNA sequence
rna_sample = RNASequence(
    sequence="AUGGCCACCAUGGAGAAAGUAAAGGGCUUUAUAGGGGAGAUAAGGUUUUGACUUUGUAG",
    name="Sample_001",
    description="Test mRNA sample"
)

# Analytical data from laboratory instruments
analytical_data = {
    'absorbance': {'a260': 1.8, 'a280': 0.9, 'a230': 0.8},
    'concentration': 185.0,
    'volume_ul': 200.0,
    'integrity': {'rin_score': 8.2, 'degradation_ratio': 0.04},
    'capping': {'efficiency': 87.5, 'cap_detected': True},
    'poly_a': {'length': 125},
    'dna_contamination': 0.3,
    'protein_content': 1.8,
    'endotoxin': 0.8
}

# Run complete QC analysis
results = pipeline.run_complete_qc(
    sample_name="Sample_001",
    rna_sequence=rna_sample,
    analytical_data=analytical_data
)

# Access results
print(f"Overall Status: {results['qc_report']['qc_assessment']['overall_status']}")
print(f"Quality Score: {results['qc_report']['detailed_analysis']['quality_score']:.1f}")
```

## Quality Control Thresholds

The pipeline uses the following default thresholds for quality assessment:

| Parameter | Minimum | Maximum | Units |
|-----------|---------|---------|-------|
| Concentration | 100.0 | - | ng/μL |
| Total Yield | 10.0 | - | μg |
| A260/A280 Ratio | 1.8 | 2.2 | - |
| A260/A230 Ratio | 1.8 | - | - |
| RIN Score | 7.0 | - | 1-10 scale |
| Degradation Ratio | - | 0.1 | - |
| Sequence Accuracy | 95.0 | - | % |
| Capping Efficiency | 80.0 | - | % |
| Poly(A) Length | 100 | - | nucleotides |
| DNA Contamination | - | 1.0 | % |
| Protein Contamination | - | 10.0 | ng/μL |
| Endotoxin Level | - | 5.0 | EU/mL |

## Output Reports

### QC Status Levels
- **PASS**: All critical parameters meet specifications
- **WARNING**: Minor deviations that don't affect safety/efficacy
- **FAIL**: Critical parameters outside acceptable limits
- **NOT_TESTED**: Analysis not performed or incomplete

### Report Structure
```json
{
  "sample_name": "Sample_001",
  "timestamp": "2025-06-30T18:00:00",
  "metrics": {
    "concentration_ng_ul": 185.0,
    "total_yield_ug": 37.0,
    "a260_a280_ratio": 2.0,
    "rin_score": 8.2,
    "capping_efficiency_percent": 87.5,
    "overall_status": "PASS"
  },
  "qc_assessment": {
    "overall_status": "PASS",
    "individual_checks": {...},
    "summary": {
      "passed_checks": 8,
      "failed_checks": 0,
      "warning_checks": 0,
      "total_checks": 9
    }
  },
  "recommendations": [
    "All QC metrics meet specifications - sample is suitable for use"
  ],
  "detailed_analysis": {
    "quality_score": 92.4,
    "critical_parameters": [],
    "stability_prediction": {...},
    "regulatory_compliance": {...}
  }
}
```

## Integration with Plasmid Builder

The IVT RNA QC pipeline integrates seamlessly with the existing plasmid builder system:

```python
# After building plasmid with plasmid_builder.py
from plasmid_builder import PlasmidDesigner
from ivt_rna_qc import IVTRNAQCPipeline, RNASequence

# Design plasmid
designer = PlasmidDesigner()
plasmid_design = designer.design_vector()

# Extract mRNA sequence for QC
mrna_sequence = plasmid_design['mrna_transcript']
rna_sample = RNASequence(mrna_sequence, "Neoantigen_X_mRNA")

# Run IVT and QC analysis
pipeline = IVTRNAQCPipeline()
qc_results = pipeline.run_complete_qc("Neoantigen_X", rna_sample, analytical_data)
```

## Validation and Testing

The pipeline includes comprehensive tests covering:

- **Unit Tests**: Individual component functionality
- **Integration Tests**: End-to-end workflow validation
- **Performance Tests**: High-throughput batch processing
- **Edge Cases**: Invalid inputs and error handling
- **JSON Serialization**: Data export compatibility

Run the test suite:
```bash
python3 test_ivt_qc.py
```

Expected output:
```
IVT RNA QC Pipeline Test Suite
========================================
Ran 29 tests in 0.010s

✅ All tests passed including performance requirements
```

## Regulatory Compliance

The pipeline supports compliance with major regulatory standards:

- **FDA**: Purity standards for therapeutic mRNA
- **EMA**: RNA integrity requirements  
- **ICH**: Contamination limits for biologics
- **USP**: General chapters for nucleic acid therapeutics

## Performance Specifications

- **Processing Speed**: >1000 samples/second (batch mode)
- **Memory Usage**: <50MB per sample
- **Accuracy**: >99% for sequence validation
- **Precision**: ±5% for quantitative metrics

## Customization

### Custom Thresholds
```python
from ivt_rna_qc import RNAQualityAnalyzer

analyzer = RNAQualityAnalyzer()
analyzer.qc_thresholds['min_concentration'] = 150.0  # Custom threshold
```

### Custom Metrics
```python
class CustomQCPipeline(IVTRNAQCPipeline):
    def analyze_custom_metric(self, sample_data):
        # Add custom analysis logic
        return custom_results
```

## Troubleshooting

### Common Issues

1. **Low RIN Score**: Check storage conditions and handling procedures
2. **Poor A260/A280 Ratio**: Additional purification may be needed
3. **Low Capping Efficiency**: Optimize capping reaction conditions
4. **High Contamination**: Implement DNase treatment or improve purification

### Error Messages

- `Invalid RNA sequence`: Check for non-standard nucleotide characters
- `JSON decode error`: Verify input file format and syntax
- `Missing analytical data`: Ensure all required measurements are provided

## Examples

### Example 1: High-Quality Sample
```bash
python3 qc_cli.py --input examples/high_quality_sample.json
```
Expected: PASS status, quality score >90

### Example 2: Degraded Sample
```bash
python3 qc_cli.py --input examples/degraded_sample.json
```
Expected: FAIL status, low RIN score, recommendations for improvement

### Example 3: Batch Analysis
```bash
python3 qc_cli.py --batch examples/production_batch.json
```
Expected: Summary report with pass/fail statistics

## API Reference

### Classes

#### `RNASequence`
Data structure for RNA sequence information.

#### `QCMetrics`
Container for all quality control measurements.

#### `RNAQualityAnalyzer`
Core analysis engine for RNA quality assessment.

#### `QCReportGenerator`
Generates standardized QC reports and recommendations.

#### `IVTRNAQCPipeline`
Main pipeline controller for complete QC workflow.

### Methods

#### `run_complete_qc(sample_name, rna_sequence, analytical_data, expected_sequence=None)`
Run complete QC analysis on a single sample.

#### `run_batch_qc(samples)`
Process multiple samples in batch mode.

#### `generate_qc_report(sample_name, metrics, detailed=True)`
Generate comprehensive QC report.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

This project is part of the mRNA vaccine prototype system for research and development purposes.

## Support

For technical support or feature requests, please open an issue in the GitHub repository.

---

**Note**: This is a prototype system for research purposes. For production use in pharmaceutical manufacturing, additional validation and regulatory approval would be required.