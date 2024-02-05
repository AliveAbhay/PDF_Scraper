import os
import PyPDF2
import fitz
import re
import uuid

def extract_year_of_publication(pdf_document):
    extracted_years = []  # Store extracted years in a list

    # Regular expression pattern to match dates
    date_pattern = re.compile(r'\b(?:\d{1,2} (?:[a-zA-Z]+|\d{1,2}),? \d{4}|[a-zA-Z]+ \d{1,2},? \d{4})\b')

    # Keywords associated with the publication process
    publication_keywords = ["Accepted", "Published"]

    # Iterate through each page in the PDF
    for page_number in range(pdf_document.page_count):
        # Get the text content of the page
        page = pdf_document[page_number]
        text = page.get_text()

        # Search for the date pattern in the context of publication keywords
        for keyword in publication_keywords:
            keyword_index = text.find(keyword)
            if keyword_index != -1:
                # Extract the text around the keyword
                context_text = text[keyword_index:keyword_index + 50]  # Adjust the context length as needed

                # Search for the date pattern within the context
                match = date_pattern.search(context_text)
                if match:
                    # Extract the year from the matched date
                    date_text = match.group(0)
                    year = re.search(r'\d{4}', date_text).group(0)

                    # Append the year to the list
                    extracted_years.append(year)

    return extracted_years

def extract_info_from_metadata(metadata):
    author_match = re.search(r'\b(\w+)\b', metadata.get('/Author', ''))
    title = metadata.get('/Title', 'Unknown')

    author = author_match.group(1) if author_match else None

    return author, title

def rename_pdf(original_path, new_path, years_of_publication, author, title):
    if not all((author, title)):
        print(f"Skipping file: {original_path}")
        return

    year_to_use = years_of_publication[0] if years_of_publication else 'Unknown'
    new_filename = f"{year_to_use}_{author}_{title}.pdf"
    new_full_path = os.path.join(new_path, new_filename)

    counter = 1
    while os.path.exists(new_full_path):
        unique_identifier = uuid.uuid4().hex[:6]
        new_filename = f"already_exist_{year_to_use}_{author}_{title}_{unique_identifier}.pdf"
        new_full_path = os.path.join(new_path, new_filename)
        counter += 1

    original_path = os.path.abspath(original_path)
    temp_filename = f'temp_{uuid.uuid4().hex[:6]}.pdf'
    file_path = os.path.join(new_path, temp_filename)

    os.rename(original_path, file_path)

    new_full_path = os.path.join(new_path, new_filename)

    os.rename(file_path, new_full_path)
    print(f"{original_path} renamed successfully.")

# Directory where PDF files are located
pdf_directory = 'Pdf_scraper'
files = os.listdir(pdf_directory)
pdf_files = [file for file in files if file.lower().endswith('.pdf')]
destination_folder = os.path.join(pdf_directory, 'Update_pdf')
os.makedirs(destination_folder, exist_ok=True)

# Iterate over PDF files
for pdf_file in pdf_files:
    pdf_path = os.path.join(pdf_directory, pdf_file)

    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        metadata = pdf_reader.metadata

        # Extract information from metadata
        author, title = extract_info_from_metadata(metadata)
        years_of_publication = extract_year_of_publication(fitz.open(pdf_path))

    # Print extracted information
    print("Years of publication:", ", ".join(years_of_publication))
    print(f"Author: {author}")
    print(f"Title: {title}")

    # Rename the PDF file
    rename_pdf(pdf_path, destination_folder, years_of_publication, author, title)
