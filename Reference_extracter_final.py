import fitz
import logging

def clean_blocks(page, threshold=50):
    """Clean blocks to remove headers and footers."""
    blocks = page.get_text("blocks")
    blocks = [block for block in blocks if block[3] > threshold and block[1] < page.rect.height - threshold]

    cleaned_text_lines = [line for block in blocks for line in block[4].splitlines()]
    return '\n'.join(cleaned_text_lines)

def extract_text_from_pages(pdf_document, start_page, end_page):
    """Extract text from specified pages."""
    extracted_text = ""
    for page_num in range(start_page, end_page):
        page = pdf_document[page_num]
        cleaned_text = clean_blocks(page)
        extracted_text += cleaned_text + '\n'
    return extracted_text

def extract_after_references_and_save(pdf_path, keyword, output_file_path):
    """Extract and save text from 'References' to the end of the document."""
    try:
        pdf_document = fitz.open(pdf_path)
    except Exception as e:
        logging.error(f"Error opening the PDF file: {e}")
        return

    found_references = False

    for page_num in range(pdf_document.page_count - 1, -1, -1):
        page = pdf_document[page_num]
        page_text_without_headers = clean_blocks(page)

        if keyword.lower() in page_text_without_headers.lower():
            found_references = True
            break

    if found_references:
        extracted_text = extract_text_from_pages(pdf_document, page_num, pdf_document.page_count)
        pdf_document.close()

        print("Extracted text from 'References' to the end of the document:")
        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(extracted_text)

        print(f"Extracted text saved to {output_file_path}")
    else:
        pdf_document.close()
        print(f"'{keyword}' not found in the document.")

# Example usage
pdf_file_path = 'Pdf_scraper/Update_pdf/2020_Roberto_Ulcerative colitis_ Gut microbiota, immunopathogenesis and application of natural products in animal models.pdf'
search_keyword = 'References'
output_txt_path = 'output.txt'

extract_after_references_and_save(pdf_file_path, search_keyword, output_txt_path)
