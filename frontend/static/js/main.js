const recordButton = document.getElementById('recordButton');
const audioPlayback = document.getElementById('audioPlayback');
let mediaRecorder;
let audioChunks = [];

recordButton.addEventListener('click', async () => {
    if (mediaRecorder && mediaRecorder.state === 'recording') {
        mediaRecorder.stop();
        recordButton.textContent = 'Start Recording';
    } else {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        mediaRecorder.start();
        recordButton.textContent = 'Stop Recording';
        mediaRecorder.ondataavailable = event => {
            audioChunks.push(event.data);
        };
        mediaRecorder.onstop = async () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
            audioChunks = [];
            const formData = new FormData();
            formData.append('audio', audioBlob, 'audio.wav');
            const response = await fetch('http://localhost:8000/process_audio', {
                method: 'POST',
                body: formData
            });
        
            if (!response.ok) {
                console.error('Backend error:', response.statusText);
                return;
            }
        
            const audioResponse = await response.blob();
            const audioUrl = URL.createObjectURL(audioResponse);
            audioPlayback.src = audioUrl;
            console.log('Audio source set to:', audioPlayback.src); // Verify the URL
        
            audioPlayback.play().then(() => {
                console.log('Audio is playing');
            }).catch(error => {
                console.error('Playback error:', error);
            });
        };
    }
});