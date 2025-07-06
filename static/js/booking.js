document.addEventListener('DOMContentLoaded', function() {
    // Get all traveler inputs
    const travelerInputs = document.querySelectorAll('input[type="number"][data-destination-id]');
    
    // Add event listeners to each input
    travelerInputs.forEach(function(input) {
        const destinationId = input.getAttribute('data-destination-id');
        const pricePerPerson = parseFloat(input.getAttribute('data-price'));
        
        // Add input event listener for real-time updates
        input.addEventListener('input', function() {
            calculateTotalPrice(destinationId, pricePerPerson);
        });
        
        // Set initial values
        calculateTotalPrice(destinationId, pricePerPerson);
    });

    // Add form submission handlers
    const bookingForms = document.querySelectorAll('form[id^="bookingForm"]');
    bookingForms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            
            fetch(this.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            })
            .then(response => {
                if (response.ok) {
                    // Close the modal
                    const modalId = this.id.replace('bookingForm', 'bookingModal');
                    const modal = document.getElementById(modalId);
                    if (modal) {
                        $(modal).modal('hide');
                    }
                    // Show success message
                    alert('Booking created successfully!');
                    // Redirect to my bookings page
                    window.location.href = "/bookings/my-bookings/";
                } else {
                    // Handle error
                    alert('There was an error processing your booking. Please try again.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('There was an error processing your booking. Please try again.');
            });
        });
    });
});

function calculateTotalPrice(destinationId, pricePerPerson) {
    const travelersInput = document.getElementById('travelers' + destinationId);
    const travelersCount = document.getElementById('travelersCount' + destinationId);
    const totalPrice = document.getElementById('totalPrice' + destinationId);
    const totalAmountInput = document.getElementById('totalAmount' + destinationId);
    
    if (travelersInput && travelersCount && totalPrice && totalAmountInput) {
        const travelers = parseInt(travelersInput.value) || 1;
        const total = travelers * pricePerPerson;
        
        travelersCount.textContent = travelers;
        totalPrice.textContent = '₹' + total.toFixed(2);
        totalAmountInput.value = total.toFixed(2);
    }
} 