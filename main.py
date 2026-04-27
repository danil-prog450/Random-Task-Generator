import tkinter as tk
from tkinter import messagebox
import json
from book import Book

class BookTracker:
    def __init__(self, master):
        self.master = master
        master.title("Book Tracker")
        self.books = []
        self.load_books()

        # Labels
        self.title_label = tk.Label(master, text="Title:")
        self.title_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.author_label = tk.Label(master, text="Author:")
        self.author_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.genre_label = tk.Label(master, text="Genre:")
        self.genre_label.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.pages_label = tk.Label(master, text="Pages:")
        self.pages_label.grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)

        # Entry fields
        self.title_entry = tk.Entry(master, width=30)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)
        self.author_entry = tk.Entry(master, width=30)
        self.author_entry.grid(row=1, column=1, padx=5, pady=5)
        self.genre_entry = tk.Entry(master, width=30)
        self.genre_entry.grid(row=2, column=1, padx=5, pady=5)
        self.pages_entry = tk.Entry(master, width=30)
        self.pages_entry.grid(row=3, column=1, padx=5, pady=5)

        # Buttons
        self.add_button = tk.Button(master, text="Add Book", command=self.add_book)
        self.add_button.grid(row=4, column=0, columnspan=2, pady=10)
        self.filter_button = tk.Button(master, text="Filter", command=self.filter_books)
        self.filter_button.grid(row=5, column=0, columnspan=2, pady=10)

        # Listbox
        self.book_listbox = tk.Listbox(master, width=60)
        self.book_listbox.grid(row=6, column=0, columnspan=2, padx=5, pady=5)
        self.update_listbox()

    def add_book(self):
        title = self.title_entry.get()
        author = self.author_entry.get()
        genre = self.genre_entry.get()
        pages_str = self.pages_entry.get()

        if not all([title, author, genre, pages_str]):
            messagebox.showerror("Error", "All fields are required.")
            return

        try:
            pages = int(pages_str)
            if pages <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Pages must be a positive integer.")
            return

        book = Book(title, author, genre, pages)
        self.books.append(book)
        self.save_books()
        self.update_listbox()
        self.clear_entries()
        messagebox.showinfo("Success", "Book added successfully!")

    def filter_books(self):
        genre_filter = self.genre_entry.get().lower()
        pages_filter_str = self.pages_entry.get()

        try:
            pages_filter = int(pages_filter_str) if pages_filter_str else None
        except ValueError:
            messagebox.showerror("Error", "Pages filter must be a number.")
            return

        filtered_books = []
        for book in self.books:
            match_genre = not genre_filter or genre_filter in book.genre.lower()
            match_pages = pages_filter is None or book.pages > pages_filter

            if match_genre and match_pages:
                filtered_books.append(book)

        self.update_listbox(filtered_books)

    def save_books(self):
        try:
            with open("data.json", "w") as f:
                json.dump([book.to_dict() for book in self.books], f, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save books: {e}")

    def load_books(self):
        try:
            with open("data.json", "r") as f:
                data = json.load(f)
                self.books = [Book.from_dict(book_data) for book_data in data]
        except FileNotFoundError:
            self.books = []
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Invalid JSON format in data.json. Starting with an empty list.")
            self.books = []
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load books: {e}")

    def update_listbox(self, books_to_display=None):
        self.book_listbox.delete(0, tk.END)
        books = books_to_display if books_to_display is not None else self.books
        for book in books:
            self.book_listbox.insert(tk.END, str(book))

    def clear_entries(self):
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.pages_entry.delete(0, tk.END)

root = tk.Tk()
book_tracker = BookTracker(root)
root.mainloop()
