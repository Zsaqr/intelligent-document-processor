# app.py
import io
from typing import List, Dict

import streamlit as st
from PIL import Image
import pandas as pd

from ocr_utils import ocr_image
from ner_utils import extract_entities


# ============= Helper functions ============= #

def build_highlighted_html(text: str, entities: List[Dict]) -> str:
    """
    Takes raw text + entities and returns HTML with highlighted spans.
    """

    if not text:
        return "<p><em>No text to display.</em></p>"

    if not entities:
        # Just return the plain text if no entities found
        return f"<p>{text}</p>"

    # Sort entities by start_char
    entities_sorted = sorted(entities, key=lambda e: e["start_char"])

    # Simple color palette per label (you can expand this)
    label_colors = {
        "PERSON": "#ffeeba",
        "ORG": "#bee5eb",
        "GPE": "#c3e6cb",
        "LOC": "#d6d8db",
        "DATE": "#f5c6cb",
        "TIME": "#faf2cc",
        "MONEY": "#f1c40f33",
        "DEFAULT": "#e2e3e5",
    }

    result_html = ""
    last_idx = 0

    for ent in entities_sorted:
        start = ent["start_char"]
        end = ent["end_char"]
        label = ent["label"]
        color = label_colors.get(label, label_colors["DEFAULT"])

        # Add text before the entity
        if start > last_idx:
            result_html += text[last_idx:start]

        # Add the entity span
        span_text = text[start:end]
        result_html += (
            f'<span style="background-color:{color};'
            f' padding:2px 4px; border-radius:4px; '
            f'border:1px solid #999; margin:1px;">'
            f'{span_text} '
            f'<span style="font-size:0.7em; color:#555;">[{label}]</span>'
            f'</span>'
        )
        last_idx = end

    # Add remaining text after the last entity
    if last_idx < len(text):
        result_html += text[last_idx:]

    return f"<p>{result_html}</p>"


def run_ocr_flow():
    st.subheader("1️⃣ Upload an image for OCR")

    uploaded_file = st.file_uploader(
        "Upload a scanned document / image",
        type=["png", "jpg", "jpeg"],
    )

    ocr_lang = st.selectbox(
        "OCR language (Tesseract)",
        ["eng", "ara", "eng+ara"],  # ممكن تزود مثلا "ara" لو مسطب لغة عربية
        index=0,
    )

    if uploaded_file is not None:
        # Open the image
        image_bytes = uploaded_file.read()
        pil_image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

        st.image(pil_image, caption="Uploaded Image", use_column_width=True)

        if st.button("Run OCR"):
            with st.spinner("Running OCR..."):
                extracted_text = ocr_image(pil_image, lang=ocr_lang)

            st.success("OCR completed!")
            st.text_area("Extracted Text", value=extracted_text, height=200)

            return extracted_text

    return ""


def run_ner_flow(input_text: str = ""):
    st.subheader("2️⃣ Named Entity Recognition (NER)")

    text = st.text_area(
        "Enter or paste text here (or use the OCR output above 👆)",
        value=input_text,
        height=200,
    )

    model_name = "en_core_web_sm"

    if st.button("Run NER"):
        if not text.strip():
            st.warning("Please enter some text first.")
            return

        with st.spinner("Running NER..."):
            entities = extract_entities(text, model_name=model_name)

        if not entities:
            st.info("No entities found in the text.")
            return

        # Show table
        df = pd.DataFrame(entities)
        st.markdown("### Extracted Entities")
        st.dataframe(df)

        # Show highlighted text
        st.markdown("### Highlighted Text")
        highlighted_html = build_highlighted_html(text, entities)
        st.markdown(highlighted_html, unsafe_allow_html=True)


# ============= Streamlit App Layout ============= #

def main():
    st.set_page_config(
        page_title="Intelligent Document Processor (OCR + NER)",
        layout="wide",
    )

    st.title("📄 Intelligent Document Processor")
    st.write(
        "Combined **Optical Character Recognition (OCR)** and "
        "**Named Entity Recognition (NER)** pipeline."
    )

    mode = st.sidebar.radio(
        "Mode",
        ["OCR → NER Pipeline", "OCR Only", "NER Only"],
    )

    if mode == "OCR Only":
        st.header("OCR Only")
        _ = run_ocr_flow()

    elif mode == "NER Only":
        st.header("NER Only")
        run_ner_flow()

    else:
        st.header("End-to-End: OCR → NER Pipeline")
        st.write(
            "1. Upload an image (scanned document / handwritten note).\n"
            "2. Run OCR to extract text.\n"
            "3. Run NER on the extracted text."
        )

        extracted_text = run_ocr_flow()
        st.markdown("---")
        run_ner_flow(input_text=extracted_text)


if __name__ == "__main__":
    main()
