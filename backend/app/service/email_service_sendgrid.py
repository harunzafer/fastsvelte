import logging
from app.service.email_service_base import EmailService
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import httpx

logger = logging.getLogger(__name__)


class SendGridEmailService(EmailService):
    def __init__(self, api_key: str, sender_address: str, sender_name: str = None):
        self.api_key = api_key
        self.sender_address = sender_address
        self.sender_name = sender_name or "FastSvelte"
        self.client = SendGridAPIClient(api_key=api_key)

    async def _send_email(
        self, recipient: str, subject: str, plain_text: str, html: str
    ) -> None:
        try:
            from_email = (
                (self.sender_address, self.sender_name)
                if self.sender_name
                else self.sender_address
            )

            message = Mail(
                from_email=from_email,
                to_emails=recipient,
                subject=subject,
                plain_text_content=plain_text,
                html_content=html,
            )

            # Use httpx for async HTTP request instead of SendGrid's sync client
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.sendgrid.com/v3/mail/send",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                    },
                    json=message.get(),
                )

                if response.status_code == 202:
                    logger.info(f"[SendGrid] Email sent successfully to {recipient}")
                else:
                    error_msg = f"SendGrid API error: {response.status_code} - {response.text}"
                    logger.error(f"[SendGrid] {error_msg}")
                    raise RuntimeError(error_msg)

        except Exception as e:
            logger.error(f"[SendGrid] Failed to send email to {recipient}: {e}")
            raise