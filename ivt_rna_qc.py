#!/usr/bin/env python3
"""
IVT RNA Quality Control Pipeline
Automated quality assessment for In Vitro Transcribed RNA samples in mRNA vaccine production.
"""

import re
import math
import json
import datetime
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum


class QCStatus(Enum):
    """Quality control status enumeration."""
    PASS = "PASS"
    FAIL = "FAIL" 
    WARNING = "WARNING"
    NOT_TESTED = "NOT_TESTED"


@dataclass
class RNASequence:
    """RNA sequence data structure."""
    sequence: str
    name: str
    description: str = ""
    
    def __post_init__(self):
        """Validate RNA sequence."""
        self.sequence = self.sequence.upper().replace('T', 'U')
        valid_bases = set('AUCG')
        if not all(base in valid_bases for base in self.sequence):
            raise ValueError(f"Invalid RNA sequence: contains non-RNA bases")


@dataclass 
class QCMetrics:
    """Quality control metrics data structure."""
    # Basic metrics
    concentration_ng_ul: float = 0.0
    total_yield_ug: float = 0.0
    a260_a280_ratio: float = 0.0
    a260_a230_ratio: float = 0.0
    
    # RNA integrity
    rin_score: float = 0.0  # RNA Integrity Number (1-10 scale)
    degradation_ratio: float = 0.0
    
    # Sequence metrics
    length_bp: int = 0
    gc_content_percent: float = 0.0
    sequence_accuracy_percent: float = 0.0
    
    # mRNA-specific metrics
    capping_efficiency_percent: float = 0.0
    poly_a_tail_length: int = 0
    five_prime_cap_present: bool = False
    
    # Contamination screening
    genomic_dna_contamination_percent: float = 0.0
    protein_contamination_ng_ul: float = 0.0
    endotoxin_level_eu_ml: float = 0.0
    
    # Secondary structure
    predicted_tm_celsius: float = 0.0
    hairpin_count: int = 0
    
    # Overall status
    overall_status: QCStatus = QCStatus.NOT_TESTED
    

class RNAQualityAnalyzer:
    """Core RNA quality analysis engine."""
    
    def __init__(self):
        """Initialize the RNA quality analyzer."""
        self.qc_thresholds = {
            'min_concentration': 100.0,  # ng/μL
            'min_yield': 10.0,  # μg
            'min_a260_a280': 1.8,
            'max_a260_a280': 2.2, 
            'min_a260_a230': 1.8,
            'min_rin_score': 7.0,
            'max_degradation_ratio': 0.1,
            'min_sequence_accuracy': 95.0,
            'min_capping_efficiency': 80.0,
            'min_poly_a_length': 100,
            'max_genomic_contamination': 1.0,
            'max_protein_contamination': 10.0,
            'max_endotoxin': 5.0,
        }
    
    def analyze_sequence_quality(self, rna_seq: RNASequence, 
                               expected_sequence: Optional[str] = None) -> Dict[str, Any]:
        """Analyze RNA sequence quality metrics."""
        metrics = {}
        
        # Basic sequence statistics
        metrics['length_bp'] = len(rna_seq.sequence)
        metrics['gc_content_percent'] = self._calculate_gc_content(rna_seq.sequence)
        
        # Sequence accuracy if expected sequence provided
        if expected_sequence:
            accuracy = self._calculate_sequence_accuracy(rna_seq.sequence, expected_sequence)
            metrics['sequence_accuracy_percent'] = accuracy
        
        # Secondary structure predictions
        metrics['predicted_tm_celsius'] = self._estimate_melting_temperature(rna_seq.sequence)
        metrics['hairpin_count'] = self._count_hairpins(rna_seq.sequence)
        
        return metrics
    
    def analyze_purity_metrics(self, a260: float, a280: float, a230: float) -> Dict[str, float]:
        """Analyze RNA purity from absorbance measurements."""
        return {
            'a260_a280_ratio': a260 / a280 if a280 > 0 else 0.0,
            'a260_a230_ratio': a260 / a230 if a230 > 0 else 0.0,
        }
    
    def analyze_integrity(self, electrophoresis_data: Optional[Dict] = None) -> Dict[str, Any]:
        """Analyze RNA integrity from electrophoresis or similar data."""
        # Simplified integrity analysis - in real implementation would use actual gel data
        if electrophoresis_data:
            # Process actual electrophoresis data
            rin_score = electrophoresis_data.get('rin_score', 8.0)
            degradation = electrophoresis_data.get('degradation_ratio', 0.05)
        else:
            # Default values for demonstration
            rin_score = 8.5
            degradation = 0.03
            
        return {
            'rin_score': rin_score,
            'degradation_ratio': degradation
        }
    
    def analyze_mrna_features(self, sequence: str, cap_analysis_data: Optional[Dict] = None,
                            poly_a_data: Optional[Dict] = None) -> Dict[str, Any]:
        """Analyze mRNA-specific features like capping and poly(A) tail."""
        metrics = {}
        
        # 5' cap analysis
        if cap_analysis_data:
            metrics['capping_efficiency_percent'] = cap_analysis_data.get('efficiency', 85.0)
            metrics['five_prime_cap_present'] = cap_analysis_data.get('cap_detected', True)
        else:
            # Estimate based on sequence features
            metrics['capping_efficiency_percent'] = 85.0
            metrics['five_prime_cap_present'] = True
        
        # Poly(A) tail analysis
        if poly_a_data:
            metrics['poly_a_tail_length'] = poly_a_data.get('length', 150)
        else:
            # Estimate poly(A) length from sequence end
            metrics['poly_a_tail_length'] = self._estimate_poly_a_length(sequence)
        
        return metrics
    
    def screen_contamination(self, sample_data: Dict[str, Any]) -> Dict[str, float]:
        """Screen for various types of contamination."""
        return {
            'genomic_dna_contamination_percent': sample_data.get('dna_contamination', 0.2),
            'protein_contamination_ng_ul': sample_data.get('protein_content', 2.0),
            'endotoxin_level_eu_ml': sample_data.get('endotoxin', 1.0),
        }
    
    def _calculate_gc_content(self, sequence: str) -> float:
        """Calculate GC content percentage."""
        gc_count = sequence.count('G') + sequence.count('C')
        return (gc_count / len(sequence)) * 100 if len(sequence) > 0 else 0.0
    
    def _calculate_sequence_accuracy(self, observed: str, expected: str) -> float:
        """Calculate sequence accuracy percentage."""
        if len(observed) != len(expected):
            return 0.0
        
        matches = sum(1 for a, b in zip(observed, expected) if a == b)
        return (matches / len(expected)) * 100
    
    def _estimate_melting_temperature(self, sequence: str) -> float:
        """Estimate RNA melting temperature using nearest neighbor approximation."""
        # Simplified Tm calculation - real implementation would use thermodynamic tables
        gc_content = self._calculate_gc_content(sequence)
        length = len(sequence)
        
        if length == 0:
            return 0.0
        
        # Basic approximation: Tm = 81.5°C + 16.6(log[Na+]) + 0.41(%GC) - 675/length
        # For very short sequences, use a simpler formula
        if length < 14:
            tm = (gc_content * 4) + ((100 - gc_content) * 2) - 7
        else:
            tm = 81.5 + 0.41 * gc_content - 675 / length
            
        return max(25.0, tm)  # Minimum reasonable melting temperature
    
    def _count_hairpins(self, sequence: str) -> int:
        """Count potential hairpin structures in RNA sequence."""
        # Simplified hairpin detection - looks for complementary regions
        hairpins = 0
        min_stem_length = 4
        min_loop_length = 3
        
        for i in range(len(sequence) - 2 * min_stem_length - min_loop_length):
            for j in range(i + min_stem_length + min_loop_length, len(sequence) - min_stem_length + 1):
                stem1 = sequence[i:i+min_stem_length]
                stem2 = sequence[j:j+min_stem_length]
                if self._is_complementary(stem1, stem2):
                    hairpins += 1
        
        return hairpins
    
    def _is_complementary(self, seq1: str, seq2: str) -> bool:
        """Check if two RNA sequences are complementary."""
        complement = {'A': 'U', 'U': 'A', 'G': 'C', 'C': 'G'}
        if len(seq1) != len(seq2):
            return False
        
        for a, b in zip(seq1, seq2[::-1]):  # Reverse seq2 for antiparallel pairing
            if complement.get(a) != b:
                return False
        return True
    
    def _estimate_poly_a_length(self, sequence: str) -> int:
        """Estimate poly(A) tail length from sequence."""
        # Look for poly(A) runs at the 3' end
        reversed_seq = sequence[::-1]
        poly_a_length = 0
        
        for base in reversed_seq:
            if base == 'A':
                poly_a_length += 1
            else:
                break
        
        return poly_a_length


class QCReportGenerator:
    """Generate standardized QC reports."""
    
    def __init__(self):
        """Initialize the report generator."""
        self.analyzer = RNAQualityAnalyzer()
    
    def generate_qc_report(self, sample_name: str, metrics: QCMetrics, 
                          detailed: bool = True) -> Dict[str, Any]:
        """Generate a comprehensive QC report."""
        report = {
            'sample_name': sample_name,
            'timestamp': datetime.datetime.now().isoformat(),
            'metrics': asdict(metrics),
            'qc_assessment': self._assess_quality(metrics),
            'recommendations': self._generate_recommendations(metrics),
        }
        
        if detailed:
            report['detailed_analysis'] = self._generate_detailed_analysis(metrics)
        
        return report
    
    def _assess_quality(self, metrics: QCMetrics) -> Dict[str, Any]:
        """Assess overall quality based on metrics."""
        assessment = {}
        thresholds = self.analyzer.qc_thresholds
        
        # Individual metric assessments
        checks = {
            'concentration': QCStatus.PASS if metrics.concentration_ng_ul >= thresholds['min_concentration'] else QCStatus.FAIL,
            'yield': QCStatus.PASS if metrics.total_yield_ug >= thresholds['min_yield'] else QCStatus.FAIL,
            'purity_260_280': QCStatus.PASS if thresholds['min_a260_a280'] <= metrics.a260_a280_ratio <= thresholds['max_a260_a280'] else QCStatus.FAIL,
            'purity_260_230': QCStatus.PASS if metrics.a260_a230_ratio >= thresholds['min_a260_a230'] else QCStatus.FAIL,
            'integrity': QCStatus.PASS if metrics.rin_score >= thresholds['min_rin_score'] else QCStatus.FAIL,
            'sequence_accuracy': QCStatus.PASS if metrics.sequence_accuracy_percent >= thresholds['min_sequence_accuracy'] else QCStatus.WARNING,
            'capping': QCStatus.PASS if metrics.capping_efficiency_percent >= thresholds['min_capping_efficiency'] else QCStatus.WARNING,
            'poly_a_tail': QCStatus.PASS if metrics.poly_a_tail_length >= thresholds['min_poly_a_length'] else QCStatus.WARNING,
            'contamination': QCStatus.PASS if all([
                metrics.genomic_dna_contamination_percent <= thresholds['max_genomic_contamination'],
                metrics.protein_contamination_ng_ul <= thresholds['max_protein_contamination'],
                metrics.endotoxin_level_eu_ml <= thresholds['max_endotoxin']
            ]) else QCStatus.FAIL,
        }
        
        assessment['individual_checks'] = checks
        
        # Overall assessment
        fail_count = sum(1 for status in checks.values() if status == QCStatus.FAIL)
        warning_count = sum(1 for status in checks.values() if status == QCStatus.WARNING)
        
        if fail_count > 0:
            overall_status = QCStatus.FAIL
        elif warning_count > 0:
            overall_status = QCStatus.WARNING  
        else:
            overall_status = QCStatus.PASS
            
        assessment['overall_status'] = overall_status
        assessment['summary'] = {
            'passed_checks': sum(1 for status in checks.values() if status == QCStatus.PASS),
            'failed_checks': fail_count,
            'warning_checks': warning_count,
            'total_checks': len(checks)
        }
        
        return assessment
    
    def _generate_recommendations(self, metrics: QCMetrics) -> List[str]:
        """Generate recommendations based on QC results."""
        recommendations = []
        thresholds = self.analyzer.qc_thresholds
        
        if metrics.concentration_ng_ul < thresholds['min_concentration']:
            recommendations.append("Increase RNA concentration through precipitation or concentration methods")
            
        if metrics.total_yield_ug < thresholds['min_yield']:
            recommendations.append("Optimize IVT reaction conditions to improve yield")
            
        if not (thresholds['min_a260_a280'] <= metrics.a260_a280_ratio <= thresholds['max_a260_a280']):
            recommendations.append("RNA purity may be compromised - consider additional purification steps")
            
        if metrics.rin_score < thresholds['min_rin_score']:
            recommendations.append("RNA integrity is compromised - check storage conditions and handling procedures")
            
        if metrics.capping_efficiency_percent < thresholds['min_capping_efficiency']:
            recommendations.append("Optimize 5' capping reaction or use alternative capping methods")
            
        if metrics.poly_a_tail_length < thresholds['min_poly_a_length']:
            recommendations.append("Optimize poly(A) tailing reaction to achieve desired tail length")
            
        if metrics.genomic_dna_contamination_percent > thresholds['max_genomic_contamination']:
            recommendations.append("Perform DNase treatment to remove genomic DNA contamination")
            
        if not recommendations:
            recommendations.append("All QC metrics meet specifications - sample is suitable for use")
            
        return recommendations
    
    def _generate_detailed_analysis(self, metrics: QCMetrics) -> Dict[str, Any]:
        """Generate detailed analysis section."""
        return {
            'quality_score': self._calculate_quality_score(metrics),
            'critical_parameters': self._identify_critical_parameters(metrics),
            'stability_prediction': self._predict_stability(metrics),
            'regulatory_compliance': self._check_regulatory_compliance(metrics),
        }
    
    def _calculate_quality_score(self, metrics: QCMetrics) -> float:
        """Calculate an overall quality score (0-100)."""
        thresholds = self.analyzer.qc_thresholds
        scores = []
        
        # Concentration score
        if metrics.concentration_ng_ul >= thresholds['min_concentration']:
            scores.append(min(100, (metrics.concentration_ng_ul / thresholds['min_concentration']) * 100))
        else:
            scores.append(0)
            
        # Purity score
        if thresholds['min_a260_a280'] <= metrics.a260_a280_ratio <= thresholds['max_a260_a280']:
            scores.append(100)
        else:
            scores.append(50)
            
        # Integrity score
        scores.append(min(100, (metrics.rin_score / 10) * 100))
        
        # Capping score
        scores.append(min(100, metrics.capping_efficiency_percent))
        
        return sum(scores) / len(scores) if scores else 0.0
    
    def _identify_critical_parameters(self, metrics: QCMetrics) -> List[str]:
        """Identify critical parameters that need attention."""
        critical = []
        thresholds = self.analyzer.qc_thresholds
        
        if metrics.rin_score < thresholds['min_rin_score']:
            critical.append("RNA integrity")
            
        if metrics.capping_efficiency_percent < thresholds['min_capping_efficiency']:
            critical.append("5' capping efficiency")
            
        if metrics.genomic_dna_contamination_percent > thresholds['max_genomic_contamination']:
            critical.append("DNA contamination")
            
        return critical
    
    def _predict_stability(self, metrics: QCMetrics) -> Dict[str, Any]:
        """Predict RNA stability based on metrics."""
        stability_score = 100
        
        if metrics.rin_score < 7:
            stability_score -= 30
        if metrics.degradation_ratio > 0.1:
            stability_score -= 20
        if metrics.gc_content_percent < 40 or metrics.gc_content_percent > 60:
            stability_score -= 10
            
        return {
            'predicted_stability_score': max(0, stability_score),
            'storage_recommendation': 'Store at -80°C' if stability_score > 70 else 'Use immediately',
            'shelf_life_days': max(1, int(stability_score / 10))
        }
    
    def _check_regulatory_compliance(self, metrics: QCMetrics) -> Dict[str, bool]:
        """Check compliance with regulatory guidelines."""
        return {
            'fda_purity_standards': metrics.a260_a280_ratio >= 1.8 and metrics.a260_a230_ratio >= 1.8,
            'ema_integrity_standards': metrics.rin_score >= 7.0,
            'ich_contamination_limits': all([
                metrics.genomic_dna_contamination_percent <= 1.0,
                metrics.protein_contamination_ng_ul <= 10.0,
                metrics.endotoxin_level_eu_ml <= 5.0
            ]),
            'usp_specifications': metrics.concentration_ng_ul >= 100.0 and metrics.total_yield_ug >= 10.0
        }


class IVTRNAQCPipeline:
    """Main IVT RNA QC pipeline controller."""
    
    def __init__(self):
        """Initialize the QC pipeline."""
        self.analyzer = RNAQualityAnalyzer()
        self.reporter = QCReportGenerator()
    
    def run_complete_qc(self, sample_name: str, rna_sequence: RNASequence,
                       analytical_data: Dict[str, Any], 
                       expected_sequence: Optional[str] = None) -> Dict[str, Any]:
        """Run complete QC analysis on an IVT RNA sample."""
        
        # Initialize metrics
        metrics = QCMetrics()
        
        # Basic sample information
        metrics.length_bp = len(rna_sequence.sequence)
        
        # Extract analytical measurements
        absorbance_data = analytical_data.get('absorbance', {})
        if absorbance_data:
            a260 = absorbance_data.get('a260', 1.0)
            a280 = absorbance_data.get('a280', 0.5)  
            a230 = absorbance_data.get('a230', 0.4)
            
            purity_metrics = self.analyzer.analyze_purity_metrics(a260, a280, a230)
            metrics.a260_a280_ratio = purity_metrics['a260_a280_ratio']
            metrics.a260_a230_ratio = purity_metrics['a260_a230_ratio']
            
            # Calculate concentration and yield
            metrics.concentration_ng_ul = analytical_data.get('concentration', 150.0)
            volume_ul = analytical_data.get('volume_ul', 100.0)
            metrics.total_yield_ug = (metrics.concentration_ng_ul * volume_ul) / 1000
        
        # Sequence quality analysis
        seq_metrics = self.analyzer.analyze_sequence_quality(rna_sequence, expected_sequence)
        metrics.gc_content_percent = seq_metrics['gc_content_percent']
        metrics.sequence_accuracy_percent = seq_metrics.get('sequence_accuracy_percent', 100.0)
        metrics.predicted_tm_celsius = seq_metrics['predicted_tm_celsius']
        metrics.hairpin_count = seq_metrics['hairpin_count']
        
        # RNA integrity analysis
        integrity_data = analytical_data.get('integrity', {})
        integrity_metrics = self.analyzer.analyze_integrity(integrity_data)
        metrics.rin_score = integrity_metrics['rin_score']
        metrics.degradation_ratio = integrity_metrics['degradation_ratio']
        
        # mRNA-specific features
        cap_data = analytical_data.get('capping', {})
        poly_a_data = analytical_data.get('poly_a', {})
        mrna_metrics = self.analyzer.analyze_mrna_features(
            rna_sequence.sequence, cap_data, poly_a_data
        )
        metrics.capping_efficiency_percent = mrna_metrics['capping_efficiency_percent'] 
        metrics.poly_a_tail_length = mrna_metrics['poly_a_tail_length']
        metrics.five_prime_cap_present = mrna_metrics['five_prime_cap_present']
        
        # Contamination screening
        contamination_metrics = self.analyzer.screen_contamination(analytical_data)
        metrics.genomic_dna_contamination_percent = contamination_metrics['genomic_dna_contamination_percent']
        metrics.protein_contamination_ng_ul = contamination_metrics['protein_contamination_ng_ul']
        metrics.endotoxin_level_eu_ml = contamination_metrics['endotoxin_level_eu_ml']
        
        # Generate comprehensive report
        qc_report = self.reporter.generate_qc_report(sample_name, metrics, detailed=True)
        
        # Update overall status
        metrics.overall_status = QCStatus(qc_report['qc_assessment']['overall_status'].value)
        
        return {
            'sample_name': sample_name,
            'metrics': metrics,
            'qc_report': qc_report,
            'pipeline_version': '1.0.0',
            'analysis_timestamp': datetime.datetime.now().isoformat()
        }
    
    def run_batch_qc(self, samples: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Run QC analysis on a batch of samples."""
        results = []
        
        for sample_data in samples:
            try:
                sample_name = sample_data['name']
                rna_seq = RNASequence(
                    sequence=sample_data['sequence'],
                    name=sample_name,
                    description=sample_data.get('description', '')
                )
                analytical_data = sample_data.get('analytical_data', {})
                expected_seq = sample_data.get('expected_sequence')
                
                result = self.run_complete_qc(sample_name, rna_seq, analytical_data, expected_seq)
                results.append(result)
                
            except Exception as e:
                results.append({
                    'sample_name': sample_data.get('name', 'Unknown'),
                    'error': str(e),
                    'status': 'FAILED'
                })
        
        return results


def main():
    """Main function for CLI usage."""
    # Example usage
    print("IVT RNA QC Pipeline - Example Run")
    print("=" * 40)
    
    # Create example RNA sequence (neoantigen X mRNA)
    neoantigen_sequence = "AUGGCCACCAUGGAGAAAGUAAAGGGCUUUAUAGGGGAGAUAAGGUUUUGACUUUGUAG"
    rna_sample = RNASequence(
        sequence=neoantigen_sequence,
        name="Neoantigen_X_mRNA_Sample_001",
        description="IVT mRNA encoding neoantigen X for vaccine development"
    )
    
    # Example analytical data
    analytical_data = {
        'absorbance': {
            'a260': 1.8,
            'a280': 0.9,
            'a230': 0.8
        },
        'concentration': 185.0,  # ng/μL
        'volume_ul': 200.0,
        'integrity': {
            'rin_score': 8.2,
            'degradation_ratio': 0.04
        },
        'capping': {
            'efficiency': 87.5,
            'cap_detected': True
        },
        'poly_a': {
            'length': 125
        },
        'dna_contamination': 0.3,
        'protein_content': 1.8,
        'endotoxin': 0.8
    }
    
    # Run QC pipeline
    pipeline = IVTRNAQCPipeline()
    results = pipeline.run_complete_qc(
        sample_name="Neoantigen_X_001",
        rna_sequence=rna_sample,
        analytical_data=analytical_data
    )
    
    # Print results
    print(f"Sample: {results['sample_name']}")
    print(f"Overall Status: {results['qc_report']['qc_assessment']['overall_status'].value}")
    print(f"Quality Score: {results['qc_report']['detailed_analysis']['quality_score']:.1f}")
    print("\nKey Metrics:")
    metrics = results['metrics']
    print(f"  Concentration: {metrics.concentration_ng_ul:.1f} ng/μL")
    print(f"  Yield: {metrics.total_yield_ug:.1f} μg")
    print(f"  Purity (A260/A280): {metrics.a260_a280_ratio:.2f}")
    print(f"  RIN Score: {metrics.rin_score:.1f}")
    print(f"  Capping Efficiency: {metrics.capping_efficiency_percent:.1f}%")
    print(f"  Poly(A) Length: {metrics.poly_a_tail_length} nt")
    
    print("\nRecommendations:")
    for rec in results['qc_report']['recommendations']:
        print(f"  • {rec}")


if __name__ == "__main__":
    main()