import os
import time
import random
import ssl
import requests
from googlesearch import search


class PDFDownloader:
    def __init__(self, books, download_dir="books"):
        self.books = books
        self.download_dir = download_dir
        self.downloaded_books = []
        self.unsuccessful_books = []
        os.makedirs(self.download_dir, exist_ok=True)
        ssl._create_default_https_context = ssl._create_unverified_context

    def download_pdf(self, url, title):
        file_path = os.path.join(self.download_dir, f"{title}.pdf")
        if os.path.exists(file_path):
            print(f"Skipping (already downloaded): {url}")
            return "Skipped"

        try:
            response = requests.get(url, stream=True, timeout=10)
            if response.headers.get("content-type", "").lower() == "application/pdf":
                with open(file_path, "wb") as pdf_file:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            pdf_file.write(chunk)
                print(f"Downloaded: {file_path}")
                return "Downloaded"
            else:
                print(f"Skipping (not a PDF): {url}")
                return "Try_again"
        except Exception as e:
            print(f"Error downloading {url}: {e}")
            return "Error"

    def search_and_download(self):
        for book in self.books:
            query = f"{book} free PDF"
            print(f"Searching for: {query}\n")
            try:
                for result in search(query, num=1, stop=1, pause=random.randint(5, 10)):
                    print(f"Found: {result}")
                    feedback = self.download_pdf(
                        result, book.replace(' ', '_'))
                    if feedback == "Downloaded":
                        self.downloaded_books.append(book)
                        break
                    elif feedback == "Skipped":
                        break
                    elif feedback == "Try_again":
                        self.unsuccessful_books.append(book)
                        continue
                    elif feedback == "Error":
                        self.unsuccessful_books.append(book)
                print("\n---\n")
                # Longer delay to avoid rate limits
                time.sleep(random.randint(5, 15))
            except Exception as e:
                print(f"An error occurred while searching for '{book}': {e}\n")
                self.unsuccessful_books.append(book)

    def print_summary(self):
        print(f"Downloaded {len(self.downloaded_books)} books:")
        for book in self.downloaded_books:
            print(book)
        print(
            f"\nBooks not downloaded are total {len(self.unsuccessful_books)}:")
        for book in self.unsuccessful_books:
            print(book)


if __name__ == "__main__":
    books = [
        "The Art of Laziness Library Mindset",
        "When Breath Becomes Air Paul Kalanithi",
        "Shoe Dog Phil Knight",
        "The Stranger Albert Camus",
    ]

    downloader = PDFDownloader(books)
    downloader.search_and_download()
    downloader.print_summary()
