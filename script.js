async function startDownload(format) {
    const url = document.getElementById('videoUrl').value;
    const quality = document.getElementById('res').value; // Dropdown se value lena
    const status = document.getElementById('loader');

    status.classList.remove('hidden');
    status.innerText = "Downloading... Please wait.";

    const fd = new FormData();
    fd.append('url', url);
    fd.append('format', format);
    fd.append('quality', quality); // Quality data bhejna
    
    try {
        const res = await fetch('/download', { method: 'POST', body: fd });
        if (res.ok) {
            const blob = await res.blob();
            const dUrl = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = dUrl;
            a.download = video_${quality}.${format};
            a.click();
            status.innerText = "Download Finished!";
        } else {
            status.innerText = "Error in downloading.";
        }
    } catch (e) {
        status.innerText = "Server Error.";
    }
}