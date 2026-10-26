from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR

def search_meeting_notes(query):
    results = []
    keywords = query.lower().split()

    if not DATA_DIR.exists():
        return ["ERROR: data folder not found."]

    for file_path in DATA_DIR.glob("*.txt"):
        text = file_path.read_text(encoding="utf-8")

        for line in text.splitlines():
            line_lower = line.lower()

            if any(word in line_lower for word in keywords):
                results.append(f"{file_path.name}: {line.strip()}")

    if not results:
        return ["No matching notes found."]

    return results