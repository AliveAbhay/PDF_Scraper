import fitz  # PyMuPDF
import re

pdf_path = 'Pdf_scraper/1-s2.0-S1756464620302450-main.pdf'

def extract_doi(pdf_path):
    with fitz.open(pdf_path) as pdf_document:
        # Extract text from the entire document
        full_text = ''
        for page_number in range(pdf_document.page_count):
            page = pdf_document[page_number]
            full_text += page.get_text()

        # Define a more flexible pattern to capture potential DOIs based on context
        doi_pattern = re.compile(r'https?://doi\.org/(\S+)|doi:\s*(10\.\S+)', re.IGNORECASE)

        # Search for potential DOIs in the text
        doi_matches = doi_pattern.findall(full_text)

        # Check if any matches are found and return the first one
        for doi_match in doi_matches:
            for doi in doi_match:
                if doi:
                    return f"https://doi.org/{doi}"
        return "DOI not found."

# Extract DOI from the PDF
doi = extract_doi(pdf_path)
print(f"DOI: {doi}")
