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
    # Fetch data for the dashboard
    books = library.view_all_books()
    users = library.get_all_users()
    active_borrows = list(library.transactions_collection.find({"status": "borrowed"}))
    return render_template('index.html', books=books, active_borrows=active_borrows, users=users)

@app.route('/register_user', methods=['POST'])
def register_user():
    user_id = request.form.get('user_id')
    name = request.form.get('name')
    
    success, msg = library.register_user(user_id, name)
    if success:
        flash(msg, 'success')
    else:
        flash(msg, 'error')
        
    return redirect(url_for('index'))

@app.route('/add_book', methods=['POST'])
def add_book():
    book_id = request.form.get('book_id')
    title = request.form.get('title')
    author = request.form.get('author')
    isbn = request.form.get('isbn')
    copies = int(request.form.get('copies', 1))
    
    success, msg = library.add_book(book_id, title, author, isbn, copies)
    if success:
        flash(msg, 'success')
    else:
        flash(msg, 'error')
        
    return redirect(url_for('index'))

@app.route('/borrow', methods=['POST'])
def borrow_book():
    book_id = request.form.get('book_id')
    user_id = request.form.get('user_id')
    
    success, msg = library.borrow_book(book_id, user_id)
    if success:
        flash(msg, 'success')
    else:
        flash(msg, 'error')
        
    return redirect(url_for('index'))

@app.route('/return_book', methods=['POST'])
def return_book():
    book_id = request.form.get('book_id')
    user_id = request.form.get('user_id')
    
    success, msg = library.return_book(book_id, user_id)
    if success:
        flash(msg, 'success')
    else:
        flash(msg, 'error')
        
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
