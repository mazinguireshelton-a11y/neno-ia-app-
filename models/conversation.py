"""
Modelo de Conversa para a NENO IA
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid

class Conversation:
    def __init__(self, id: Optional[str] = None, user_id: str = "", 
                 title: str = "Nova conversa", mode: str = "default", 
                 lang: str = "auto", created_at: Optional[datetime] = None,
                 updated_at: Optional[datetime] = None, message_count: int = 0):
        """
        Inicializa uma nova conversa
        
        Args:
            id: ID único da conversa (gerado automaticamente se None)
            user_id: ID do usuário dono da conversa
            title: Título da conversa
            mode: Modo da conversa (default, programmer, creative, research, voice)
            lang: Idioma da conversa
            created_at: Data de criação
            updated_at: Data da última atualização
            message_count: Número de mensagens na conversa
        """
        self.id = id or str(uuid.uuid4())
        self.user_id = user_id
        self.title = title
        self.mode = mode
        self.lang = lang
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or self.created_at
        self.message_count = message_count
        self.is_archived = False
        self.tags: List[str] = []
        
    def update_title(self, new_title: str) -> None:
        """
        Atualiza o título da conversa
        
        Args:
            new_title: Novo título
        """
        self.title = new_title[:100]  # Limita a 100 caracteres
        self.updated_at = datetime.now()
        
    def update_mode(self, new_mode: str) -> None:
        """
        Atualiza o modo da conversa
        
        Args:
            new_mode: Novo modo
        """
        from backend.utils.constants import MODES
        if new_mode in MODES:
            self.mode = new_mode
            self.updated_at = datetime.now()
        
    def increment_message_count(self) -> None:
        """Incrementa o contador de mensagens"""
        self.message_count += 1
        self.updated_at = datetime.now()
        
    def add_tag(self, tag: str) -> None:
        """
        Adiciona uma tag à conversa
        
        Args:
            tag: Tag a ser adicionada
        """
        if tag and tag not in self.tags and len(self.tags) < 10:
            self.tags.append(tag)
            self.updated_at = datetime.now()
            
    def remove_tag(self, tag: str) -> None:
        """
        Remove uma tag da conversa
        
        Args:
            tag: Tag a ser removida
        """
        if tag in self.tags:
            self.tags.remove(tag)
            self.updated_at = datetime.now()
            
    def archive(self) -> None:
        """Arquiva a conversa"""
        self.is_archived = True
        self.updated_at = datetime.now()
        
    def unarchive(self) -> None:
        """Desarquiva a conversa"""
        self.is_archived = False
        self.updated_at = datetime.now()
        
    def to_dict(self) -> Dict[str, Any]:
        """
        Converte a conversa para dicionário
        
        Returns:
            Dict: Dicionário com os dados da conversa
        """
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "mode": self.mode,
            "lang": self.lang,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "message_count": self.message_count,
            "is_archived": self.is_archived,
            "tags": self.tags
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Conversation':
        """
        Cria uma Conversation a partir de um dicionário
        
        Args:
            data: Dicionário com os dados
            
        Returns:
            Conversation: Instância de Conversation
        """
        try:
            created_at = datetime.fromisoformat(data['created_at']) if 'created_at' in data else None
            updated_at = datetime.fromisoformat(data['updated_at']) if 'updated_at' in data else None
            
            return cls(
                id=data.get('id'),
                user_id=data.get('user_id', ''),
                title=data.get('title', 'Nova conversa'),
                mode=data.get('mode', 'default'),
                lang=data.get('lang', 'auto'),
                created_at=created_at,
                updated_at=updated_at,
                message_count=data.get('message_count', 0)
            )
        except (ValueError, KeyError) as e:
            raise ValueError(f"Erro ao criar Conversation from dict: {e}")
    
    def __repr__(self) -> str:
        return f"<Conversation {self.id} - {self.title} - {self.mode}>"
    
    def __str__(self) -> str:
        return f"{self.title} ({self.message_count} mensagens)"
