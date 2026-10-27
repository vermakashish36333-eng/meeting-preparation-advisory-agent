from datetime import date, datetime
from pathlib import Path
import json


def identify_pending_tasks(tasks_text):
    """Convert pending tasks into a clean list."""
    return [
        task.strip()
        for task in tasks_text.split(",")
        if task.strip()
    ]


def generate_meeting_questions(topic, pending_tasks):
    """Suggest questions for the meeting."""
    questions = [
        f"What progress has been made on {topic}?",
        "What problems are blocking the team?",
    ]

    if pending_tasks:
        questions.append(
            f"What is the next step for {pending_tasks[0]}?"
        )

    questions.append("Who will handle the next action items?")
    return questions


def prioritise_agenda_items(actions, available_minutes=30):
    """Prioritize actions, merge duplicate topics, and fit meeting time."""
    priority_rank = {"high": 1, "medium": 2, "low": 3}
    merged = {}

    for action in actions:
        topic = action.get("description", "").strip()
        key = topic.casefold()

        if key not in merged:
            merged[key] = {
                **action,
                "action_ids": [action.get("action_id", "Unknown")]
            }
        else:
            existing = merged[key]
            existing["action_ids"].append(
                action.get("action_id", "Unknown")
            )

            old_priority = existing.get("priority", "").lower()
            new_priority = action.get("priority", "").lower()

            if priority_rank.get(new_priority, 4) < priority_rank.get(old_priority, 4):
                existing["priority"] = action.get("priority", "")

            old_due = existing.get("due_date", "9999-12-31")
            new_due = action.get("due_date", "9999-12-31")

            if new_due < old_due:
                existing["due_date"] = new_due

    sorted_actions = sorted(
        merged.values(),
        key=lambda action: (
            priority_rank.get(action.get("priority", "").lower(), 4),
            0 if action.get("due_date", "9999-12-31") < str(date.today()) else 1,
            action.get("due_date", "9999-12-31")
        )
    )

    agenda = []
    deferred = []
    remaining_minutes = available_minutes

    for action in sorted_actions:
        item = {
            "action_id": action.get("action_id", "Unknown"),
            "action_ids": action["action_ids"],
            "topic": action.get("description", "Untitled task"),
            "owner": action.get("owner", "Unassigned"),
            "priority": action.get("priority", "Unknown"),
            "due_date": action.get("due_date", "Unknown"),
            "overdue": (
                action.get("due_date", "9999-12-31") < str(date.today())
            ),
            "minutes": 10
        }

        if remaining_minutes >= 10:
            agenda.append(item)
            remaining_minutes -= 10
        else:
            deferred.append({
                "topic": item["topic"],
                "reason": "Deferred because the meeting has insufficient time."
            })

    return {
        "agenda": agenda,
        "deferred": deferred,
        "available_minutes": available_minutes,
        "unused_minutes": remaining_minutes
    }


def detect_status_conflicts(actions, meeting_notes):
    """Flag notes that suggest completion while tracker says Open."""
    conflicts = []
    completion_phrases = [
        "completed", "finished", "done",
        "has been finalised", "has been finalized"
    ]

    for action in actions:
        description = action.get("description", "")
        action_words = [
            word.lower().strip(".,:;")
            for word in description.split()
            if len(word) > 3
        ]

        for line in meeting_notes.splitlines():
            note = line.lower()
            mentions_action = any(word in note for word in action_words)
            says_completed = any(
                phrase in note for phrase in completion_phrases
            )

            if (
                mentions_action
                and says_completed
                and action.get("status", "").lower() == "open"
            ):
                conflicts.append({
                    "action_id": action.get("action_id", "Unknown"),
                    "action": description,
                    "tracker_status": action["status"],
                    "meeting_note": line.strip(),
                    "warning": "Notes suggest completion, but tracker says Open."
                })
                break

    return conflicts


def save_meeting_brief(brief, output_file="meeting_brief.json"):
    """Save the brief without modifying source records."""
    if not isinstance(brief, dict):
        raise ValueError("Brief must be a dictionary.")

    output_path = Path(__file__).resolve().parent / output_file
    saved_brief = {
        **brief,
        "saved_at": datetime.now().isoformat(timespec="seconds")
    }

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(saved_brief, file, indent=2, ensure_ascii=False)

    return str(output_path)