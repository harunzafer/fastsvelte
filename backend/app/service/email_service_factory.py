from app.config.settings import settings
from app.service.email_service_base import EmailService
from app.service.email_service_stub import StubEmailService


def create_email_service() -> EmailService:
    """
    Factory function to create the appropriate email service based on configuration.
    """
    if settings.email_provider == "azure":
        from app.service.email_service_azure import AzureEmailService
        
        if not settings.azure_email_connection_string or not settings.azure_email_sender_address:
            raise ValueError(
                "Azure email service requires azure_email_connection_string and azure_email_sender_address"
            )
        
        return AzureEmailService(
            connection_string=settings.azure_email_connection_string,
            sender_address=settings.azure_email_sender_address,
        )
    
    elif settings.email_provider == "sendgrid":
        from app.service.email_service_sendgrid import SendGridEmailService
        
        if not settings.sendgrid_api_key or not settings.sendgrid_sender_address:
            raise ValueError(
                "SendGrid email service requires sendgrid_api_key and sendgrid_sender_address"
            )
        
        return SendGridEmailService(
            api_key=settings.sendgrid_api_key,
            sender_address=settings.sendgrid_sender_address,
            sender_name=settings.sendgrid_sender_name,
        )
    
    else:  # Default to stub
        return StubEmailService()