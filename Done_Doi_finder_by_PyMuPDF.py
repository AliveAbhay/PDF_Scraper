import fitz  # PyMuPDF
import re

pdf_path = 'Update_pdf/2022_Kamalesh_Seaweeds, an aquatic plant-based protein for sustainable nutrition - A review.pdf'

def extract_doi(pdf_path):
    with fitz.open(pdf_path) as pdf_document:
        # Extract text from the entire document
        full_text = ''
        for page_number in range(pdf_document.page_count):
            page = pdf_document[page_number]
            full_text += page.get_text()

        # Define a more flexible pattern to capture potential DOIs based on context
        doi_pattern = re.compile(r'(https?://doi\.org/\S+|https?://dx.\S+|doi:\s*10\.\S+)', re.IGNORECASE)

        # Search for potential DOIs in the text
        doi_matches = doi_pattern.findall(full_text)

        # Check if any matches are found and return the first one
        for doi in doi_matches:
            if doi:
                return doi

        return "DOI not found."

# Extract DOI from the PDF
doi = extract_doi(pdf_path)
print(doi)