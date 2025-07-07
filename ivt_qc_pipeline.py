#!/usr/bin/env python3
"""
IVT RNA QC Pipeline - Automated Quality Control for In Vitro Transcribed RNA

This module provides automated quality control analysis for IVT RNA samples,
processing NanoDrop absorbance data to calculate concentration and purity ratios,
and flagging samples outside acceptance limits.

Author: AI Assistant
Date: 2024
"""

import json
import csv
import sys
import argparse
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class QCLimits:
    """QC acceptance limits for IVT RNA samples."""
    MIN_CONCENTRATION = 1.0  # µg/µL
    MIN_260_280_RATIO = 1.8  # Minimum A260/A280 ratio
    MAX_260_280_RATIO = 2.2  # Maximum A260/A280 ratio
    MIN_260_230_RATIO = 1.8  # Minimum A260/A230 ratio
    MAX_260_230_RATIO = 2.5  # Maximum A260/A230 ratio


class NanoDropParser:
    """Parser for NanoDrop CSV export files."""

    def __init__(self, csv_path: str):
        self.csv_path = Path(csv_path)
        if not self.csv_path.exists():
            raise FileNotFoundError(f"CSV file not found: {csv_path}")

    def parse_nanodrop_csv(self) -> List[Dict[str, Any]]:
        """Parse NanoDrop CSV file and extract sample data."""
        samples = []

        try:
            with open(self.csv_path, 'r', encoding='utf-8') as file:
                # Skip header lines until we find the data table
                content = file.read()
                lines = content.strip().split('\n')

                # Find the data table header
                data_start_idx = None
                for i, line in enumerate(lines):
                    if 'Sample ID' in line or 'Sample Name' in line:
                        data_start_idx = i
                        break

                if data_start_idx is None:
                    raise ValueError("Could not find data table in CSV file")

                # Parse CSV data starting from the header
                csv_reader = csv.DictReader(lines[data_start_idx:])

                for row in csv_reader:
                    # Skip empty rows
                    if not any(row.values()):
                        continue

                    # Extract sample data with flexible column name matching
                    sample_data = self._extract_sample_data(row)
                    if sample_data:
                        samples.append(sample_data)

        except Exception as e:
            logger.error(f"Error parsing NanoDrop CSV: {e}")
            raise

        logger.info(f"Successfully parsed {len(samples)} samples from {self.csv_path}")
        return samples

    def _extract_sample_data(self, row: Dict[str, str]) -> Optional[Dict[str, Any]]:
        """Extract and validate sample data from CSV row."""
        try:
            # Flexible column name matching
            sample_id = self._find_column_value(row, ['Sample ID', 'Sample Name', 'Sample', 'ID'])
            concentration = self._find_column_value(row, ['Concentration', 'Conc', 'ng/µL', 'ng/uL'])
            a260_280 = self._find_column_value(row, ['A260/A280', '260/280', 'A260/280'])
            a260_230 = self._find_column_value(row, ['A260/A230', '260/230', 'A260/230'])

            # Convert to appropriate types
            if concentration:
                concentration = float(concentration.replace(',', '.'))
            if a260_280:
                a260_280 = float(a260_280.replace(',', '.'))
            if a260_230:
                a260_230 = float(a260_230.replace(',', '.'))

            # Validate required fields
            if not sample_id or concentration is None:
                return None

            return {
                'sample_id': sample_id,
                'concentration_ng_ul': concentration,
                'a260_280_ratio': a260_280,
                'a260_230_ratio': a260_230,
                'timestamp': datetime.now().isoformat()
            }

        except (ValueError, TypeError) as e:
            logger.warning(f"Error processing sample row: {e}")
            return None

    def _find_column_value(self, row: Dict[str, str], possible_names: List[str]) -> Optional[str]:
        """Find column value by trying multiple possible column names."""
        for name in possible_names:
            # Try exact match first
            if name in row and row[name]:
                return row[name].strip()

            # Try case-insensitive match
            for col_name in row.keys():
                if col_name.lower() == name.lower() and row[col_name]:
                    return row[col_name].strip()

        return None


class IVTQCAnalyzer:
    """Main QC analyzer for IVT RNA samples."""

    def __init__(self, limits: QCLimits = None):
        self.limits = limits or QCLimits()
        self.results = []

    def analyze_samples(self, samples: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze all samples and generate QC results."""
        analysis_results = []
        summary_stats = {
            'total_samples': len(samples),
            'passed': 0,
            'failed': 0,
            'warnings': 0,
            'analysis_timestamp': datetime.now().isoformat()
        }

        for sample in samples:
            result = self._analyze_single_sample(sample)
            analysis_results.append(result)

            # Update summary statistics
            status = result['qc_status']
            if status == 'PASS':
                summary_stats['passed'] += 1
            elif status == 'FAIL':
                summary_stats['failed'] += 1
            elif status == 'WARNING':
                summary_stats['warnings'] += 1

        # Calculate success rate
        if summary_stats['total_samples'] > 0:
            summary_stats['success_rate'] = (summary_stats['passed'] / summary_stats['total_samples']) * 100
        else:
            summary_stats['success_rate'] = 0.0

        return {
            'summary': summary_stats,
            'sample_results': analysis_results,
            'qc_limits': {
                'min_concentration_ug_ul': self.limits.MIN_CONCENTRATION,
                'min_260_280_ratio': self.limits.MIN_260_280_RATIO,
                'max_260_280_ratio': self.limits.MAX_260_280_RATIO,
                'min_260_230_ratio': self.limits.MIN_260_230_RATIO,
                'max_260_230_ratio': self.limits.MAX_260_230_RATIO
            }
        }

    def _analyze_single_sample(self, sample: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze a single sample for QC compliance."""
        sample_id = sample['sample_id']
        concentration_ng_ul = sample['concentration_ng_ul']
        a260_280 = sample.get('a260_280_ratio')
        a260_230 = sample.get('a260_230_ratio')

        # Convert concentration from ng/µL to µg/µL
        concentration_ug_ul = concentration_ng_ul / 1000.0

        # Initialize QC flags
        qc_flags = []
        qc_status = 'PASS'

        # Check concentration
        if concentration_ug_ul < self.limits.MIN_CONCENTRATION:
            qc_flags.append(f"Low concentration: {concentration_ug_ul:.3f} µg/µL < {self.limits.MIN_CONCENTRATION} µg/µL")
            qc_status = 'FAIL'

        # Check A260/A280 ratio
        if a260_280 is not None:
            if a260_280 < self.limits.MIN_260_280_RATIO:
                qc_flags.append(f"Low A260/A280 ratio: {a260_280:.2f} < {self.limits.MIN_260_280_RATIO}")
                qc_status = 'FAIL'
            elif a260_280 > self.limits.MAX_260_280_RATIO:
                qc_flags.append(f"High A260/A280 ratio: {a260_280:.2f} > {self.limits.MAX_260_280_RATIO}")
                if qc_status == 'PASS':
                    qc_status = 'WARNING'
        else:
            qc_flags.append("A260/A280 ratio not available")
            if qc_status == 'PASS':
                qc_status = 'WARNING'

        # Check A260/A230 ratio
        if a260_230 is not None:
            if a260_230 < self.limits.MIN_260_230_RATIO:
                qc_flags.append(f"Low A260/A230 ratio: {a260_230:.2f} < {self.limits.MIN_260_230_RATIO}")
                if qc_status == 'PASS':
                    qc_status = 'WARNING'
            elif a260_230 > self.limits.MAX_260_230_RATIO:
                qc_flags.append(f"High A260/A230 ratio: {a260_230:.2f} > {self.limits.MAX_260_230_RATIO}")
                if qc_status == 'PASS':
                    qc_status = 'WARNING'
        else:
            qc_flags.append("A260/A230 ratio not available")

        return {
            'sample_id': sample_id,
            'concentration_ng_ul': concentration_ng_ul,
            'concentration_ug_ul': concentration_ug_ul,
            'a260_280_ratio': a260_280,
            'a260_230_ratio': a260_230,
            'qc_status': qc_status,
            'qc_flags': qc_flags,
            'timestamp': sample['timestamp']
        }


class QCReporter:
    """Generate QC reports in various formats."""

    @staticmethod
    def generate_json_report(results: Dict[str, Any], output_path: str = "qc_results.json"):
        """Generate JSON report file."""
        try:
            with open(output_path, 'w') as f:
                json.dump(results, f, indent=2)
            logger.info(f"JSON report saved to {output_path}")
        except Exception as e:
            logger.error(f"Error saving JSON report: {e}")
            raise

    @staticmethod
    def generate_markdown_summary(results: Dict[str, Any]) -> str:
        """Generate markdown summary for GitHub issue comments."""
        summary = results['summary']
        sample_results = results['sample_results']

        # Create markdown table
        md_content = f"""## IVT RNA QC Pipeline Results

**Analysis Date:** {summary['analysis_timestamp']}
**Total Samples:** {summary['total_samples']}
**Success Rate:** {summary['success_rate']:.1f}%

### Summary
- ✅ **Passed:** {summary['passed']} samples
- ⚠️ **Warnings:** {summary['warnings']} samples
- ❌ **Failed:** {summary['failed']} samples

### Sample Results
| Sample ID | Status | Concentration (µg/µL) | A260/A280 | A260/A230 | QC Flags |
|-----------|--------|----------------------|-----------|-----------|----------|
"""

        for sample in sample_results:
            status_emoji = {
                'PASS': '✅',
                'WARNING': '⚠️',
                'FAIL': '❌'
            }.get(sample['qc_status'], '❓')

            flags_str = '; '.join(sample['qc_flags']) if sample['qc_flags'] else 'None'
            if len(flags_str) > 50:
                flags_str = flags_str[:47] + '...'

            md_content += f"| {sample['sample_id']} | {status_emoji} {sample['qc_status']} | {sample['concentration_ug_ul']:.3f} | {sample.get('a260_280_ratio', 'N/A')} | {sample.get('a260_230_ratio', 'N/A')} | {flags_str} |\n"

        md_content += f"""
### QC Limits Applied
- **Minimum Concentration:** {results['qc_limits']['min_concentration_ug_ul']} µg/µL
- **A260/A280 Ratio:** {results['qc_limits']['min_260_280_ratio']}-{results['qc_limits']['max_260_280_ratio']}
- **A260/A230 Ratio:** {results['qc_limits']['min_260_230_ratio']}-{results['qc_limits']['max_260_230_ratio']}

---
*Generated by IVT RNA QC Pipeline*
"""

        return md_content

    @staticmethod
    def print_console_summary(results: Dict[str, Any]):
        """Print formatted summary to console."""
        summary = results['summary']

        print("="*60)
        print("IVT RNA QC PIPELINE SUMMARY REPORT")
        print("="*60)
        print(f"Total Samples Analyzed: {summary['total_samples']}")
        print(f"Passed: {summary['passed']}")
        print(f"Warnings: {summary['warnings']}")
        print(f"Failed: {summary['failed']}")
        print(f"Success Rate: {summary['success_rate']:.1f}%")
        print()

        print("DETAILED RESULTS:")
        print("-"*60)

        for sample in results['sample_results']:
            status_color = {
                'PASS': '\033[92m',    # Green
                'WARNING': '\033[93m', # Yellow
                'FAIL': '\033[91m',    # Red
            }.get(sample['qc_status'], '')
            reset_color = '\033[0m'

            print(f"{sample['sample_id']:<20} | {status_color}{sample['qc_status']:<8}{reset_color} | "
                  f"Conc: {sample['concentration_ug_ul']:.3f} µg/µL | "
                  f"A260/280: {sample.get('a260_280_ratio', 'N/A'):<5} | "
                  f"A260/230: {sample.get('a260_230_ratio', 'N/A'):<5}")

        print("="*60)


def main():
    """Main function for command-line usage."""
    parser = argparse.ArgumentParser(description="IVT RNA QC Pipeline")
    parser.add_argument("csv_file", help="Path to NanoDrop CSV file")
    parser.add_argument("--output", "-o", default="qc_results.json",
                       help="Output JSON file path (default: qc_results.json)")
    parser.add_argument("--quiet", "-q", action="store_true",
                       help="Suppress console output")
    parser.add_argument("--markdown", "-m", action="store_true",
                       help="Generate markdown summary to stdout")

    args = parser.parse_args()

    try:
        # Parse NanoDrop CSV
        parser_obj = NanoDropParser(args.csv_file)
        samples = parser_obj.parse_nanodrop_csv()

        if not samples:
            logger.error("No valid samples found in CSV file")
            return 1

        # Analyze samples
        analyzer = IVTQCAnalyzer()
        results = analyzer.analyze_samples(samples)

        # Generate JSON report
        QCReporter.generate_json_report(results, args.output)

        # Generate outputs
        if args.markdown:
            print(QCReporter.generate_markdown_summary(results))
        elif not args.quiet:
            QCReporter.print_console_summary(results)

        # Return appropriate exit code
        if results['summary']['failed'] > 0:
            return 1
        else:
            return 0

    except Exception as e:
        logger.error(f"QC pipeline failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
