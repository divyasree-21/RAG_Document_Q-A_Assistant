
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    raise ValueError(
        "GROQ_API_KEY is missing. Add it to your .env file."
    )

client = Groq(api_key=API_KEY)


def generate_answer(question, retrieved_chunks):
    """Generate an answer using relevant document passages."""

    if not retrieved_chunks:
        return "I couldn't find relevant information in the document."

    context_parts = []

    for chunk in retrieved_chunks:
        page = chunk.get("page", "Unknown")
        text = chunk.get("text", "")
        context_parts.append(
            f"Source page {page}:\n{text}"
        )

    context = "\n\n".join(context_parts)

    response = client.chat.completions.create(
        # model="llama-3.3-70b-versatile",
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a document question-answering assistant. "
                    "Answer using only the supplied document context. "
                    "If the context does not contain the answer, "
                    "say that the information was not found in the "
                    "provided document. Do not invent facts. "
                    "Mention the relevant source page numbers."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Document context:\n{context}\n\n"
                    f"Question: {question}\n\n"
                    "Answer clearly and concisely."
                ),
            },
        ],
        temperature=0.2,
        max_tokens=800,
    )

    return response.choices[0].message.content or (
        "The model returned an empty response."
    )
