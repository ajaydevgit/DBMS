from database import get_database
from library import LibraryManagement

def seed():
    print("Connecting to database...")
    db = get_database()
    lib = LibraryManagement(db)
    
    books = [
        ("The Prisma Guide", "Alex Johnson", "9781111111111", 3),
        ("Advanced React Patterns", "Nadia Makarevich", "9782222222222", 5),
        ("Designing Data-Intensive Applications", "Martin Kleppmann", "9781449373320", 2),
        ("The Phoenix Project", "Gene Kim", "9781942788294", 4),
        ("Refactoring UI", "Adam Wathan", "9783333333333", 6),
        ("Clean Architecture", "Robert C. Martin", "9780134494166", 3)
    ]
    
    print(f"Adding {len(books)} books...")
    for title, author, isbn, copies in books:
        success, msg = lib.add_book(title, author, isbn, copies)
        print(f"[{title}] - {msg}")
        
    print("Finished adding books!")

if __name__ == '__main__':
    seed()
