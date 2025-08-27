import chromadb
from chromadb.config import Settings
from typing import List, Dict, Optional
import uuid
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class VectorDBService:
    def __init__(self, persist_directory: str = "./chroma_db"):
        self.client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=persist_directory
        ))
        
        # Criar collections principais
        self.memories = self.client.get_or_create_collection("memories")
        self.conversations = self.client.get_or_create_collection("conversations")
        
    def add_memory(self, user_id: str, text: str, metadata: Dict = None):
        """Adiciona memória com embedding automático"""
        memory_id = str(uuid.uuid4())
        self.memories.add(
            documents=[text],
            metadatas=[{
                "user_id": user_id,
                "type": "memory",
                **(metadata or {})
            }],
            ids=[memory_id]
        )
        return memory_id
        
    def search_memories(self, user_id: str, query: str, n_results: int = 5):
        """Busca memórias semanticamente relevantes"""
        results = self.memories.query(
            query_texts=[query],
            n_results=n_results,
            where={"user_id": user_id}
        )
        return results
        
    def add_conversation(self, conversation_data: Dict):
        """Armazena conversa com contexto"""
        conv_id = conversation_data.get("id", str(uuid.uuid4()))
        self.conversations.add(
            documents=[conversation_data.get("summary", "")],
            metadatas=conversation_data,
            ids=[conv_id]
        )
        return conv_id

# Instância global
vector_db = VectorDBService()
