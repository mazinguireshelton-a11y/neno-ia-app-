# grpc.py (stub) — evita ModuleNotFoundError em Termux quando grpcio não está instalado
# Se você realmente precisar de grpcio, instale em um ambiente com suporte (PC / Docker)
import types, sys
grpc = types.ModuleType("grpc")
grpc.__version__ = "0.0.0-termux-stub"
def _missing(*a, **k):
    raise RuntimeError("grpc is not available in this Termux environment. Install grpcio on a proper Linux/PC if needed.")
class _Missing(types.ModuleType):
    def __getattr__(self, name):
        return lambda *a, **k: _missing(*a, **k)
grpc._channel = _Missing("grpc._channel")
grpc.aio = _Missing("grpc.aio")
sys.modules['grpc'] = grpc
sys.modules['grpc._channel'] = grpc._channel
sys.modules['grpc.aio'] = grpc.aio
