import unittest
from unittest.mock import patch, MagicMock
from backend.services.cooperative_orchestrator import CooperativeOrchestrator

class TestCooperativeSystem(unittest.TestCase):
    
    def setUp(self):
        # Mock do LLM Service
        self.mock_llm_service = MagicMock()
        self.orchestrator = CooperativeOrchestrator(self.mock_llm_service)
    
    def test_complexity_analysis_simple(self):
        """Testa análise de complexidade para prompt simples"""
        prompt = "Olá, como você está?"
        analysis = self.orchestrator.analyze_complexity(prompt)
        
        self.assertFalse(analysis["needs_cooperation"])
        self.assertLess(analysis["complexity_score"], 100)
    
    def test_complexity_analysis_complex(self):
        """Testa análise de complexidade para prompt complexo"""
        prompt = """
        Escreva um ebook completo de 100 páginas sobre inteligência artificial 
        com 10 capítulos detalhados, incluindo exemplos práticos, estudos de caso,
        e exercícios para cada capítulo. O ebook deve cobrir desde conceitos básicos
        até aplicações avançadas de deep learning e redes neurais.
        """
        analysis = self.orchestrator.analyze_complexity(prompt)
        
        self.assertTrue(analysis["needs_cooperation"])
        self.assertGreater(analysis["complexity_score"], 500)
        self.assertEqual(analysis["recommended_workers"], 3)
    
    def test_task_division(self):
        """Testa divisão de tarefas complexas"""
        prompt = "Escreva um livro sobre machine learning com 5 capítulos"
        subtasks = self.orchestrator.divide_task(prompt, 3)
        
        self.assertEqual(len(subtasks), 3)
        self.assertTrue(all('task' in task for task in subtasks))
        self.assertTrue(all('role' in task for task in subtasks))
    
    @patch('concurrent.futures.ThreadPoolExecutor')
    def test_parallel_execution(self, mock_executor):
        """Testa execução paralela de subtasks"""
        # Configurar mock
        mock_future = MagicMock()
        mock_future.result.return_value = {"content": "Resultado teste"}
        mock_executor.return_value.__enter__.return_value.submit.return_value = mock_future
        
        subtasks = [
            {"task": "Subtarefa 1", "role": "pesquisador"},
            {"task": "Subtarefa 2", "role": "escritor"}
        ]
        
        results = self.orchestrator._execute_parallel_blocking(subtasks)
        
        self.assertEqual(len(results), 2)
        self.assertTrue(all(result["success"] for result in results))

if __name__ == '__main__':
    unittest.main()
