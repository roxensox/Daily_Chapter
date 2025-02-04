from bs4 import BeautifulSoup
import ebooklib, pickle, os
from ebooklib import epub


class Book:
    def __init__(self, fileName):
        self.epub_name = fileName
        self.filename = fileName.split(".")[0]
        self.data = self.load_epub(self.epub_name)
        self.title = self.data.title
        self.chapters = self.get_chapters()
        self.chapter_text = dict()
        i = 1
        for chapt in self.chapters:
            self.chapter_text[i] = self.get_chapter_text(chapt)
            i += 1


    def load_epub(self, fName):
        return epub.read_epub(f"../resources/files/books/{fName}")


    def get_chapters(self):
        return [i for i in list(self.data.get_items_of_type(ebooklib.ITEM_DOCUMENT)) if i.is_chapter()]


    def get_chapter_text(self, chapter: epub.EpubHtml):
        soup = BeautifulSoup(chapter.get_body_content(), "html.parser")
        text = [p.get_text() for p in soup.findAll("p")]
        return ' '.join(text)


    def to_pickle(self):
        with open(f"../resources/files/pickles/{self.filename}.pickle", "wb") as out:
            pickle.dump(self, out)


if __name__ == "__main__":
    epubs = os.listdir("../resources/files/books/")
    pickles = os.listdir("../resources/files/pickles/")
    for file in epubs:
        if f"{file.split(".")[0]}.pickle" not in pickles:
            curr_book = Book(file)
            curr_book.to_pickle()
