async function refactorCode() {
    const code = document.getElementById('codeInput').value;
    const refactoredCodeElement = document.getElementById('refactoredCode');
    const errorMessageElement = document.getElementById('errorMessage');

    // Очистка предыдущих сообщений
    refactoredCodeElement.textContent = '';
    errorMessageElement.style.display = 'none';

    try {
        const response = await fetch('/refactor', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ code }),
        });
        const result = await response.json();

        if (result.refactored_code) {
            refactoredCodeElement.textContent = result.refactored_code;
        } else {
            errorMessageElement.textContent = "Error: " + result.error;
            errorMessageElement.style.display = 'block';
        }
    } catch (error) {
        errorMessageElement.textContent = "Error: Failed to connect to the server.";
        errorMessageElement.style.display = 'block';
    }
}