from pathlib import Path

def get_startup_message():
    root_path = Path(__file__).parent.parent
    language = "en"
    path = root_path / f"chainlit_{language}.md" if (root_path / f"chainlit_{language}.md").exists() else root_path / "chainlit.md"
    return path.read_text()
