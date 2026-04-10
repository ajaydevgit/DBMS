import datetime

class LibraryManagement:
    def __init__(self, db):
        self.books_collection = db['books']
        self.transactions_collection = db['transactions']

    def add_book(self, title, author, isbn, copies=1):
        """Adds a new book to the library or updates copies if it exists."""
        # Check if the book already exists by ISBN
        existing_book = self.books_collection.find_one({"isbn": isbn})
        
        if existing_book:
            new_copies = existing_book.get("copies_available", 0) + copies
            self.books_collection.update_one(
                {"_id": existing_book["_id"]},
                {"$set": {"copies_available": new_copies}}
            )
            return True, f"Updated '{title}'. Total copies available: {new_copies}."
        else:
            book_data = {
                "title": title,
                "author": author,
                "isbn": isbn,
                "copies_available": copies
            }
            self.books_collection.insert_one(book_data)
            return True, f"Successfully added new book '{title}'."

    def view_all_books(self):
        """Returns a list of all books in the library."""
        return list(self.books_collection.find({}))

    def borrow_book(self, isbn, member_name):
        """Allows a member to borrow a book by its ISBN."""
        book = self.books_collection.find_one({"isbn": isbn})
        
        if not book:
            return False, "Book not found."
            
        if book.get("copies_available", 0) <= 0:
            return False, "Currently no copies available."
            
        # Update the book copies
        self.books_collection.update_one(
            {"_id": book["_id"]},
            {"$inc": {"copies_available": -1}}
        )
        
        # Record the transaction
        transaction = {
            "isbn": isbn,
            "book_title": book["title"],
            "member_name": member_name,
            "borrow_date": datetime.datetime.now(),
            "status": "borrowed"
        }
        self.transactions_collection.insert_one(transaction)
        return True, f"Successfully borrowed '{book['title']}'."

    def return_book(self, isbn, member_name):
        """Allows a member to return a borrowed book."""
        # Find the active borrow transaction for this member and book
        transaction = self.transactions_collection.find_one({
            "isbn": isbn,
            "member_name": member_name,
            "status": "borrowed"
        })
        
        if not transaction:
            return False, "No active borrowing record found for this member and book."
            
        # Update the transaction status to returned
        self.transactions_collection.update_one(
            {"_id": transaction["_id"]},
            {
                "$set": {
                    "status": "returned",
                    "return_date": datetime.datetime.now()
                }
            }
        )
        
        # Increment available copies
        book = self.books_collection.find_one({"isbn": isbn})
        if book:
            self.books_collection.update_one(
                {"_id": book["_id"]},
                {"$inc": {"copies_available": 1}}
            )
            
        return True, "Book successfully returned."
