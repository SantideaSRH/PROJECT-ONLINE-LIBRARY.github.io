# Book_library.py contains a dictionary with a 'media' key holding a list of books.
from Book_library import library_data

# Get the list of books from Book_library
book_list = library_data["media"]

def search_books(book_list, value):
    # Accepts partial matches and is case-insensitive, checks all fields
    value = value.lower()
    results = []
    for book in book_list:
        for k, v in book.items():
            if value in str(v).lower():
                results.append(book)
                break
    return results

# Example usage:
if __name__ == "__main__":
    print("Welcome to the Book Library Search!")
    value = input("Enter any value to search for: ").strip()
    results = search_books(book_list, value)
    if results:
        print(f"\nFound {len(results)} book(s):")
        for book in results:
            print("---------------------------")
            for k, v in book.items():
                print(f"{k.title()}: {v}")
    else:
        print("No books found matching your search.")