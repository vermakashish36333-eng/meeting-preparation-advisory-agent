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
tasks = st.text_area("Pending Tasks", help="Enter tasks separated by commas or new lines.")

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

            st.success("Meeting brief generated!")
            st.write("**Date:**", date.today())
            st.write("**Meeting Topic:**", topic)
            st.write("**Project Updates:**", updates or "Not provided")

            st.subheader("Pending Tasks")
            for task in pending_tasks:
                st.write("•", task)

            st.subheader("Relevant Meeting Notes")
            for note in notes:
                st.write("•", note)

            st.subheader("Suggested Questions")
            for question in generate_meeting_questions(topic, pending_tasks):
                st.write("•", question)

            st.subheader("AI-Generated Meeting Advice")
            with st.spinner("Generating AI advice..."):
                advice = generate_ai_advice(
                    topic=topic,
                    updates=updates or "Not provided",
                    pending_tasks=", ".join(pending_tasks),
                    notes="\n".join(notes),
                )
            st.markdown(advice)

        except Exception as e:
            st.error(f"Error: {e}")