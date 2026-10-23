import sys
from pathlib import Path

import streamlit as st

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1])
)

from src.rag_pipeline import (
    extract_text,
    split_text,
    create_vector_index,
    retrieve_context,
    generate_answer
)


st.set_page_config(
    page_title="RAG Document Chatbot",
    page_icon="📚",
    layout="wide"
)

st.title("📚 AI Document Chatbot")
st.write("Upload a PDF and ask questions about its content.")

uploaded_file = st.file_uploader(
    "Upload your PDF",
    type=["pdf"]
)

if uploaded_file is not None:

    if st.button("Process Document"):

        with st.spinner("Processing your PDF..."):

            text = extract_text(uploaded_file)

            if not text.strip():
                st.error(
                    "No readable text found. "
                    "The PDF may contain scanned images."
                )
                st.stop()

            chunks = split_text(text)

            index, embeddings = create_vector_index(chunks)

            st.session_state["chunks"] = chunks
            st.session_state["index"] = index
            st.session_state["filename"] = uploaded_file.name

        st.success(
            f"Document processed successfully! "
            f"Created {len(chunks)} chunks."
        )


if "index" in st.session_state:

    st.subheader("Ask a question")

    question = st.text_input(
        "Enter your question about the document"
    )

    if st.button("Get Answer") and question.strip():

        with st.spinner("Searching and generating an answer..."):

            context = retrieve_context(
                question,
                st.session_state["chunks"],
                st.session_state["index"]
            )

            try:
                answer = generate_answer(question, context)

                st.markdown("### Answer")
                st.write(answer)

                with st.expander("View retrieved context"):
                    st.write(context)

            except Exception as error:
                st.error(f"Could not generate answer: {error}")
