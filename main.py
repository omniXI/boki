import os
import shutil
import ebooklib
from pathlib import Path
from ebooklib import epub
import re
from pypdf import PdfReader

path = input("Please specify the path of your book directory: ")
output_path = input("Specify folder to save data in: ")
source_folder = Path(path)
books = []

for book in source_folder.rglob("*"):
    if book.is_file() and book.suffix in [".epub", ".pdf", ".azw3"]:
        books.append(book)

for book_path in books:
    filename = book_path.name
    filename_no_ext = filename.rsplit(".", 1)[0]
    match = re.search(r"\(([^)]+)\)$", filename_no_ext)

    if book_path.suffix == ".epub":
        book = epub.read_epub(str(book_path))
        try:
            title = book.get_metadata('DC', 'title')[0][0]
        except IndexError:
            title = book_path.stem

        try:
            author = book.get_metadata('DC', 'creator')[0][0]
        except IndexError:
            author = "Unknown Author"

        if author == "Unknown Author" and "-" in book_path.stem:
            parts = book_path.stem.split("-")
            potential_author = parts[0].strip()
            if (
                potential_author and
                potential_author[0].isupper() and
                len(potential_author.split()) >= 2 and
                len(potential_author) <= 60
            ):
                author = potential_author
    elif book_path.suffix == ".pdf":
        try:
            reader = PdfReader(str(book_path))
            if reader.is_encrypted:
                print(f"Skipping encrypted file: {book_path}")
                continue

            first_page = reader.pages[0]
            author = "Unknown Author"
            found_author = False
            max_pages_to_check = min(10, len(reader.pages))

            for page_num in range(max_pages_to_check):
                page = reader.pages[page_num]
                text = page.extract_text() or ""
                for line in text.split("\n"):
                    line_lower = line.lower().strip()
                    author_candidate = None
                    if "author:" in line_lower:
                        author_candidate = line.split(":", 1)[1].strip()
                    elif line_lower.startswith("written by "):
                        author_candidate = line[10:].strip()
                    elif re.search(r"\bby\s+([A-Z][a-zA-Z ,.'\-]+)$", line):
                        match = re.search(r"\bby\s+([A-Z][a-zA-Z ,.'\-]+)$", line)
                        author_candidate = match.group(1).strip()
                    if author_candidate:
                        if (
                            len(author_candidate) < 3 or
                            len(author_candidate) > 60 or
                            len(author_candidate.split()) < 2 or
                            author_candidate[-1] in [",", ".", ";"] or
                            not author_candidate[0].isupper()
                        ):
                            continue # Skip suspicious lines
                        author = author_candidate
                        break
                if len(author) < 3:
                    author = "Unknown Author"

                title = filename_no_ext
        except Exception as e:
            print(f"Skipping unreadable or encrypted file: {book_path} ({e})")
    else:
        if match:
            author = match.group(1).strip()
            title = filename_no_ext[:match.start()].strip()
        elif "-" in filename_no_ext:
            parts = filename_no_ext.split("-")
            author = parts[0].strip()
            title = parts[1].strip().rsplit(".", 1)[0]
        else:
            author = "Unknown Author"
            title = filename_no_ext.rsplit(".", 1)[0]

    destination_folder = Path(output_path) / author / title
    destination_folder.mkdir(parents=True, exist_ok=True)
    shutil.copy(book_path, destination_folder / book_path.name)
    print(f"Title: {title}, Author: {author}")
