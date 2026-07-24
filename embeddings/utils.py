import re

def clean_markdown(markdown_text):

    "Convert markdown to plain text."

    if not markdown_text:
        return ""

    text = markdown_text
    text = re.sub(r"#+\s*", "", text)
    text = re.sub(r"[*_`]", "", text)
    text = re.sub(r"\[(.*?)\]\((.*?)\)", r"\1", text)
    text = re.sub(r"\n+", "\n", text)
    return text.strip()

def chunk_text(text, chunk_size=250, overlap=50):
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")
    words = text.split()
    chunks = []
    step = chunk_size - overlap

    for i in range(0, len(words), step):

        chunk = " ".join(words[i:i + chunk_size])
        if chunk.strip():
            chunks.append(chunk)

    return chunks