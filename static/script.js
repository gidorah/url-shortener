document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('shorten-form');
    const resultDiv = document.getElementById('shortened-url');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const originalUrl = document.getElementById('original-url').value;

        try {
            const response = await fetch('/shorten', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ url: originalUrl }),
            });

            if (response.ok) {
                const data = await response.json();
                const shortUrl = `${window.location.origin}/${data.short_code}`;
                resultDiv.innerHTML = `
                    <p>Shortened URL:</p>
                    <a href="${shortUrl}" target="_blank">${shortUrl}</a>
                `;
            } else {
                resultDiv.textContent = 'Error: Unable to shorten URL';
            }
        } catch (error) {
            console.error('Error:', error);
            resultDiv.textContent = 'Error: Unable to shorten URL';
        }
    });
});