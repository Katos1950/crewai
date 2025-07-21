import json
from fastapi import APIRouter
from pydantic import BaseModel
from openai import AsyncOpenAI
import os

router = APIRouter()
openai = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
model = "gpt-4o-mini"

class CharacterRequest(BaseModel):
    genre: str
    tone: str
    storyPrompt: str
    charCount: int

@router.post("/generateCharacters")
async def generate_characters(req: CharacterRequest):
    full_prompt = f"""
    Create {req.charCount} characters for a {req.tone.lower()} {req.genre.lower()} story.
    Story prompt: {req.storyPrompt}
    For each character, give:
    - Name
    - Role
    - Motivation
    - Flaw
    - Secrets
    - Relationships to other characters.
    It is not necessary that every character has a relationship with every other character.
    Return an array of character objects in this exact format:
    format:
    [
        {{
            "name": "...",
            "role": "...",
            "motivation": "...",
            "flaw": "...",
            "secret": "...",
            "relationships": {{
                "{{target1}}": "{{relationship description}}",
                "{{target2}}": "{{relationship description}}",
            }}
        }},
        ...
    ]"""

    res = await openai.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": full_prompt}]
    )

    content = res.choices[0].message.content.replace("```json", "").replace("```", "").strip()
    return {"characters": json.loads(content)}


class SummaryRequest(BaseModel):
    story: str

@router.post("/summarizeStory")
async def summarize_story(req: SummaryRequest):
    prompt = f"Summarize the following story for memory context:\n\n{req.story}"
    response = await openai.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    content = response.choices[0].message.content
    return {"summary": content}
