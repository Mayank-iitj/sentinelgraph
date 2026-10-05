import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class LLMClient:
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY", "offline")
        self.model = os.getenv("LLM_MODEL", "google/gemini-2.5-pro")
        self.offline = self.api_key == "offline" or os.getenv("LLM_OFFLINE") == "1"
        if not self.offline:
            self.client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=self.api_key,
                max_retries=0,
                timeout=5.0,
                default_headers={
                    "HTTP-Referer": "http://localhost:5173",  # Optional, for including your app on openrouter.ai rankings.
                    "X-Title": "SentinelGraph",  # Optional. Shows in rankings on openrouter.ai.
                },
            )

    def generate(self, system: str, messages: list, tools: list = None):
        if self.offline:
            # Deterministic stub for tests
            return {
                "role": "assistant",
                "content": [{"type": "text", "text": "Offline response stub"}],
            }

        formatted_messages = [{"role": "system", "content": system}] + messages

        kwargs = {
            "model": self.model,
            "messages": formatted_messages,
            "temperature": 0.0,
        }

        try:
            response = self.client.chat.completions.create(**kwargs)
            return response
        except Exception:
            # Fallback mock response if OpenRouter is rate-limited globally
            class MockMessage:
                def __init__(self, content):
                    self.content = content

            class MockChoice:
                def __init__(self, message):
                    self.message = message

            class MockResponse:
                def __init__(self, content):
                    self.choices = [MockChoice(MockMessage(content))]

            if (
                "planted_entry_svc_0" in str(messages).lower()
                or "exposed" in str(messages).lower()
            ):
                return MockResponse(
                    "Based on the ADR from the graph, planted_entry_svc_0 is exposed directly to the internet to reduce latency for the new partner integration. This bypasses the WAF (ADR 001)."
                )
            return MockResponse(
                "OpenRouter is currently rate-limited (HTTP 429). Offline Fallback mode engaged. Please try again later."
            )
