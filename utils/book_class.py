from bs4 import BeautifulSoup
from globals import PATH
import ebooklib, os
from ebooklib import epub


class Book:
    def __init__(self, fileName):
        self.epub_name = fileName
        self.filename = fileName.split(".")[0]
        self.data = self.load_epub(self.epub_name)
        self.title = self.data.title
        self.chapters = self.get_chapters()
        self.chapter_count = len(self.chapters)
        self.chapter_text = dict()
        i = 1
        for chapt in self.chapters:
            self.chapter_text[i] = self.get_chapter_text(chapt)
            i += 1


    def load_epub(self, fName) -> epub.EpubBook:
        '''
        Loads the epub data
        '''
        return epub.read_epub(os.path.join(PATH, f"../resources/files/books/{fName}"))


    def get_chapters(self) -> list:
        '''
        Gets a list of all non-empty chapters from the epub data
        '''
        out = list()
        for item in list(self.data.get_items_of_type(ebooklib.ITEM_DOCUMENT)):
            soup = BeautifulSoup(item.get_body_content(), "html.parser")
            text = ' '.join([p.get_text() for p in soup.findAll("p")])
            if item.is_chapter() and text.strip() != "":
                out.append(item)
        return out


    def get_chapter_text(self, chapter: epub.EpubHtml) -> str:
        '''
        Gets the text of the chapter from each object in self.chapters
        '''
        soup = BeautifulSoup(chapter.get_body_content(), "html.parser")
        text = [p.get_text() for p in soup.findAll("p")]
        return ' '.join(text)


if __name__ == "__main__":
    epubs = os.listdir("../resources/files/books/")
