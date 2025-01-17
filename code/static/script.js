function startProgress() {
    let progressBar = document.getElementById('progress-bar');
    let width = 0;
    let interval = setInterval(() => {
        if (width >= 100) {
            clearInterval(interval);
        } else {
            width++;
            progressBar.style.width = width + '%';
        }
    }, 100);
}

function setProgress(target) {
    let progressBar = document.getElementById('progress-bar');
    progressBar.style.width = target + '%';
}
