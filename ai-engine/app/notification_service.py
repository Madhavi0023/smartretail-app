import os
import smtplib
from email.message import EmailMessage

from dotenv import load_dotenv


load_dotenv()


class NotificationService:
    """Send Kubernetes incident notifications via email."""

    def __init__(self):
        self.smtp_host = os.getenv("SMTP_HOST")
        self.smtp_port = int(
            os.getenv("SMTP_PORT", "587")
        )
        self.smtp_email = os.getenv("SMTP_EMAIL")
        self.smtp_password = os.getenv("SMTP_PASSWORD")
        self.notification_email = os.getenv(
            "NOTIFICATION_EMAIL"
        )

        if not all(
            [
                self.smtp_host,
                self.smtp_email,
                self.smtp_password,
                self.notification_email,
            ]
        ):
            raise ValueError(
                "SMTP notification configuration is missing "
                "in .env"
            )

    def send_incident_notification(
        self,
        incident: dict,
        jira_result: dict,
    ):
        """
        Send an email containing Kubernetes incident,
        AI analysis, and Jira ticket information.
        """

        pod = incident.get("pod", "Unknown")
        namespace = incident.get(
            "namespace",
            "Unknown",
        )
        status = incident.get(
            "status",
            "Unknown",
        )
        analysis = incident.get(
            "analysis",
            "No analysis available.",
        )

        jira_key = jira_result.get("key")

        subject = (
            f"Kubernetes Incident - {pod}"
        )

        body = (
            "Kubernetes Incident Alert\n\n"
            "----------------------------------------\n"
            f"Pod: {pod}\n"
            f"Namespace: {namespace}\n"
            f"Status: {status}\n"
            "----------------------------------------\n\n"
            "AI Analysis:\n"
            f"{analysis}\n\n"
            "----------------------------------------\n"
            f"Jira Ticket: {jira_key or 'Not created'}\n"
            "----------------------------------------\n"
        )

        message = EmailMessage()

        message["Subject"] = subject
        message["From"] = self.smtp_email
        message["To"] = self.notification_email

        message.set_content(body)

        try:
            with smtplib.SMTP(
                self.smtp_host,
                self.smtp_port,
                timeout=30,
            ) as server:

                server.starttls()

                server.login(
                    self.smtp_email,
                    self.smtp_password,
                )

                server.send_message(message)

        except (
            smtplib.SMTPException,
            OSError,
        ) as exc:

            return {
                "sent": False,
                "channel": "email",
                "jira_key": jira_key,
                "pod": pod,
                "recipient": self.notification_email,
                "error": str(exc),
            }

        return {
            "sent": True,
            "channel": "email",
            "jira_key": jira_key,
            "pod": pod,
            "recipient": self.notification_email,
        }