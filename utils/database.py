import sqlite3, os
from book_class import Book


class DB_Accessor:
    def __init__(self):
        self.connection = sqlite3.connect("../resources/book_data.db")
        self.refresh_filenames()

    def refresh_filenames(self):
        fNames = self.connection.execute("SELECT DISTINCT filename FROM books;").fetchall()
        self.filenames = [i[0] for i in fNames]


    def add_books(self):
        for fName in os.listdir("../resources/books/"):
            if fName not in self.filenames:
                curr_book = Book(fName)
                self.connection.execute("INSERT INTO books (title, filename) VALUES (?, ?)", [curr_book.title, curr_book.file])
        self.connection.commit()
        self.refresh_filenames()


    def get_mailing_list(self, fName: str, chapter: int):
        mailing_list = self.connection.execute("SELECT email FROM choices JOIN books ON title = book WHERE filename = ? AND chapter = ?", [fName, chapter]).fetchall()
        return [i[0] for i in mailing_list]


if __name__ == "__main__":
    x = DB_Accessor()
    x.add_books()
    print(x.get_mailing_list("moby_dick.epub", 1))
