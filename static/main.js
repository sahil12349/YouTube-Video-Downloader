document.getElementById('download-form').addEventListener('submit', async function(e) {
    e.preventDefault();
    const url = document.getElementById('url').value;
    const response = await fetch('/download', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: url }),
    });
    const result = await response.json();
    const resultDiv = document.getElementById('result');
    if (result.success) {
        resultDiv.innerHTML = `
            <p>Title: ${result.title}</p>
            <img src="${result.thumbnail_url}" alt="Thumbnail" class="thumbnail">
            <p class="btn"><a href="${result.download_url}" target="_blank">Download</a></p>
        `;
    } else {
        resultDiv.innerHTML = `<p>${result.message}</p>`;
    }
});