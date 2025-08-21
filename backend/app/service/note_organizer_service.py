from app.model.note_model import NoteImprovement
from app.service.openai_service import OpenAIService


class NoteOrganizerService:
    def __init__(self, openai_service: OpenAIService):
        self.openai_service = openai_service

    async def organize_and_improve(self, text: str) -> str:
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant that organizes and improves notes. "
                    "Fix spelling errors, grammar mistakes, and improve formatting while "
                    "preserving the original wording and tone. Make only light improvements "
                    "without changing the core meaning or style of the content."
                ),
            },
            {"role": "user", "content": f"Organize and improve the following note:\n\n{text}"},
        ]
        result = await self.openai_service.get_structured_response(
            messages, NoteImprovement
        )
        return result.improved_content.strip()
