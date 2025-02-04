import sqlite3, pickle, os
from book_class import Book


class DB_Accessor:
    def __init__(self):
        self.connection = sqlite3.connect("../resources/book_data.db")
        self.refresh_filenames()

    def refresh_filenames(self) -> None:
        fNames = self.connection.execute("SELECT DISTINCT filename FROM books;").fetchall()
        self.filenames = [i[0] for i in fNames]


    def add_book(self, curr_book: Book) -> None:
        self.connection.execute("INSERT INTO books (title, filename) VALUES (?, ?)", [curr_book.title, curr_book.filename])
        self.connection.commit()
        self.refresh_filenames()


    def get_mailing_list(self, fName: str, chapter: int) -> list:
        mailing_list = self.connection.execute("SELECT email FROM choices JOIN books ON title = book WHERE filename = ? AND chapter = ?", [fName, chapter]).fetchall()
        return [i[0] for i in mailing_list]


if __name__ == "__main__":
    x = DB_Accessor()
    pickle_path = "../resources/files/pickles/"
    for file in os.listdir(pickle_path):
        book = pickle.load(open(pickle_path + file, "rb"))
        x.add_book(book)
