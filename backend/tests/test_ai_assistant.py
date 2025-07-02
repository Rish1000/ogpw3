import unittest
from ai_assistant import AIAssistant

class TestAIAssistant(unittest.TestCase):
    def setUp(self):
        """Set up test assistant"""
        self.assistant = AIAssistant()

    def test_assistant_initialization(self):
        """Test assistant initializes correctly"""
        self.assertIsInstance(self.assistant, AIAssistant)

    def test_fallback_response_basic_stats(self):
        """Test fallback response for basic stats query"""
        analysis_data = {
            'basic_stats': {
                'total_packets': 1000,
                'total_bytes': 50000,
                'duration_seconds': 60
            }
        }
        
        response = self.assistant._process_with_fallback(
            "How many packets?", analysis_data)
        self.assertIn('1000', response)
        self.assertIn('packets', response.lower())

    def test_fallback_response_help(self):
        """Test fallback response for help query"""
        response = self.assistant._process_with_fallback("help", {})
        self.assertIn('analyze', response.lower())
        self.assertIn('traffic', response.lower())

if __name__ == '__main__':
    unittest.main()