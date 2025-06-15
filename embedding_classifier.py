#!/usr/bin/env python3
"""
Embedding-based classifier: uses OpenAI Embedding API to classify
Obsidian notes by similarity to tag embeddings.
"""
import math
import subprocess
import json
import sys
import openai

class OpenAIEmbeddingProvider:
    """
    Embedding-based classifier using OpenAI Embedding API.
    Computes cosine similarity between text embedding and tag embeddings.
    """
    def __init__(self, api_key, model=None, top_k=3):
        openai.api_key = api_key
        self.openai = openai
        # Default to next-gen small embedding model for cost efficiency
        self.model = model or "text-embedding-3-small"
        self.top_k = top_k
        self.tags_list = None
        self.tag_embeddings = None

    def load_tags(self, tags_list):
        if self.tag_embeddings is not None:
            return
        self.tags_list = tags_list
        # Use new OpenAI embeddings API: embeddings.create
        resp = self.openai.embeddings.create(
            model=self.model,
            input=tags_list
        )
        # resp.data is a list of objects with .embedding attribute
        self.tag_embeddings = [d.embedding for d in resp.data]

    def classify(self, text, tags_list):
        self.load_tags(tags_list)
        # Compute embedding for the note text, chunk if too long
        def get_emb(chunk_text):
            resp = self.openai.embeddings.create(model=self.model, input=chunk_text)
            return resp.data[0].embedding
        # Approximate char limit to avoid token overflow (<~8192 tokens)
        # Reduce to 8000 chars to account for Japanese characters (~1 char per token)
        MAX_CHARS = 8000
        if len(text) > MAX_CHARS:
            chunks = [text[i:i+MAX_CHARS] for i in range(0, len(text), MAX_CHARS)]
            embs = [get_emb(chunk) for chunk in chunks]
            # average embeddings across chunks
            dim = len(embs[0])
            text_emb = [sum(e[i] for e in embs) / len(embs) for i in range(dim)]
        else:
            text_emb = get_emb(text)
        sims = []
        for tag, tag_emb in zip(self.tags_list, self.tag_embeddings):
            dot = sum(te * qe for te, qe in zip(text_emb, tag_emb))
            norm_t = math.sqrt(sum(te * te for te in text_emb))
            norm_q = math.sqrt(sum(qe * qe for qe in tag_emb))
            sim = dot / (norm_t * norm_q) if norm_t and norm_q else 0.0
            sims.append((tag, sim))
        sims.sort(key=lambda x: x[1], reverse=True)
        return [tag for tag, _ in sims[:self.top_k]]

class GeminiEmbeddingProvider:
    """
    Embedding-based classifier using Google Gemini Embedding API.
    """
    def __init__(self, api_key, model=None, top_k=3):
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        self.genai = genai
        # Default to experimental high-performance embedding
        self.model = model or "gemini-embedding-exp-03-07"
        self.top_k = top_k
        self.tags_list = None
        self.tag_embeddings = None

    def load_tags(self, tags_list):
        if self.tag_embeddings is not None:
            return
        self.tags_list = tags_list
        resp = self.genai.embed_content(self.model, tags_list)
        self.tag_embeddings = resp['embedding']

    def classify(self, text, tags_list):
        self.load_tags(tags_list)
        resp = self.genai.embed_content(self.model, text)
        text_emb = resp['embedding']
        sims = []
        for tag, tag_emb in zip(self.tags_list, self.tag_embeddings):
            dot = sum(te * qe for te, qe in zip(text_emb, tag_emb))
            norm_t = math.sqrt(sum(te * te for te in text_emb))
            norm_q = math.sqrt(sum(qe * qe for qe in tag_emb))
            sim = dot / (norm_t * norm_q) if norm_t and norm_q else 0.0
            sims.append((tag, sim))
        sims.sort(key=lambda x: x[1], reverse=True)
        return [tag for tag, _ in sims[:self.top_k]]

class OllamaEmbeddingProvider:
    """
    Embedding-based classifier using an Ollama-hosted embedding model.
    Expects the model to output JSON-formatted embeddings for input content.
    """
    def __init__(self, model=None, top_k=3):
        # Default to high-performance local embedding model
        self.model = model or "mxbai-embed-large"
        self.top_k = top_k
        self.tags_list = None
        self.tag_embeddings = None

    def load_tags(self, tags_list):
        if self.tag_embeddings is not None:
            return
        self.tags_list = tags_list
        try:
            result = subprocess.run([
                "ollama", "run", self.model, "--json"
            ], input=json.dumps(tags_list), capture_output=True, text=True, check=True)
            self.tag_embeddings = json.loads(result.stdout)
        except Exception as e:
            print(f"Error embedding tags via Ollama: {e}", file=sys.stderr)
            self.tag_embeddings = [[ ] for _ in tags_list]

    def classify(self, text, tags_list):
        self.load_tags(tags_list)
        try:
            result = subprocess.run([
                "ollama", "run", self.model, "--json"
            ], input=json.dumps(text), capture_output=True, text=True, check=True)
            text_emb = json.loads(result.stdout)
        except Exception as e:
            print(f"Error embedding text via Ollama: {e}", file=sys.stderr)
            return []
        sims = []
        for tag, tag_emb in zip(self.tags_list, self.tag_embeddings):
            if not tag_emb or not text_emb:
                sim = 0.0
            else:
                dot = sum(te * qe for te, qe in zip(text_emb, tag_emb))
                norm_t = math.sqrt(sum(te * te for te in text_emb))
                norm_q = math.sqrt(sum(qe * qe for qe in tag_emb))
                sim = dot / (norm_t * norm_q) if norm_t and norm_q else 0.0
            sims.append((tag, sim))
        sims.sort(key=lambda x: x[1], reverse=True)
        return [tag for tag, _ in sims[:self.top_k]]