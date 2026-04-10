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

// Helper function to open modal globally
function openModal(modalId, isbn = '', title = '') {
    const modal = document.getElementById(modalId);
    if(isbn) {
        modal.querySelector('input[name="isbn"]').value = isbn;
    }
    if(title) {
        const titleSpan = modal.querySelector('.modal-book-title');
        if(titleSpan) titleSpan.textContent = title;
    }
    modal.classList.add('active');
}
