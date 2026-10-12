
from llm import generate_answer

sample_chunks = [
    {
        "page": 1,
        "text": (
            "Machine learning is a branch of artificial "
            "intelligence that learns patterns from data."
        ),
    }
]

question = "What is machine learning?"

answer = generate_answer(question, sample_chunks)

print("\nAnswer:")
print(answer)
