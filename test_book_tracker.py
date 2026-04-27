import unittest
from unittest.mock import patch
import tkinter as tk
from main import BookTracker
from tkinter import messagebox

class TestBookTracker(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.book_tracker = BookTracker(self.root)

    def tearDown(self):
        self.root.destroy()

    @patch('tkinter.messagebox.showerror')
    def test_add_book_empty_fields(self, mock_showerror):
        self.book_tracker.add_book()
        mock_showerror.assert_called_once_with(
            "Error", "Please fill in all fields."
        )

    @patch('tkinter.messagebox.showerror')
    def test_add_book_invalid_pages(self, mock_showerror):
        self.book_tracker.pages_entry.insert(0, "abc")
        self.book_tracker.add_book()
        mock_showerror.assert_called_once_with(
            "Error", "Pages must be a positive integer."
        )

    def test_add_book_valid_input(self):
        self.book_tracker.title_entry.insert(0, "Test Title")
        self.book_tracker.author_entry.insert(0, "Test Author")
        self.book_tracker.pages_entry.insert(0, "100")
        self.book_tracker.add_book()
        self.assertEqual(len(self.book_tracker.books), 1)
        self.assertEqual(self.book_tracker.books[0]["Title"], "Test Title")
        self.assertEqual(self.book_tracker.books[0]["Author"], "Test Author")
        self.assertEqual(self.book_tracker.books[0]["Pages"], 100)

    def test_clear_entries(self):
        self.book_tracker.title_entry.insert(0, "Test Title")
        self.book_tracker.author_entry.insert(0, "Test Author")
        self.book_tracker.pages_entry.insert(0, "100")
        self.book_tracker.clear_entries()
        self.assertEqual(self.book_tracker.title_entry.get(), "")
        self.assertEqual(self.book_tracker.author_entry.get(), "")
        self.assertEqual(self.book_tracker.pages_entry.get(), "")

    @patch('tkinter.messagebox.showerror')
    def test_save_books_error(self, mock_showerror):
        # Simulate an error during saving (e.g., permission issue)
        with patch('builtins.open', side_effect=IOError("Simulated error")):
            self.book_tracker.save_books()
        mock_showerror.assert_called_once()  # Check if error message was shown

    @patch('tkinter.messagebox.showinfo')
    def test_load_books_no_file(self, mock_showinfo):
        # Simulate no file found
        self.book_tracker.load_books(filename="nonexistent_file.json")
        mock_showinfo.assert_called_once_with("Info", "No saved books found.")

if __name__ == '__main__':
    unittest.main()
