"""Thin wrapper around the OpenAI client.

Loads OPENAI_API_KEY from .env via python-dotenv, exposes a singleton
client and a small retry helper. Callers pass model name (default
gpt-4.1-mini) and prompt; the wrapper is intentionally minimal.
"""
