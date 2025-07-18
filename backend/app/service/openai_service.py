from typing import Type, TypeVar

from openai import AsyncOpenAI
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class OpenAIService:
    def __init__(self, model: str = "gpt-4o-2024-08-06", temperature: float = 0.1, api_key: str = None):
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = model
        self.temperature = temperature

    async def get_structured_response(self, messages: list[dict], model: Type[T]) -> T:
        response = await self.client.responses.parse(
            model=self.model,
            input=messages,
            text_format=model,
            temperature=self.temperature,
        )
        return response.output_parsed
