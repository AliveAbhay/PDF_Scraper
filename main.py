import PyPDF2

with open('Pdf_scraper/Unknown_Hui_Potential biomedical applications of marine algae.pdf', 'rb') as file:
    pdf_reader = PyPDF2.PdfReader(file)
    metadata = pdf_reader.metadata
    #print(metadata)
    
    # Print each key-value pair on separate lines
    for key, value in metadata.items():
        print(f'{key}: {value}')