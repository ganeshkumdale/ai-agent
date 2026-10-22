import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def ask_agent(user_input, conversation_history):

    messages = []

    # Add previous conversation
    for message in conversation_history:
        messages.append(
            f"{message['role'].upper()}: {message['content']}"
        )

    # Add current question
    messages.append(
        f"USER: {user_input}"
    )

    prompt = """
You are a helpful AI assistant.

Use the previous conversation to understand
the context of the user's current question.

If the user refers to something mentioned earlier,
use that information when answering.

Conversation:
""" + "\n".join(messages) + """

ASSISTANT:
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text