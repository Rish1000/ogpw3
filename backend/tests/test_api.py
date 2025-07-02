import unittest
import json
import tempfile
import os
from app import app

class TestOGPWAPI(unittest.TestCase):
    def setUp(self):
        """Set up test client"""
        self.app = app.test_client()
        self.app.testing = True

    def test_health_check(self):
        """Test health check endpoint"""
        response = self.app.get('/api/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')

    def test_upload_no_file(self):
        """Test upload endpoint with no file"""
        response = self.app.post('/api/upload')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_upload_invalid_file(self):
        """Test upload endpoint with invalid file"""
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as tmp:
            tmp.write(b'test content')
            tmp_path = tmp.name

        try:
            with open(tmp_path, 'rb') as test_file:
                response = self.app.post('/api/upload', 
                    data={'file': (test_file, 'test.txt')})
            self.assertEqual(response.status_code, 400)
        finally:
            os.unlink(tmp_path)

    def test_chat_no_analysis(self):
        """Test chat endpoint with no analysis data"""
        response = self.app.post('/api/chat', 
            data=json.dumps({'message': 'test'}),
            content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_current_analysis_no_data(self):
        """Test current analysis endpoint with no data"""
        response = self.app.get('/api/analysis/current')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()