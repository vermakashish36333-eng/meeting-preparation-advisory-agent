import csv
from pathlib import Path
from pypdf import PdfReader

BASE_DIR = Path(__file__).resolve().parent


def search_meeting_notes(query):
    """Search meeting notes and clearly report missing or empty notes."""
    notes_file = BASE_DIR / "meeting_notes.txt"

    if not notes_file.exists():
        return [{
            "source": "meeting_notes.txt",
            "content": (
                "Meeting notes file is missing. "
                "Proceeding with the action tracker."
            )
        }]

    text = notes_file.read_text(encoding="utf-8").strip()

    if not text:
        return [{
            "source": "meeting_notes.txt",
            "content": (
                "Meeting notes are empty. "
                "Proceeding with the action tracker."
            )
        }]

    results = []
    keywords = query.lower().split()

    for line in text.splitlines():
        line = line.strip()

        if line and any(word in line.lower() for word in keywords):
            results.append({
                "source": "meeting_notes.txt",
                "content": line
            })

    if not results:
        return [{
            "source": "meeting_notes.txt",
            "content": (
                "No matching notes found. "
                "Proceeding with the action tracker."
            )
        }]

    return results


def get_pending_actions(project_id="PRJ-7"):
    """Return pending actions for the selected project."""
    file_path = BASE_DIR / "action_tracker.csv"

    if not file_path.exists():
        return []

    with file_path.open(
        "r", encoding="utf-8-sig", newline=""
    ) as file:
        rows = list(csv.DictReader(file))

    return [
        row for row in rows
        if row.get("project_id", "").strip().upper()
        == project_id.strip().upper()
        and row.get("status", "").strip().lower() != "done"
    ]


def get_project_updates(project_id="PRJ-7"):
    """Return project updates for the selected project."""
    file_path = BASE_DIR / "project_updates.csv"

    if not file_path.exists():
        return []

    with file_path.open(
        "r", encoding="utf-8-sig", newline=""
    ) as file:
        rows = list(csv.DictReader(file))

    return [
        row for row in rows
        if row.get("project_id", "").strip().upper()
        == project_id.strip().upper()
    ]


def get_meeting_guidelines():
    """Read meeting rules from the guidelines PDF."""
    pdf_path = BASE_DIR / "meeting_guidelines.pdf"

    if not pdf_path.exists():
        return "Meeting guidelines PDF is missing."

    reader = PdfReader(str(pdf_path))
    pages = []

    for page in reader.pages:
        text = page.extract_text()
        if text:
            pages.append(text.strip())

    if not pages:
        return "No readable text found in meeting guidelines PDF."

    return "\n".join(pages)