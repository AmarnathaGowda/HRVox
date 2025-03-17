import React, { useState, useRef, useEffect } from 'react';
import { Fab, CircularProgress, Typography } from '@mui/material';
import MicIcon from '@mui/icons-material/Mic';
import StopIcon from '@mui/icons-material/Stop';
import { styled } from '@mui/system';
import WaveSurfer from 'wavesurfer.js';

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
    0% { box-shadow: 0 0 15px #00ffcc, 0 0 25px #00b3ff; }
    50% { box-shadow: 0 0 25px #00ffcc, 0 0 40px #00b3ff; }
    100% { box-shadow: 0 0 15px #00ffcc, 0 0 25px #00b3ff; }
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

function App() {
  const [recording, setRecording] = useState(false);
  const [processing, setProcessing] = useState(false);
  const waveformRef = useRef(null);

  useEffect(() => {
    const wavesurfer = WaveSurfer.create({
      container: waveformRef.current,
      waveColor: '#00ffcc',  // Neon green for the waveform
      progressColor: '#00b3ff',  // Neon blue for the progress
      cursorColor: '#fff',
      barWidth: 3,
      barRadius: 3,
      height: 100,
      barGap: 2,
    });
    // Load a sample audio file (replace with your audio source)
    wavesurfer.load('/sample.mp3');  // Ensure this path points to a valid audio file
  }, []);

  const handleRecord = () => {
    if (recording) {
      setRecording(false);
      setProcessing(true);
      // Simulate backend processing
      setTimeout(() => setProcessing(false), 2000);
    } else {
      setRecording(true);
    }
  };

  return (
    <>
      <style>{styles}</style>
      <Container>
        <Title variant="h4">HRVox</Title>
        <div style={{ position: 'relative' }}>
          {/* Rotating ring effect when recording */}
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
        <audio
          id="audioPlayback"
          controls
          style={{
            marginTop: '20px',
            filter: 'drop-shadow(0 0 10px #00b3ff)',
          }}
        />
        {/* Waveform Visualizer */}
        <div
          ref={waveformRef}
          style={{
            width: '80%',
            marginTop: '20px',
            filter: 'drop-shadow(0 0 10px #00ffcc)',
          }}
        />
      </Container>
    </>
  );
}

export default App;