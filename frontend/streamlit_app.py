import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="MEDI ASSIST CHATBOT",
    layout="wide"
)

# Initialize chat history
if "history" not in st.session_state:
    st.session_state.history = []

# Create two columns
left_col, right_col = st.columns([1, 4])

###################################################
# LEFT PANEL
###################################################

with left_col:

    st.header("Upload Documents")

    uploaded_file = st.file_uploader(
        "Upload PDF",
        type=["pdf"]
    )

    if uploaded_file is not None:

        files = {
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                "application/pdf"
            )
        }

        response = requests.post(
            f"{BACKEND_URL}/upload",
            files=files
        )

        if response.status_code == 200:
            st.success("Document uploaded successfully")

    st.divider()

    st.subheader("Sources")

    st.write("• External PDF documents")
    st.write("• Images")
    st.write("• Database")

###################################################
# RIGHT PANEL
###################################################

with right_col:

    st.title("MEDI ASSIST CHATBOT")

    question = st.text_input(
        "Ask your question"
    )

    if st.button("Submit"):

        if question.strip() != "":

            response = requests.post(
                f"{BACKEND_URL}/ask",
                json={
                    "question": question
                }
            )

            result = response.json()

            st.session_state.history.append(
                {
                    "question": question,
                    "answer": result["answer"],
                    "score": result["score"],
                    "source": result["source"]
                }
            )

            # Maintain only last 10 chats
            if len(st.session_state.history) > 10:
                st.session_state.history.pop(0)

    st.divider()

    st.subheader("Conversation")

    for chat in reversed(st.session_state.history):

        with st.chat_message("user"):
            st.write(chat["question"])

        with st.chat_message("assistant"):
            st.write(chat["answer"])

            st.caption(
                f"Source: {chat['source']}"
            )

            st.caption(
                f"Similarity Score: {chat['score']:.4f}"
            )