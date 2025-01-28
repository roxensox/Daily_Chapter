import os, sqlite3, ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
from pprint import pprint
from html.parser import HTMLParser


def extract_metadata() -> None:
    connection = sqlite3.connect("../resources/book_data.db")
    books = connection.execute("SELECT title FROM books;").fetchall()
    titles = [t[0] for t in books]
    for book in os.listdir("../resources/books/"):
        title = get_title(book)
        if title not in titles:
            add_to_db(title, book, connection)
    connection.commit()


def epub_to_dict(filename: str) -> dict:
    '''
    Extracts contents of an epub file to a dictionary
    '''
    book = epub.read_epub(f"../resources/books/{filename}")
    toc = None
    contents = None
    book_dict = {}
    out = open("temp.html", "w")
    for item in book.get_items():
        name, extension = item.get_name().split(".")[:2]
        try:
            if extension in ["htm", "html", "xhtml"]:
                out.write(item.get_content().decode("utf-8"))
        except:
            pass
        if name == "toc":
            toc = item
            break
    if toc != None:
        if extension == "html":
            contents = parse_toc_html(toc.get_content())
        elif extension == "ncx":
            contents = parse_toc_ncx(toc.get_content())
    out.close()

    get_chapter(contents)
    book_dict['contents'] = contents


# TODO: Finish this function, pass the html back to the email for complete basic functionality
def get_chapter(contents):
    soup = BeautifulSoup(open("temp.html", "r"), "html.parser")
    for id in contents.keys():
        # NOTE: THIS WORKS!!
        section = soup.find(id=id).parent
        


def parse_toc_html(toc: object) -> dict:
    '''
    Reads the table of contents from an xhtml file

    Args:
        toc: toc.xhtml content

    Returns:
        dictionary holding table of contents data
    '''
    toc_dict = {}
    soup = BeautifulSoup(toc, 'html.parser')
    cells = soup.find_all(name = "a", href=True)
    for cell in cells:
        toc_dict[cell['href'].split("#")[1]] = cell.text
    return toc_dict


def parse_toc_ncx(toc: object) -> dict:
    '''
    Reads the table of contents from an ncx file

    Args:
        toc: toc.ncx content

    Returns:
        dictionary holding table of contents data
    '''
    toc_dict = {}
    soup = BeautifulSoup(toc, "xml")
    nav_map = soup.find('navMap')
    nav_points = soup.find_all('navPoint')
    for nav_point in nav_points:
        if nav_point == None:
            continue
        id = nav_point.find('content')["src"].split("#")[1]
        title = nav_point.find('text').text
        toc_dict[id] = title
    return toc_dict


def get_title(file_name: str) -> str:
    with open(f"../resources/books/{file_name}", "r") as book_data:
        for line in book_data:
            if "The Project Gutenberg eBook of" in line:
                title = " ".join(line.split(" ")[5:]).strip()
                return title


def add_to_db(title: str, filename: str, connection: object) -> None:
    query = "INSERT INTO books (title, filename) VALUES (?, ?);"
    args = (title, filename)
    connection.execute(query, args)


if __name__ == "__main__":
    epub_to_dict("moby_dick.epub")
