# Book_list.py contains a dictionary with a 'media' key holding a list of books.
import Book_list

# Get the list of books from Book_list
book_list = Book_list["media"]

def search_books(book_list, key, value):
    # Accepts partial matches and is case-insensitive
    value = value.lower()
    return [book for book in book_list if key in book and value in book[key].lower()]

# Example usage:
if __name__ == "__main__":
    # Search by author
    results = search_books(book_list, "author", "tolkien")
    for book in results:
        print(book)