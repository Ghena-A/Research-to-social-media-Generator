import streamlit as st
from generator import generate_social_post
from pdf_pipeline import prepare_pdf_content

# =========================
# Page config
# =========================
st.set_page_config(
    page_title="Research to Social Media Generator",
    layout="centered"
)

# =========================
# Custom CSS (colors & style)
# =========================
st.markdown("""
<style>
    /* خلفية غامقة نظيفة مثل Streamlit الأصلي */
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
    }

    /* صندوق المحتوى */
    .block-container {
        padding-top: 2rem;
    }

    /* زر Generate فقط */
    .stButton > button {
        background-color: #7c3aed; /* موف */
        color: white;
        border-radius: 10px;
        padding: 0.6em 1.4em;
        font-weight: 600;
        border: none;
    }

    .stButton > button:hover {
        background-color: #6d28d9; /* موف أغمق */
        color: white;
    }

    /* إزالة الخطوط والمسافات الزائدة */
    hr {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

# =========================
# Header + language (top right)
# =========================
col_title, col_lang = st.columns([4, 1])

with col_lang:
    ui_lang = st.selectbox(
        "🌐",
        ["English", "Arabic"],
        label_visibility="collapsed"
    )

def t(en, ar):
    return ar if ui_lang == "Arabic" else en

with col_title:
    st.title(t(
        "Research to Social Media Generator",
        "تحويل الأبحاث إلى محتوى وسائل التواصل"
    ))
    st.caption(t(
        "Turn research papers or summaries into ready-to-publish social media posts",
        "حوّل الأبحاث أو الملخصات إلى منشورات جاهزة للنشر"
    ))

# =========================
# Platform & language
# =========================
col1, col2 = st.columns(2)

with col1:
    platform = st.selectbox(
        t("Platform", "المنصة"),
        ["linkedin", "instagram", "facebook"]
    )

with col2:
    lang = st.selectbox(
        t("Post Language", "لغة المنشور"),
        ["en", "ar"]
    )

# =========================
# Input type
# =========================
input_type = st.radio(
    t(
        "Choose input type",
        "اختاري نوع المحتوى"
    ),
    [
        t("Research paper (PDF)", "بحث علمي (PDF)"),
        t("Written summary", "ملخص مكتوب")
    ]
)

content = ""

# =========================
# Conditional input
# =========================
if input_type == t("Research paper (PDF)", "بحث علمي (PDF)"):
    uploaded_file = st.file_uploader(
        t(
            "Upload ONE PDF file",
            "ارفع ملف pdf واحد فقط"
        ),
        type=["pdf"]
    )

    if uploaded_file is not None:
        with st.spinner(t("Processing PDF...", "جاري معالجة الملف...")):
            content = prepare_pdf_content(uploaded_file)

else:
    content = st.text_area(
        t("Paste your summary here", "الصق الملخص هنا"),
        height=220,
        placeholder=t(
            "Paste a research summary or technical text...",
            "الصق ملخص البحث أو النص هنا..."
        )
    )

# =========================
# Generate
# =========================
if st.button(t("Generate ✨", "إنشاء المحتوى ✨"), use_container_width=True):

    if not content.strip():
        st.warning(t(
            "Please provide content first.",
            "من فضلك أدخل محتوى أولًا."
        ))
    else:
        with st.spinner(t("Generating post...", "جاري إنشاء المنشور...")):
            output = generate_social_post(
                content=content,
                platform=platform,
                lang=lang
            )

        st.subheader(t("Result", "النتيجة"))

        st.text_area(
            t("Generated Post", "النص النهائي"),
            output,
            height=350
        )

        st.success(t(
            "Post generated successfully!",
            "تم إنشاء المنشور بنجاح!"
        ))
