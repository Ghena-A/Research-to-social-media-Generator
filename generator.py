# generator.py
from llm_clients import openrouter_generate, ollama_generate
from prompts import (
    linkedin_prompt,
    instagram_prompt,
    facebook_prompt,
    arabic_rewrite_prompt,
    social_hashtags_prompt,
    english_hashtags_prompt,
    arabic_social_hashtags_prompt
)
from postprocess import fix_rtl_display, remove_out_tokens, remove_inline_english


# =======================
# Prompt builder
# =======================
def build_prompt(content, platform, lang, length="medium"):
    if platform == "linkedin":
        return linkedin_prompt(content, lang)
    elif platform == "instagram":
        return instagram_prompt(content, lang)
    elif platform == "facebook":
        return facebook_prompt(content, lang)
    else:
        raise ValueError("Unsupported platform")


# =======================
# Low-level generate
# =======================
def generate(
    content,
    platform="linkedin",
    lang="ar",
    length="medium",
    provider="auto"
):
    prompt = build_prompt(content, platform, lang)

    if lang == "ar":
        return openrouter_generate(prompt)

    if provider == "ollama":
        try:
            return ollama_generate(prompt)
        except Exception:
            return openrouter_generate(prompt)

    return openrouter_generate(prompt)


# =======================
# High-level Social Generator
# =======================
def generate_social_post(
    content,
    platform="linkedin",
    lang="ar",
):
        # 🔹 إذا المحتوى قصير (ملخص)، نعطي توجيه صريح للتوسيع التحليلي
    if len(content.split()) < 120:
        if lang == "ar":
           content = (
                "هذا نص مختصر جدًا. "
                "المطلوب إعادة صياغته وتوسيعه بشكل مهني "
                "بالاعتماد فقط على المعلومات المذكورة صراحة في النص أدناه. "
                "يُمنع منعًا باتًا:\n"
                "- إضافة أمثلة تطبيقية\n"
                "- ذكر مجالات استخدام\n"
                "- ذكر تقنيات أو مصطلحات أو نماذج غير موجودة في النص\n"
                "- التوسع المستقبلي أو التنبؤ\n\n"
                 "النص التالي تعريف مختصر جدًا. "
                "المطلوب شرحه وتوضيحه فقط دون تكرار المعنى "
                "ودون تحويله إلى نص طويل أو مقالي:\n\n"
                + content
           )
        else:
            content = (
                "This is a short summary or brief text. "
                "Please expand it into a professional, analytical social media post suitable for the selected platform, "
                "strictly based on the ideas provided without adding promotional content, services, or external information:\n\n"
                + content
            )

    
    platform = platform.lower()

    # 1️⃣ Generate base text
    raw_text = generate(
        content=content,
        platform=platform,
        lang=lang,
    )

    # =======================
    # Arabic flow
    # =======================
    if lang == "ar":
        # Rewrite Arabic
        rewritten = openrouter_generate(
            arabic_rewrite_prompt(raw_text)
        )

        final_text = fix_rtl_display(rewritten)
        final_text = remove_out_tokens(final_text)

        if platform in ["instagram", "facebook"]:
            final_text = remove_inline_english(final_text)

        # Generate hashtags
        if platform == "facebook":
            hashtags_raw = openrouter_generate(
                arabic_social_hashtags_prompt(final_text)
            )
        else:
            hashtags_raw = openrouter_generate(
                social_hashtags_prompt(final_text)
            )

        hashtags = " ".join(
            line.strip()
            for line in hashtags_raw.split("\n")
            if line.strip().startswith("#")
        )

        return final_text.strip() + "\n\n" + hashtags

    # =======================
    # English flow
    # =======================
    else:
        hashtags_raw = openrouter_generate(
            english_hashtags_prompt(raw_text)
        )

        hashtags = " ".join(
            line.strip()
            for line in hashtags_raw.split("\n")
            if line.strip().startswith("#")
        )

        return raw_text.strip() + "\n\n" + hashtags
