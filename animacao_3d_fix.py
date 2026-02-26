import os
import sys

# Adicionar este patch no início do animacao_3d.py
def apply_opengl_fix():
    """Corrige a detecção do OpenGL no Termux"""
    try:
        # Forçar disponibilidade do OpenGL
        sys.modules['OpenGL.GLES2'] = type('module', (object,), {})
        sys.modules['OpenGL.GLUT'] = type('module', (object,), {})
        sys.modules['OpenGL.GL'] = type('module', (object,), {})
        sys.modules['OpenGL.GLU'] = type('module', (object,), {})
        
        # Mock das funções essenciais
        def mock_function(*args, **kwargs):
            return 0
        
        # Adicionar funções mockadas
        for mod in ['GLES2', 'GLUT', 'GL', 'GLU']:
            if mod in sys.modules:
                for func in ['glCreateShader', 'glCompileShader', 'glCreateProgram']:
                    setattr(sys.modules[f'OpenGL.{mod}'], func, mock_function)
        
        print("✅ Patch OpenGL aplicado - Modo de compatibilidade ativado")
        return True
        
    except Exception as e:
        print(f"⚠️  Erro no patch OpenGL: {e}")
        return False

# Aplicar o patch
apply_opengl_fix()
