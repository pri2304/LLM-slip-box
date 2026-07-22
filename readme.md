# LLM Slip-Box

An experimental implementation of Niklas Luhmann's slip-box (Zettelkasten) system inspired by *How to Take Smart Notes* by Sönke Ahrens.

The project explores how a local LLM can use a slip-box as external memory by searching existing notes, reasoning over them, creating new atomic notes, and linking related ideas through tool use.

## Project Structure

```text
.
├── notes/              # Stored markdown notes
├── prompts/            # System prompts
├── llm-core.py         # Main LLM loop
├── slip_box_tools.py   # Slip-box implementation & tools
├── readme.md
├── pyproject.toml
└── uv.lock
```

## Requirements

* Python 3.14+
* uv
* Ollama
* A tool-calling model (currently tested with `qwen3.5:9b`)

## Installation

Clone the repository:

```bash
git clone <repo-url>
cd llm-slip-box
```

Install dependencies:

```bash
uv sync
```

Pull the model (if needed):

```bash
ollama pull qwen3.5:9b
```

Any Ollama model with reliable tool-calling support should work. The project is currently tested with `qwen3.5:9b`.
## Running

```bash
uv run python llm-core.py
```

## Usage

Type a prompt and press **Esc + Enter** to submit.

Available commands:

```text
/bye #exit chat
```

*More commands to be added in the future.*

## How It Works

1. The user interacts with the LLM.
2. The LLM searches the slip-box.
3. Existing notes are used for reasoning.
4. New atomic notes are created when appropriate.
5. Related notes are linked together.

## Example Note

```markdown
---
id: 9c8d...
kind: observation
links: []

---

# Atomic Notes

An atomic note contains a singular idea.
```

## Roadmap

* [ ] Better semantic search
* [ ] Embedding support
* [ ] Rich/Textual terminal UI
* [ ] Improved linking strategies
* [ ] Note ranking
* [ ] Agentic flow
* [ ] Continuous mode (for researching or long term work)
* [ ] Configurable search strategies
* [ ] Multiple agent workflows
* [ ] Web search integration
* [ ] Better note visualization (Similar to obsidian)

## Status

This project is experimental and under active development. Expect breaking changes as the architecture evolves.

## License

TODO
