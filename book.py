class Book:
    def __init__(self, title, author, genre, pages):
        self.title = title
        self.author = author
        self.genre = genre
        self.pages = pages

    def __str__(self):
        return f"Title: {self.title}, Author: {self.author}, Genre: {self.genre}, Pages: {self.pages}"

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "genre": self.genre,
            "pages": self.pages
        }

    @staticmethod
    def from_dict(data):
        return Book(data["title"], data["author"], data["genre"], data["pages"])
