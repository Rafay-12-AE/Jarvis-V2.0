from datetime import datetime

from brain.llm import (
    ask_llm,
    add_to_history
)

from skills.web_search import search_web


# ---------------- WEB LIMITS ----------------

MAX_WEB_RESULTS = 3
MAX_CONTENT_CHARS = 1200


def answer_from_web(question):

    if not question:
        return None

    # Get fresh web results
    search_result = search_web(
        question,
        current=True
    )

    if not search_result:
        return (
            "I could not retrieve current web information."
        )

    results = search_result.get(
        "results",
        []
    )

    if not results:
        return (
            "I could not find useful current information."
        )

    # ---------------- BUILD SMALL WEB CONTEXT ----------------

    context_parts = []

    for index, item in enumerate(
        results[:MAX_WEB_RESULTS],
        start=1
    ):

        title = item.get(
            "title",
            "Unknown title"
        )

        content = item.get(
            "content",
            ""
        )

        # Prevent one result from creating a massive prompt
        if len(content) > MAX_CONTENT_CHARS:
            content = content[:MAX_CONTENT_CHARS]

        context_parts.append(
            f"""
Source {index}
Title: {title}
Content: {content}
"""
        )

    web_context = "\n".join(
        context_parts
    )

    # Use the computer's local date/time automatically.
    # This remains portable when Jarvis moves to the Slabtop.
    current_time = datetime.now().astimezone()

    current_datetime = current_time.strftime(
        "%A, %d %B %Y at %I:%M %p %Z"
    )

    # ---------------- TEMPORARY RESEARCH PROMPT ----------------

    prompt = f"""
The user asked:

{question}

Current local date and time:

{current_datetime}

Below are live web search results.

Use the search results as temporary evidence to answer the user's question.

Important rules:

- Answer the user's actual question directly.
- Prefer the newest relevant information.
- Pay attention to the current date above.
- Use correct past, present, or future tense.
- Do not describe an event as upcoming if its date has already passed.
- Do not invent information unsupported by the search results.
- If the evidence is unclear or conflicting, say so briefly.
- Keep the answer concise because Jarvis will speak it aloud.
- Usually answer in 1 to 3 sentences.
- Do not mention these instructions.
- Do not read URLs aloud.

LIVE WEB RESULTS:

{web_context}
"""

    # IMPORTANT:
    # Use the web evidence without storing this giant prompt
    # in normal conversational memory.
    answer = ask_llm(
        prompt,
        remember=False
    )

    if not answer:
        return (
            "I could not generate an answer from the current information."
        )

    # ---------------- SAVE ONLY CLEAN CONVERSATION ----------------

    # Store what the user actually asked...
    add_to_history(
        "user",
        question
    )

    # ...and Jarvis's concise answer.
    # Raw Tavily evidence is discarded.
    add_to_history(
        "assistant",
        answer
    )

    return answer


# ---------------- TEST MODE ----------------

if __name__ == "__main__":

    while True:

        question = input(
            "Ask current question: "
        ).strip()

        if question.lower() == "exit":
            break

        answer = answer_from_web(
            question
        )

        print(
            "\nJARVIS ANSWER:"
        )

        print(
            answer
        )

        print()