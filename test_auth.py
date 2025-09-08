#!/usr/bin/env python3
"""
Test script to verify the refactored authentication system works correctly.
"""

from provider_auth import (
    create_gmail_auth_manager,
    create_calendar_auth_manager,
    GoogleAuthManager,
)
from email_utils.gmail_auth import gmail_authenticate
from calendar_utils.google_calendar import GoogleCalendarProvider


def test_gmail_auth():
    """Test Gmail authentication using the new modular system."""
    print("Testing Gmail authentication...")
    try:
        # Test the convenience function
        service = gmail_authenticate()
        print("✅ Gmail authentication successful (convenience function)")

        # Test the auth manager directly
        auth_manager = create_gmail_auth_manager()
        service2 = auth_manager.authenticate("gmail", "v1")
        print("✅ Gmail authentication successful (auth manager)")

        return True
    except Exception as e:
        print(f"❌ Gmail authentication failed: {e}")
        return False


def test_calendar_auth():
    """Test Calendar authentication using the new modular system."""
    print("Testing Calendar authentication...")
    try:
        # Test the calendar provider
        calendar_provider = GoogleCalendarProvider()
        calendar_provider.authenticate()
        print("✅ Calendar authentication successful (provider)")

        # Test the auth manager directly
        auth_manager = create_calendar_auth_manager()
        service = auth_manager.authenticate("calendar", "v3")
        print("✅ Calendar authentication successful (auth manager)")

        return True
    except Exception as e:
        print(f"❌ Calendar authentication failed: {e}")
        return False


def test_custom_auth():
    """Test custom authentication with different scopes."""
    print("Testing custom authentication...")
    try:
        # Test with custom scopes
        custom_scopes = [
            "https://www.googleapis.com/auth/gmail.readonly",
            "https://www.googleapis.com/auth/calendar.readonly",
        ]

        auth_manager = GoogleAuthManager(
            scopes=custom_scopes,
            token_path="custom_token.json",
            creds_path="credentials.json",
        )

        # This would require both scopes to be available
        print("✅ Custom auth manager created successfully")
        return True
    except Exception as e:
        print(f"❌ Custom authentication failed: {e}")
        return False


def main():
    """Run all authentication tests."""
    print("🧪 Testing Refactored Authentication System\n")

    tests = [test_gmail_auth, test_calendar_auth, test_custom_auth]

    results = []
    for test in tests:
        results.append(test())
        print()

    passed = sum(results)
    total = len(results)

    print(f"📊 Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! Authentication refactoring successful.")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")


if __name__ == "__main__":
    main()
