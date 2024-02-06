import PyPDF2
import re

def extract_abstract(pdf_path):
    abstract = ""
    
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        
        # Extract text from all pages
        all_text = ""
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            all_text += page.extract_text()

        # Try to find the abstract using regular expressions
        abstract_match = re.search(r'abstract\s*([\s\S]*?)(?:introduction|\d+\s*\.\s*introduction|©|keywords|$)', all_text, re.IGNORECASE)
        
        if abstract_match:
            abstract = abstract_match.group(1).strip()
            abstract = ' '.join(abstract.split())
        return abstract

# Replace 'your_paper.pdf' with the actual path to your PDF file
pdf_path = 'Update_pdf/2020_Si_Implications of agar and agarase in industrial applications of sustainable marine biomass.pdf'
output_file_path = 'abstract.txt'
abstract_text = extract_abstract(pdf_path)

if abstract_text:
    print("Abstract: ",abstract_text)
else:
    print("No abstract found.")

with open(output_file_path, 'w', encoding='utf-8') as output_file:
    output_file.write("Abstract: " + abstract_text)

print(f"Abstract saved to {output_file_path}")