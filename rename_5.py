import os
import PyPDF2
import re
import uuid
#from Pdf_scraper.Update_pdf.Lang_model_torch import specific_function, specific_class

# Directory where PDF files are located
pdf_directory = 'Pdf_scraper'
files = os.listdir(pdf_directory)
pdf_files = [file for file in files if file.lower().endswith('.pdf')]
destination_folder = os.path.join(pdf_directory, 'Update_pdf')
os.makedirs(destination_folder, exist_ok=True)

def extract_accepted_year(pdf_path):
    accepted_year = ""
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        first_page_text = pdf_reader.pages[0].extract_text()
        # Define the pattern for extracting the accepted year
        year_pattern = re.compile(r'accepted.*?(\d{4})', re.IGNORECASE)
        #year_pattern = re.compile(r'accepted\s*\d{1,2}\s\w+\s(\d{4})', re.IGNORECASE)
        # Search for the accepted year in the text
        year_match = year_pattern.search(first_page_text)
        if year_match:
            accepted_year = year_match.group(1).strip()
    return accepted_year

def extract_info_from_metadata(metadata):
    # Extract author and title from metadata
    author_match = re.search(r'\b(\w+)\b', metadata.get('/Author', ''))
    title = metadata.get('/Title', 'Unknown')

    author = author_match.group(1) if author_match else None

    return author, title

def rename_pdf(original_path, new_path, year, author, title):
    # Skip if essential information is missing
    if not all((year, author, title)):
        print(f"Skipping file: {original_path}")
        return

    # Create a new filename based on extracted information
    new_filename = f"{year}_{author}_{title}.pdf"
    new_full_path = os.path.join(new_path, new_filename)

    # Check for existing files in the destination folder
    counter = 1
    while os.path.exists(new_full_path):
        # Append a unique identifier to the filename
        unique_identifier = uuid.uuid4().hex[:6]
        new_filename = f"already_exist_{year}_{author}_{title}_{unique_identifier}.pdf"
        new_full_path = os.path.join(new_path, new_filename)
        counter += 1

    # Construct the new full path
    new_full_path = os.path.join(new_path, new_filename)

    # Rename the file
    os.rename(original_path, new_full_path)
    print(f"{original_path} renamed successfully.")

# Iterate over PDF files and rename them
for pdf_file in pdf_files:
    pdf_path = os.path.join(pdf_directory, pdf_file)

    pdf_reader = PyPDF2.PdfReader(pdf_path)
    metadata = pdf_reader.metadata

    # Extract information from metadata
    year = extract_accepted_year(pdf_path)
    author, title = extract_info_from_metadata(metadata)

    # Print extracted information
    print(f"Year: {year}")
    print(f"Author: {author}")
    print(f"Title: {title}")

    # Rename the PDF file
    rename_pdf(pdf_path, destination_folder, year, author, title)
