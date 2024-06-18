function uploadPhoto() {
    const form = document.getElementById('uploadForm');
    const formData = new FormData(form);
    fetch('/api/upload-photo', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        const contentType = response.headers.get("content-type");
        if (!response.ok) {
            if (contentType && contentType.includes("application/json")) {
                return response.json().then(data => {
                    throw new Error(data.detail || `Failed to upload: Server responded with status ${response.status}`);
                });
            } else {
                return response.text().then(text => {
                    throw new Error(`Unexpected response type: ${contentType || 'unknown'}, response: ${text}`);
                });
            }
        }
        return response.json();
    })
    .then(data => {
        console.log('Success:', data);
        alert('Photo uploaded successfully!');
    })
    .catch(error => {
        console.error('Error:', error);
        alert(`Failed to upload photo: ${error.message}`);
    });
}

document.getElementById('photo-input').addEventListener('change', function() {
    const file = this.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const img = document.createElement('img');
            img.src = e.target.result;
            const preview = document.getElementById('preview');
            preview.innerHTML = '';
            preview.appendChild(img);
        };
         reader.onerror = function (error) {
             console.error('Error reading file:', error);
             alert('Error reading file, please try again.');
         };
        reader.readAsDataURL(file);
    }
});
