"""
Modelo de Mensagem para a NENO IA
"""
from typing import Optional, Dict, Any, List
from datetime import datetime
import uuid

class Message:
    def __init__(self, id: Optional[str] = None, conversation_id: str = "", 
                 role: str = "user", content: str = "", 
                 created_at: Optional[datetime] = None, 
                 metadata: Optional[Dict[str, Any]] = None,
                 tokens: int = 0, feedback: Optional[Dict[str, Any]] = None):
        """
        Inicializa uma nova mensagem
        
        Args:
            id: ID único da mensagem (gerado automaticamente se None)
            conversation_id: ID da conversa
            role: Role da mensagem (user, assistant, system)
            content: Conteúdo da mensagem
            created_at: Data de criação
            metadata: Metadados adicionais
            tokens: Número de tokens da mensagem
            feedback: Feedback da mensagem
        """
        self.id = id or str(uuid.uuid4())
        self.conversation_id = conversation_id
        self.role = role
        self.content = content
        self.created_at = created_at or datetime.now()
        self.metadata = metadata or {}
        self.tokens = tokens
        self.feedback = feedback or {}
        self.is_edited = False
        self.edit_history: List[Dict[str, Any]] = []
        
    def update_content(self, new_content: str, reason: str = "edit") -> None:
        """
        Atualiza o conteúdo da mensagem
        
        Args:
            new_content: Novo conteúdo
            reason: Razão da edição
        """
        # Salva no histórico de edições
        self.edit_history.append({
            "previous_content": self.content,
            "new_content": new_content,
            "reason": reason,
            "edited_at": datetime.now().isoformat(),
            "tokens_before": self.tokens
        })
        
        self.content = new_content
        self.is_edited = True
        
        # Atualiza contagem de tokens (estimativa)
        self.tokens = len(new_content) // 4
        
    def add_feedback(self, feedback_type: str, rating: int, 
                    comment: str = "", user_id: str = "") -> None:
        """
        Adiciona feedback à mensagem
        
        Args:
            feedback_type: Tipo de feedback (like, dislike, helpful, etc.)
            rating: Nota de 1 a 5
            comment: Comentário opcional
            user_id: ID do usuário que deu o feedback
        """
        if 'feedback' not in self.feedback:
            self.feedback = {}
            
        self.feedback[feedback_type] = {
            "rating": max(1, min(5, rating)),
            "comment": comment,
            "user_id": user_id,
            "given_at": datetime.now().isoformat()
        }
        
    def get_feedback_score(self) -> float:
        """
        Calcula a pontuação média do feedback
        
        Returns:
            float: Pontuação média (0-5)
        """
        if not self.feedback:
            return 0.0
            
        ratings = [fb['rating'] for fb in self.feedback.values() if 'rating' in fb]
        if not ratings:
            return 0.0
            
        return sum(ratings) / len(ratings)
    
    def add_metadata(self, key: str, value: Any) -> None:
        """
        Adiciona metadado à mensagem
        
        Args:
            key: Chave do metadado
            value: Valor do metadado
        """
        self.metadata[key] = value
        
    def get_metadata(self, key: str, default: Any = None) -> Any:
        """
        Obtém metadado da mensagem
        
        Args:
            key: Chave do metadado
            default: Valor padrão se não existir
            
        Returns:
            Any: Valor do metadado
        """
        return self.metadata.get(key, default)
    
    def estimate_tokens(self) -> int:
        """
        Estima o número de tokens na mensagem
        
        Returns:
            int: Número estimado de tokens
        """
        # Estimativa simples: 1 token ≈ 4 caracteres
        return len(self.content) // 4
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Converte a mensagem para dicionário
        
        Returns:
            Dict: Dicionário com os dados da mensagem
        """
        return {
            "id": self.id,
            "conversation_id": self.conversation_id,
            "role": self.role,
            "content": self.content,
            "created_at": self.created_at.isoformat(),
            "metadata": self.metadata,
            "tokens": self.tokens,
            "feedback": self.feedback,
            "is_edited": self.is_edited,
            "edit_history": self.edit_history
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Message':
        """
        Cria uma Message a partir de um dicionário
        
        Args:
            data: Dicionário com os dados
            
        Returns:
            Message: Instância de Message
        """
        try:
            created_at = datetime.fromisoformat(data['created_at']) if 'created_at' in data else None
            
            return cls(
                id=data.get('id'),
                conversation_id=data.get('conversation_id', ''),
                role=data.get('role', 'user'),
                content=data.get('content', ''),
                created_at=created_at,
                metadata=data.get('metadata', {}),
                tokens=data.get('tokens', 0),
                feedback=data.get('feedback', {})
            )
        except (ValueError, KeyError) as e:
            raise ValueError(f"Erro ao criar Message from dict: {e}")
    
    def __repr__(self) -> str:
        return f"<Message {self.id} - {self.role} - {len(self.content)} chars>"
    
    def __str__(self) -> str:
        role_emoji = "👤" if self.role == "user" else "🤖" if self.role == "assistant" else "⚙️"
        return f"{role_emoji} {self.content[:50]}{'...' if len(self.content) > 50 else ''}"
