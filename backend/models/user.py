# backend/models/user.py
from typing import Optional
from datetime import datetime
import uuid

class User:
    def __init__(self, id: str, email: str, name: Optional[str] = None, 
                 avatar_url: Optional[str] = None, providers: Optional[list] = None):
        self.id = id
        self.email = email
        self.name = name
        self.avatar_url = avatar_url
        self.providers = providers or []
        self.created_at = datetime.now()
        self.last_login = datetime.now()
        
    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "avatar_url": self.avatar_url,
            "providers": self.providers,
            "created_at": self.created_at.isoformat(),
            "last_login": self.last_login.isoformat()
        }

# backend/models/conversation.py
from typing import List, Optional
from datetime import datetime
import uuid

class Conversation:
    def __init__(self, id: str, user_id: str, title: str, mode: str = "default", 
                 lang: str = "auto", created_at: Optional[datetime] = None):
        self.id = id or str(uuid.uuid4())
        self.user_id = user_id
        self.title = title
        self.mode = mode
        self.lang = lang
        self.created_at = created_at or datetime.now()
        self.updated_at = datetime.now()
        
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "mode": self.mode,
            "lang": self.lang,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

# backend/models/message.py
from typing import Optional
from datetime import datetime
import uuid

class Message:
    def __init__(self, id: str, conversation_id: str, role: str, content: str, 
                 created_at: Optional[datetime] = None):
        self.id = id or str(uuid.uuid4())
        self.conversation_id = conversation_id
        self.role = role  # "user" or "assistant"
        self.content = content
        self.created_at = created_at or datetime.now()
        
    def to_dict(self):
        return {
            "id": self.id,
            "conversation_id": self.conversation_id,
            "role": self.role,
            "content": self.content,
            "created_at": self.created_at.isoformat()
        }
