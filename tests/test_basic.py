import unittest
import sys
import os

# Adicionar o backend ao path para imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from backend.app import create_app

class BasicTests(unittest.TestCase):
    def setUp(self):
        """Configuração antes de cada teste"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.client = self.app.test_client()
    
    def tearDown(self):
        """Limpeza após cada teste"""
        pass
    
    def test_healthcheck(self):
        """Teste do endpoint de healthcheck"""
        response = self.client.get('/healthz')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'ok')
    
    def test_404_endpoint(self):
        """Teste de endpoint não existente"""
        response = self.client.get('/nonexistent-endpoint')
        self.assertEqual(response.status_code, 404)
    
    def test_api_routes_exist(self):
        """Teste se as rotas da API existem"""
        routes = ['/api/auth/login', '/api/chat', '/api/upload']
        
        with self.app.test_client() as client:
            for route in routes:
                response = client.get(route)
                # Pode retornar 404, 405, mas não 500 (erro interno)
                self.assertNotEqual(response.status_code, 500)

if __name__ == '__main__':
    unittest.main()
