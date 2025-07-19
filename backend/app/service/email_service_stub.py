from app.service.email_service_base import EmailService


class StubEmailService(EmailService):
    async def _send_email(
        self, to_email: str, subject: str, plain_text: str, html_content: str
    ) -> None:
        print(f"\n[STUB EMAIL] To: {to_email}")
        print(f"Subject: {subject}")
        print("--- Text ---")
        print(plain_text.strip())
        print("--- HTML ---")
        print(html_content.strip())
        print("[/STUB EMAIL]\n")
