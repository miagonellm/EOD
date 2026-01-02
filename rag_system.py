import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from datetime import datetime
import os
import json
from pattern_library import get_all_patterns

class RAGMemory:
    def __init__(self, persona_name):
        self.persona_name = persona_name.lower()
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

        # Initialize ChromaDB client with persistent storage
        self.client = chromadb.Client(Settings(
            persist_directory=f"./memories/{self.persona_name}",
            anonymized_telemetry=False
        ))

        # Get or create collection for this persona
        try:
            self.collection = self.client.get_collection(name=f"{self.persona_name}_memory")
        except:
            self.collection = self.client.create_collection(
                name=f"{self.persona_name}_memory",
                metadata={"description": f"Conversation memory for {self.persona_name}"}
            )

    def store_interaction(self, user_message, assistant_response):
        """Store a conversation turn in memory"""
        timestamp = datetime.now().isoformat()

        # Create a combined text for embedding (captures full context)
        combined_text = f"User: {user_message}\n{self.persona_name.title()}: {assistant_response}"

        # Generate embedding
        embedding = self.model.encode(combined_text).tolist()

        # Create unique ID based on timestamp
        interaction_id = f"{self.persona_name}_{timestamp}"

        # Store in ChromaDB
        self.collection.add(
            embeddings=[embedding],
            documents=[combined_text],
            metadatas=[{
                "timestamp": timestamp,
                "user_message": user_message,
                "assistant_response": assistant_response,
                "persona": self.persona_name
            }],
            ids=[interaction_id]
        )

    def retrieve_context(self, query, n_results=5):
        """Retrieve relevant past interactions based on current query"""
        # Generate embedding for query
        query_embedding = self.model.encode(query).tolist()

        # Query ChromaDB for similar past interactions
        try:
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results
            )

            if not results['documents'] or not results['documents'][0]:
                return []

            # Format retrieved context
            context_items = []
            for i, doc in enumerate(results['documents'][0]):
                metadata = results['metadatas'][0][i]
                context_items.append({
                    'text': doc,
                    'timestamp': metadata.get('timestamp', 'unknown'),
                    'distance': results['distances'][0][i] if 'distances' in results else None
                })

            return context_items
        except Exception as e:
            print(f"Retrieval error: {e}")
            return []

    def build_context_prompt(self, query, n_results=5, include_patterns=True):
        """
        Build a context string to inject into the system prompt

        This combines:
        1. Relevant past conversations (RAG memory)
        2. Pattern library (meta-knowledge about code/systems thinking)

        For Ego, we include patterns to make him connect technical answers
        to broader thinking patterns. For Ode, patterns might be different
        (more philosophical, less action-oriented).
        """
        context_items = self.retrieve_context(query, n_results)

        context_parts = []

        # Add memory context if we have relevant past conversations
        if context_items:
            context_parts.append("\n[RELEVANT MEMORY CONTEXT:]")
            for item in context_items:
                context_parts.append(f"{item['text']}")
            context_parts.append("[END MEMORY CONTEXT]\n")

        # Add pattern library for Ego only
        # This gives Ego the meta-patterns to connect code to thinking
        if include_patterns and self.persona_name == 'ego':
            context_parts.append("\n[PATTERN RECOGNITION LIBRARY:]")
            context_parts.append("Use these patterns to connect technical answers to broader systems thinking:")
            context_parts.append(get_all_patterns())
            context_parts.append("[END PATTERNS]\n")

        return "\n".join(context_parts)

    def get_memory_stats(self):
        """Get statistics about stored memories"""
        try:
            count = self.collection.count()
            return {
                "persona": self.persona_name,
                "total_interactions": count,
                "storage_path": f"./memories/{self.persona_name}"
            }
        except:
            return {
                "persona": self.persona_name,
                "total_interactions": 0,
                "storage_path": f"./memories/{self.persona_name}"
            }

# Initialize memory systems for both personas
ego_memory = RAGMemory("ego")
ode_memory = RAGMemory("ode")
