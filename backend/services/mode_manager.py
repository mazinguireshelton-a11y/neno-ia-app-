# backend/services/mode_manager.py
import logging
from typing import Dict, Any, Optional
from backend.utils.constants import MODES

logger = logging.getLogger(__name__)

class ModeManager:
    def __init__(self, plugin_service, llm_router):
        self.plugin_service = plugin_service
        self.llm_router = llm_router
        self.active_mode = "default"
        self.mode_configs = MODES
    
    def set_mode(self, mode_name: str) -> Dict[str, Any]:
        """Define o modo ativo"""
        if mode_name not in self.mode_configs:
            return {"ok": False, "error": f"Modo '{mode_name}' não encontrado"}
        
        self.active_mode = mode_name
        logger.info(f"Modo alterado para: {mode_name}")
        
        return {
            "ok": True, 
            "mode": mode_name,
            "config": self.mode_configs[mode_name]
        }
    
    def get_current_mode(self) -> Dict[str, Any]:
        """Retorna o modo atual"""
        return {
            "ok": True,
            "mode": self.active_mode,
            "config": self.mode_configs.get(self.active_mode, {})
        }
    
    def handle_request(self, message: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Processa uma requisição de acordo com o modo atual"""
        params = params or {}
        
        # Modos de física usam o plugin diretamente
        if self.active_mode in ["physics_basic", "physics_advanced"]:
            return self._handle_physics_mode(message, params)
        
        # Outros modos usam LLM com prompt específico
        return self._handle_llm_mode(message, params)
    
    def _handle_physics_mode(self, message: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Processa requisições do modo física"""
        try:
            # Extrai comando da mensagem ou usa parâmetro
            command = params.get("command", "")
            if not command and message:
                # Tenta inferir comando da mensagem
                if any(word in message.lower() for word in ["esfera", "cubo", "cilindro", "objeto"]):
                    command = "create_3d_object"
                elif any(word in message.lower() for word in ["campo", "vetor", "elétrico", "magnético"]):
                    command = "vector_field_3d"
                elif any(word in message.lower() for word in ["animar", "animação", "simular"]):
                    command = "animate_physics"
                else:
                    command = "create_3d_object"
            
            # Parâmetros para o plugin
            plugin_params = params.get("params", {})
            if not plugin_params and message:
                plugin_params["description"] = message
            
            # Executa o plugin
            result = self.plugin_service.execute("physics", command, plugin_params)
            
            return {
                "ok": "error" not in result,
                "mode": self.active_mode,
                "command": command,
                "result": result
            }
            
        except Exception as e:
            logger.error(f"Erro no modo física: {e}")
            return {"ok": False, "error": str(e)}
    
    def _handle_llm_mode(self, message: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Processa requisições usando LLM com prompt específico"""
        try:
            # System prompt baseado no modo
            mode_config = self.mode_configs.get(self.active_mode, {})
            mode_name = mode_config.get("name", "Padrão")
            mode_desc = mode_config.get("description", "")
            
            system_prompt = f"""
            Você é a NENO IA operando no modo {mode_name}. {mode_desc}
            Responda no mesmo idioma do usuário. Seja claro, objetivo e útil.
            """
            
            # Prompt específico por modo
            if self.active_mode == "programmer":
                system_prompt += """
                Você é um engenheiro de software sênior. Forneça respostas técnicas precisas, 
                exemplos de código bem formatados e explique decisões de design.
                """
            elif self.active_mode == "creative":
                system_prompt += """
                Você é um parceiro criativo. Pense fora da caixa, proponha variações, 
                estilos diferentes e mantenha a coerência com o pedido.
                """
            elif self.active_mode == "research":
                system_prompt += """
                Você é um pesquisador acadêmico. Forneça respostas baseadas em evidências, 
                cite fontes quando possível e mantenha rigor científico.
                """
            
            # Chama o LLM
            response = self.llm_router.ask(message, system_prompt)
            
            return {
                "ok": True,
                "mode": self.active_mode,
                "response": response
            }
            
        except Exception as e:
            logger.error(f"Erro no modo {self.active_mode}: {e}")
            return {"ok": False, "error": str(e)}
    
    def list_modes(self) -> Dict[str, Any]:
        """Lista todos os modos disponíveis"""
        return {
            "ok": True,
            "modes": self.mode_configs,
            "categories": {
                category: {
                    "name": config["name"],
                    "color": config["color"],
                    "modes": [mode for mode, mode_config in self.mode_configs.items() 
                             if mode_config.get("category") == category]
                }
                for category in set(mode_config.get("category", "geral") 
                                  for mode_config in self.mode_configs.values())
            }
        }
