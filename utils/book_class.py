from bs4 import BeautifulSoup
import ebooklib
from ebooklib import epub


class Book:
    def __init__(self, fileName):
        self.file = fileName
        self.data = self.load_epub(self.file)
        self.title = self.data.title
        self.chapters = self.get_chapters()
        self.chapter_text = dict()
        i = 1
        for chapt in self.chapters:
            self.chapter_text[i] = self.get_chapter_text(chapt)
            i += 1


    def load_epub(self, fName):
        return epub.read_epub(f"../resources/books/{fName}")


    def get_chapters(self):
        return [i for i in list(self.data.get_items_of_type(ebooklib.ITEM_DOCUMENT)) if i.is_chapter()]


    def get_chapter_text(self, chapter: epub.EpubHtml):
        soup = BeautifulSoup(chapter.get_body_content(), "html.parser")
        text = [p.get_text() for p in soup.findAll("p")]
        return ' '.join(text)


if __name__ == "__main__":
    bk = Book("moby_dick.epub")
    for ch in bk.chapter_text.keys():
        print(bk.chapter_text[ch])
        input()
