import PyPDF2
import re

pdf_path = 'Update_pdf/2022_Kamalesh_Seaweeds, an aquatic plant-based protein for sustainable nutrition - A review.pdf'
output_file_path = 'abstract.txt'

def extract_abstract(pdf_path):
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        
        # Extract text from the first page
        first_page_text = pdf_reader.pages[0].extract_text()
        
        # Define the pattern for extracting the abstract
        abstract_pattern = re.compile(r'ABSTRACT(.*?)(?:\n\n|\n\d+\s*\.\s*[A-Z])', re.DOTALL)
        
        # Search for the abstract in the first page text
        abstract_match = abstract_pattern.search(first_page_text)
        
        # Check if a match is found and extract the abstract
        if abstract_match:
            abstract = abstract_match.group(1).strip()
            # Replace multiple spaces with a single space
            abstract = ' '.join(abstract.split())
            return abstract
        else:
            return "Abstract not found."

# Extract abstract from the PDF
abstract = extract_abstract(pdf_path)

# Save the abstract to a text file
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    output_file.write(abstract)

print(f"Abstract saved to {output_file_path}")

#print(abstract)
