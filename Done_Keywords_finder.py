import fitz  # PyMuPDF
import re
#from Pdf_scraper.Update_pdf.Lang_model_torch import 
pdf_path = 'Update_pdf/2022_Kamalesh_Seaweeds, an aquatic plant-based protein for sustainable nutrition - A review.pdf'

def extract_keyword(pdf_path):
    with fitz.open(pdf_path) as pdf_document:
        # Extract text from the entire document
        full_text = ''
        for page_number in range(pdf_document.page_count):
            page = pdf_document[page_number]
            full_text += page.get_text()

        # Define a more flexible pattern to capture potential Keywords based on context
        keywords_pattern = re.compile(r'keywords:\s*([\s\S]*?)(?:a b s t r a c t|abstract|introduction|©|$)', re.IGNORECASE)
#        abstract_match = re.search(r'abstract\s*([\s\S]*?)(?:introduction|\d+\s*\.\s*introduction|©|keywords|$)', all_text, re.IGNORECASE)

        # Search for potential DOIs in the text
        keyword_matches = keywords_pattern.findall(full_text)

        # Check if any matches are found and return the first one        
        for keyword in keyword_matches:
            if keyword:
                keyword = keyword.replace('\n', ', ').replace(' ,', ',')
                #keyword = keyword.replace(' ',', ')
                #keyword = ''.join(keyword.split())
                return keyword

        return "DOI not found."


# Extract DOI from the PDF
keyword = extract_keyword(pdf_path)
print("Keywords: " + keyword)
