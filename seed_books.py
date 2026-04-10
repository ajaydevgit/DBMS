from database import get_database
from library import LibraryManagement

def seed():
    print("Connecting to database...")
    db = get_database()
    lib = LibraryManagement(db)
    
    books = [
     
    ]
    
    print(f"Adding {len(books)} books...")
    for title, author, isbn, copies in books:
        success, msg = lib.add_book(title, author, isbn, copies)
        print(f"[{title}] - {msg}")
        
    print("Finished adding books!")

if __name__ == '__main__':
    seed()
