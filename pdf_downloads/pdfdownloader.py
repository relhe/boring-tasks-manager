########################################################################################################################
# PDF Book Downloader Script                                                                                           #
#                                                                                                                      #
# This script searches for PDF listed in NEW_BOOKS from `bookname.py`.                                                 #
# It downloads the PDFs and stores them in a specified directory, skipping duplicates and handling errors gracefully.  #
#                                                                                                                      #
# Author: Renel Lherisson                                                                                              #
# Date: 2024-12-14                                                                                                     #
# Purpose: Automate the search and download PDFs.                                                    #
# Dependencies:                                                                                                        #
#    - google: `pip install google`                                                                                    #
#    - requests: `pip install requests`                                                                                #
#    - certifi: `pip install certifi`                                                                                  #
#    - googlesearch: `pip install google-search`                                                                       #
#    - bookname.py: A file containing the list of pdf to download.                                                     #
########################################################################################################################

from bookname import NEW_BOOKS
import os
import time
import random
import ssl
import requests
from googlesearch import search
import booknamecleaner
import importlib
import bookname
importlib.reload(bookname)


class PDFDownloader:
    def __init__(self, books, download_dir="books"):
        self.books = books
        self.download_dir = download_dir
        self.downloaded_books = []
        self.unsuccessful_books = []
        os.makedirs(self.download_dir, exist_ok=True)
        ssl._create_default_https_context = ssl._create_unverified_context

    def download_pdf(self, url, title):
        """
        Downloads a PDF file from the given URL and saves it with the specified title.

        Parameters:
        url (str): The URL of the PDF file to download.
        title (str): The title of the PDF file, used to name the downloaded file.

        Returns:
        str: A string indicating the status of the download. It can be one of the following:
            - "Downloaded": The PDF file was successfully downloaded.
            - "Skipped": The PDF file was not downloaded because it already exists in the download directory.
            - "Try_again": The PDF file was not downloaded because it is not a PDF file.
            - "Error": An error occurred while downloading the PDF file.
        """
        file_path = os.path.join(self.download_dir, f"{title}.pdf")
        if os.path.exists(file_path):
            print(f"Skipping (already downloaded): {url}")
            return "Skipped"

        try:
            response = requests.get(url, stream=True, timeout=15)
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
        """
        This function searches for free PDFs of each book in the 'books' list,
        and attempts to download them. If the first URL does not yield a PDF file,
        it tries additional URLs until one works or the list is exhausted.

        Parameters:
        self (PDFDownloader): The instance of the PDFDownloader class.

        Returns:
        None
        """
        for book in self.books:
            query = f"{book} free PDF"
            print(f"Searching for: {query}\n")
            try:
                for result in search(query, num=5, stop=5, pause=random.randint(5, 10)):
                    print(f"Found: {result}")
                    feedback = self.download_pdf(
                        result, book.replace(' ', '_'))

                    if feedback == "Downloaded":
                        self.downloaded_books.append(book)
                        break
                    elif feedback in ["Skipped", "Try_again"]:
                        print(f"Skipping this URL: {result}")
                        continue
                    elif feedback == "Error":
                        print(f"Error encountered with URL: {result}")
                        self.unsuccessful_books.append(book)
                        break

                if book not in self.downloaded_books:
                    self.unsuccessful_books.append(book)

                print("\n---\n")
                time.sleep(random.randint(10, 20))

            except Exception as e:
                print(f"An error occurred while searching for '{book}': {e}\n")
                self.unsuccessful_books.append(book)

    def print_summary(self):
        """
        Prints a summary of the books downloaded and those that were not.

        This function prints two sections: one for the books that were successfully downloaded,
        and another for the books that were not downloaded. It includes the total count of each section.

        Parameters:
        self (PDFDownloader): The instance of the PDFDownloader class.

        Returns:
        None
        """
        booknamecleaner.add_books_to_downloaded_list(self.downloaded_books)
        booknamecleaner.add_books_to_not_downloaded_list(
            self.unsuccessful_books)
        print(f"Downloaded {len(self.downloaded_books)} books:")
        for book in self.downloaded_books:
            print(book)
        print(
            f"\nBooks not downloaded are total {len(self.unsuccessful_books)}:")
        for book in self.unsuccessful_books:
            print(book)


if __name__ == "__main__":
    """
    Main Execution Section

    This section initializes the PDFDownloader class with a list of books to download.
    It then searches for and downloads the books, and finally prints a summary of the results.
    """
    downloader = PDFDownloader(NEW_BOOKS)
    downloader.search_and_download()
    downloader.print_summary()
