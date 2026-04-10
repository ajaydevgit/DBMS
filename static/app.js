document.addEventListener('DOMContentLoaded', () => {
    // Automatically dismiss flashes after 5 seconds
    const flashes = document.querySelectorAll('.flash');
    flashes.forEach(flash => {
        setTimeout(() => {
            flash.style.opacity = '0';
            flash.style.transform = 'translateY(-10px)';
            setTimeout(() => flash.remove(), 300);
        }, 5000);
    });

    // Modal Logic
    const modals = document.querySelectorAll('.modal-overlay');
    const closeBtns = document.querySelectorAll('.close-modal');

    // Close Modals
    closeBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const modalId = btn.getAttribute('data-close');
            document.getElementById(modalId).classList.remove('active');
        });
    });

    // Clicking outside modal to close
    modals.forEach(modal => {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.classList.remove('active');
            }
        });
    });
});

// Helper function to open modal globally and inject book_id dynamically
function openModal(modalId, book_id = '', title = '') {
    const modal = document.getElementById(modalId);
    if(book_id) {
        modal.querySelector('input[name="book_id"]').value = book_id; // changed from isbn to book_id
    }
    if(title) {
        const titleSpan = modal.querySelector('.modal-book-title');
        if(titleSpan) titleSpan.textContent = title;
    }
    modal.classList.add('active');
}
