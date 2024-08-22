document.addEventListener('DOMContentLoaded', () => {
    const addToCartButtons = document.querySelectorAll('.add-to-cart');

    // Initialize cart from localStorage or empty cart
    let cart = JSON.parse(localStorage.getItem('cart')) || [];

    addToCartButtons.forEach(button => {
        const sneakerId = button.dataset.sneakerId;

        // Update button state on page load
        updateButtonState(button, sneakerId);

        button.addEventListener('click', () => {
            const isInCart = cart.some(item => item.id === sneakerId);

            if (isInCart) {
                removeFromCart(sneakerId);
            } else {
                addToCart(sneakerId);
            }

            // Update button state after adding/removing
            updateButtonState(button, sneakerId);
        });
    });

    function addToCart(sneakerId) {
        // Add item to cart
        if (!cart.some(item => item.id === sneakerId)) {
            cart.push({ id: sneakerId, quantity: 1 });
            localStorage.setItem('cart', JSON.stringify(cart));
        }
    }

    function removeFromCart(sneakerId) {
        // Remove item from cart
        cart = cart.filter(item => item.id !== sneakerId);
        localStorage.setItem('cart', JSON.stringify(cart));
    }

    function updateButtonState(button, sneakerId) {
        // Check if the item is in the cart
        const isInCart = cart.some(item => item.id === sneakerId);

        if (isInCart) {
            button.style.backgroundColor = '#3CC755'; // Change background color for item in cart
        } else {
            button.style.backgroundColor = '#ffffff'; // Default background color
        }
    }
});


document.addEventListener('DOMContentLoaded', () => {
    const cart = JSON.parse(localStorage.getItem('cart')) || [];
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    if (cart.length > 0) {
        fetch('/view-cart/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({ cart: cart })
        })
        .then(response => response.json())
        .then(data => {
            console.log('Cart data sent to the server:', data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
});
