#!/usr/bin/env python3
"""
Test suite for the IVT RNA QC Pipeline.
"""

import sys
import os
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, mock_open

# Add the current directory to the path to import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ivt_qc_pipeline import (
    NanoDropParser, IVTQCAnalyzer, QCReporter, QCLimits, main
)


class TestQCLimits(unittest.TestCase):
    """Test QC limits configuration."""
    
    def test_default_limits(self):
        """Test default QC limits."""
        limits = QCLimits()
        self.assertEqual(limits.MIN_CONCENTRATION, 1.0)
        self.assertEqual(limits.MIN_260_280_RATIO, 1.8)
        self.assertEqual(limits.MAX_260_280_RATIO, 2.2)


class TestNanoDropParser(unittest.TestCase):
    """Test NanoDrop CSV parsing functionality."""
    
    def setUp(self):
        """Set up test data."""
        self.test_csv_content = """NanoDrop Data Export
Date: 2024-07-07
User: Test User

Sample ID,Concentration,A260,A280,A230,A260/A280,A260/A230,Sample Type
IVT-001,145.2,2.904,1.523,1.452,1.91,2.00,RNA
IVT-002,89.5,1.790,0.995,0.895,1.80,2.00,RNA
IVT-003,234.7,4.694,2.347,2.094,2.00,2.24,RNA
"""
        
        # Create temporary CSV file
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv')
        self.temp_file.write(self.test_csv_content)
        self.temp_file.close()
    
    def tearDown(self):
        """Clean up temporary files."""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_parse_valid_csv(self):
        """Test parsing a valid NanoDrop CSV file."""
        parser = NanoDropParser(self.temp_file.name)
        samples = parser.parse_nanodrop_csv()
        
        self.assertEqual(len(samples), 3)
        
        # Check first sample
        sample1 = samples[0]
        self.assertEqual(sample1['sample_id'], 'IVT-001')
        self.assertEqual(sample1['concentration_ng_ul'], 145.2)
        self.assertEqual(sample1['a260_280_ratio'], 1.91)
        self.assertEqual(sample1['a260_230_ratio'], 2.00)
    
    def test_file_not_found(self):
        """Test handling of non-existent file."""
        with self.assertRaises(FileNotFoundError):
            NanoDropParser("nonexistent_file.csv")
    
    def test_invalid_csv_format(self):
        """Test handling of invalid CSV format."""
        invalid_csv = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv')
        invalid_csv.write("Invalid,Data,Format\n1,2,3\n")
        invalid_csv.close()
        
        try:
            parser = NanoDropParser(invalid_csv.name)
            with self.assertRaises(ValueError):
                parser.parse_nanodrop_csv()
        finally:
            os.unlink(invalid_csv.name)
    
    def test_extract_sample_data(self):
        """Test sample data extraction from CSV row."""
        parser = NanoDropParser(self.temp_file.name)
        
        row = {
            'Sample ID': 'TEST-001',
            'Concentration': '123.45',
            'A260/A280': '1.95',
            'A260/A230': '2.10'
        }
        
        sample_data = parser._extract_sample_data(row)
        
        self.assertIsNotNone(sample_data)
        self.assertEqual(sample_data['sample_id'], 'TEST-001')
        self.assertEqual(sample_data['concentration_ng_ul'], 123.45)
        self.assertEqual(sample_data['a260_280_ratio'], 1.95)
        self.assertEqual(sample_data['a260_230_ratio'], 2.10)
    
    def test_missing_required_fields(self):
        """Test handling of rows with missing required fields."""
        parser = NanoDropParser(self.temp_file.name)
        
        # Missing sample ID
        row1 = {'Concentration': '123.45', 'A260/A280': '1.95'}
        self.assertIsNone(parser._extract_sample_data(row1))
        
        # Missing concentration
        row2 = {'Sample ID': 'TEST-001', 'A260/A280': '1.95'}
        self.assertIsNone(parser._extract_sample_data(row2))


class TestIVTQCAnalyzer(unittest.TestCase):
    """Test IVT QC analysis functionality."""
    
    def setUp(self):
        """Set up test data."""
        self.analyzer = IVTQCAnalyzer()
        
        self.sample_data = [
            {
                'sample_id': 'PASS-001',
                'concentration_ng_ul': 1500.0,  # 1.5 µg/µL - PASS
                'a260_280_ratio': 1.95,         # PASS
                'a260_230_ratio': 2.10,         # PASS
                'timestamp': '2024-07-07T10:00:00'
            },
            {
                'sample_id': 'FAIL-001',
                'concentration_ng_ul': 800.0,   # 0.8 µg/µL - FAIL
                'a260_280_ratio': 1.60,         # FAIL
                'a260_230_ratio': 1.50,         # WARNING
                'timestamp': '2024-07-07T10:00:00'
            },
            {
                'sample_id': 'WARN-001',
                'concentration_ng_ul': 1200.0,  # 1.2 µg/µL - PASS
                'a260_280_ratio': 2.30,         # WARNING
                'a260_230_ratio': None,         # WARNING - missing
                'timestamp': '2024-07-07T10:00:00'
            }
        ]
    
    def test_analyze_passing_sample(self):
        """Test analysis of a sample that passes all QC checks."""
        sample = self.sample_data[0]
        result = self.analyzer._analyze_single_sample(sample)
        
        self.assertEqual(result['qc_status'], 'PASS')
        self.assertEqual(len(result['qc_flags']), 0)
        self.assertEqual(result['concentration_ug_ul'], 1.5)
    
    def test_analyze_failing_sample(self):
        """Test analysis of a sample that fails QC checks."""
        sample = self.sample_data[1]
        result = self.analyzer._analyze_single_sample(sample)
        
        self.assertEqual(result['qc_status'], 'FAIL')
        self.assertGreater(len(result['qc_flags']), 0)
        
        # Check specific flags
        flag_text = ' '.join(result['qc_flags'])
        self.assertIn('Low concentration', flag_text)
        self.assertIn('Low A260/A280 ratio', flag_text)
    
    def test_analyze_warning_sample(self):
        """Test analysis of a sample with warnings."""
        sample = self.sample_data[2]
        result = self.analyzer._analyze_single_sample(sample)
        
        self.assertEqual(result['qc_status'], 'WARNING')
        self.assertGreater(len(result['qc_flags']), 0)
        
        # Check for specific warnings
        flag_text = ' '.join(result['qc_flags'])
        self.assertIn('High A260/A280 ratio', flag_text)
        self.assertIn('A260/A230 ratio not available', flag_text)
    
    def test_analyze_samples_summary(self):
        """Test analysis of multiple samples and summary generation."""
        results = self.analyzer.analyze_samples(self.sample_data)
        
        # Check summary statistics
        summary = results['summary']
        self.assertEqual(summary['total_samples'], 3)
        self.assertEqual(summary['passed'], 1)
        self.assertEqual(summary['failed'], 1)
        self.assertEqual(summary['warnings'], 1)
        self.assertAlmostEqual(summary['success_rate'], 33.33, places=1)
        
        # Check that QC limits are included
        self.assertIn('qc_limits', results)
        self.assertEqual(results['qc_limits']['min_concentration_ug_ul'], 1.0)


class TestQCReporter(unittest.TestCase):
    """Test QC reporting functionality."""
    
    def setUp(self):
        """Set up test data."""
        self.test_results = {
            'summary': {
                'total_samples': 2,
                'passed': 1,
                'failed': 1,
                'warnings': 0,
                'success_rate': 50.0,
                'analysis_timestamp': '2024-07-07T10:00:00'
            },
            'sample_results': [
                {
                    'sample_id': 'TEST-001',
                    'concentration_ng_ul': 1500.0,
                    'concentration_ug_ul': 1.5,
                    'a260_280_ratio': 1.95,
                    'a260_230_ratio': 2.10,
                    'qc_status': 'PASS',
                    'qc_flags': [],
                    'timestamp': '2024-07-07T10:00:00'
                },
                {
                    'sample_id': 'TEST-002',
                    'concentration_ng_ul': 800.0,
                    'concentration_ug_ul': 0.8,
                    'a260_280_ratio': 1.60,
                    'a260_230_ratio': 1.50,
                    'qc_status': 'FAIL',
                    'qc_flags': ['Low concentration: 0.800 µg/µL < 1.0 µg/µL'],
                    'timestamp': '2024-07-07T10:00:00'
                }
            ],
            'qc_limits': {
                'min_concentration_ug_ul': 1.0,
                'min_260_280_ratio': 1.8,
                'max_260_280_ratio': 2.2,
                'min_260_230_ratio': 1.8,
                'max_260_230_ratio': 2.5
            }
        }
    
    def test_generate_json_report(self):
        """Test JSON report generation."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as temp_file:
            temp_path = temp_file.name
        
        try:
            QCReporter.generate_json_report(self.test_results, temp_path)
            
            # Verify file was created and contains valid JSON
            self.assertTrue(os.path.exists(temp_path))
            
            with open(temp_path, 'r') as f:
                loaded_data = json.load(f)
            
            self.assertEqual(loaded_data['summary']['total_samples'], 2)
            self.assertEqual(len(loaded_data['sample_results']), 2)
            
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    def test_generate_markdown_summary(self):
        """Test markdown summary generation."""
        markdown = QCReporter.generate_markdown_summary(self.test_results)
        
        # Check that key elements are present
        self.assertIn('## IVT RNA QC Pipeline Results', markdown)
        self.assertIn('**Total Samples:** 2', markdown)
        self.assertIn('**Success Rate:** 50.0%', markdown)
        self.assertIn('| Sample ID | Status |', markdown)
        self.assertIn('TEST-001', markdown)
        self.assertIn('TEST-002', markdown)
        self.assertIn('✅ PASS', markdown)
        self.assertIn('❌ FAIL', markdown)
    
    def test_print_console_summary(self):
        """Test console summary printing."""
        # Capture stdout
        import io
        from contextlib import redirect_stdout
        
        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            QCReporter.print_console_summary(self.test_results)
        
        output = captured_output.getvalue()
        
        # Check that key information is present
        self.assertIn('IVT RNA QC PIPELINE SUMMARY REPORT', output)
        self.assertIn('Total Samples Analyzed: 2', output)
        self.assertIn('Success Rate: 50.0%', output)
        self.assertIn('TEST-001', output)
        self.assertIn('TEST-002', output)


class TestMainFunction(unittest.TestCase):
    """Test the main command-line interface."""
    
    def setUp(self):
        """Set up test CSV file."""
        self.test_csv_content = """Sample ID,Concentration,A260/A280,A260/A230
IVT-001,1500.0,1.95,2.10
IVT-002,800.0,1.60,1.50
"""
        
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv')
        self.temp_file.write(self.test_csv_content)
        self.temp_file.close()
    
    def tearDown(self):
        """Clean up temporary files."""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    @patch('sys.argv')
    def test_main_successful_run(self, mock_argv):
        """Test successful main function execution."""
        # Create temporary output file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as temp_output:
            temp_output_path = temp_output.name
        
        try:
            mock_argv.__getitem__.side_effect = [
                'ivt_qc_pipeline.py',     # Program name
                self.temp_file.name,      # CSV file
                '--output', temp_output_path,
                '--quiet'
            ]
            
            # Mock argparse to return our test arguments
            with patch('argparse.ArgumentParser.parse_args') as mock_parse_args:
                mock_args = type('Args', (), {
                    'csv_file': self.temp_file.name,
                    'output': temp_output_path,
                    'quiet': True,
                    'markdown': False
                })()
                mock_parse_args.return_value = mock_args
                
                # Run main function
                exit_code = main()
                
                # Should return 1 since we have failing samples
                self.assertEqual(exit_code, 1)
                
                # Check that output file was created
                self.assertTrue(os.path.exists(temp_output_path))
                
        finally:
            if os.path.exists(temp_output_path):
                os.unlink(temp_output_path)
    
    @patch('sys.argv')
    def test_main_file_not_found(self, mock_argv):
        """Test main function with non-existent file."""
        mock_argv.__getitem__.side_effect = [
            'ivt_qc_pipeline.py',
            'nonexistent_file.csv'
        ]
        
        with patch('argparse.ArgumentParser.parse_args') as mock_parse_args:
            mock_args = type('Args', (), {
                'csv_file': 'nonexistent_file.csv',
                'output': 'output.json',
                'quiet': True,
                'markdown': False
            })()
            mock_parse_args.return_value = mock_args
            
            exit_code = main()
            self.assertEqual(exit_code, 1)


def run_ivt_qc_tests():
    """Run all IVT QC pipeline tests."""
    print("Running IVT QC Pipeline tests...")
    
    # Create test suite
    test_classes = [
        TestQCLimits,
        TestNanoDropParser,
        TestIVTQCAnalyzer,
        TestQCReporter,
        TestMainFunction
    ]
    
    suite = unittest.TestSuite()
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    total_tests = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    passed = total_tests - failures - errors
    
    print(f"\n{'='*60}")
    print(f"IVT QC PIPELINE TEST SUMMARY")
    print(f"{'='*60}")
    print(f"Total tests: {total_tests}")
    print(f"Passed: {passed}")
    print(f"Failed: {failures}")
    print(f"Errors: {errors}")
    
    if failures == 0 and errors == 0:
        print(f"✅ All IVT QC tests passed!")
        return True
    else:
        print(f"❌ Some IVT QC tests failed.")
        return False


if __name__ == "__main__":
    success = run_ivt_qc_tests()
    sys.exit(0 if success else 1)