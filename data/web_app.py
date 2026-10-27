import streamlit as st
from datetime import date

from retriever import search_meeting_notes
from agent_tools import (
    identify_pending_tasks,
    generate_meeting_questions,
)
from ai_agent import generate_ai_advice


st.set_page_config(
    page_title="Meeting Preparation Advisory Agent",
    layout="wide",
)

st.title("📋 Meeting Preparation Advisory Agent")
st.write("Prepare your next meeting here.")

topic = st.text_input("Meeting Topic")
updates = st.text_area("Project Updates")
tasks = st.text_area(
    "Pending Tasks",
    help="Enter tasks separated by commas or new lines."
)

if st.button("Generate Meeting Brief"):
    if not topic.strip():
        st.warning("Please enter a meeting topic.")
    else:
        try:
            pending_tasks = identify_pending_tasks(
                tasks.replace("\n", ",")
            )

            notes = search_meeting_notes(
                topic + " " + updates + " " + tasks
            )

            # Convert note dictionaries into readable text
            notes_text = "\n".join(
                note.get("content", "")
                if isinstance(note, dict)
                else str(note)
                for note in notes
            )

            st.success("Meeting brief generated!")
            st.write("**Date:**", date.today())
            st.write("**Meeting Topic:**", topic)
            st.write(
                "**Project Updates:**",
                updates or "Not provided"
            )

            st.subheader("Pending Tasks")
            if pending_tasks:
                for task in pending_tasks:
                    st.write("•", task)
            else:
                st.info("No pending tasks provided.")

            st.subheader("Relevant Meeting Notes")
            if notes:
                for note in notes:
                    if isinstance(note, dict):
                        source = note.get("source", "Unknown source")
                        content = note.get("content", "")
                        st.write(f"• **{source}:** {content}")
                    else:
                        st.write("•", note)
            else:
                st.info("No relevant meeting notes found.")

            st.subheader("Suggested Questions")
            questions = generate_meeting_questions(
                topic, pending_tasks
            )
            for question in questions:
                st.write("•", question)

            st.subheader("AI-Generated Meeting Advice")
            with st.spinner("Generating AI advice..."):
                advice = generate_ai_advice(
                    topic=topic,
                    updates=updates or "Not provided",
                    pending_tasks=", ".join(pending_tasks),
                    notes=notes_text or "No relevant meeting notes found."
                )

            if advice:
                st.markdown(advice)
            else:
                st.warning("The AI returned an empty response.")

        except Exception as e:
            st.error(f"Error: {e}")