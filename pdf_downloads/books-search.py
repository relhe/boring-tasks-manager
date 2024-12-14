from googlesearch import search
import time
import ssl
import requests
import certifi
import os

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
books = [
    "The Art of Laziness Library Mindset",
    "When Breath Becomes Air Paul Kalanithi",
    "Shoe Dog Phil Knight",
    "The Stranger Albert Camus",
    "How to Win Friends & Influence People Dale Carnegie",
    "The Alchemist Paulo Coelho",
    "Never Split the Difference Chris Voss",
    "The Psychology of Money Morgan Housel",
    "The Iliad Homer",
    "The Odyssey Homer",
    "The 48 Laws of Power Robert Greene",
    "Rich Dad Poor Dad Robert T. Kiyosaki",
    "Steve Jobs Walter Isaacson",
    "The Prince Niccolò Machiavelli",
    "The Laws of Human Nature Robert Greene",
    "Meditations Marcus Aurelius",
    "The Idiot Fyodor Dostoevsky",
    "Good Vibes, Good Life Vex King",
    "Can't Hurt Me David Goggins",
    "Crime and Punishment Fyodor Dostoevsky",
    "Notes from Underground Fyodor Dostoevsky",
    "The Monk Who Sold His Ferrari Robin Sharma",
    "The Subtle Art of Not Giving a F*ck Mark Manson",
    "Ikigai Héctor García and Francesc Miralles",
    "Tuesdays with Morrie Mitch Albom",
    "The Art of War Sun Tzu",
    "Thinking, Fast and Slow Daniel Kahneman",
    "The War of Art Steven Pressfield",
    "Influence: The Psychology of Persuasion Robert B. Cialdini",
    "Man's Search for Meaning Viktor E. Frankl",
    "The Last Lecture Randy Pausch",
    "The Almanack of Naval Ravikant Eric Jorgenson",
    "Tiny Habits BJ Fogg",
    "Meditations on First Philosophy René Descartes",
    "Nicomachean Ethics Aristotle",
    "Siddhartha Hermann Hesse",
    "The Courage to Be Disliked Ichiro Kishimi and Fumitake Koga",
    "The Book of Five Rings Miyamoto Musashi",
    "Atomic Habits James Clear",
    "The Things You Can See Only When You Slow Down Haemin Sunim",
    "Leonardo da Vinci Walter Isaacson",
    "Beyond Good and Evil Friedrich Nietzsche",
    "Thus Spoke Zarathustra Friedrich Nietzsche",
    "White Nights Fyodor Dostoevsky",
    "Don't Believe Everything You Think Joseph Nguyen",
    "100 Harsh Truths of Life Library Mindset",
    "100 Quotes That Will Change Your Life Library Mindset",
    "On the Shortness of Life Seneca",
    "The Power of Now Eckhart Tolle",
    "The Courage to Be Happy Ichiro Kishimi and Fumitake Koga",
    "Meditations (Revisited) Marcus Aurelius",
    "The Tao Te Ching Lao Tzu"
]

# Perform Google searches for free PDF versions
for book in books:
    query = f"{book} free PDF"
    print(f"Searching for: {query}\n")

    try:
        for result in search(query, num=3, stop=3, pause=2):
            print(f"Found: {result}")
            download_pdf(result, book.replace(' ', '_'))

        print("\n---\n")
        time.sleep(2)  # To avoid being flagged by Google
    except Exception as e:
        print(f"An error occurred while searching for '{book}': {e}\n")
