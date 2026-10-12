# RAG Document Q&A Assistant

An AI-powered document question-answering application that allows users to upload PDF documents, ask questions about their contents, and receive context-based answers using Retrieval-Augmented Generation (RAG).

## Overview

Searching through lengthy documents manually can be time-consuming. This project combines semantic search with a Large Language Model (LLM) to retrieve relevant passages from an uploaded PDF and generate concise answers grounded in the retrieved context.

## Features

- **PDF Upload:** Upload PDF documents through a Streamlit interface.
- **Text Extraction:** Extract text from PDF pages using PyMuPDF.
- **Text Chunking:** Divide extracted text into smaller, overlapping chunks.
- **Semantic Search:** Generate text embeddings using Sentence Transformers.
- **Vector Similarity Search:** Retrieve relevant document passages using FAISS.
- **LLM-Based Answers:** Generate answers using the Groq API.
- **Source References:** Display retrieved passages with their source page numbers.
- **Interactive Interface:** Ask questions through a chat-style Streamlit interface.
- **Context-Grounded Responses:** Instruct the LLM to acknowledge when the supplied context does not contain an answer.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Application development |
| Streamlit | Interactive user interface |
| PyMuPDF | PDF text extraction |
| Sentence Transformers | Text embeddings |
| FAISS | Vector similarity search |
| Groq API | LLM-based answer generation |
| python-dotenv | Environment variable management |
| NumPy | Numerical operations |

## Project Structure

```text
RAG_Document_Assistant/
├── data/                    # Sample documents (optional)
├── vector_store/            # Reserved for vector storage
├── .env                     # API key; never commit
├── .gitignore
├── app.py                   # Streamlit application
├── document_processor.py    # PDF extraction and chunking
├── retriever.py             # Embeddings and FAISS search
├── llm.py                   # LLM integration
├── test_llm.py              # LLM connection test
├── requirements.txt         # Python dependencies
└── README.md
```

## Setup and Installation

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd RAG_Document_Assistant
```

### 2. Create and activate a virtual environment

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure the Groq API key

Create a `.env` file in the project root:

```text
GROQ_API_KEY=your_groq_api_key
```

Obtain an API key through the official Groq Console: https://console.groq.com/

Never publish your API key or commit your `.env` file.

### 5. Run the application

```bash
streamlit run app.py
```

Open the local URL displayed in the terminal, usually `http://localhost:8501`.

## How to Use

1. Launch the application.
2. Upload a text-based PDF document.
3. Select **Process Document** and wait for indexing to finish.
4. Enter a question related to the uploaded document.
5. Read the generated answer.
6. Expand the retrieved source passages to inspect the relevant text and page numbers.

## How It Works

1. **Document processing:** Extract text from the uploaded PDF and split it into overlapping chunks.
2. **Embedding generation:** Convert chunks into numerical vector representations using Sentence Transformers.
3. **Retrieval:** Use FAISS to find passages most similar to the user's question.
4. **Context construction:** Pass the retrieved passages to the LLM along with the question.
5. **Answer generation:** Use the Groq API to generate an answer based on the supplied context.
6. **Presentation:** Display the answer and retrieved source passages in Streamlit.

## Limitations

- The application requires an internet connection and working Groq API access for answer generation.
- API availability, model access, rate limits, and usage restrictions depend on the provider and account.
- Scanned PDFs without extractable text may require OCR.
- Answers can still be inaccurate; retrieved passages should be checked.
- The current implementation builds the vector index in memory when a document is processed.
- Persistent document storage and cross-session conversation history are not currently implemented.

## Future Enhancements

- Persistent vector storage and document indexing.
- Support for multiple documents.
- OCR support for scanned PDFs.
- Improved source citations and answer evaluation.
- Conversation history persistence.
- Automated tests and deployment.

## Security

Store API credentials in environment variables. Keep `.env` and `.venv/` out of version control, and never expose API keys in source code, screenshots, logs, or public repositories.

## Author

**Divya Sri Challa**

Final-year B.Tech student specializing in Computer Science and Engineering (AI & ML).

## License

Add a license before distributing or reusing this project publicly. If you choose an open-source license, include its full text in a `LICENSE` file.
