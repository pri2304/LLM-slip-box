from typing import Literal
from langchain_core.tools import tool
from pydantic import BaseModel, Field
from uuid import uuid4
from pathlib import Path
from ast import literal_eval
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

class SlipBox:
    def __init__(self):
        self.notes_dir = Path("notes")
        self.notes_dir.mkdir(exist_ok=True)

    def create(self, note: Note):
        safe_title = re.sub(r'[<>:"/\\|?*]', "", note.title)

        filename = self.notes_dir / f"{safe_title}.md"

        filename.write_text(
            note.to_markdown(),
            encoding="utf-8"
        )

        return note.id

    def parse_note(self, filename: Path):
        id, kind, links, title, content = "", "", [], "", ""
        i = 0
        c = 0
        filename =Path(filename)
        text = filename.read_text(encoding="utf-8")
        lines = text.splitlines()
        for line in lines:
            if line.startswith("id:"):
                id = line[len("id: "):]
            if line.startswith("kind:"):
                kind = line[len("kind: "):]
            if line.startswith("links:"):
                links = literal_eval(line[len("links: "):])
            if line.startswith("# "):
                title = line[len("# "):]
                i = c
            c += 1
        content = lines[i + 1:]
        for line in content:
            if line == "":
                content.remove(line)
        content = " ".join(content)

        note = Note(id=id, kind=kind, links=links, title=title, content=content)
        return note

    def parse_notes(self, directory: Path):
        notes = []
        for filename in directory.rglob("*.md"):
            note = self.parse_note(filename)
            notes.append(note)

        return notes

    def save_note(self, note: Note):
        path = self.notes_dir / f"{note.title}.md"
        path.write_text(note.to_markdown(), encoding="utf-8")
        return None

    def add_link(self, note1: Note, note2: Note):
        note1.links.append(note2.id)
        slipbox.save_note(note1)
        return None

    def search(self, query: str):
        notes = self.parse_notes(self.notes_dir)
        results = []
        query = query.lower()
        for note in notes:
            if query in note.title.lower():
                results.append(note)
            elif query in note.content.lower():
                results.append(note)

        return results

    def get_note(self, note_id: str):
        notes = self.parse_notes(self.notes_dir)
        for note in notes:
            if note.id == note_id:
                return note

        return None

    def follow_links(self, id: str):
        note = self.get_note(id)

        linked_notes = []

        for link_id in note.links:
            linked_notes.append(self.get_note(link_id))

        return linked_notes

slipbox = SlipBox()

@tool
def create_note(note: Note) -> dict:
    """
    Create a new atomic note in the slip-box.

    Use this when a new standalone idea, observation, question, contradiction,
    or thought should be permanently stored.

    Always provide:
    - title
    - kind
    - content

    Leave links empty unless explicitly instructed otherwise.
    """

    slipbox.create(note)

    return {"id": note.id, "title": note.title}

@tool
def search_notes(query: str):
    """
    Search the slip-box for notes related to a query.

    Returns notes whose title or content match the query.

    Use this whenever you need to retrieve relevant knowledge before answering
    or deciding what to do next.
    """
    return slipbox.search(query)

@tool
def explore_links(note_id: str):
    """
    Explore notes directly linked from a given note.

    Use this after finding an interesting note when you want additional
    related context.

    This only returns notes one link away.
    """
    return slipbox.follow_links(note_id)

@tool
def create_link(note_id1: str, note_id2: str):
    """
    Create a relationship between two existing notes.

    Use this when two ideas are meaningfully related and should reference
    each other for future retrieval.

    Do not create links unless there is a clear conceptual connection.
    """
    note1 = slipbox.get_note(note_id1)
    note2 = slipbox.get_note(note_id2)
    slipbox.add_link(note1, note2)
    return f"Successfully created link '{note_id1}' to '{note_id2}'."