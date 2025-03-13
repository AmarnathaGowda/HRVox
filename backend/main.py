from fastapi import FastAPI, UploadFile, File,HTTPException
from google.cloud import speech_v1p1beta1 as speech
import io
import requests

app = FastAPI(title="HRVox Backend", 
              description="Backedn for HRVox Chatbot",
              version="0.1.0")

@app.get("/health", summary="Check Server status")
async def health_check():
    return {"status": "healthy", "message": "HRVox backend is up and running!"}

@app.post("/transcribe", summary="Transcribe audio to text")
async def transcribe_audio(audio: UploadFile = File(...)):
    try:
        # Read audio file content
        audio_content = await audio.read()
        # Initialize Google Speech-to-Text client
        client = speech.SpeechClient()
        # Configure audio settings
        audio = speech.RecognitionAudio(content=audio_content)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=24000,
            language_code="en-US",
        )
        # Perform transcription
        response = client.recognize(config=config, audio=audio)
        # Extract transcript
        transcript = ""
        for result in response.results:
            transcript += result.alternatives[0].transcript

        # Send transcript to Rasa
        rasa_response = requests.post(
            "http://localhost:5005/webhooks/rest/webhook",
            json={"sender": "user", "message": transcript}
        ).json()

         # Get Rasa's response
        rasa_message = rasa_response[0]["text"] if rasa_response else "Sorry, I didn't understand that."
        return {"transcript": transcript, "response": rasa_message}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")