import os
import shutil
import ebooklib
from pathlib import Path
from ebooklib import epub
import re

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
    elif book_path.suffix in [".pdf", ".azw3"]:
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
