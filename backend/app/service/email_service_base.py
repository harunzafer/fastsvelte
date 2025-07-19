from abc import ABC, abstractmethod

from app.config.settings import settings


class EmailService(ABC):
    async def send_email_verification(self, email: str, verification_link: str) -> None:
        subject, plain_text, html_content = self._get_email_verification_content(
            verification_link
        )
        await self._send_email(email, subject, plain_text, html_content)

    async def send_invitation_email(self, email: str, invite_link: str) -> None:
        subject, plain_text, html_content = self._get_invitation_email_content(
            invite_link
        )
        await self._send_email(email, subject, plain_text, html_content)

    async def send_password_reset_email(self, email: str, reset_link: str) -> None:
        subject, plain_text, html_content = self._get_password_reset_email_content(
            reset_link
        )
        await self._send_email(email, subject, plain_text, html_content)

    @abstractmethod
    async def _send_email(
        self, to_email: str, subject: str, plain_text: str, html_content: str
    ) -> None:
        pass

    def _get_invitation_email_content(self, invite_link: str) -> tuple[str, str, str]:
        app_name = settings.app_name
        app_description = settings.app_description
        subject = f"You're invited to join {app_name}"

        plain_text = f"""\

You've been invited to join {app_name}.

{app_name} {app_description}.

To accept your invitation and get started, please click the link below:

{invite_link}

If you have any questions, feel free to reach out to our support team.

— The {app_name} Team
"""

        html_content = f"""\

<html>
<body style="font-family: Arial, sans-serif; color: #333;">
  <div style="max-width: 600px; margin: auto; padding: 20px; border: 1px solid #eee; border-radius: 8px;">
    <h2 style="color: #0056b3;">You’re Invited to Join {app_name}</h2>
    <p>
      {app_name} {app_description}.
    </p>

    <div style="margin: 24px 0;">
      <a href="{invite_link}" style="
        background-color: #0056b3;
        color: white;
        padding: 10px 15px;
        text-decoration: none;
        border-radius: 5px;
        display: inline-block;
      ">
        Accept Invitation
      </a>
    </div>

    <p>If the button doesn't work, copy and paste this link:</p>
    <p style="word-break: break-all;"><a href="{invite_link}">{invite_link}</a></p>

    <p style="margin-top: 30px;">If you have any questions, feel free to reach out to our support team.</p>
    <p>— The {app_name} Team</p>
  </div>
</body>
</html>
"""
        return subject, plain_text, html_content

    def _get_password_reset_email_content(
        self, reset_link: str
    ) -> tuple[str, str, str]:
        app_name = settings.app_name
        subject = f"Reset your {app_name} password"

        plain_text = f"""\

We received a request to reset your {app_name} password.

To proceed, click the link below:

{reset_link}

If you did not request this, you can safely ignore this email.

— The {app_name} Team
"""

        html_content = f"""\

<html>
  <body style="font-family: Arial, sans-serif; color: #333;">
    <div style="max-width: 600px; margin: auto; padding: 20px; border: 1px solid #eee; border-radius: 8px;">
      <h2 style="color: #0056b3;">Reset Your Password</h2>
      <p>We received a request to reset your {app_name} password.</p>

      <div style="margin: 24px 0;">
        <a href="{reset_link}" style="
          background-color: #0056b3;
          color: white;
          padding: 10px 15px;
          text-decoration: none;
          border-radius: 5px;
          display: inline-block;
        ">
          Reset Password
        </a>
      </div>

      <p>If the button doesn't work, copy and paste this link:</p>
      <p style="word-break: break-all;"><a href="{reset_link}">{reset_link}</a></p>

      <p style="margin-top: 30px;">If you did not request this, you can safely ignore this email.</p>
      <p>— The {app_name} Team</p>
    </div>
  </body>
</html>
"""
        return subject, plain_text, html_content

    def _get_email_verification_content(
        self, verification_link: str
    ) -> tuple[str, str, str]:
        app_name = settings.app_name
        subject = f"Verify your {app_name} email address"

        plain_text = f"""\

  Thank you for signing up for {app_name}!

  Please verify your email address by clicking the link below:

  {verification_link}

  If you did not sign up, you can safely ignore this email.

  — The {app_name} Team
  """

        html_content = f"""\

  <html>
    <body style="font-family: Arial, sans-serif; color: #333;">
      <div style="max-width: 600px; margin: auto; padding: 20px; border: 1px solid #eee; border-radius: 8px;">
        <h2 style="color: #0056b3;">Verify Your Email Address</h2>
        <p>Thank you for signing up for {app_name}!</p>

        <div style="margin: 24px 0;">
          <a href="{verification_link}" style="
            background-color: #0056b3;
            color: white;
            padding: 10px 15px;
            text-decoration: none;
            border-radius: 5px;
            display: inline-block;
          ">
            Verify Email
          </a>
        </div>

        <p>If the button doesn't work, copy and paste this link:</p>
        <p style="word-break: break-all;"><a href="{verification_link}">{verification_link}</a></p>

        <p style="margin-top: 30px;">If you did not sign up, you can safely ignore this email.</p>
        <p>— The {app_name} Team</p>
      </div>
    </body>
  </html>
  """
        return subject, plain_text, html_content
