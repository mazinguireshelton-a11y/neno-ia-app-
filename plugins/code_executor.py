"""
Plugin de execução de código seguro para a NENO IA
"""
import subprocess
import tempfile
import os
from typing import Dict, List
import docker

class CodeExecutorPlugin:
    def __init__(self):
        self.docker_client = None
        try:
            self.docker_client = docker.from_env()
        except:
            pass
    
    def execute(self, code: str, language: str = "python") -> Dict:
        """Executa código em ambiente seguro"""
        try:
            if language == "python":
                return self._execute_python(code)
            elif language == "javascript":
                return self._execute_javascript(code)
            elif language == "bash":
                return self._execute_bash(code)
            else:
                return {"error": f"Linguagem {language} não suportada"}
                
        except Exception as e:
            return {"error": f"Erro na execução: {str(e)}"}
    
    def _execute_python(self, code: str) -> Dict:
        """Executa código Python em container Docker seguro"""
        if not self.docker_client:
            return self._execute_python_local(code)
        
        try:
            # Cria container temporário
            container = self.docker_client.containers.run(
                "python:3.9-slim",
                command=["python", "-c", code],
                detach=True,
                mem_limit="100m",
                cpu_period=100000,
                cpu_quota=50000,
                network_mode="none"
            )
            
            # Aguarda execução
            result = container.wait()
            output = container.logs().decode('utf-8')
            container.remove()
            
            return {
                "exit_code": result["StatusCode"],
                "output": output,
                "truncated": len(output) > 1000
            }
            
        except Exception as e:
            return {"error": f"Erro Docker: {str(e)}"}
    
    def _execute_python_local(self, code: str) -> Dict:
        """Fallback para execução local (menos seguro)"""
        try:
            result = subprocess.run(
                ["python", "-c", code],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            return {
                "exit_code": result.returncode,
                "output": result.stdout,
                "error": result.stderr,
                "truncated": len(result.stdout) > 1000
            }
            
        except subprocess.TimeoutExpired:
            return {"error": "Timeout: código executou por muito tempo"}
        except Exception as e:
            return {"error": f"Erro local: {str(e)}"}

def register():
    return CodeExecutorPlugin()
