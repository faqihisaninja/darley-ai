from googleapiclient.discovery import Resource
from provider_auth import create_gmail_auth_manager


def gmail_authenticate() -> Resource:
    """Authenticate with Gmail using the modular auth system."""
    auth_manager = create_gmail_auth_manager()
    return auth_manager.authenticate("gmail", "v1")
