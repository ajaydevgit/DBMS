from flask import Flask, render_template, request, redirect, url_for, flash
import os
from database import get_database
from library import LibraryManagement

app = Flask(__name__)
# Secret key for flash messages securely loaded from environment
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'default_fallback_secret_dbms_key_123!')

# Initialize Library Logic
db = get_database()
library = LibraryManagement(db)

@app.route('/')
def index():
    # Fetch all books and active borrows for the dashboard
    books = library.view_all_books()
    active_borrows = list(library.transactions_collection.find({"status": "borrowed"}))
    return render_template('index.html', books=books, active_borrows=active_borrows)

@app.route('/add_book', methods=['POST'])
def add_book():
    title = request.form.get('title')
    author = request.form.get('author')
    isbn = request.form.get('isbn')
    copies = int(request.form.get('copies', 1))
    
    success, msg = library.add_book(title, author, isbn, copies)
    if success:
        flash(msg, 'success')
    else:
        flash(msg, 'error')
        
    return redirect(url_for('index'))

@app.route('/borrow', methods=['POST'])
def borrow_book():
    isbn = request.form.get('isbn')
    member_name = request.form.get('member_name')
    
    success, msg = library.borrow_book(isbn, member_name)
    if success:
        flash(msg, 'success')
    else:
        flash(msg, 'error')
        
    return redirect(url_for('index'))

@app.route('/return_book', methods=['POST'])
def return_book():
    isbn = request.form.get('isbn')
    member_name = request.form.get('member_name')
    
    success, msg = library.return_book(isbn, member_name)
    if success:
        flash(msg, 'success')
    else:
        flash(msg, 'error')
        
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Start the robust Flask application on port 5000
    app.run(debug=True, port=5000)
