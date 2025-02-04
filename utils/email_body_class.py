from bs4 import BeautifulSoup


class HTMLBody:
    def __init__(self):
        soup = BeautifulSoup(open("../resources/html/mailpage.html", "r"), "html.parser")
        self.content = soup


    def add_chapter_text(self, text):
        self.content.find(id="text").string = text


    def add_username(self, user_name):
        self.content.find(id="user_name").string = f"Your daily chapter is here, {user_name}!"


    def add_title(self, title):
        self.content.find(id="book_title").string = title


    def export(self):
        return self.content.decode()


if __name__ == "__main__":
    x = HTMLBody()
    x.add_chapter_text("Bingo wings")
    x.add_title("The Chungus Mungus")
    x.add_username("Neeth Thneed")
    with open("test.html", "w") as out:
        out.write(x.export())
