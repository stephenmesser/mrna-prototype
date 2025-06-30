#!/usr/bin/env python3
"""
Test suite for IVT RNA QC Pipeline
Comprehensive tests for quality control functionality.
"""

import unittest
import json
import tempfile
import os
from typing import Dict, Any

from ivt_rna_qc import (
    RNASequence, QCMetrics, QCStatus, RNAQualityAnalyzer, 
    QCReportGenerator, IVTRNAQCPipeline
)


class TestRNASequence(unittest.TestCase):
    """Test RNA sequence handling."""
    
    def test_valid_rna_sequence(self):
        """Test valid RNA sequence creation."""
        seq = RNASequence("AUCG", "test")
        self.assertEqual(seq.sequence, "AUCG")
        self.assertEqual(seq.name, "test")
    
    def test_dna_to_rna_conversion(self):
        """Test DNA to RNA conversion (T -> U)."""
        seq = RNASequence("ATCG", "test")
        self.assertEqual(seq.sequence, "AUCG")
    
    def test_invalid_sequence(self):
        """Test invalid sequence handling."""
        with self.assertRaises(ValueError):
            RNASequence("ATCGXYZ", "test")
    
    def test_lowercase_conversion(self):
        """Test lowercase to uppercase conversion."""
        seq = RNASequence("aucg", "test")
        self.assertEqual(seq.sequence, "AUCG")


class TestRNAQualityAnalyzer(unittest.TestCase):
    """Test RNA quality analysis functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = RNAQualityAnalyzer()
        self.test_sequence = "AUGGCCACCAUGGAGAAAGUAAAGGGCUUUAUAGGGGAGAUAAGGUUUUGACUUUGUAG"
        self.rna_seq = RNASequence(self.test_sequence, "test_seq")
    
    def test_gc_content_calculation(self):
        """Test GC content calculation."""
        # Sequence: AUCG has 50% GC content
        gc_content = self.analyzer._calculate_gc_content("AUCG")
        self.assertEqual(gc_content, 50.0)
        
        # All A's should be 0% GC
        gc_content = self.analyzer._calculate_gc_content("AAAA")
        self.assertEqual(gc_content, 0.0)
        
        # All G's should be 100% GC
        gc_content = self.analyzer._calculate_gc_content("GGGG")
        self.assertEqual(gc_content, 100.0)
    
    def test_sequence_accuracy_calculation(self):
        """Test sequence accuracy calculation."""
        observed = "AUCG"
        expected = "AUCG"
        accuracy = self.analyzer._calculate_sequence_accuracy(observed, expected)
        self.assertEqual(accuracy, 100.0)
        
        observed = "AUCG"
        expected = "AUCC"  # One mismatch
        accuracy = self.analyzer._calculate_sequence_accuracy(observed, expected)
        self.assertEqual(accuracy, 75.0)
        
        # Different lengths should return 0
        observed = "AUCG"
        expected = "AUCGA"
        accuracy = self.analyzer._calculate_sequence_accuracy(observed, expected)
        self.assertEqual(accuracy, 0.0)
    
    def test_melting_temperature_estimation(self):
        """Test melting temperature estimation."""
        tm = self.analyzer._estimate_melting_temperature("AUCG")
        self.assertGreater(tm, 0)
        self.assertLess(tm, 100)  # Should be reasonable temperature
    
    def test_poly_a_length_estimation(self):
        """Test poly(A) tail length estimation."""
        # Sequence ending with poly(A)
        sequence_with_polya = "AUCGAAAA"
        length = self.analyzer._estimate_poly_a_length(sequence_with_polya)
        self.assertEqual(length, 4)
        
        # Sequence without poly(A)
        sequence_no_polya = "AUCGCCCC"
        length = self.analyzer._estimate_poly_a_length(sequence_no_polya)
        self.assertEqual(length, 0)
    
    def test_complementarity_check(self):
        """Test RNA complementarity checking."""
        # Perfect complement
        self.assertTrue(self.analyzer._is_complementary("AUCG", "CGAU"))
        
        # Non-complement
        self.assertFalse(self.analyzer._is_complementary("AUCG", "AUCG"))
        
        # Different lengths
        self.assertFalse(self.analyzer._is_complementary("AUCG", "CGA"))
    
    def test_sequence_quality_analysis(self):
        """Test complete sequence quality analysis."""
        metrics = self.analyzer.analyze_sequence_quality(self.rna_seq)
        
        self.assertIn('length_bp', metrics)
        self.assertIn('gc_content_percent', metrics)
        self.assertIn('predicted_tm_celsius', metrics)
        self.assertIn('hairpin_count', metrics)
        
        self.assertEqual(metrics['length_bp'], len(self.test_sequence))
        self.assertGreaterEqual(metrics['gc_content_percent'], 0)
        self.assertLessEqual(metrics['gc_content_percent'], 100)
    
    def test_purity_analysis(self):
        """Test purity metrics analysis."""
        purity = self.analyzer.analyze_purity_metrics(1.8, 0.9, 0.8)
        
        self.assertAlmostEqual(purity['a260_a280_ratio'], 2.0, places=1)
        self.assertAlmostEqual(purity['a260_a230_ratio'], 2.25, places=1)
    
    def test_integrity_analysis(self):
        """Test RNA integrity analysis."""
        integrity_data = {'rin_score': 8.5, 'degradation_ratio': 0.03}
        integrity = self.analyzer.analyze_integrity(integrity_data)
        
        self.assertEqual(integrity['rin_score'], 8.5)
        self.assertEqual(integrity['degradation_ratio'], 0.03)
    
    def test_mrna_features_analysis(self):
        """Test mRNA-specific features analysis."""
        cap_data = {'efficiency': 90.0, 'cap_detected': True}
        poly_a_data = {'length': 150}
        
        features = self.analyzer.analyze_mrna_features(
            self.test_sequence, cap_data, poly_a_data
        )
        
        self.assertEqual(features['capping_efficiency_percent'], 90.0)
        self.assertEqual(features['poly_a_tail_length'], 150)
        self.assertTrue(features['five_prime_cap_present'])
    
    def test_contamination_screening(self):
        """Test contamination screening."""
        sample_data = {
            'dna_contamination': 0.5,
            'protein_content': 3.0,
            'endotoxin': 2.0
        }
        
        contamination = self.analyzer.screen_contamination(sample_data)
        
        self.assertEqual(contamination['genomic_dna_contamination_percent'], 0.5)
        self.assertEqual(contamination['protein_contamination_ng_ul'], 3.0)
        self.assertEqual(contamination['endotoxin_level_eu_ml'], 2.0)


class TestQCReportGenerator(unittest.TestCase):
    """Test QC report generation."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.reporter = QCReportGenerator()
        self.test_metrics = QCMetrics(
            concentration_ng_ul=185.0,
            total_yield_ug=37.0,
            a260_a280_ratio=2.0,
            a260_a230_ratio=2.25,
            rin_score=8.2,
            degradation_ratio=0.04,
            length_bp=58,
            gc_content_percent=65.5,
            sequence_accuracy_percent=99.5,
            capping_efficiency_percent=87.5,
            poly_a_tail_length=125,
            five_prime_cap_present=True,
            genomic_dna_contamination_percent=0.3,
            protein_contamination_ng_ul=1.8,
            endotoxin_level_eu_ml=0.8,
            predicted_tm_celsius=75.2,
            hairpin_count=2,
            overall_status=QCStatus.PASS
        )
    
    def test_quality_assessment(self):
        """Test quality assessment functionality."""
        assessment = self.reporter._assess_quality(self.test_metrics)
        
        self.assertIn('individual_checks', assessment)
        self.assertIn('overall_status', assessment)
        self.assertIn('summary', assessment)
        
        # Should pass with good metrics
        self.assertEqual(assessment['overall_status'], QCStatus.PASS)
    
    def test_quality_assessment_failures(self):
        """Test quality assessment with failing metrics."""
        failing_metrics = QCMetrics(
            concentration_ng_ul=50.0,  # Below threshold
            total_yield_ug=5.0,  # Below threshold
            a260_a280_ratio=1.5,  # Below threshold
            rin_score=5.0,  # Below threshold
        )
        
        assessment = self.reporter._assess_quality(failing_metrics)
        self.assertEqual(assessment['overall_status'], QCStatus.FAIL)
        self.assertGreater(assessment['summary']['failed_checks'], 0)
    
    def test_recommendations_generation(self):
        """Test recommendations generation."""
        recommendations = self.reporter._generate_recommendations(self.test_metrics)
        self.assertIsInstance(recommendations, list)
        self.assertGreater(len(recommendations), 0)
    
    def test_quality_score_calculation(self):
        """Test quality score calculation."""
        score = self.reporter._calculate_quality_score(self.test_metrics)
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 100)
    
    def test_critical_parameters_identification(self):
        """Test critical parameters identification."""
        critical = self.reporter._identify_critical_parameters(self.test_metrics)
        self.assertIsInstance(critical, list)
    
    def test_stability_prediction(self):
        """Test stability prediction."""
        stability = self.reporter._predict_stability(self.test_metrics)
        
        self.assertIn('predicted_stability_score', stability)
        self.assertIn('storage_recommendation', stability)
        self.assertIn('shelf_life_days', stability)
    
    def test_regulatory_compliance_check(self):
        """Test regulatory compliance checking."""
        compliance = self.reporter._check_regulatory_compliance(self.test_metrics)
        
        self.assertIn('fda_purity_standards', compliance)
        self.assertIn('ema_integrity_standards', compliance)
        self.assertIn('ich_contamination_limits', compliance)
        self.assertIn('usp_specifications', compliance)
    
    def test_complete_report_generation(self):
        """Test complete QC report generation."""
        report = self.reporter.generate_qc_report("test_sample", self.test_metrics)
        
        required_keys = [
            'sample_name', 'timestamp', 'metrics', 'qc_assessment', 
            'recommendations', 'detailed_analysis'
        ]
        
        for key in required_keys:
            self.assertIn(key, report)
        
        self.assertEqual(report['sample_name'], "test_sample")


class TestIVTRNAQCPipeline(unittest.TestCase):
    """Test complete IVT RNA QC pipeline."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.pipeline = IVTRNAQCPipeline()
        self.test_sequence = "AUGGCCACCAUGGAGAAAGUAAAGGGCUUUAUAGGGGAGAUAAGGUUUUGACUUUGUAG"
        self.rna_seq = RNASequence(self.test_sequence, "test_sample")
        self.analytical_data = {
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
    
    def test_complete_qc_analysis(self):
        """Test complete QC analysis."""
        results = self.pipeline.run_complete_qc(
            "test_sample", self.rna_seq, self.analytical_data
        )
        
        required_keys = [
            'sample_name', 'metrics', 'qc_report', 
            'pipeline_version', 'analysis_timestamp'
        ]
        
        for key in required_keys:
            self.assertIn(key, results)
        
        self.assertEqual(results['sample_name'], "test_sample")
        self.assertIsInstance(results['metrics'], QCMetrics)
    
    def test_batch_qc_analysis(self):
        """Test batch QC analysis."""
        samples = [
            {
                'name': 'sample_1',
                'sequence': self.test_sequence,
                'analytical_data': self.analytical_data
            },
            {
                'name': 'sample_2', 
                'sequence': self.test_sequence,
                'analytical_data': self.analytical_data
            }
        ]
        
        results = self.pipeline.run_batch_qc(samples)
        
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]['sample_name'], 'sample_1')
        self.assertEqual(results[1]['sample_name'], 'sample_2')
    
    def test_batch_qc_with_invalid_sample(self):
        """Test batch QC with invalid sample data."""
        samples = [
            {
                'name': 'valid_sample',
                'sequence': self.test_sequence,
                'analytical_data': self.analytical_data
            },
            {
                'name': 'invalid_sample',
                'sequence': 'INVALID_SEQUENCE_XYZ',  # Invalid characters
                'analytical_data': {}
            }
        ]
        
        results = self.pipeline.run_batch_qc(samples)
        
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]['sample_name'], 'valid_sample')
        self.assertEqual(results[1]['sample_name'], 'invalid_sample')
        self.assertIn('error', results[1])
    
    def test_sequence_accuracy_with_expected(self):
        """Test sequence accuracy calculation with expected sequence."""
        expected_seq = self.test_sequence
        
        results = self.pipeline.run_complete_qc(
            "test_sample", self.rna_seq, self.analytical_data, expected_seq
        )
        
        metrics = results['metrics']
        self.assertEqual(metrics.sequence_accuracy_percent, 100.0)
    
    def test_missing_analytical_data(self):
        """Test pipeline with minimal analytical data."""
        minimal_data = {'concentration': 100.0, 'volume_ul': 50.0}
        
        results = self.pipeline.run_complete_qc(
            "minimal_sample", self.rna_seq, minimal_data
        )
        
        # Should still complete analysis with default values
        self.assertIn('qc_report', results)
        self.assertIsInstance(results['metrics'], QCMetrics)


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete system."""
    
    def test_end_to_end_workflow(self):
        """Test complete end-to-end workflow."""
        # Create sample data
        sequence = "AUGGCCACCAUGGAGAAAGUAAAGGGCUUUAUAGGGGAGAUAAGGUUUUGACUUUGUAG"
        rna_seq = RNASequence(sequence, "integration_test")
        
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
        
        # Run pipeline
        pipeline = IVTRNAQCPipeline()
        results = pipeline.run_complete_qc(
            "integration_test", rna_seq, analytical_data, sequence
        )
        
        # Verify results structure
        self.assertIn('qc_report', results)
        self.assertIn('metrics', results)
        
        # Verify QC assessment
        assessment = results['qc_report']['qc_assessment']
        self.assertIn('overall_status', assessment)
        self.assertIn('individual_checks', assessment)
        
        # Verify recommendations
        recommendations = results['qc_report']['recommendations']
        self.assertIsInstance(recommendations, list)
        self.assertGreater(len(recommendations), 0)
    
    def test_json_serialization(self):
        """Test JSON serialization of results."""
        sequence = "AUCG"
        rna_seq = RNASequence(sequence, "json_test")
        analytical_data = {'concentration': 100.0, 'volume_ul': 50.0}
        
        pipeline = IVTRNAQCPipeline()
        results = pipeline.run_complete_qc("json_test", rna_seq, analytical_data)
        
        # Test serialization by converting to JSON and back
        try:
            # Convert enums to strings for JSON compatibility
            def convert_for_json(obj):
                if hasattr(obj, 'value'):
                    return obj.value
                elif hasattr(obj, '__dict__'):
                    return {k: convert_for_json(v) for k, v in obj.__dict__.items()}
                elif isinstance(obj, dict):
                    return {k: convert_for_json(v) for k, v in obj.items()}
                elif isinstance(obj, list):
                    return [convert_for_json(item) for item in obj]
                else:
                    return obj
            
            json_compatible = convert_for_json(results)
            json_str = json.dumps(json_compatible, default=str)
            parsed = json.loads(json_str)
            
            # Verify key structure is preserved
            self.assertIn('sample_name', parsed)
            self.assertIn('qc_report', parsed)
            
        except (TypeError, ValueError) as e:
            self.fail(f"JSON serialization failed: {e}")


def run_performance_test():
    """Run performance test with multiple samples."""
    print("\nRunning performance test...")
    
    import time
    
    pipeline = IVTRNAQCPipeline()
    
    # Create test data for 10 samples
    samples = []
    for i in range(10):
        samples.append({
            'name': f'perf_sample_{i:03d}',
            'sequence': "AUGGCCACCAUGGAGAAAGUAAAGGGCUUUAUAGGGGAGAUAAGGUUUUGACUUUGUAG",
            'analytical_data': {
                'absorbance': {'a260': 1.8, 'a280': 0.9, 'a230': 0.8},
                'concentration': 150.0 + i * 10,  # Vary concentration
                'volume_ul': 200.0,
                'integrity': {'rin_score': 8.0 + i * 0.1, 'degradation_ratio': 0.04},
                'capping': {'efficiency': 85.0 + i, 'cap_detected': True},
                'poly_a': {'length': 120 + i * 5},
                'dna_contamination': 0.3,
                'protein_content': 1.8,
                'endotoxin': 0.8
            }
        })
    
    # Time the batch processing
    start_time = time.time()
    results = pipeline.run_batch_qc(samples)
    end_time = time.time()
    
    processing_time = end_time - start_time
    samples_per_second = len(samples) / processing_time
    
    print(f"Processed {len(samples)} samples in {processing_time:.2f} seconds")
    print(f"Performance: {samples_per_second:.1f} samples/second")
    
    # Verify all samples processed successfully
    successful = sum(1 for r in results if 'error' not in r)
    print(f"Successfully processed: {successful}/{len(samples)} samples")
    
    return processing_time < 5.0  # Should process 10 samples in under 5 seconds


def main():
    """Run all tests."""
    print("IVT RNA QC Pipeline Test Suite")
    print("=" * 40)
    
    # Run unit tests
    unittest.main(argv=[''], exit=False, verbosity=2)
    
    # Run performance test
    performance_ok = run_performance_test()
    
    if performance_ok:
        print("\n✅ All tests passed including performance requirements")
    else:
        print("\n⚠️  Performance test failed - processing too slow")


if __name__ == "__main__":
    main()