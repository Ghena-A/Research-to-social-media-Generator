# pdf_pipeline.py

import re
from PyPDF2 import PdfReader


# 1️⃣ Read PDF
def read_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text


# 2️⃣ Clean raw text
def clean_text_keep_sentences(text):
    text = re.sub(r'http\S+|www\.\S+', '', text)
    text = re.sub(r"[^\w\s\u0600-\u06FF.!؟]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# 3️⃣ Split into sentences
def split_into_sentences(text):
    sentences = re.split(r'(?<=[.!?؟])\s+', text)
    return [s.strip() for s in sentences if s.strip()]


# 4️⃣ Filter bad sentences
def clean_sentences(sentences):
    cleaned = []

    for s in sentences:
        if len(s.split()) < 6:
            continue

        if re.search(
            r'\b(doi|Elsevier|ScienceDirect|license|Published|Available online)\b',
            s,
            re.IGNORECASE
        ):
            continue

        digit_ratio = sum(c.isdigit() for c in s) / max(len(s), 1)
        if digit_ratio > 0.3:
            continue

        cleaned.append(s.strip())

    return cleaned


# 5️⃣ Chunk sentences
def chunk_text(sentences, chunk_size=50, overlap=10):
    chunks = []
    i = 0
    while i < len(sentences):
        chunk = sentences[i:i + chunk_size]
        chunks.append(" ".join(chunk))
        i += chunk_size - overlap
    return chunks


# 6️⃣ Final pipeline (للإنترفيس)
def prepare_pdf_content(file, max_chunks=3):
    raw_text = read_pdf(file)
    cleaned_text = clean_text_keep_sentences(raw_text)
    sentences = split_into_sentences(cleaned_text)
    filtered = clean_sentences(sentences)
    chunks = chunk_text(filtered)

    # نأخذ أول N chunks فقط (خفيف وآمن)
    selected_chunks = chunks[:max_chunks]

    return "\n".join(selected_chunks)
