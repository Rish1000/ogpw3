import unittest
import tempfile
import os
from pcap_analyzer import PcapAnalyzer

class TestPcapAnalyzer(unittest.TestCase):
    def setUp(self):
        """Set up test analyzer"""
        self.analyzer = PcapAnalyzer()

    def test_analyzer_initialization(self):
        """Test analyzer initializes correctly"""
        self.assertIsInstance(self.analyzer, PcapAnalyzer)
        self.assertEqual(len(self.analyzer.packets), 0)

    def test_invalid_file_analysis(self):
        """Test analysis with invalid file"""
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as tmp:
            tmp.write(b'invalid pcap content')
            tmp_path = tmp.name

        try:
            with self.assertRaises(Exception):
                self.analyzer.analyze_pcap(tmp_path)
        finally:
            os.unlink(tmp_path)

    def test_filter_by_protocol_invalid(self):
        """Test filtering with invalid protocol"""
        with self.assertRaises(ValueError):
            self.analyzer.filter_by_protocol({}, 'INVALID')

if __name__ == '__main__':
    unittest.main()