from abc import ABC, abstractmethod
from typing import Any

from openai import OpenAI
from anthropic import Anthropic

from secretary.config import settings


class BaseAIProvider(ABC):
    @abstractmethod
    def complete(self, prompt: str, **kwargs) -> str:
        pass

    @abstractmethod
    def embed(self, text: str) -> list[float]:
        pass


class OpenAIProvider(BaseAIProvider):
    def __init__(self, api_key: str | None = None, model: str = "gpt-4o-mini"):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def complete(self, prompt: str, **kwargs) -> str:
        response = self.client.chat.completions.create(
            model=kwargs.get("model", self.model),
            messages=[{"role": "user", "content": prompt}],
            temperature=kwargs.get("temperature", 0.7),
            max_tokens=kwargs.get("max_tokens", 4096),
        )
        return response.choices[0].message.content

    def embed(self, text: str) -> list[float]:
        response = self.client.embeddings.create(
            model="text-embedding-3-small",
            input=text,
        )
        return response.data[0].embedding


class AnthropicProvider(BaseAIProvider):
    def __init__(self, api_key: str | None = None, model: str = "claude-3-5-sonnet-20241022"):
        self.client = Anthropic(api_key=api_key)
        self.model = model

    def complete(self, prompt: str, **kwargs) -> str:
        response = self.client.messages.create(
            model=kwargs.get("model", self.model),
            max_tokens=kwargs.get("max_tokens", 4096),
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text

    def embed(self, text: str) -> list[float]:
        raise NotImplementedError("Anthropic does not provide embeddings API")


class OllamaProvider(BaseAIProvider):
    def __init__(
        self,
        base_url: str = "http://localhost:11434",
        model: str = "llama3.2",
        embedding_model: str = "nomic-embed-text"
    ):
        self.base_url = base_url
        self.model = model
        self.embedding_model = embedding_model
        self.client = OpenAI(base_url=f"{base_url}/v1", api_key="ollama")

    def complete(self, prompt: str, **kwargs) -> str:
        response = self.client.chat.completions.create(
            model=kwargs.get("model", self.model),
            messages=[{"role": "user", "content": prompt}],
            temperature=kwargs.get("temperature", 0.7),
        )
        return response.choices[0].message.content

    def embed(self, text: str) -> list[float]:
        response = self.client.embeddings.create(
            model=self.embedding_model,
            input=text,
        )
        return response.data[0].embedding


class SiliconFlowProvider(BaseAIProvider):
    def __init__(self, api_key: str | None = None, model: str = "Qwen/Qwen2.5-32B-Instruct"):
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.siliconflow.cn/v1"
        )
        self.model = model

    def complete(self, prompt: str, **kwargs) -> str:
        response = self.client.chat.completions.create(
            model=kwargs.get("model", self.model),
            messages=[{"role": "user", "content": prompt}],
            temperature=kwargs.get("temperature", 0.7),
            max_tokens=kwargs.get("max_tokens", 4096),
        )
        return response.choices[0].message.content

    def embed(self, text: str) -> list[float]:
        response = self.client.embeddings.create(
            model="BAAI/bge-m3",
            input=text,
        )
        return response.data[0].embedding


class ZhipuProvider(BaseAIProvider):
    def __init__(self, api_key: str | None = None, model: str = "glm-4-flash"):
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://open.bigmodel.cn/api/paas/v4"
        )
        self.model = model

    def complete(self, prompt: str, **kwargs) -> str:
        response = self.client.chat.completions.create(
            model=kwargs.get("model", self.model),
            messages=[{"role": "user", "content": prompt}],
            temperature=kwargs.get("temperature", 0.7),
            max_tokens=kwargs.get("max_tokens", 4096),
        )
        return response.choices[0].message.content

    def embed(self, text: str) -> list[float]:
        response = self.client.embeddings.create(
            model="embedding-3",
            input=text,
        )
        return response.data[0].embedding


class AIRouter:
    def __init__(self):
        self.providers: dict[str, BaseAIProvider] = {}
        self._init_providers()
        
        # Priority order for auto-selection (free first)
        self.provider_priority = [
            "ollama",      # Free, local, private
            "zhipu",       # Free tier, Chinese
            "siliconflow", # Free tier (if has balance)
            "openai",      # Paid fallback
            "anthropic",   # Paid fallback
        ]

    def _init_providers(self):
        if settings.openai_api_key:
            self.providers["openai"] = OpenAIProvider(
                api_key=settings.openai_api_key
            )
        
        if settings.anthropic_api_key:
            self.providers["anthropic"] = AnthropicProvider(
                api_key=settings.anthropic_api_key
            )
        
        if settings.siliconflow_api_key:
            self.providers["siliconflow"] = SiliconFlowProvider(
                api_key=settings.siliconflow_api_key
            )
        
        if settings.zhipu_api_key:
            self.providers["zhipu"] = ZhipuProvider(
                api_key=settings.zhipu_api_key
            )
        
        self.providers["ollama"] = OllamaProvider(
            base_url=settings.ollama_base_url,
            model=settings.ollama_model
        )

    def get_available_providers(self) -> list[str]:
        """Return list of working providers."""
        available = []
        for name in self.provider_priority:
            if name in self.providers:
                try:
                    # Quick health check - simple completion
                    self.providers[name].complete("hi", max_tokens=5)
                    available.append(name)
                except Exception:
                    continue
        return available

    def get_best_provider(self) -> str:
        """Auto-select best available provider (free first)."""
        available = self.get_available_providers()
        
        if not available:
            raise RuntimeError("No AI providers available")
        
        # Return highest priority available
        for name in self.provider_priority:
            if name in available:
                return name
        
        return available[0]

    def complete(
        self,
        prompt: str,
        provider: str | None = None,
        **kwargs
    ) -> str:
        # Auto-select if no provider specified
        if provider is None:
            provider = self.get_best_provider()
        
        if provider not in self.providers:
            raise ValueError(f"Provider '{provider}' not available")
        
        return self.providers[provider].complete(prompt, **kwargs)

    def complete_with_fallback(
        self,
        prompt: str,
        preferred_provider: str | None = None,
        **kwargs
    ) -> tuple[str, str]:
        """Try preferred provider, fallback to others if fails.
        
        Returns: (result, provider_name)
        """
        # Build fallback order
        if preferred_provider and preferred_provider in self.providers:
            providers_to_try = [preferred_provider] + [
                p for p in self.provider_priority 
                if p in self.providers and p != preferred_provider
            ]
        else:
            providers_to_try = [
                p for p in self.provider_priority 
                if p in self.providers
            ]
        
        last_error = None
        for provider_name in providers_to_try:
            try:
                result = self.providers[provider_name].complete(prompt, **kwargs)
                return result, provider_name
            except Exception as e:
                last_error = e
                continue
        
        raise RuntimeError(f"All providers failed. Last error: {last_error}")

    def embed(self, text: str, provider: str | None = None) -> list[float]:
        # Auto-select if no provider specified
        if provider is None:
            provider = self.get_best_provider()
        
        if provider not in self.providers:
            raise ValueError(f"Provider '{provider}' not available")
        
        return self.providers[provider].embed(text)

    def summarize(self, text: str, max_length: int = 300) -> str:
        truncated = text[:3000] if len(text) > 3000 else text
        prompt = f"""╨í╤â╨╝╨╝╨░╤Ç╨╕╨╖╨╕╤Ç╤â╨╣ ╤ü╨╗╨╡╨┤╤â╤Ä╤ë╨╕╨╣ ╤é╨╡╨║╤ü╤é. ╨Æ╨╡╤Ç╨╜╨╕ ╨║╤Ç╨░╤é╨║╨╛╨╡ ╤Ç╨╡╨╖╤Ä╨╝╨╡ ╨┤╨╗╨╕╨╜╨╛╨╣ ╨╜╨╡ ╨▒╨╛╨╗╨╡╨╡ {max_length} ╤ü╨╕╨╝╨▓╨╛╨╗╨╛╨▓.

╨ó╨╡╨║╤ü╤é:
{truncated}

╨á╨╡╨╖╤Ä╨╝╨╡:"""
        return self.complete(prompt)

    def extract_tags(self, text: str) -> list[str]:
        prompt = f"""Extract ONLY English tags (lowercase, 1-3 words). Max 16 tags.
Return ONLY comma-separated list, nothing else.
Example: ai, youtube, summarizer, tools, productivity

Text:
{text[:3000]}

Tags:"""
        
        result = self.complete(prompt)
        
        tags = []
        seen = set()
        for t in result.replace('\n', ',').split(","):
            t = t.strip().lower()
            t = t.strip('-').strip()
            t = ''.join(c for c in t if c.isalnum() or c == ' ' or c == '-')
            if t and len(t.split()) <= 3 and len(t) > 1 and t not in seen:
                tags.append(t)
                seen.add(t)
        
        return tags[:16]

    def compute_novelty(
        self,
        new_text: str,
        existing_texts: list[str]
    ) -> float:
        new_embedding = self.embed(new_text)
        existing_embeddings = [self.embed(t) for t in existing_texts]
        
        max_similarity = 0.0
        for existing_emb in existing_embeddings:
            similarity = self._cosine_similarity(new_embedding, existing_emb)
            max_similarity = max(max_similarity, similarity)
        
        novelty = 1 - max_similarity
        return round(novelty, 2)

    def _cosine_similarity(self, a: list[float], b: list[float]) -> float:
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = sum(x * x for x in a) ** 0.5
        norm_b = sum(x * x for x in b) ** 0.5
        return dot / (norm_a * norm_b + 1e-8)


ai_router = AIRouter()
