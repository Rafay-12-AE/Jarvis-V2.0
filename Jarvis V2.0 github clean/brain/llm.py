import os

from groq import Groq


client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)


# ---------------- SHORT-TERM MEMORY ----------------

conversation_history = []

# Four user/assistant exchanges
MAX_HISTORY_MESSAGES = 8

# Prevent one message from filling memory with huge web/search content
MAX_MEMORY_MESSAGE_CHARS = 1500

# Final safety limit for total stored conversation text
MAX_MEMORY_TOTAL_CHARS = 6000


def add_to_history(role, content):

    if not content:
        return

    content = str(content).strip()

    # Never allow a huge message to live in conversational memory
    if len(content) > MAX_MEMORY_MESSAGE_CHARS:
        content = content[:MAX_MEMORY_MESSAGE_CHARS]

    conversation_history.append(
        {
            "role": role,
            "content": content
        }
    )

    trim_history()


def trim_history():

    # First limit the number of stored messages
    while len(conversation_history) > MAX_HISTORY_MESSAGES:
        conversation_history.pop(0)

    # Then enforce a total character limit
    while conversation_history:

        total_chars = sum(
            len(item.get("content", ""))
            for item in conversation_history
        )

        if total_chars <= MAX_MEMORY_TOTAL_CHARS:
            break

        conversation_history.pop(0)


def clear_history():

    conversation_history.clear()


def get_history():

    return conversation_history.copy()


# ---------------- LLM ----------------

def ask_llm(message, remember=True):

    if not message:
        return None

    try:

        messages = [
            {
                "role": "system",
                "content": (
                    "You are Jarvis, a helpful, intelligent voice assistant. "
                    "Keep normal spoken answers short and natural, usually 1 to 3 sentences. "
                    "Do not give long lists or detailed explanations unless the user specifically asks for detail. "
                    "If the user asks a simple question, answer it simply. "
                    "Use the recent conversation context when the user refers to something said earlier. "
                    "Understand corrections, follow-up questions, pronouns, and incomplete references from context. "
                    "Respond clearly and conversationally."
                )
            }
        ]

        messages.extend(
            conversation_history
        )

        messages.append(
            {
                "role": "user",
                "content": message
            }
        )

        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=messages
        )

        answer = response.choices[0].message.content

        # Only save real conversational turns.
        # Temporary research prompts will later use remember=False.
        if remember:

            add_to_history(
                "user",
                message
            )

            add_to_history(
                "assistant",
                answer
            )

        return answer

    except Exception as error:

        print(
            "LLM error:",
            error
        )

        return "I'm having trouble reaching my AI service right now."