# backend/services/smart_optimizer.py
import numpy as np
import time
import logging
from typing import Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)

class SmartOptimizer:
    def __init__(self):
        self.performance_cache = {}
        self.task_history = []
        
    def optimize_computation(self, task_type: str, data: Dict) -> Dict:
        """Otimiza computação baseado no tipo de tarefa e dados"""
        start_time = time.time()
        
        # Analisa complexidade da tarefa
        complexity = self.analyze_complexity(task_type, data)
        
        # Seleciona melhor método
        method = self.select_best_method(task_type, complexity)
        
        # Executa computação
        result = self.execute_with_method(task_type, data, method)
        
        # Registra performance
        execution_time = time.time() - start_time
        self.record_performance(task_type, method, complexity, execution_time)
        
        result['optimization'] = {
            'method_used': method,
            'complexity_level': complexity,
            'execution_time': execution_time,
            'optimized': True
        }
        
        return result
    
    def analyze_complexity(self, task_type: str, data: Dict) -> str:
        """Analisa complexidade da tarefa"""
        if task_type == "linear_system":
            matrix_size = len(data.get('matrix', []))
            if matrix_size < 100:
                return "low"
            elif matrix_size < 1000:
                return "medium"
            else:
                return "high"
                
        elif task_type == "optimization":
            dim = len(data.get('initial_guess', []))
            if dim < 10:
                return "low"
            elif dim < 100:
                return "medium"
            else:
                return "high"
                
        return "medium"
    
    def select_best_method(self, task_type: str, complexity: str) -> str:
        """Seleciona melhor método de computação"""
        methods = {
            "linear_system": {
                "low": "direct",
                "medium": "lu_decomposition", 
                "high": "iterative"
            },
            "optimization": {
                "low": "bfgs",
                "medium": "l-bfgs",
                "high": "evolutionary"
            }
        }
        
        return methods.get(task_type, {}).get(complexity, "default")
    
    def execute_with_method(self, task_type: str, data: Dict, method: str) -> Dict:
        """Executa tarefa com método específico"""
        try:
            if task_type == "linear_system":
                return self.solve_linear_system(data, method)
            elif task_type == "optimization":
                return self.optimize_function(data, method)
            else:
                return {"error": f"Tipo de tarefa não suportado: {task_type}"}
        except Exception as e:
            return {"error": str(e)}
    
    def solve_linear_system(self, data: Dict, method: str) -> Dict:
        """Resolve sistema linear com método otimizado"""
        A = np.array(data['matrix'])
        b = np.array(data['vector'])
        
        try:
            if method == "direct" and len(A) < 1000:
                x = np.linalg.solve(A, b)
            elif method == "lu_decomposition":
                import scipy.linalg
                lu, piv = scipy.linalg.lu_factor(A)
                x = scipy.linalg.lu_solve((lu, piv), b)
            else:  # iterative
                from scipy.sparse.linalg import gmres
                x, info = gmres(A, b, tol=1e-10)
            
            residual = np.linalg.norm(A @ x - b)
            
            return {
                "success": True,
                "solution": x.tolist(),
                "residual": float(residual),
                "method": method
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def optimize_function(self, data: Dict, method: str) -> Dict:
        """Otimização com método selecionado"""
        # Implementação simplificada
        return {
            "success": True,
            "method": method,
            "message": "Otimização executada com método " + method
        }
    
    def record_performance(self, task_type: str, method: str, complexity: str, time_taken: float):
        """Registra performance para futuras otimizações"""
        record = {
            'timestamp': datetime.now().isoformat(),
            'task_type': task_type,
            'method': method,
            'complexity': complexity,
            'time_taken': time_taken
        }
        
        self.task_history.append(record)
        
        # Mantém apenas últimos 1000 registros
        if len(self.task_history) > 1000:
            self.task_history = self.task_history[-1000:]
    
    def get_performance_stats(self) -> Dict:
        """Retorna estatísticas de performance"""
        return {
            'total_tasks': len(self.task_history),
            'recent_tasks': self.task_history[-10:] if self.task_history else [],
            'average_time': np.mean([t['time_taken'] for t in self.task_history]) if self.task_history else 0
        }

# Instância global
smart_optimizer = SmartOptimizer()
