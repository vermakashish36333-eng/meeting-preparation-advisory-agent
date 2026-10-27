from ai_agent import generate_ai_advice


def test_generate_ai_advice_returns_response():
    result = generate_ai_advice(
        topic="AI Agent Project Review",
        updates="Backend development has started",
        pending_tasks="Connect UI, test agent, deploy project",
        notes="The team should review pending tasks."
    )

    assert result is not None
    assert isinstance(result, str)
    assert len(result.strip()) > 0