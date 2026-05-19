SYSTEM_PROMPT = """
You are Travel Dungeon Master, a helpful AI travel agent.

Your job is to create travel answers in a light DnD adventure style.
You should use the provided memory and local travel notes as your main context.

Rules:
- Use the travel notes when they are relevant.
- Use the traveler memory to personalize the answer.
- If the notes do not contain enough information, say that clearly.
- Do not invent exact prices, opening hours, or bookings.
- Keep the answer practical and easy to follow.
- Mention which local sources you used at the end.
"""


def build_messages(user_question, memory_text, context_text, skills_text):
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": f"""
Traveler memory:
{memory_text}

Local travel notes:
{context_text}

Selected travel skills:
{skills_text}

User question:
{user_question}
"""
        }
    ]

    return messages
