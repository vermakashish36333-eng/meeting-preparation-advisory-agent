def identify_pending_tasks(tasks_text):
    """Convert pending tasks into a clean list."""

    tasks = tasks_text.split(",")

    return [
        task.strip()
        for task in tasks
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