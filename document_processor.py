
import fitz


def extract_text_from_pdf(pdf_path):
    """Extract text from every page of a PDF."""

    document = fitz.open(pdf_path)
    pages = []

    for page_number, page in enumerate(document, start=1):
        text = page.get_text("text")

        if text.strip():
            pages.append({
                "page": page_number,
                "text": text
            })

    document.close()
    return pages


def split_into_chunks(pages, chunk_size=500, overlap=100):
    """Split extracted page text into overlapping chunks."""

    chunks = []

    for page in pages:
        text = page["text"]
        start = 0

        while start < len(text):
            end = min(start + chunk_size, len(text))
            chunk_text = text[start:end].strip()

            if chunk_text:
                chunks.append({
                    "page": page["page"],
                    "text": chunk_text
                })

            if end == len(text):
                break

            start = end - overlap

    return chunks


if __name__ == "__main__":
    pdf_path = input("Enter the PDF file path: ")

    pages = extract_text_from_pdf(pdf_path)
    chunks = split_into_chunks(pages)

    print("Pages extracted:", len(pages))
    print("Chunks created:", len(chunks))

    for index, chunk in enumerate(chunks[:3], start=1):
        print(f"\n--- Chunk {index} | Page {chunk['page']} ---")
        print(chunk["text"])
