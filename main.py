import PyPDF2
import streamlit as st
import tempfile
import os
import qrcode

def extract_text_from_pdf(uploaded_file):
    text = ''
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    num_pages = len(pdf_reader.pages)
    for page_number in range(num_pages):
        page = pdf_reader.pages[page_number]
        text += page.extract_text()
    return text.strip()

def generate_temp_pdf_link(uploaded_file):
    temp_dir = tempfile.TemporaryDirectory()
    temp_path = os.path.join(temp_dir.name, "uploaded_pdf.pdf")
    with open(temp_path, "wb") as temp_file:
        temp_file.write(uploaded_file.getvalue())
    return temp_path

def generate_qr_code(url):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    return img

def main():
    st.title('PDF to QR Code Converter')
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    if uploaded_file is not None:
        pdf_contents = extract_text_from_pdf(uploaded_file)
        st.subheader("PDF Content:")
        st.write(pdf_contents)

        temp_pdf_path = generate_temp_pdf_link(uploaded_file)
        st.subheader("Temporary PDF Link:")
        st.text(temp_pdf_path)

        qr = generate_qr_code(temp_pdf_path)
        qr_file_path = "generated_qr_code.png"
        qr.save(qr_file_path)
        st.subheader("Generated QR Code:")
        st.image(qr_file_path, caption='QR Code', use_column_width=True)

if __name__ == "__main__":
    main()
