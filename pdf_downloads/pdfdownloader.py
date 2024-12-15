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
        and attempts to download them. It also handles rate limiting and errors.

        Parameters:
        self (PDFDownloader): The instance of the PDFDownloader class.

        Returns:
        None
        """
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
        "The Alchemist Paulo Coelho",
        "The Great Gatsby F. Scott Fitzgerald",
        "To Kill a Mockingbird Harper Lee",
        "1984 George Orwell",
        "Pride and Prejudice Jane Austen",
        "The Catcher in the Rye J.D. Salinger",
        "The Da Vinci Code Dan Brown",
        "The Hobbit J.R.R. Tolkien",
        "The Hunger Games Suzanne Collins",
        "The Kite Runner Khaled Hos",
        "The Lord of the Rings J.R.R. Tolkien",
        "The Lovely Bones Alice Sebold",
        "The Notebook Nicholas Sparks",
        "The Picture of Dorian Gray Oscar Wilde",
        "The Secret Garden Frances Hodgson Burnett",
        "The Shining Stephen King",
        "The Time Traveler's Wife Audrey Niffenegger",
        "The Wizard of Oz L. Frank Baum ",
        "The Adventures of Sherlock Holmes Arthur Conan Doyle",
        "The Adventures of Tom Sawyer Mark Twain",
        "The Book Thief Markus Zusak ",
        "The Call of the Wild Jack London",
        "The Canterbury Tales Geoffrey Chaucer",
        "The Chronicles of Narnia C.S. Lewis",
        "The Color Purple Alice Walker",
        "The Count of Monte Cristo Alexandre Dumas",
        "The Curious Incident of the Dog in the Night-Time Mark Haddon",
        "The Divine Comedy Dante Alighieri",
        "The Fault in Our Stars John Green",
    ]

    books_list = [
        "Millionaire from the Heart by Anne-Claire Meret",
        "The Greatness Guide by Robin Sharma",
        "No Excuses: The Power of Self-Discipline by Brian Tracy",
        "The 5 Elements of Effective Thinking by Edward B. Burger and Michael Starbird",
        "How to Change by Katy Milkman",
        "The Art of People by Dave Kerpen"
    ]

    downloader = PDFDownloader(books_list)
    downloader.search_and_download()
    downloader.print_summary()
