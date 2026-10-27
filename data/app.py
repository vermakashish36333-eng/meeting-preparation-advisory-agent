from datetime import date
from retriever import (
    get_meeting_guidelines,
    search_meeting_notes,
    get_pending_actions,
    get_project_updates,
)
from agent_tools import (
    generate_meeting_questions,
    prioritise_agenda_items,
    detect_status_conflicts,
    save_meeting_brief,
)


def prepare_meeting_brief(project_id="PRJ-7", available_minutes=30):
    actions = get_pending_actions(project_id)
    updates = get_project_updates(project_id)
    guidelines = get_meeting_guidelines()

    query = " ".join(
        [project_id]
        + [item["description"] for item in actions]
        + [item["update"] for item in updates]
    )
    notes = search_meeting_notes(query)
    notes_text = "\n".join(item["content"] for item in notes)

    agenda_result = prioritise_agenda_items(actions, available_minutes)
    conflicts = detect_status_conflicts(actions, notes_text)

    questions = generate_meeting_questions(
        project_id,
        [item["description"] for item in actions],
    )

    brief = {
        "date": str(date.today()),
        "project_id": project_id,
        "available_minutes": available_minutes,
        "project_updates": updates,
        "pending_actions": actions,
        "agenda": agenda_result["agenda"],
        "deferred_items": agenda_result["deferred"],
        "unused_minutes": agenda_result["unused_minutes"],
        "status_conflicts": conflicts,
        "relevant_notes": notes,
        "suggested_questions": questions,
        "meeting_guidelines": guidelines,
        "sources": [
            "action_tracker.csv",
            "project_updates.csv",
            "meeting_notes.txt",
            "meeting_guidelines.pdf",
        ],
    }

    return brief


def main():
    print("=== Meeting Preparation Advisory Agent ===")

    project_id = input("Enter project ID (default PRJ-7): ").strip()
    if not project_id:
        project_id = "PRJ-7"

    minutes_text = input("Available meeting minutes (default 30): ").strip()
    try:
        minutes = int(minutes_text) if minutes_text else 30
        if minutes <= 0:
            raise ValueError
    except ValueError:
        print("Please enter a positive whole number for meeting minutes.")
        return

    brief = prepare_meeting_brief(project_id, minutes)

    print("\n--- Project Updates ---")
    for update in brief["project_updates"]:
        print(
            f"- {update['date']}: {update['update']} "
            f"(Blocker: {update['blocker']})"
        )

    print("\n--- Pending Actions ---")
    for action in brief["pending_actions"]:
        print(
            f"- {action['action_id']}: {action['description']} "
            f"| Owner: {action['owner']} | Priority: {action['priority']} "
            f"| Due: {action['due_date']}"
        )

    print("\n--- Prioritised Agenda ---")
    for item in brief["agenda"]:
        print(
            f"- {item['topic']} ({item['minutes']} min; "
            f"owner: {item['owner']})"
        )

    print("\n--- Deferred Items ---")
    print(brief["deferred_items"] or "None")

    print("\n--- Status Conflicts ---")
    print(
        brief["status_conflicts"]
        or "No conflicts detected in retrieved notes."
    )

    print("\n--- Relevant Notes ---")
    for note in brief["relevant_notes"]:
        print(f"- [{note['source']}] {note['content']}")

    print("\n--- Meeting Guidelines from PDF ---")
    print(brief["meeting_guidelines"])

    print("\n--- Suggested Questions ---")
    for question in brief["suggested_questions"]:
        print("-", question)

    output_path = save_meeting_brief(brief)
    print("\nMeeting brief saved to:", output_path)


if __name__ == "__main__":
    main()