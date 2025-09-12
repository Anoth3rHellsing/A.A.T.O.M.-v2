"""Simple OpenAI chat engine with automatic rate-limit retries."""

import asyncio
from typing import List, Dict

import openai


class OpenAIChatEngine:
    """A minimal wrapper around OpenAI's chat completion API."""

    def __init__(self, api_key: str, model: str = "gpt-5") -> None:
        """Initialize the chat engine.

        Args:
            api_key: OpenAI API key.
            model: Model name to use for chat completions.
        """
        self.api_key = api_key
        self.model = model
        openai.api_key = api_key

    async def chat(self, messages: List[Dict], temperature: float = 0.7) -> str:
        """Send messages to the OpenAI chat API and return the response.

        Automatically retries up to three times if a rate limit error occurs.

        Args:
            messages: A list of message dicts as expected by the OpenAI API.
            temperature: Sampling temperature.

        Returns:
            The content of the assistant's reply.

        Raises:
            RuntimeError: If the API request fails after retries.
        """
        for attempt in range(3):
            try:
                response = await openai.ChatCompletion.acreate(
                    model=self.model,
                    messages=messages,
                    temperature=temperature,
                )
                return response["choices"][0]["message"]["content"]
            except openai.error.RateLimitError as exc:  # type: ignore[attr-defined]
                if attempt == 2:
                    raise RuntimeError("Rate limit exceeded") from exc
                await asyncio.sleep(2 ** attempt)
            except Exception as exc:
                raise RuntimeError("OpenAI API error") from exc


async def main() -> None:
    engine = OpenAIChatEngine(api_key="YOUR_API_KEY_HERE")
    messages = [{"role": "user", "content": "Hello, world!"}]
    response = await engine.chat(messages)
    print(response)


if __name__ == "__main__":
    asyncio.run(main())
