document.addEventListener('DOMContentLoaded', function() {
    const nationalidField = document.getElementById('id_callphone');
    const errorMessage = document.createElement('div');
    errorMessage.style.color = 'red';
    nationalidField.parentNode.appendChild(errorMessage);

    nationalidField.addEventListener('input', function() {
        const nationalid = nationalidField.value;
        // Clear previous error message
        errorMessage.textContent = '';

        if (nationalid.length >= 10) {
            // First check if the national ID exists in the database
            fetch(`/check-mobile/${nationalid}/`)
                .then(response => response.json())
                .then(data => {
                    if (data.exists) {
                        errorMessage.textContent = `${nationalid} : شماره همراه وارد شده در دیتابیس موجود است`;
                    } else {
                        // If it doesn't exist, check if it's a valid national ID
                        fetch(`/validate-mobile/${nationalid}/`)
                            .then(response => response.json())
                            .then(validationData => {
                                if (!validationData.valid) {
                                    errorMessage.textContent = `${nationalid} : شماره همراه وارد شده نامعتبر است`;
                                }
                            });
                    }
                })
                .catch(error => console.error('Error:', error));
        }
    });
});