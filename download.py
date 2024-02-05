import requests

def download_file(url, destination):
    response = requests.get(url)
    with open(destination, 'wb') as file:
        file.write(response.content)

# Example usage:
url = 'https://sci-hub.ru/https://doi.org/10.1016/j.jnutbio.2018.03.008'
destination = 'downloaded_Pdf_scraper.pdf'

download_file(url, destination)
