import os
import argparse
import multiprocessing as mp
from collections import Counter
import PyPDF2  # For reading PDFs


class WordCounter:
    def __init__(self, path):
        self.path = path

    def _count_words_in_chunk(self, chunk):
        """
        Count words in a given chunk of text.
        """
        words = chunk.decode("utf-8", errors="ignore").split()
        return Counter(words)

    def _read_file_in_chunks(self, file_path, chunk_size=1024 * 1024):
        """
        Generator to read file in chunks.
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
        """
        text = ""
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() or ""
        return text.encode("utf-8")

    def count_words(self):
        """
        Count words in a file using multiprocessing.
        Supports text and PDF files.
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Count words in a file (text or PDF) using multiprocessing.")
    parser.add_argument("path", type=str, help="Path to the file to analyze")
    args = parser.parse_args()

    word_counter = WordCounter(args.path)
    try:
        result = word_counter.count_words()
        for word, count in result.most_common(50):
            print(f"{word}: {count}")
    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"An error occurred: {e}")
