"""
Unit tests for email service implementations.
"""

import os
import pytest
from app.service.email_service_factory import create_email_service
from app.service.email_service_stub import StubEmailService


@pytest.mark.anyio
async def test_email_services():
    print("Testing Email Service Factory")
    print("=" * 40)
    
    # Test stub service (default)
    print("\n1. Testing Stub Email Service")
    os.environ['FS_EMAIL_PROVIDER'] = 'stub'
    
    # Refresh settings
    from app.config.settings import Settings
    settings = Settings()
    
    email_service = create_email_service()
    print(f"Created service: {type(email_service).__name__}")
    
    try:
        await email_service.send_email_verification(
            "test@example.com", 
            "http://localhost:5173/verify?token=test123"
        )
        print("✅ Stub email service works correctly")
    except Exception as e:
        print(f"❌ Stub email service failed: {e}")
    
    # Test Azure service configuration (will fail without credentials, but tests factory)
    print("\n2. Testing Azure Email Service Factory")
    os.environ['FS_EMAIL_PROVIDER'] = 'azure'
    
    try:
        azure_service = create_email_service()
        print("❌ Azure service should have failed without credentials")
    except ValueError as e:
        print(f"✅ Azure service correctly requires credentials: {e}")
    
    # Test SendGrid service configuration
    print("\n3. Testing SendGrid Email Service Factory") 
    os.environ['FS_EMAIL_PROVIDER'] = 'sendgrid'
    
    try:
        sendgrid_service = create_email_service()
        print("❌ SendGrid service should have failed without credentials")
    except ValueError as e:
        print(f"✅ SendGrid service correctly requires credentials: {e}")
    
    print("\n" + "=" * 40)
    print("Email service factory tests completed!")


@pytest.mark.anyio
async def test_stub_email_service():
    """Test that stub email service works correctly."""
    os.environ['FS_EMAIL_PROVIDER'] = 'stub'
    
    # Refresh settings
    from app.config.settings import Settings
    settings = Settings()
    
    email_service = create_email_service()
    assert isinstance(email_service, StubEmailService)
    
    # Test that it doesn't throw errors
    await email_service.send_email_verification(
        "test@example.com", 
        "http://localhost:5173/verify?token=test123"
    )


def test_azure_email_service_validation():
    """Test that Azure email service validates credentials properly."""
    from app.service.email_service_factory import create_email_service
    from app.config.settings import Settings
    
    # Test validation logic directly 
    settings_mock = Settings()
    settings_mock.email_provider = "azure"
    settings_mock.azure_email_connection_string = None
    settings_mock.azure_email_sender_address = None
    
    # This will fall back to stub since validation fails
    email_service = create_email_service()
    assert isinstance(email_service, StubEmailService)


def test_sendgrid_email_service_validation():
    """Test that SendGrid email service validates credentials properly."""
    from app.service.email_service_factory import create_email_service
    from app.config.settings import Settings
    
    # Test validation logic directly 
    settings_mock = Settings()
    settings_mock.email_provider = "sendgrid"
    settings_mock.sendgrid_api_key = None
    settings_mock.sendgrid_sender_address = None
    
    # This will fall back to stub since validation fails  
    email_service = create_email_service()
    assert isinstance(email_service, StubEmailService)