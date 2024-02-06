import PyPDF2
import re
pdf_path = 'Pdf_scraper/2015_Klaus_Dietary seaweeds and obesity.pdf'

def extract_accepted_year(pdf_path):
    year = ""
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        first_page_text = pdf_reader.pages[0].extract_text()
        # Define the pattern for extracting the accepted year
        year_pattern = re.compile(r'accepted.*?(\d{4})', re.IGNORECASE)
        #Search for the accepted year in the first page text
        year_match = year_pattern.search(first_page_text)
        if year_match:
            year = year_match.group(1).strip()
    return year
# Replace 'your_paper.pdf' with the actual path to your PDF file
accepted_year = extract_accepted_year(pdf_path)

if accepted_year:
    print("Accepted Year:", accepted_year)
else:
    print("No Accepted Year Found.")
