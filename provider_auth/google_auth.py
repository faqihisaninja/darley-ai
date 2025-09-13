import os
from typing import List, Optional
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build, Resource


class GoogleAuthManager:
    """A modular Google authentication manager that can be used across different Google services."""

    def __init__(
        self,
        scopes: List[str],
        token_path: str = "token.json",
        creds_path: str = "credentials.json",
    ) -> None:
        """
        Initialize the Google Auth Manager.

        Args:
            scopes: List of Google API scopes to request
            token_path: Path to store/load the OAuth token
            creds_path: Path to the Google credentials file
        """
        self.scopes = scopes
        self.token_path = token_path
        self.creds_path = creds_path
        self.creds: Optional[Credentials] = None
        self.service: Optional[Resource] = None

    def authenticate(self, service_name: str, version: str = "v1") -> Resource:
        """
        Authenticate with Google and build a service client.

        Args:
            service_name: The Google service name (e.g., 'gmail', 'calendar')
            version: The API version to use

        Returns:
            The authenticated service client
        """
        self._get_credentials()
        self.service = build(service_name, version, credentials=self.creds)
        return self.service

    def _get_credentials(self) -> None:
        """Get or refresh Google OAuth credentials."""
        creds: Optional[Credentials] = None

        # Try to load existing credentials
        if os.path.exists(self.token_path):
            creds = Credentials.from_authorized_user_file(self.token_path, self.scopes)

        # If no valid credentials available, get new ones
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                # Refresh expired credentials
                creds.refresh(Request())
            else:
                # Get new credentials through OAuth flow
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.creds_path, self.scopes
                )
                creds = flow.run_local_server(port=0)

            # Save the credentials for next run
            with open(self.token_path, "w") as token:
                token.write(creds.to_json())

        self.creds = creds

    def get_service(self) -> Optional[Resource]:
        """Get the current service client if authenticated."""
        return self.service

    def is_authenticated(self) -> bool:
        """Check if the manager is authenticated."""
        return self.creds is not None and self.creds.valid
