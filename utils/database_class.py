import sqlite3, pickle, os
from book_class import Book


class DB_Accessor:
    def __init__(self):
        self.connection = sqlite3.connect("../resources/book_data.db")
        self.refresh_filenames()

    def refresh_filenames(self) -> None:
        fNames = self.connection.execute("SELECT DISTINCT title FROM books;").fetchall()
        self.filenames = [i[0] for i in fNames]


    def add_book(self, curr_book: Book) -> None:
        self.connection.execute("INSERT INTO books (title, chapter_count) VALUES (?, ?)", [curr_book.title, curr_book.chapter_count])
        curr_book.book_id = self.connection.execute("SELECT id FROM books WHERE title = ?", [curr_book.title]).fetchall()[0][0]
        print(curr_book.book_id)
        for key in curr_book.chapter_text.keys():
            self.connection.execute("INSERT INTO chapters (book_id, chapter_text, chapter_number) VALUES (?, ?, ?)", [curr_book.book_id, curr_book.chapter_text[key], key])
        self.connection.commit()
        self.refresh_filenames()


    def get_mailing_list(self, fName: str, chapter: int) -> list:
        mailing_list = self.connection.execute("SELECT email FROM choices JOIN books ON title = book WHERE filename = ? AND chapter = ?", [fName, chapter]).fetchall()
        return [i[0] for i in mailing_list]


if __name__ == "__main__":
    x = DB_Accessor()
    y = Book("moby_dick.epub")
    x.add_book(y)
