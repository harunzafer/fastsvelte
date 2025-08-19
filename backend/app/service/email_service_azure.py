from anyio.to_thread import run_sync
from app.service.email_service_base import EmailService
from azure.communication.email import EmailClient
import logging as log

class AzureEmailService(EmailService):
    def __init__(self, connection_string: str, sender_address: str):
        self.client = EmailClient.from_connection_string(connection_string)
        self.sender_address = sender_address

    async def _send_email(
        self, recipient: str, subject: str, plain_text: str, html: str
    ) -> None:
        message = {
            "senderAddress": self.sender_address,
            "recipients": {"to": [{"address": recipient}]},
            "content": {
                "subject": subject,
                "plainText": plain_text,
                "html": html,
            },
        }

        def send_blocking():
            poller = self.client.begin_send(message)

            POLLER_WAIT_TIME = 1  # seconds
            MAX_WAIT_TIME = 10  # seconds
            time_elapsed = 0

            while not poller.done():
                log.info(f"[AzureEmail] Polling status: {poller.status()}")
                poller.wait(POLLER_WAIT_TIME)
                time_elapsed += POLLER_WAIT_TIME

                if time_elapsed > MAX_WAIT_TIME:
                    raise RuntimeError("Email sending timed out")

            result = poller.result()
            if result["status"] == "Succeeded":
                log.info(f"[AzureEmail] Email sent (operation ID: {result['id']})")
                return result["id"]
            else:
                raise RuntimeError(f"Send failed: {result['error']}")

        try:
            await run_sync(send_blocking)
        except Exception as e:
            log.error(f"[AzureEmail] Failed to send to {recipient}: {e}")
            raise