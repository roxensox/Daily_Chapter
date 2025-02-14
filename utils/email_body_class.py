import os
from bs4 import BeautifulSoup
from globals import PATH


class HTMLBody:
    def __init__(self):
        soup = BeautifulSoup(open(os.path.join(PATH, "../resources/html/mailpage.html"), "r"), "html.parser")
        self.content = soup


    def add_chapter_text(self, text):
        '''
        Adds the input string (should be chapter text) to the field marked to receive it
        '''
        lines = text.split("\n")
        paragraphs = []
        p_string = ""
        for line in lines:
            if line.strip() != "":
                p_string += line + " "
            else:
                paragraphs.append(p_string)
                p_string = ""
        paragraphs = [i for i in paragraphs if i != ""]


        for i, paragraph in enumerate(paragraphs):
            new_div = self.content.new_tag("div", id = f"line{i}")
            new_br = self.content.new_tag("br")
            self.content.find(id="text").append(new_div)
            self.content.find(id=f"line{i}").string = f"\t{paragraph}"
            self.content.find(id="text").append(new_br)


    def add_username(self, user_name):
        '''
        Adds the user's name to the field marked to receive it
        '''
        self.content.find(id="user_name").string = f"Your daily chapter is here, {user_name}!"


    def add_title(self, title):
        '''
        Adds the book title to the field marked to receive it
        '''
        self.content.find(id="book_title").string = title


    def export(self) -> str:
        '''
        Returns the HTML version of this object as a string
        '''
        return self.content.decode()


if __name__ == "__main__":
    x = HTMLBody()
    x.add_chapter_text("Bingo wings")
    x.add_title("The Chungus Mungus")
    x.add_username("Neeth Thneed")
    with open("test.html", "w") as out:
        out.write(x.export())
