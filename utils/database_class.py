import sqlite3, pickle, os, datetime
from globals import PATH
from book_class import Book


class DB_Accessor:
    def __init__(self):
        self.connection = sqlite3.connect(os.path.join(PATH, "../resources/book_data.db"))
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
        results = self.connection.execute("SELECT UserID, email, last_mail FROM users;")
        return [i for i in results]


    def get_chapter(self, id: int) -> dict:
        '''
        Gets the chapter text for the user's currently chosen chapter based on their user id
        '''
        max_chapters, book_id, title, chapter_num, chapter_text, name = self.connection.execute("SELECT chapter_count, book_id, title, chapter, chapter_text, first_name FROM books JOIN (SELECT * FROM chapters JOIN (SELECT * FROM users JOIN choices ON UserID = user) AS user_choices ON chapters.book_id = user_choices.book_id) ON book_id = books.id AND chapter_number = chapter WHERE UserID = ?", [id]).fetchall()[0]

        is_final = max_chapters == chapter_num
        if not is_final:
            self.connection.execute("UPDATE choices SET chapter = ? WHERE user = ?;", [chapter_num + 1, id])
            self.connection.execute("INSERT INTO records (user_id, book_id, current_chapter) VALUES (?, ?, ?)", [id, book_id, chapter_num])
            self.connection.execute("UPDATE users SET last_mail = datetime('now', 'localtime') WHERE UserID = ?", [id])
            self.connection.commit()
        return {"chapter_text": chapter_text, "chapter_number": chapter_num, "is_final": is_final, "book_title": title, "name": name}


if __name__ == "__main__":
    conn = DB_Accessor()
    book = Book("hound_of_baskervilles.epub")
    conn.add_book(book)
