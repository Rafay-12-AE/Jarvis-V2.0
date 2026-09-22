import os
import json

from groq import Groq

from brain.llm import get_history


client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)


# ---------------- CONTEXT ----------------

MAX_CONTEXT_CHARS = 800


def get_intent_context():

    history = get_history()

    if not history:
        return ""

    # Only use the most recent user/assistant exchange.
    recent_history = history[-2:]

    context_parts = []

    for item in recent_history:

        role = item.get(
            "role",
            ""
        )

        content = item.get(
            "content",
            ""
        ).strip()

        if not content:
            continue

        # Extra protection against large context
        if len(content) > MAX_CONTEXT_CHARS:
            content = content[:MAX_CONTEXT_CHARS]

        if role == "user":
            label = "User"

        elif role == "assistant":
            label = "Jarvis"

        else:
            continue

        context_parts.append(
            f"{label}: {content}"
        )

    return "\n".join(
        context_parts
    )


# ---------------- INTENT CLASSIFIER ----------------

def detect_intent(message):

    try:

        recent_context = get_intent_context()

        if recent_context:

            user_input = f"""
Recent conversation:

{recent_context}

Current user request:

{message}
"""

        else:

            user_input = message

        response = client.chat.completions.create(

            model="openai/gpt-oss-120b",

            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are the intent classifier for a voice assistant "
                        "called Jarvis. Your job is NOT to answer the user. "
                        "Your job is only to decide what action Jarvis should take. "
                        "\n\n"
                        "Available intents:\n"
                        "OPEN_APP - open an application\n"
                        "OPEN_YOUTUBE - open YouTube\n"
                        "OPEN_GOOGLE - open Google\n"
                        "OPEN_CHROME - open Chrome\n"
                        "SEARCH_YOUTUBE - search YouTube\n"
                        "PLAY_YOUTUBE - play something on YouTube\n"
                        "SEARCH_GOOGLE - search Google\n"
                        "SEARCH_SPOTIFY - search Spotify\n"
                        "GET_TIME - tell the current time\n"
                        "GET_DATE - tell the current date\n"
                        "EXIT - shut down Jarvis\n"
                        "WEB_SEARCH - the user needs current, recent, live, "
                        "changing, or externally verified information\n"
                        "CHAT - normal conversation or timeless knowledge\n"
                        "\n"
                        "Use WEB_SEARCH when the answer could have changed recently "
                        "or depends on live information. Examples include current news, "
                        "sports results, weather, prices, company leadership, elections, "
                        "recent events, today's information, latest releases, live scores, "
                        "current records, or anything asking what is happening now or recently. "
                        "Do not require the user to literally say 'latest' or 'current'. "
                        "Infer whether fresh information is needed from the meaning of the request. "
                        "\n\n"
                        "You may receive a small amount of recent conversation context. "
                        "Use it only when necessary to understand references such as "
                        "'it', 'he', 'she', 'they', 'that', 'there', 'the race', "
                        "'that event', or another incomplete follow-up. "
                        "\n"
                        "When the current request depends on previous context, resolve the "
                        "reference and put a COMPLETE standalone question or target into query. "
                        "Do not put vague references such as 'it' into a WEB_SEARCH query when "
                        "the recent context tells you what 'it' means. "
                        "\n\n"
                        "Examples:\n"
                        "'Who won the latest Formula 1 race?' -> WEB_SEARCH\n"
                        "'Who is the current president of France?' -> WEB_SEARCH\n"
                        "'What happened in Formula 1 yesterday?' -> WEB_SEARCH\n"
                        "'Why do Formula 1 cars generate downforce?' -> CHAT\n"
                        "'What is a black hole?' -> CHAT\n"
                        "'Could you open Discord for me?' -> OPEN_APP\n"
                        "'Put F1 highlights on YouTube' -> PLAY_YOUTUBE\n"
                        "\n"
                        "Context example:\n"
                        "Recent conversation says the user asked who won the latest "
                        "Formula 1 Grand Prix and Jarvis identified the race. "
                        "Current request: 'When was it held?'\n"
                        "Result: WEB_SEARCH with a complete query identifying that "
                        "Formula 1 Grand Prix rather than simply 'When was it held?'. "
                        "\n\n"
                        "Put the important target of the request into query. "
                        "For WEB_SEARCH, put a complete useful search question into query. "
                        "For app, search, YouTube, or Spotify actions, put the useful target "
                        "into query. "
                        "For CHAT, query may be empty. "
                        "If no query is needed, return an empty string."
                    )
                },

                {
                    "role": "user",
                    "content": user_input
                }
            ],

            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "jarvis_intent",
                    "strict": True,
                    "schema": {
                        "type": "object",
                        "properties": {
                            "intent": {
                                "type": "string",
                                "enum": [
                                    "OPEN_APP",
                                    "OPEN_YOUTUBE",
                                    "OPEN_GOOGLE",
                                    "OPEN_CHROME",
                                    "SEARCH_YOUTUBE",
                                    "PLAY_YOUTUBE",
                                    "SEARCH_GOOGLE",
                                    "SEARCH_SPOTIFY",
                                    "GET_TIME",
                                    "GET_DATE",
                                    "EXIT",
                                    "WEB_SEARCH",
                                    "CHAT"
                                ]
                            },

                            "query": {
                                "type": "string"
                            }
                        },

                        "required": [
                            "intent",
                            "query"
                        ],

                        "additionalProperties": False
                    }
                }
            }
        )

        result = json.loads(
            response.choices[0].message.content
        )

        return result

    except Exception as error:

        print(
            "Intent detection error:",
            error
        )

        return {
            "intent": "CHAT",
            "query": message
        }


# ---------------- TEST MODE ----------------

if __name__ == "__main__":

    while True:

        message = input(
            "Test command: "
        ).strip()

        if message.lower() == "exit":
            break

        result = detect_intent(
            message
        )

        print(
            json.dumps(
                result,
                indent=2
            )
        )