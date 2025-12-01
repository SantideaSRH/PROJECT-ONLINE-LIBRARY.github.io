import os
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QLabel
from PyQt6.QtCore import Qt

# Import the book data and search function from Book_library
from Book_library import library_data

# The search function from your original code
def search_books(book_list, value):
    # Accepts partial matches and is case-insensitive, checks all fields
    value = value.lower()
    results = []
    for book in book_list:
        for k, v in book.items():
            if value in str(v).lower():
                results.append(book)
                break # Found a match in this book, move to the next book
    return results

# Load the UI file
# Ensure mainwindow.ui is in the same directory or provide a full path
script_dir = os.path.dirname(__file__)
ui_file_path = os.path.join(script_dir, "mainwindow.ui")

try:
    MainWindowUI, _ = uic.loadUiType(ui_file_path)
except Exception as e:
    print(f"Error loading UI file: {e}")
    print(f"Please ensure '{ui_file_path}' exists in the same directory as this script.")
    exit()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = MainWindowUI()
        self.ui.setupUi(self)
        self.setWindowTitle("Book Library Search")

        # Get the list of all books from the imported library_data
        self.all_books = library_data["media"]

        # Defensive checks for required widgets
        required_widgets = ["search_button", "search_input", "results_table", "status_label"]
        for widget_name in required_widgets:
            if not hasattr(self.ui, widget_name):
                print(f"Error: UI file is missing widget '{widget_name}'. Please check your mainwindow.ui file.")
                self.close()
                return

        # Connect the search button to the search function
        self.ui.search_button.clicked.connect(self.perform_search)
        # Allow pressing Enter in the search input to trigger search
        self.ui.search_input.returnPressed.connect(self.perform_search)

        # Ensure the table widget has 4 columns and set headers
        self.ui.results_table.setColumnCount(4)
        self.ui.results_table.setHorizontalHeaderLabels(["Name", "Author", "Date Published", "Category"])
        self.ui.results_table.setColumnWidth(0, 200) # Name
        self.ui.results_table.setColumnWidth(1, 150) # Author
        self.ui.results_table.setColumnWidth(2, 150) # Date Published
        # The last column will stretch due to horizontalHeaderStretchLastSection=true

        self.ui.status_label.setText("Enter a search term and click 'Search'")

        self.display_results(self.all_books)  # Show all books at startup

    def perform_search(self):
        search_term = self.ui.search_input.text().strip()
        self.ui.results_table.setRowCount(0) # Clear previous results

        if not search_term:
            self.ui.status_label.setText("Showing all books.")
            self.display_results(self.all_books)
            return

        results = search_books(self.all_books, search_term)

        if results:
            self.ui.status_label.setText(f"Found {len(results)} book(s) matching '{search_term}'.")
            self.display_results(results)
        else:
            self.ui.status_label.setText(f"No books found matching '{search_term}'.")
            self.ui.results_table.setRowCount(0)

    def display_results(self, results):
        self.ui.results_table.setRowCount(len(results))
        for row_idx, book in enumerate(results):
            self.ui.results_table.setItem(row_idx, 0, QTableWidgetItem(book.get("name", "")))
            self.ui.results_table.setItem(row_idx, 1, QTableWidgetItem(book.get("author", "")))
            self.ui.results_table.setItem(row_idx, 2, QTableWidgetItem(book.get("date_published", "")))
            self.ui.results_table.setItem(row_idx, 3, QTableWidgetItem(book.get("category", "")))

app = QApplication([])
window = MainWindow()
window.show()
app.exec()
