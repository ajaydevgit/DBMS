import datetime

class LibraryManagement:
    def __init__(self, db):
        self.books_collection = db['books']
        self.transactions_collection = db['transactions']
        self.users_collection = db['users']

    def register_user(self, user_id, name):
        """Registers a new user in the library system."""
        # Check if user already exists
        if self.users_collection.find_one({"user_id": user_id}):
            return False, f"User ID '{user_id}' is already taken."
        
        user_data = {
            "user_id": user_id,
            "name": name,
            "registered_at": datetime.datetime.now()
        }
        self.users_collection.insert_one(user_data)
        return True, f"Successfully registered user '{name}' with ID '{user_id}'."

    def get_all_users(self):
        """Returns a list of all registered users."""
        return list(self.users_collection.find({}))

    def add_book(self, book_id, title, author, isbn, copies=1):
        """Adds a new book using an explicit book_id, or updates copies if it exists."""
        # Check if the book already exists by book_id
        existing_book = self.books_collection.find_one({"book_id": book_id})
        
        if existing_book:
            new_copies = existing_book.get("copies_available", 0) + copies
            self.books_collection.update_one(
                {"_id": existing_book["_id"]},
                {"$set": {"copies_available": new_copies}}
            )
            return True, f"Updated '{title}'. Total copies available: {new_copies}."
        else:
            book_data = {
                "book_id": book_id,
                "title": title,
                "author": author,
                "isbn": isbn,
                "copies_available": copies
            }
            self.books_collection.insert_one(book_data)
            return True, f"Successfully added new book '{title}' (ID: {book_id})."

    def view_all_books(self):
        """Returns a list of all books in the library."""
        return list(self.books_collection.find({}))

    def borrow_book(self, book_id, user_id):
        """Allows a strict registered user to borrow a book by its Book ID."""
        # 1. Strict Validation: Ensure User Exists
        user = self.users_collection.find_one({"user_id": user_id})
        if not user:
            return False, f"User ID '{user_id}' is not registered in the system."

        # 2. Validation: Ensure Book Exists and has copies
        book = self.books_collection.find_one({"book_id": book_id})
        if not book:
            return False, "Book ID not found in library."
            
        if book.get("copies_available", 0) <= 0:
            return False, "Currently no copies of this book are available."
            
        # Update the book copies
        self.books_collection.update_one(
            {"_id": book["_id"]},
            {"$inc": {"copies_available": -1}}
        )
        
        # Record the transaction linking explicitly to user and book IDs
        transaction = {
            "book_id": book_id,
            "book_title": book["title"],
            "user_id": user_id,
            "member_name": user["name"],
            "borrow_date": datetime.datetime.now(),
            "status": "borrowed"
        }
        self.transactions_collection.insert_one(transaction)
        return True, f"'{user['name']}' successfully borrowed '{book['title']}'."

    def return_book(self, book_id, user_id):
        """Allows a user to return a borrowed book using IDs."""
        # Find the active borrow transaction for this explicit user ID and book ID
        transaction = self.transactions_collection.find_one({
            "book_id": book_id,
            "user_id": user_id,
            "status": "borrowed"
        })
        
        if not transaction:
            return False, f"No active borrowing record found for User ID '{user_id}' with Book '{book_id}'."
            
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
        book = self.books_collection.find_one({"book_id": book_id})
        if book:
            self.books_collection.update_one(
                {"_id": book["_id"]},
                {"$inc": {"copies_available": 1}}
            )
            
        return True, f"Book successfully returned by User ID '{user_id}'."

