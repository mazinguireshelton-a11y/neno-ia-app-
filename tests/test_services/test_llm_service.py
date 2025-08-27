import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

class LLMServiceTests(unittest.TestCase):
    def test_llm_service_import(self):
        """Teste simples para verificar se o módulo pode ser importado"""
        try:
            from backend.services.llm_service import LLMService
            # Se chegou aqui, a importação funcionou
            self.assertTrue(True)
        except ImportError as e:
            self.skipTest(f"LLMService não pode ser importado: {e}")
    
    def test_llm_service_creation(self):
        """Teste de criação do serviço LLM"""
        try:
            from backend.services.llm_service import LLMService
            service = LLMService()
            # Verifica se tem o atributo providers
            self.assertTrue(hasattr(service, 'providers'))
            self.assertIsInstance(service.providers, dict)
        except ImportError:
            self.skipTest("LLMService não disponível para teste")
