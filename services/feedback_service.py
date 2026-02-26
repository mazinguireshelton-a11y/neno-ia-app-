# backend/services/feedback_service.py
"""
Sistema de coleta e análise de feedback para melhoria contínua
"""
from typing import Dict, List
import json
from datetime import datetime
from pathlib import Path

class FeedbackService:
    def __init__(self, storage_path: Path):
        self.storage_path = storage_path
        self.feedback_data = self._load_feedback()
        
    def _load_feedback(self) -> List[Dict]:
        """Carrega feedback do arquivo"""
        try:
            if self.storage_path.exists():
                with open(self.storage_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception:
            pass
        return []
        
    def save_feedback(self):
        """Salva feedback no arquivo"""
        try:
            self.storage_path.parent.mkdir(exist_ok=True)
            with open(self.storage_path, 'w', encoding='utf-8') as f:
                json.dump(self.feedback_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Erro ao salvar feedback: {e}")
            
    def add_feedback(self, message_id: str, feedback_type: str, rating: int, 
                    comments: str = "", metadata: Dict = None):
        """Adiciona um feedback"""
        feedback = {
            "message_id": message_id,
            "feedback_type": feedback_type,
            "rating": rating,
            "comments": comments,
            "metadata": metadata or {},
            "timestamp": datetime.now().isoformat()
        }
        
        self.feedback_data.append(feedback)
        self.save_feedback()
        
    def get_analytics(self) -> Dict:
        """Retorna analytics agregados do feedback"""
        if not self.feedback_data:
            return {}
            
        total = len(self.feedback_data)
        positive = sum(1 for f in self.feedback_data if f['rating'] >= 4)
        negative = sum(1 for f in self.feedback_data if f['rating'] <= 2)
        
        return {
            "total_feedback": total,
            "positive_rate": positive / total if total > 0 else 0,
            "negative_rate": negative / total if total > 0 else 0,
            "average_rating": sum(f['rating'] for f in self.feedback_data) / total if total > 0 else 0
        }
