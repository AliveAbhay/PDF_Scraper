import PyPDF2

pdf_path = 'Pdf_scraper/Unknown_Hui_Potential biomedical applications of marine algae.pdf'

def extract_metadata(pdf_path):
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)

        # Access the Info dictionary containing metadata
        metadata = pdf_reader.metadata

        # Extract specific metadata items
        creator = metadata.get('/Creator', None)
        keywords = metadata.get('/Keywords', None)

        return creator, keywords

# Extract metadata from the PDF using PyPDF2
creator, keywords = extract_metadata(pdf_path)

# Check if Creator metadata is available
if creator is not None:
    print(f"Journal: {creator}")
else:
    print("Creator metadata not available.")

# Check if Keywords metadata is available
if keywords is not None:
    print(f"Keywords: {keywords}")
else:
    print("Keywords metadata not available.")
