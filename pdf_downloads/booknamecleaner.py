########################################################################################################################
# PDF Book Downloader Script                                                                                           #
#                                                                                                                      #
# This script searches for PDF listed in NEW_BOOKS.                                                                    #
#                                                                                                                      #
# Author: Renel Lherisson                                                                                              #
# Date: 2024-12-17                                                                                                     #
# Purpose: Automate the search, update, and download of PDFs.                                                          #
# Dependencies:                                                                                                        #
#    - bookname.py: A file containing the list of PDFs.                                                                #
########################################################################################################################

from bookname import DOWNLOADED_BOOKS, NOT_DOWNLOADED_BOOKS, NEW_BOOKS
import os
import importlib
import bookname
importlib.reload(bookname)


def clean_and_update_booklists():
    """
    Cleans, deduplicates, and updates the book lists, and rewrites them to `booklist.py`.

    Parameters:
    None

    Returns:
    None

    The function performs the following tasks:
    1. Deduplicates the lists `NOT_DOWNLOADED_BOOKS`, `DOWNLOADED_BOOKS`, and `NEW_BOOKS` using `set` and converts them back to sorted lists.
    2. Excludes books already in `NOT_DOWNLOADED_BOOKS` and `DOWNLOADED_BOOKS` from `NEW_BOOKS`.
    3. Specifies the target file to rewrite as `./booklist.py`.
    4. Creates the directory if it does not exist using `os.makedirs()`.
    5. Opens the target file in write mode and writes the updated content into `booklist.py`.
    6. Prints a success message.
    """
    unique_not_downloaded = sorted(set(NOT_DOWNLOADED_BOOKS))
    unique_downloaded = sorted(set(DOWNLOADED_BOOKS))
    unique_new_books = sorted(set(NEW_BOOKS))

    filtered_new_books = [
        book for book in unique_new_books
        if book not in unique_not_downloaded and book not in unique_downloaded
    ]

    print(f"Unique not downloaded books: {len(unique_new_books)}")
    output_file = "./bookname.py"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as file:
        file.write(f"NOT_DOWNLOADED_BOOKS = {unique_not_downloaded}\n")
        file.write(f"DOWNLOADED_BOOKS = {unique_downloaded}\n")
        file.write(f"NEW_BOOKS = {filtered_new_books}\n")

    print("Booklists have been cleaned, updated, and saved successfully!")


def add_books_to_downloaded_list(books):
    """
    Adds books to the `DOWNLOADED_BOOKS` list in `booklist.py`.

    Parameters:
    books (list): A list of books to add to the `DOWNLOADED_BOOKS` list.

    Returns:
    None

    The function performs the following tasks:
    1. Deduplicates the list of books.
    2. Adds the deduplicated list of books to the `DOWNLOADED_BOOKS` list.
    3. Calls the `clean_and_update_booklists()` function to clean and update the book lists.
    """
    books = sorted(set(books))
    bookname.DOWNLOADED_BOOKS.extend(books)
    clean_and_update_booklists()


def add_books_to_not_downloaded_list(books):
    """
    Adds books to the `NOT_DOWNLOADED_BOOKS` list in `booklist.py`.

    Parameters:
    books (list): A list of books to add to the `NOT_DOWNLOADED_BOOKS` list.

    Returns:
    None

    The function performs the following tasks:
    1. Deduplicates the list of books.
    2. Adds the deduplicated list of books to the `NOT_DOWNLOADED_BOOKS` list.
    3. Calls the `clean_and_update_booklists()` function to clean and update the book lists.
    """
    books = sorted(set(books))
    bookname.NOT_DOWNLOADED_BOOKS.extend(books)
    clean_and_update_booklists()


if __name__ == "__main__":
    clean_and_update_booklists()
