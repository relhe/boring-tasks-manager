import requests
from bs4 import BeautifulSoup
import os
import re
import time


def download_pdf(pdf_url, download_folder):
    """Downloads a PDF given its URL."""
    response = requests.get(pdf_url, stream=True)
    pdf_name = pdf_url.split('/')[-1] + ".pdf"
    pdf_path = os.path.join(download_folder, pdf_name)

    with open(pdf_path, "wb") as pdf_file:
        for chunk in response.iter_content(chunk_size=1024):
            pdf_file.write(chunk)
    print(f"Downloaded: {pdf_path}")


def get_pdf_link(detail_page_url):
    """Extracts the direct PDF download link from a detail page."""
    detail_response = requests.get(detail_page_url)
    detail_soup = BeautifulSoup(detail_response.text, "html.parser")

    # Modify selector as needed if PDF links are in different elements
    download_button = detail_soup.find("a", {"id": "download-button"})
    if download_button:
        pdf_link = download_button["href"]
        return pdf_link
    return None


def find_pdfs(base_url, download_folder="pdf_downloads"):
    """Finds and downloads PDFs from the base URL page listing."""
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Modify this selector to match the list of books or PDFs
    detail_links = soup.find_all("a", href=re.compile(r"^/.*\.html$"))

    for link in detail_links:
        detail_page_url = base_url + link["href"]

        # Retrieve and download the PDF link from the detail page
        pdf_url = get_pdf_link(detail_page_url)
        if pdf_url:
            download_pdf(pdf_url, download_folder)
        else:
            print(f"No direct PDF link found for {detail_page_url}")
        time.sleep(1)  # To respect server and avoid getting blocked


if __name__ == "__main__":
    base_url = "https://www.pdfdrive.com"
    find_pdfs(base_url)
