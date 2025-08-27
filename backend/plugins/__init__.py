"""
Package de plugins da NENO IA
"""
from .web_search import WebSearchPlugin
from .calculator import CalculatorPlugin
from .code_executor import CodeExecutorPlugin
from .image_generator import ImageGeneratorPlugin

__all__ = [
    'WebSearchPlugin',
    'CalculatorPlugin', 
    'CodeExecutorPlugin',
    'ImageGeneratorPlugin'
]
