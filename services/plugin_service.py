# backend/services/plugin_service.py
"""
Sistema de plugins para funcionalidades estendidas
"""
from typing import Dict, List, Callable, Any
import importlib
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class PluginService:
    def __init__(self):
        self.plugins = {}
        self.load_builtin_plugins()
        
    def load_builtin_plugins(self):
        """Carrega plugins embutidos"""
        builtin_plugins = {
            "web_search": "backend.plugins.web_search",
            "calculator": "backend.plugins.calculator",
            "code_executor": "backend.plugins.code_executor",
            "image_generator": "backend.plugins.image_generator",
            "physics": "backend.plugins.physics_plugin"  # ✅ NOVO PLUGIN
        }
        
        for name, module_path in builtin_plugins.items():
            try:
                module = importlib.import_module(module_path)
                if hasattr(module, "register"):
                    self.plugins[name] = module.register()
                    logger.info(f"Plugin carregado: {name}")
                else:
                    # Para o plugin de física que usa classe diretamente
                    if hasattr(module, "PhysicsPlugin"):
                        self.plugins[name] = module.PhysicsPlugin()
                        logger.info(f"Plugin carregado (classe direta): {name}")
            except ImportError as e:
                logger.warning(f"Erro ao carregar plugin {name}: {e}")
            except Exception as e:
                logger.error(f"Erro inesperado ao carregar plugin {name}: {e}")
                
    def execute_plugin(self, plugin_name: str, **kwargs) -> Any:
        """Executa um plugin específico"""
        if plugin_name not in self.plugins:
            raise ValueError(f"Plugin {plugin_name} não encontrado")
            
        try:
            return self.plugins[plugin_name].execute(**kwargs)
        except Exception as e:
            logger.error(f"Erro ao executar plugin {plugin_name}: {e}")
            return {"error": f"Erro no plugin {plugin_name}: {str(e)}"}
        
    def get_available_plugins(self) -> List[str]:
        """Retorna lista de plugins disponíveis"""
        return list(self.plugins.keys())
    
    def get_plugin_info(self, plugin_name: str) -> Dict:
        """Retorna informações sobre um plugin"""
        if plugin_name not in self.plugins:
            return {"error": "Plugin não encontrado"}
        
        plugin = self.plugins[plugin_name]
        return {
            "name": plugin_name,
            "description": getattr(plugin, "description", "Sem descrição"),
            "version": getattr(plugin, "version", "1.0.0"),
            "author": getattr(plugin, "author", "NENO Team")
        }

    # ✅ NOVO MÉTODO para compatibilidade com ModeManager
    def execute(self, plugin_name: str, command: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Interface uniforme para execução de plugins"""
        if plugin_name not in self.plugins:
            return {"error": f"Plugin '{plugin_name}' não encontrado"}
        
        try:
            # Para plugins com método execute que aceita command e params
            if hasattr(self.plugins[plugin_name], 'execute'):
                result = self.plugins[plugin_name].execute(command, params)
                return result
            else:
                return {"error": f"Plugin '{plugin_name}' não suporta execução por comando"}
        except Exception as e:
            logger.error(f"Erro ao executar plugin {plugin_name}: {e}")
            return {"error": str(e)}
