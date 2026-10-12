
import streamlit as st
import tempfile
import os

from document_processor import extract_text_from_pdf, split_into_chunks
from retriever import DocumentRetriever
from llm import generate_answer

st.set_page_config(
    page_title="RAG Document Assistant",
    page_icon="📚",
    layout="wide"
)

st.title("📚 RAG Document Q&A Assistant")
st.write(
    "Upload a PDF and ask questions based on its contents."
)

if "retriever" not in st.session_state:
    st.session_state.retriever = None

if "messages" not in st.session_state:
    st.session_state.messages = []

uploaded_file = st.file_uploader(
    "Upload your PDF document",
    type=["pdf"]
)

if uploaded_file is not None:
    if st.button("Process Document", type="primary"):
        try:
            with st.spinner("Reading and indexing your PDF..."):
                with tempfile.NamedTemporaryFile(
                    delete=False, suffix=".pdf"
                ) as temp_file:
                    temp_file.write(uploaded_file.getvalue())
                    temp_path = temp_file.name

                try:
                    pages = extract_text_from_pdf(temp_path)
                    chunks = split_into_chunks(pages)
                finally:
                    os.unlink(temp_path)

                if not chunks:
                    st.error(
                        "No extractable text found. "
                        "This may be a scanned PDF."
                    )
                else:
                    retriever = DocumentRetriever()
                    retriever.build_index(chunks)

                    st.session_state.retriever = retriever
                    st.session_state.messages = []
                    st.success(
                        f"Processed {len(pages)} pages "
                        f"and indexed {len(chunks)} chunks."
                    )

        except Exception as error:
            st.error(f"Document processing failed: {error}")

if st.session_state.retriever is not None:
    st.divider()
    st.subheader("Ask your document")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    question = st.chat_input("Ask a question about your PDF...")

    if question:
        st.session_state.messages.append({
            "role": "user",
            "content": question
        })

        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            try:
                with st.spinner("Searching and generating an answer..."):
                    results = st.session_state.retriever.search(
                        question, top_k=3
                    )
                    answer = generate_answer(question, results)

                st.markdown(answer)

                with st.expander("View retrieved source passages"):
                    for result in results:
                        st.markdown(
                            f"**Page {result['page']} "
                            f"| Similarity: {result['score']:.3f}**"
                        )
                        st.write(result["text"])

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception as error:
                st.error(f"Could not generate answer: {error}")
else:
    st.info("Upload a PDF and click Process Document to get started.")
