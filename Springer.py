import fitz
import re
import os

pdf_directory = 'Pdf_scraper'
files = os.listdir(pdf_directory)
pdf_files = [file for file in files if file.lower().endswith('.pdf')]

def extract_year_of_publication(pdf_files):
    extracted_years = []  # Store extracted years in a list

    for pdf_file in pdf_files:
        try:
            # Open the PDF file
            pdf_document = fitz.open(os.path.join(pdf_directory, pdf_file))

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

            # Close the PDF document for the current file
            pdf_document.close()

        except fitz.FileDataError as e:
            print(f"Error processing {pdf_file}: {e}")

        except Exception as e:
            print(f"An unexpected error occurred while processing {pdf_file}: {e}")

    return extracted_years

# Example usage
years_of_publication = extract_year_of_publication(pdf_files)

if years_of_publication:
    print("Years of publication:", ", ".join(years_of_publication))
else:
    print("Years of publication not found.")
