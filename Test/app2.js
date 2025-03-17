import React, { useState, useRef } from 'react';
import { Fab, CircularProgress, Typography } from '@mui/material';
import MicIcon from '@mui/icons-material/Mic';
import StopIcon from '@mui/icons-material/Stop';
import { styled } from '@mui/system';

// Custom styled components for futuristic styling
const FuturisticFab = styled(Fab)({
  background: 'linear-gradient(45deg, #00ffcc, #00b3ff)',
  boxShadow: '0 0 15px #00ffcc, 0 0 25px #00b3ff',
  transition: 'all 0.3s ease-in-out',
  '&:hover': {
    boxShadow: '0 0 20px #00ffcc, 0 0 35px #00b3ff',
    transform: 'scale(1.1)',
  },
  '&.recording': {
    animation: 'pulse 1.5s infinite',
  },
});

const Container = styled('div')({
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  justifyContent: 'center',
  height: '100vh',
  background: 'radial-gradient(circle, #1a1a2e, #0f0f1a)',
  animation: 'fadeIn 1s ease-in',
});

const Title = styled(Typography)({
  color: '#fff',
  fontFamily: "'Orbitron', sans-serif",
  textShadow: '0 0 10px #00ffcc',
  marginBottom: '20px',
});

// CSS Keyframes for animations
const styles = `
  @keyframes pulse {
    0% { boxShadow: 0 0 15px #00ffcc, 0 0 25px #00b3ff; }
    50% { boxShadow: 0 0 25px #00ffcc, 0 0 40px #00b3ff; }
    100% { boxShadow: 0 0 15px #00ffcc, 0 0 25px #00b3ff; }
  }
  @keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
  }
  @keyframes rotateRing {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
`;

function VoiceRecorder() {
  const [recording, setRecording] = useState(false);
  const [processing, setProcessing] = useState(false);
  const [audioUrl, setAudioUrl] = useState(null);
  const mediaRecorderRef = useRef(null);
  let audioChunks = [];

  const handleRecord = async () => {
    if (recording) {
      // Stop recording
      mediaRecorderRef.current.stop();
      setRecording(false);
      setProcessing(true);
    } else {
      // Start recording
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorderRef.current = new MediaRecorder(stream);
      mediaRecorderRef.current.ondataavailable = (event) => {
        audioChunks.push(event.data);
      };
      mediaRecorderRef.current.onstop = async () => {
        const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
        audioChunks = []; // Reset chunks after use
        const formData = new FormData();
        formData.append('audio', audioBlob, 'audio.wav');

        try {
          const response = await fetch('http://localhost:8000/process_audio', {
            method: 'POST',
            body: formData,
          });

          if (!response.ok) {
            console.error('Backend error:', response.statusText);
            setProcessing(false);
            return;
          }

          const audioResponse = await response.blob();
          const url = URL.createObjectURL(audioResponse);
          setAudioUrl(url);
          setProcessing(false);
        } catch (error) {
          console.error('Error:', error);
          setProcessing(false);
        }
      };
      mediaRecorderRef.current.start();
      setRecording(true);
    }
  };

  return (
    <>
      <style>{styles}</style>
      <Container>
        <Title variant="h4">Voice Recorder</Title>
        <Typography variant="h6" style={{ color: '#fff', marginBottom: '10px' }}>
          {recording ? 'Recording... Press to stop' : 'Press to start recording'}
        </Typography>
        <div style={{ position: 'relative' }}>
          {recording && (
            <div
              style={{
                position: 'absolute',
                top: '-10px',
                left: '-10px',
                width: '80px',
                height: '80px',
                border: '2px solid #00ffcc',
                borderRadius: '50%',
                animation: 'rotateRing 2s linear infinite',
                boxShadow: '0 0 20px #00ffcc',
              }}
            />
          )}
          <FuturisticFab
            className={recording ? 'recording' : ''}
            onClick={handleRecord}
          >
            {recording ? <StopIcon /> : <MicIcon />}
          </FuturisticFab>
        </div>
        {processing && (
          <CircularProgress
            sx={{
              color: '#00ffcc',
              marginTop: '20px',
              filter: 'drop-shadow(0 0 10px #00ffcc)',
            }}
          />
        )}
        {processing && (
          <Typography variant="body1" style={{ color: '#00ffcc', marginTop: '20px' }}>
            Processing your request...
          </Typography>
        )}
        <audio
          src={audioUrl}
          controls
          style={{
            marginTop: '20px',
            filter: 'drop-shadow(0 0 10px #00b3ff)',
          }}
        />
      </Container>
    </>
  );
}

export default VoiceRecorder;