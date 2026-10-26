from ai_agent import generate_ai_advice

result = generate_ai_advice(
    topic="AI Agent Project Review",
    updates="Backend development has started",
    pending_tasks="Connect UI, test agent, deploy project",
    notes="The team should review pending tasks."
)

print("\n--- AI Response ---\n")
print(result)