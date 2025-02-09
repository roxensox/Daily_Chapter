import sqlite3, pickle, os
from book_class import Book


class DB_Accessor:
    def __init__(self):
        self.connection = sqlite3.connect("../resources/book_data.db")
        self.refresh_titles()


    def refresh_titles(self) -> None:
        '''
        Updates the titles property so it can be accessed without running a query
        '''
        titles = self.connection.execute("SELECT DISTINCT title FROM books;").fetchall()
        self.titles = [i[0] for i in titles]


    def add_book(self, curr_book: Book) -> None:
        '''
        Imports a new epub into the database
        '''
        self.connection.execute("INSERT INTO books (title, chapter_count) VALUES (?, ?)", [curr_book.title, curr_book.chapter_count])
        curr_book.book_id = self.connection.execute("SELECT id FROM books WHERE title = ?", [curr_book.title]).fetchall()[0][0]
        print(curr_book.book_id)
        for key in curr_book.chapter_text.keys():
            self.connection.execute("INSERT INTO chapters (book_id, chapter_text, chapter_number) VALUES (?, ?, ?)", [curr_book.book_id, curr_book.chapter_text[key], key])
        self.connection.commit()
        self.refresh_titles()


    def get_users(self) -> list:
        '''
        Gets a list of tuples of all UserIDs and corresponding email addresses from the users table
        '''
        results = self.connection.execute("SELECT UserID, email FROM users;")
        return [i for i in results]


    def get_chapter(self, id: int) -> str:
        '''
        Gets the chapter text for the user's currently chosen chapter based on their user id
        '''
        return self.connection.execute("SELECT chapter_text FROM chapters JOIN (SELECT * FROM users JOIN choices ON UserID = user) AS user_choices ON chapters.book_id = user_choices.book_id WHERE UserID = ?", [id]).fetchall()[0][0]


if __name__ == "__main__":
    x = DB_Accessor()
    y = x.get_users()
    for i in y:
        print(x.get_chapter(i[0]))
