# agent.py
from google import genai
from google.genai import types
from tool_definitions import ALL_TOOLS
from tool_executor import ToolExecutor
from datetime import datetime, timedelta


class AIAgent:
    """The main AI agent that uses tools to help with emails and calendar"""

    def __init__(self, api_key: str, gmail_service, calendar_service):
        self.client = genai.Client(api_key=api_key)
        self.tool_executor = ToolExecutor(gmail_service, calendar_service)

        # Create the tool configuration
        self.tools = [types.Tool(function_declarations=ALL_TOOLS)]

    def chat(self, user_message: str, conversation_history: list = None) -> str:
        """Main chat method - handles the conversation with tool calling"""

        # Build conversation context
        messages = []
        if conversation_history:
            for msg in conversation_history:
                if msg["role"] == "user":
                    messages.append(
                        types.Content(
                            role="user",
                            parts=[types.Part.from_text(text=msg["content"])],
                        )
                    )
                elif msg["role"] == "assistant":
                    messages.append(
                        types.Content(
                            role="model",
                            parts=[types.Part.from_text(text=msg["content"])],
                        )
                    )

        # Add current user message
        messages.append(
            types.Content(role="user", parts=[types.Part.from_text(text=user_message)])
        )
        system_instruction = f"""
            You are Darley, a personal AI assistant for calendar and email management.
            Be conversational but professional. Always prioritize urgent/important items.
            When checking calendar and emails together, look for connections and conflicts.
            Current date and time: {datetime.now().strftime('%A, %B %d, %Y at %H:%M')} (Sydney timezone)

            When creating calendar events:
            - Use proper ISO datetime format for start_time and end_time
            - Always use Sydney timezone
            - If user says "tomorrow", that means {(datetime.now() + timedelta(days=1)).strftime('%B %d, %Y')}
            - If user says "today", that means {datetime.now().strftime('%B %d, %Y')}
            
            "You MUST use a tool when performing an action. Never say an action is done unless you actually called the tool successfully."
            
            Speak like Gen Z. PLEASE.
            """

        try:
            # Call Gemini with tools available
            response = self.client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=self.tools,
                    temperature=0.7,
                    system_instruction=system_instruction,
                ),
            )

            # Check if Gemini wants to call tools
            if response.function_calls:
                return self._handle_function_calls(response, messages)
            else:
                # Direct response without tools
                return response.text

        except Exception as e:
            return f"Sorry, I encountered an error: {str(e)}"

    def _handle_function_calls(self, response, messages):
        """Handle when Gemini wants to call functions"""

        # Add Gemini's response (with function calls) to conversation
        messages.append(response.candidates[0].content)

        # Execute each function call
        for function_call in response.function_calls:
            print(f"🔧 AI is calling: {function_call.name}")

            # Execute the tool
            result = self.tool_executor.execute_tool(
                function_call.name, function_call.args
            )

            # Add function result back to conversation as proper Content
            function_response = types.Part.from_function_response(
                name=function_call.name, response=result
            )
            messages.append(types.Content(role="tool", parts=[function_response]))

        # Now ask Gemini to respond based on the tool results
        try:
            final_response = self.client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=self.tools,
                    temperature=0.7,
                ),
            )

            # Check if it wants to call MORE tools
            if final_response.function_calls:
                return self._handle_function_calls(final_response, messages)
            else:
                return final_response.text

        except Exception as e:
            return f"Error processing tool results: {str(e)}"
