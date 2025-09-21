# main.py
import os
import json
from datetime import datetime
from agent import AIAgent
from provider_auth.google_auth import GoogleAuthManager


class ChatApp:
    """Main chat application with persistent memory"""

    def __init__(self):
        self.history_file = "chat_history.json"
        self.conversation_history = self.load_history()
        self.setup_services()

    def setup_services(self):
        """Initialize Google services and AI agent"""
        # API key
        api_key = os.getenv("GOOGLE_STUDIO_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_STUDIO_API_KEY not found")

        # Google auth
        scopes = [
            "https://www.googleapis.com/auth/gmail.readonly",
            "https://www.googleapis.com/auth/calendar",
        ]

        auth_manager = GoogleAuthManager(scopes=scopes)
        gmail_service = auth_manager.authenticate("gmail", "v1")
        calendar_service = auth_manager.authenticate("calendar", "v3")

        # AI Agent
        self.agent = AIAgent(api_key, gmail_service, calendar_service)

    def load_history(self):
        """Load chat history from file"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, "r") as f:
                    return json.load(f)
        except:
            pass
        return []

    def save_history(self):
        """Save chat history to file"""
        try:
            with open(self.history_file, "w") as f:
                json.dump(self.conversation_history, f, indent=2)
        except Exception as e:
            print(f"Failed to save history: {e}")

    def run(self):
        """Main chat loop"""
        print("🤖 AI Assistant ready! (with persistent memory)")
        print("Type 'quit' to exit, 'clear' to clear history\n")

        while True:
            try:
                user_input = input("💬 You: ").strip()

                if user_input.lower() == "quit":
                    self.save_history()
                    print("👋 Goodbye!")
                    break

                if user_input.lower() == "clear":
                    self.conversation_history = []
                    self.save_history()
                    print("🗑️ History cleared!")
                    continue

                if not user_input:
                    continue

                # Get AI response
                response = self.agent.chat(user_input, self.conversation_history)

                # Update history
                self.conversation_history.append(
                    {"role": "user", "content": user_input}
                )
                self.conversation_history.append(
                    {"role": "assistant", "content": response}
                )

                # Keep history manageable
                if len(self.conversation_history) > 20:
                    self.conversation_history = self.conversation_history[-20:]

                print(f"🤖 Assistant: {response}\n")

            except KeyboardInterrupt:
                self.save_history()
                print("\n👋 Goodbye!")
                break


if __name__ == "__main__":
    app = ChatApp()
    app.run()
