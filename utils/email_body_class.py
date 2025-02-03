from bs4 import BeautifulSoup


class HTMLBody:
    def __init__(self):
        soup = BeautifulSoup(open("../resources/mailpage.html", "r"), "html.parser")
        self.content = soup


    def add_chapter_text(self, text):
        self.content.find(id="text").string = text


    def add_username(self, user_name):
        pass


    def export(self):
        return self.content.decode()


if __name__ == "__main__":
    x = HTMLBody()
    x.add_chapter_text("Bingo wings")
    with open("test.html", "w") as out:
        out.write(x.export())
