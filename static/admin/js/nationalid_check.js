document.addEventListener('DOMContentLoaded', function() {
    const nationalidField = document.getElementById('id_NATIONALID');
    const errorMessage = document.createElement('div');
    errorMessage.style.color = 'red';
    nationalidField.parentNode.appendChild(errorMessage);

    nationalidField.addEventListener('input', function() {
        const nationalid = nationalidField.value;
        // Clear previous error message
        errorMessage.textContent = '';

        if (nationalid.length >= 10) {
            // First check if the national ID exists in the database
            fetch(`/check-nationalid/${nationalid}/`)
                .then(response => response.json())
                .then(data => {
                    if (data.exists) {
                        errorMessage.textContent = `${nationalid} : کدملی وارد شده در دیتابیس موجود است`;
                    } else {
                        // If it doesn't exist, check if it's a valid national ID
                        fetch(`/validate-nationalid/${nationalid}/`)
                            .then(response => response.json())
                            .then(validationData => {
                                if (!validationData.valid) {
                                    errorMessage.textContent = `${nationalid} : کدملی وارد شده نامعتبر است`;
                                }
                            });
                    }
                })
                .catch(error => console.error('Error:', error));
        }
    });
});