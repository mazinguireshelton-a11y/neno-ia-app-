"""
Shim definitivo para aiosqlite
"""
import asyncio

class MockConnection:
    async def __aenter__(self):
        return self
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass
    async def execute(self, query, params=None):
        print(f"📝 Executando query: {query}")
        return self
    async def fetchall(self):
        return []
    async def commit(self):
        pass
    async def close(self):
        pass

class MockAIOSqlite:
    @staticmethod
    async def connect(database):
        print(f"🔗 Conectando ao banco: {database}")
        return MockConnection()

# Tornar disponível globalmente
import sys
sys.modules['aiosqlite'] = MockAIOSqlite
connect = MockAIOSqlite.connect
