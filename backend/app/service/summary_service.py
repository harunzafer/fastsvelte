from app.model.note_model import NoteSummary
from app.service.openai_service import OpenAIService


class SummaryService:
    def __init__(self, openai_service: OpenAIService):
        self.openai_service = openai_service

    async def summarize(self, text: str) -> str:
        messages = [
            {"role": "system", "content": "You are a helpful assistant that summarizes notes."},
            {"role": "user", "content": f"Summarize the following note:\n\n{text}"},
        ]
        result = await self.openai_service.get_structured_response(messages, NoteSummary)
        return result.summary.strip()
