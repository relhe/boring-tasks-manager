from googlesearch import search
import time
import ssl
import requests
import certifi
import os
import random

# Use the certifi certificate store
ssl._create_default_https_context = ssl.create_default_context(
    cafile=certifi.where())

# Directory to save downloaded PDFs
DOWNLOAD_DIR = "pdf_downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


def download_pdf(url, title):
    try:
        response = requests.get(url, stream=True, timeout=10)
        if response.headers.get("content-type", "").lower() == "application/pdf":
            file_path = os.path.join(DOWNLOAD_DIR, f"{title}.pdf")
            with open(file_path, "wb") as pdf_file:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        pdf_file.write(chunk)
            print(f"Downloaded: {file_path}")
        else:
            print(f"Skipping (not a PDF): {url}")
    except Exception as e:
        print(f"Error downloading {url}: {e}")


# Create an unverified SSL context
ssl._create_default_https_context = ssl._create_unverified_context

# List of books and their authors
books = []

books_list = []

# Perform Google searches for free PDF versions
for book in books_list:
    query = f"{book} free PDF"
    print(f"Searching for: {query}\n")

    try:
        for result in search(query, num=3, stop=3, pause=2):
            print(f"Found: {result}")
            download_pdf(result, book.replace(' ', '_'))

        print("\n---\n")
        time.sleep(random.randint(10, 20))
    except Exception as e:
        print(f"An error occurred while searching for '{book}': {e}\n")
