from retriever import search_meeting_notes

def test_notes_found():
    results = search_meeting_notes("backend")
    assert any("Backend development has started." in item for item in results)
    print("PASS: Backend notes found")

def test_no_notes_found():
    results = search_meeting_notes("xyznotfound123")
    assert results == ["No matching notes found."]
    print("PASS: No-match case works")

test_notes_found()
test_no_notes_found()