# backend/services/memory_service.py
"""
Sistema de memória de longo prazo para personalização contínua
"""
from typing import Dict, List
import json
from pathlib import Path

class MemoryService:
    def __init__(self, storage_path: Path):
        self.storage_path = storage_path
        self.memories = self._load_memories()
        
    def _load_memories(self) -> Dict:
        """Carrega memórias do arquivo"""
        try:
            if self.storage_path.exists():
                with open(self.storage_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception:
            pass
        return {}
        
    def save_memories(self):
        """Salva memórias no arquivo"""
        try:
            self.storage_path.parent.mkdir(exist_ok=True)
            with open(self.storage_path, 'w', encoding='utf-8') as f:
                json.dump(self.memories, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Erro ao salvar memórias: {e}")
            
    def add_memory(self, user_id: str, key: str, value: str, category: str = "general"):
        """Adiciona uma memória para o usuário"""
        if user_id not in self.memories:
            self.memories[user_id] = {}
            
        if category not in self.memories[user_id]:
            self.memories[user_id][category] = {}
            
        self.memories[user_id][category][key] = value
        self.save_memories()
        
    def get_user_context(self, user_id: str) -> str:
        """Obtém contexto personalizado do usuário"""
        if user_id not in self.memories:
            return ""
            
        context_parts = []
        for category, memories in self.memories[user_id].items():
            context_parts.append(f"{category}:")
            for key, value in memories.items():
                context_parts.append(f"- {key}: {value}")
                
        return "\n".join(context_parts)
