import PyPDF2

with open('Pdf_scraper/1-s2.0-S1756464620302450-main.pdf', 'rb') as file:
    pdf_reader = PyPDF2.PdfReader(file)
    metadata = pdf_reader.metadata
    #print(metadata)
    
    # Print each key-value pair on separate lines
    for key, value in metadata.items():
        print(f'{key}: {value}')