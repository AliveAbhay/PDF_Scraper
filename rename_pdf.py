import os
import PyPDF2
import re
import uuid

def extract_info_from_metadata(metadata):
    # Extract year, author, and title from metadata
    year_match = re.search(r'\b(\d{4})\b', metadata.get('/Subject', ''))
    author_match = re.search(r'\b(\w+)\b', metadata.get('/Author', ''))
    title = metadata.get('/Title', 'Unknown')

    year = year_match.group(1) if year_match else None
    author = author_match.group(1) if author_match else None

    return year, author, title

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

    # Close the original PDF file
    original_path = os.path.abspath(original_path)
    temp_filename = f'temp_{uuid.uuid4().hex[:6]}.pdf'
    file_path = os.path.join(new_path, temp_filename)

    # Rename the file to a temporary name
    os.rename(original_path, file_path)

    # Construct the new full path
    new_full_path = os.path.join(os.path.dirname(original_path), new_filename)

    # Rename the file back to the correct name
    os.rename(file_path, new_full_path)
    print(f"{original_path} renamed successfully.")

# Directory where PDF files are located
pdf_directory = 'Pdf_scraper'
files = os.listdir(pdf_directory)
pdf_files = [file for file in files if file.lower().endswith('.pdf')]
destination_folder = os.path.join(pdf_directory, 'Update_pdf')
os.makedirs(destination_folder, exist_ok=True)

# Iterate over PDF files and rename them
for pdf_file in pdf_files:
    pdf_path = os.path.join(pdf_directory, pdf_file)

    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        metadata = pdf_reader.metadata

        # Extract information from metadata
        year, author, title = extract_info_from_metadata(metadata)

    # Print extracted information
    print(f"Year: {year}")
    print(f"Author: {author}")
    print(f"Title: {title}")

    # Rename the PDF file
    rename_pdf(pdf_path, destination_folder, year, author, title)
