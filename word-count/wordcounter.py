#############################################################################################################
# This class counts the number of words in a text file, PDF file, or Word file using multiprocessing.       #
# author:  Renel Lherisson                                                                                  #
# date: 2024-12-17                                                                                          #
# version: 0.1                                                                                              #
# usage: python wordcounter.py <path_to_file>                                                               #
# dependencies: PyPDF2, python-docx                                                                         #
#                                                                                                           #
# identification:                                                                                           #
# File Name: wordcounter.py                                                                                 #
# Purpose: To efficiently analyze and count words in various file formats (text, PDF, Word) using parallel  #
#          processing for performance optimization on large files.                                          #
#                                                                                                           #
# Notes:                                                                                                    #
# - This script handles file reading errors gracefully and supports only UTF-8 compatible text.             #
# - Outputs results in the console and a file named 'summary.txt' for review.                               #
#############################################################################################################

import os
import argparse
import multiprocessing as mp
from collections import Counter
import PyPDF2
import docx


class WordCounter:
    def __init__(self, path):
        self.path = path

    def _count_words_in_chunk(self, chunk):
        """
        Count words in a given chunk of text.

        Parameters:
        chunk (bytes): A chunk of text data.

        Returns:
        collections.Counter: A Counter object containing word frequencies.

        The function decodes the chunk of text using UTF-8 encoding and ignores any errors.
        It converts the text to lowercase and splits it into words.
        Then, it uses the Counter class from the collections module to count the frequency of each word.
        The resulting Counter object is returned.
        """
        words = chunk.decode("utf-8", errors="ignore").lower().split()
        return Counter(words)

    def _read_file_in_chunks(self, file_path, chunk_size=1024 * 1024):
        """
        Generator function to read a file in chunks.

        Parameters:
        file_path (str): The path to the file to be read.
        chunk_size (int, optional): The size of each chunk in bytes. Defaults to 1MB.

        Yields:
        bytes: A chunk of the file's content.

        This function opens the file in binary mode, reads it in chunks of the specified size,
        and yields each chunk one by one. It continues reading until the entire file has been read.
        """
        with open(file_path, 'rb') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                yield chunk

    def _read_pdf_file(self, file_path):
        """
        Extract text content from a PDF file.

        Parameters:
        file_path (str): The path to the PDF file to be read.

        Returns:
        bytes: The extracted text content from the PDF file, encoded in UTF-8.

        This function opens the specified PDF file in binary mode, reads it using PyPDF2,
        extracts the text content from each page, and concatenates them into a single string.
        The resulting text is then encoded in UTF-8 and returned.
        """
        text = ""
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() or ""
        return text.encode("utf-8")

    def _read_word_file(self, file_path):
        """
        Extract text content from a Word (.docx) file.

        Parameters:
        file_path (str): The path to the Word (.docx) file to be read.

        Returns:
        bytes: The extracted text content from the Word file, encoded in UTF-8.
               If the file does not exist, a FileNotFoundError is raised.
               If an error occurs while reading the file, a RuntimeError is raised.

        This function opens the specified Word (.docx) file, reads its content,
        extracts the text from each paragraph, and concatenates them into a single string.
        The resulting text is then encoded in UTF-8 and returned.
        If the file does not exist, a FileNotFoundError is raised.
        If an error occurs while reading the file, a RuntimeError is raised with a descriptive error message.
        """
        if not os.path.isfile(file_path):
            raise FileNotFoundError(
                f"File not found: {os.path.abspath(file_path)}")

        try:
            text = ""
            doc = docx.Document(file_path)
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text.encode("utf-8")
        except Exception as e:
            raise RuntimeError(
                f"Error reading Word file: {os.path.abspath(file_path)} - {str(e)}")

    def count_words(self):
        """
        Count words in a file using multiprocessing.
        Supports text, PDF, and Word files.

        Parameters:
        self (WordCounter): An instance of the WordCounter class.

        Returns:
        collections.Counter: A Counter object containing word frequencies.

        Raises:
        FileNotFoundError: If the file specified by the path does not exist.

        The function reads the file specified by the path, determines its type (text, PDF, or Word),
        and uses multiprocessing to count the words in the file.
        It supports text, PDF, and Word files.
        If the file does not exist, a FileNotFoundError is raised.
        """
        if not os.path.isfile(self.path):
            raise FileNotFoundError(f"File not found: {self.path}")

        file_extension = os.path.splitext(self.path)[1].lower()
        num_workers = mp.cpu_count()
        pool = mp.Pool(num_workers)

        if file_extension == ".pdf":
            # Read PDF file
            content = self._read_pdf_file(self.path)
            chunks = [content[i:i + 1024 * 1024]
                      for i in range(0, len(content), 1024 * 1024)]
        elif file_extension == ".docx":
            # Read Word file
            content = self._read_word_file(self.path)
            chunks = [content[i:i + 1024 * 1024]
                      for i in range(0, len(content), 1024 * 1024)]
        else:
            # Read text file
            chunks = list(self._read_file_in_chunks(self.path))

        # Distribute work to multiprocessing pool
        partial_results = pool.map(self._count_words_in_chunk, chunks)

        # Close the pool
        pool.close()
        pool.join()

        # Aggregate results from all processes
        total_word_counts = Counter()
        for partial_result in partial_results:
            total_word_counts.update(partial_result)

        return total_word_counts

    def summary(self, most_occurrences=50):
        """
        Generate a summary of word count analysis. The summary includes:
        1. Saving the word frequencies in descending order to a .txt file named 'summary.txt'.
        2. Printing the most frequent words to the console.

        Parameters:
        most_occurrences (int, optional): The number of most frequent words to print. Defaults to 50.

        Returns:
        None

        The function first calls the count_words method to obtain the word frequencies.
        Then, it opens a file named 'summary.txt' in write mode and writes each word and its frequency
        in descending order to the file.
        Finally, it prints the most frequent words to the console, up to the specified number of occurrences.
        """
        result = self.count_words()
        with open("summary.txt", "w") as f:
            for word, count in result.most_common():
                f.write(f"{word} {count}\n")
        for word, count in result.most_common(most_occurrences):
            print(f"{word}: {count}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Count words in a file (text, PDF, or Word) using multiprocessing."
    )
    parser.add_argument("path", type=str, help="Path to the file to analyze")
    args = parser.parse_args()

    word_counter = WordCounter(args.path)
    word_counter.summary(20)
