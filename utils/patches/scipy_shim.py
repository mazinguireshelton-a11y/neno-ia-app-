"""
Shim completo para scipy.integrate
"""
class MockOdeResult:
    def __init__(self):
        self.t = [0, 1]
        self.y = [[0], [0]]
        self.success = True

class MockIntegrate:
    def odeint(self, func, y0, t, args=()):
        return [y0] * len(t)
    
    def solve_ivp(self, func, t_span, y0, method='RK45', **kwargs):
        return MockOdeResult()
    
    def quad(self, func, a, b, **kwargs):
        return (0, 0)

# Criar módulo mock
integrate_module = MockIntegrate()

# Tornar disponível globalmente
import sys
sys.modules['scipy.integrate'] = integrate_module
integrate = integrate_module
