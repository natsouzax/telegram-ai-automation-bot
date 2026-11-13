"""Neutral demonstration content for a general technology community."""

import asyncio
from openai import OpenAI


TOPICS = (
    "digital security", "software craftsmanship", "cloud computing",
    "responsible AI", "open-source collaboration", "data privacy", "automation",
)


async def generate_tip(api_key: str | None, model: str, weekday: int) -> str:
    topic = TOPICS[weekday % len(TOPICS)]
    if not api_key:
        return f"💡 Tech tip: Explore {topic} and share one practical lesson with your community."

    def request() -> str:
        response = OpenAI(api_key=api_key).chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "Write concise, accurate, neutral educational technology tips. Avoid advertising and personal information."},
                {"role": "user", "content": f"Give one practical, helpful tip about {topic} in no more than 45 words."},
            ],
            temperature=0.6,
            max_tokens=110,
        )
        return (response.choices[0].message.content or "").strip()

    return "💡 Tech tip\n\n" + await asyncio.to_thread(request)
