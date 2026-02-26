"""
Plugin de calculadora para a NENO IA
"""
import math
import re
from typing import Dict, Any

class CalculatorPlugin:
    def execute(self, expression: str) -> Dict[str, Any]:
        """Executa cálculo matemático"""
        try:
            # Limpa e valida a expressão
            expression = self._sanitize_expression(expression)
            
            # Avalia a expressão com math functions disponíveis
            result = eval(expression, {"__builtins__": None}, {
                "abs": abs, "round": round, "min": min, "max": max,
                "sum": sum, "pow": pow, "sqrt": math.sqrt,
                "sin": math.sin, "cos": math.cos, "tan": math.tan,
                "log": math.log, "log10": math.log10, "exp": math.exp,
                "pi": math.pi, "e": math.e
            })
            
            return {
                "expression": expression,
                "result": result,
                "formatted": f"{result:,.2f}" if isinstance(result, (int, float)) else str(result)
            }
            
        except Exception as e:
            return {"error": f"Erro no cálculo: {str(e)}"}
    
    def _sanitize_expression(self, expression: str) -> str:
        """Sanitiza a expressão matemática"""
        # Remove caracteres potencialmente perigosos
        expression = re.sub(r'[^0-9+\-*/().\s^%πesincotagl]', '', expression)
        
        # Substitui símbolos comuns
        expression = expression.replace('^', '**').replace('π', 'pi')
        
        # Adiciona multiplicação implícita (ex: 2π → 2*pi)
        expression = re.sub(r'(\d)([a-zA-Zπ])', r'\1*\2', expression)
        expression = re.sub(r'([a-zA-Zπ])(\d)', r'\1*\2', expression)
        
        return expression.strip()

def register():
    return CalculatorPlugin()
