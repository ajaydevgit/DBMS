from database import get_database
from library import LibraryManagement

def test_library():
    print("Testing database connection...")
    db = get_database()
    lib = LibraryManagement(db)
    
    # 1. Clean collections for the test
    lib.books_collection.delete_many({})
    lib.transactions_collection.delete_many({})
    
    # 2. Add books
    print("Testing Add Book...")
    lib.add_book("Python Crash Course", "Eric Matthes", "9781593279288", 2)
    lib.add_book("Clean Code", "Robert C. Martin", "9780132350884", 1)
    
    # 3. View books
    books = lib.view_all_books()
    assert len(books) == 2, f"Expected 2 books, found {len(books)}"
    print(f"Books added successfully. Total: {len(books)}")
    
    # 4. Borrow book
    print("Testing Borrow Book...")
    success, msg = lib.borrow_book("9781593279288", "Alice")
    assert success, "Borrowing should be successful"
    book = lib.books_collection.find_one({"isbn": "9781593279288"})
    assert book["copies_available"] == 1, "Should have 1 copy left"
    
    # 5. Active borrows
    transactions = list(lib.transactions_collection.find({"status": "borrowed"}))
    assert len(transactions) == 1, "Should be 1 active transaction"
    print("Borrow successful.")
    
    # 6. Return book
    print("Testing Return Book...")
    success, msg = lib.return_book("9781593279288", "Alice")
    assert success, "Return should be successful"
    book = lib.books_collection.find_one({"isbn": "9781593279288"})
    assert book["copies_available"] == 2, "Should be 2 copies again"
    print("Return successful.")
    
    print("All tests passed successfully!")

if __name__ == "__main__":
    test_library()
