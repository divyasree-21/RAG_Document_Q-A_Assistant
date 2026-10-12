
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np


class DocumentRetriever:
    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        # Load a pretrained model that converts text into embeddings.
        self.model = SentenceTransformer(model_name)

        # These will hold the FAISS index and its corresponding chunks.
        self.index = None
        self.chunks = []

    def build_index(self, chunks):
        if not chunks:
            raise ValueError("No text chunks available to index.")

        self.chunks = chunks

        texts = [chunk["text"] for chunk in chunks]

        # Convert text into numerical vectors.
        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        embeddings = np.asarray(embeddings, dtype="float32")

        # Inner product equals cosine similarity for normalized vectors.
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dimension)
        self.index.add(embeddings)

        print(f"Indexed {len(chunks)} chunks.")

    def search(self, question, top_k=3):
        if self.index is None:
            raise ValueError("Build the index before searching.")

        # Encode the question using the same embedding model.
        query_embedding = self.model.encode(
            [question],
            convert_to_numpy=True,
            normalize_embeddings=True
        )
        query_embedding = np.asarray(query_embedding, dtype="float32")

        # Retrieve the most similar document chunks.
        k = min(top_k, len(self.chunks))
        scores, indices = self.index.search(query_embedding, k)

        results = []

        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue

            result = self.chunks[int(idx)].copy()
            result["score"] = float(score)
            results.append(result)

        return results


if __name__ == "__main__":
    from document_processor import extract_text_from_pdf, split_into_chunks

    pdf_path = input("Enter the PDF file path: ")

    pages = extract_text_from_pdf(pdf_path)
    chunks = split_into_chunks(pages)

    retriever = DocumentRetriever()
    retriever.build_index(chunks)

    while True:
        question = input("\nAsk a question (or type 'exit'): ")

        if question.lower() == "exit":
            break

        results = retriever.search(question, top_k=3)

        for i, result in enumerate(results, start=1):
            print(
                f"\nResult {i} | Page {result['page']} "
                f"| Similarity: {result['score']:.3f}"
            )
            print(result["text"])
