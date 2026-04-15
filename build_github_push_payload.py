import json
from pathlib import Path


def main() -> None:
    base = Path(__file__).resolve().parent
    nb = (base / "rag1.ipynb").read_text(encoding="utf-8")

    gitignore = """# Secrets
.env
.env.*

# Local vector DB / caches
chroma_db/
__pycache__/
.ipynb_checkpoints/
"""

    readme = """# AIEngineeringWeek2V1

LangChain RAG notebook: rag1.ipynb (Week 2 assignment).

## Setup

- Create a `.env` file locally with your `OPENAI_API_KEY` (do not commit it).
- Place `textbook_1.pdf` and `textbook_2.pdf` next to the notebook (not committed here).

## Run

Open `rag1.ipynb` and execute cells in order.
"""

    payload = {
        "owner": "zainabahmed4626-lab",
        "repo": "AIEngineeringWeek2V1",
        "branch": "main",
        "message": "Initial commit: add RAG notebook",
        "files": [
            {"path": "rag1.ipynb", "content": nb},
            {"path": ".gitignore", "content": gitignore},
            {"path": "README.md", "content": readme},
        ],
    }

    out = base / "_push_payload.json"
    out.write_text(json.dumps(payload), encoding="utf-8")
    print(f"wrote {out} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
