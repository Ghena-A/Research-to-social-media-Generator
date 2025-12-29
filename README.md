# Research-to-social-media-Generator
R2S is an AI-powered tool that transforms research content (PDFs or summaries) into platform-specific social media posts. It applies text preprocessing, summarization, and prompt engineering to ensure clear, professional outputs in Arabic and English. Built as a final AI course project.
# Research to Social Media Generator (R2S)

R2S is an AI-powered application that transforms research content (PDFs or written summaries) into high-quality, platform-specific social media posts.

The project focuses on **bridging the gap between academic research and social media communication**, ensuring that complex ideas are rewritten in a clear, professional, and audience-appropriate way.

---

## 🚀 Features

- Upload **one research PDF** or paste a **written summary**
- Automatic **text extraction, cleaning, and preprocessing**
- AI-powered **summarization and content restructuring**
- Platform-specific post generation for:
  - LinkedIn
  - Instagram
  - Facebook
- Supports **Arabic and English**
- Ensures:
  - Clear structure
  - Professional tone
  - No marketing or promotional hallucinations
  - Platform-appropriate style
- Clean UI built with **Streamlit**

---

## 🧠 AI Pipeline Overview

1. **PDF Processing**
   - Extract text using PyPDF2
   - Sentence filtering and noise removal
   - Chunking long documents for safe processing

2. **Summarization**
   - Uses a transformer-based summarization model
   - Produces concise, meaningful research summaries

3. **Prompt Engineering**
   - Carefully designed prompts per platform and language
   - Ensures consistent tone and structure
   - Prevents unwanted outputs (ads, services, irrelevant content)

4. **LLM Generation**
   - Supports OpenRouter and Ollama
   - Automatically falls back if one provider fails

5. **Post-processing**
   - Arabic RTL fixes
   - Token cleanup
   - English word filtering for Arabic platforms
   - Hashtag generation

---

## 🛠 Tech Stack

- Python
- Streamlit
- Transformers (HuggingFace)
- PyPDF2
- OpenRouter API
- Ollama
- Regex-based preprocessing

---

## 📌 Project Goal

This project was built as a project, with a strong emphasis on:
- Applied NLP
- Real-world AI pipelines
- Responsible prompt engineering
- Practical product thinking

The goal is not just content generation, but **content quality, clarity, and trust**.

