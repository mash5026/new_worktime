document.addEventListener('DOMContentLoaded', function() {
    const cardNumberField = document.getElementById('id_card_number');
    const errorMessage = document.createElement('div');
    errorMessage.style.color = 'red';
    cardNumberField.parentNode.appendChild(errorMessage);

    cardNumberField.addEventListener('input', function() {
        const cardNumber = cardNumberField.value.trim();
        errorMessage.textContent = '';

        if (cardNumber.length === 16) { // Ensure the input length matches a valid Iranian card number
            fetch(`/validate_cardnumber/${cardNumber}/`)
                .then(response => response.json())
                .then(validationData => {
                    if (!validationData.valid) {
                        errorMessage.textContent = `${cardNumber} : شماره کارت وارد شده نامعتبر است`;
                    }
                })
                .catch(error => console.error('Error:', error));
        }
    });
});