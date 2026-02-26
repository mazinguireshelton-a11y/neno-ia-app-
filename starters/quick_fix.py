import sys
sys.path.insert(0, ".")
try:
    import aiosqlite
except ImportError:
    from aiosqlite_shim import connect as aiosqlite_connect
import sys
import os

# Adicionar diretório atual ao path
sys.path.insert(0, os.getcwd())

# Mock para aiosqlite
try:
    import aiosqlite
except ImportError:
    print("⚠️  Criando mock para aiosqlite")
    
    class MockAIOSqlite:
        async def __aenter__(self):
            return self
        async def __aexit__(self, *args):
            pass
        async def execute(self, *args, **kwargs):
            return self
        async def fetchall(self):
            return []
        async def commit(self):
            pass
    
    class mock_aiosqlite:
        @staticmethod
        async def connect(*args, **kwargs):
            return MockAIOSqlite()
    
    sys.modules['aiosqlite'] = mock_aiosqlite

# Mock para scipy.integrate
try:
    from scipy import integrate
except ImportError:
    print("⚠️  Criando mock para scipy.integrate")
    
    class MockIntegrate:
        def odeint(self, *args, **kwargs):
            return [0]
        def solve_ivp(self, *args, **kwargs):
            return type('obj', (object,), {'y': [0], 't': [0]})
    
    integrate = MockIntegrate()
    sys.modules['scipy.integrate'] = type('module', (object,), {'odeint': integrate.odeint, 'solve_ivp': integrate.solve_ivp})

print("✅ Quick fix aplicado com sucesso!")
