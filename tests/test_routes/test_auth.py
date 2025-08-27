import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from backend.app import create_app

class AuthTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def test_login_missing_fields(self):
        """Teste de login com campos faltantes"""
        response = self.client.post('/api/auth/login', json={})
        self.assertEqual(response.status_code, 400)
    
    def test_login_invalid_credentials(self):
        """Teste de login com credenciais inválidas"""
        response = self.client.post('/api/auth/login', json={
            'email': 'invalid@email.com',
            'password': 'wrongpassword'
        })
        # Deve retornar 401 ou 400, não 500
        self.assertIn(response.status_code, [400, 401])
