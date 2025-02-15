import mail_stuff as ms, time, quickstart as qs, datetime
from email_body_class import HTMLBody
from book_class import Book
from database_class import DB_Accessor
from globals import PATH


def main():
    delta = datetime.timedelta(days=1)
    while True:
        contacts = ms.get_contacts() 
        x = datetime.datetime.strptime(contacts[0][2], "%Y-%m-%d %H:%M:%S")
        contacts = [i for i in contacts if datetime.datetime.strptime(i[2], "%Y-%m-%d %H:%M:%S") < datetime.datetime.now() - delta]
        db = DB_Accessor()
        session = qs.get_session()
        for c in contacts:
            data = db.get_chapter(c[0])
            chapter_text = data["chapter_text"]
            body = HTMLBody()
            body.add_chapter_text(chapter_text)
            chapter_num = data["chapter_number"]
            book_title = data["book_title"]
            body.add_title(f"{book_title} - Chapter {chapter_num}")
            #body.add_username(data["name"])
            subject = f"Your chapter is ready, {data["name"]}!"
            body = body.export()
            ms.create_email(body=body, subject=subject, recipients=[c[1]], session=session)
        time.sleep(600)



if __name__ == "__main__":
    main()
