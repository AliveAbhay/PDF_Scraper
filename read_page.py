import fitz  # PyMuPDF

pdf_path = 'Pdf_scraper/1-s2.0-S1756464620302450-main.pdf'

def extract_text_with_fitz(pdf_path):
    with fitz.open(pdf_path) as pdf_document:
        # Get the first page
        first_page = pdf_document[0]

        # Extract text from the first page
        text = first_page.get_text()

        return text

# Extract text from the first page of the PDF using fitz
metadata_first_page = extract_text_with_fitz(pdf_path)

# Print metadata of the first page
print(metadata_first_page)
