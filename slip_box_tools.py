from typing import Literal

from langchain_core.tools import tool
from pydantic import BaseModel, Field
from uuid import uuid4
from pathlib import Path
import re

class Note(BaseModel):
    """An atomic note"""
    id: str = Field(default_factory=lambda: str(uuid4()))
    title: str = Field(description="A concise title describing the atomic idea.")
    kind: Literal["idea", "question", "observation", "contradiction", "thought"] = Field(description="Exactly one of: idea, question, observation, contradiction, thought.")
    content : str = Field(description="The complete atomic idea. Must stand alone without requiring the original conversation.")
    links: list[str] = Field(default_factory=list, description="Related note IDs. Always leave this empty. Another tool will populate it later.")

    def to_markdown(self) -> str:
        return f"""
---
id: {self.id}

kind: {self.kind}

links: {self.links}

---

# {self.title}

{self.content}
"""

@tool
def create_note(note: Note) -> str:
    """Create an atomic note in the slip-box.

    The note MUST contain exactly these fields:

    - title
    - kind
    - content
    - links

    Never invent additional fields.
    Links should almost always be an empty list."""
    notes_dir = Path("notes")
    notes_dir.mkdir(exist_ok=True)

    safe_title = re.sub(r'[<>:"/\\|?*]', "", note.title)

    filename = notes_dir / f"{safe_title}.md"

    filename.write_text(
        note.to_markdown(),
        encoding="utf-8"
    )

    return f"Successfully created note '{safe_title}'."
