import streamlit as st
import io
from PIL import Image
import fitz  # PyMuPDF

from utils.Image_processing import (
    load_image,
    extract_text_from_image,
    resize_image,
    preprocessing_image,
)

from utils.text_cleaner import clean_text

st.set_page_config(page_title='🧾 Document Scanner + OCR', layout="centered")
st.title('🧾 Document Scanner + Text Extractor')
st.write('Upload an image or PDF document to scan and extract text using OCR.')

uploaded_file = st.file_uploader("Upload Image or PDF", type=['jpg', 'jpeg', 'png', 'pdf'])

if uploaded_file is not None:
    file_type = uploaded_file.type

    # ---------- PDF Handling ----------
    if file_type == "application/pdf":
        pdf_doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")

        for page_num in range(len(pdf_doc)):
            page = pdf_doc.load_page(page_num)
            st.subheader(f"📄 Page {page_num + 1}")

            # Try to extract direct text first
            text = page.get_text().strip()

            if text:
                st.text_area("📝 Extracted Text (Digital)", text, height=300)
            else:
                # Fall back to OCR (image-based)
                st.warning("No digital text found. Using OCR on scanned PDF.")
                image_pix = page.get_pixmap()
                img_bytes = image_pix.tobytes("png")
                image = Image.open(io.BytesIO(img_bytes))

                st.image(image, use_column_width=True)
                processed = preprocessing_image(image)
                text = extract_text_from_image(processed)
                st.text_area("📷 OCR Extracted Text", text, height=300)

    # ---------- Image Handling ----------
    elif file_type.startswith("image/"):
        image = load_image(uploaded_file)
        st.subheader("🖼️ Uploaded Image")
        st.image(image, use_column_width=True)

        processed = preprocessing_image(image)
        text = extract_text_from_image(processed)
        st.subheader("📄 Extracted Text")
        st.text_area("Text Output", text, height=500)
