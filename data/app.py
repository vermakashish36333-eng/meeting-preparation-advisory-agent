from datetime import date
from ai_agent import generate_ai_advice
from retriever import search_meeting_notes
from agent_tools import identify_pending_tasks, generate_meeting_questions


def prepare_meeting_brief(topic, updates, tasks_text):
    pending_tasks = identify_pending_tasks(tasks_text)
    questions = generate_meeting_questions(topic, pending_tasks)

    return {
        "date": str(date.today()),
        "topic": topic,
        "updates": updates,
        "pending_tasks": pending_tasks,
        "questions": questions,
    }


def main():
    print("=== Meeting Preparation Advisory Agent ===")

    topic = input("Enter meeting topic: ")
    updates = input("Enter project updates: ")
    tasks_text = input("Enter pending tasks (comma-separated): ")

    brief = prepare_meeting_brief(topic, updates, tasks_text)
    print("\n--- Relevant Meeting Notes ---")
    notes = search_meeting_notes(topic + " " + updates + " " + tasks_text)

    for note in notes:
        print("-", note)

    print("\n--- Your Meeting Brief ---")
    print("Date:", brief["date"])
    print("Topic:", brief["topic"])
    print("Project updates:", brief["updates"])

    print("\nPending tasks:")
    for task in brief["pending_tasks"]:
        print("-", task)

    print("\nSuggested questions:")
    for question in brief["questions"]:
        print("-", question)

    print("\n--- AI-Generated Meeting Advice ---")
    ai_advice = generate_ai_advice(
        topic=topic,
        updates=updates,
        pending_tasks=", ".join(brief["pending_tasks"]),
        notes="\n".join(notes)
    )
    print(ai_advice)

if __name__ == "__main__":
    main()