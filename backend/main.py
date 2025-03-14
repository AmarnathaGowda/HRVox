from fastapi import FastAPI, UploadFile, File, HTTPException
from google.cloud import speech_v1p1beta1 as speech
import io, requests


app = FastAPI(title="HRVox Backend", description="Backend for HRVox Chatbot", version="0.1.0")

@app.get("/health", summary="Check server status")
async def health_check():
    return {"status": "healthy", "message": "HRVox backend is up and running!"}

@app.post("/transcribe")
async def transcribe_audio(audio: UploadFile = File(...)):
    try:
        audio_content = await audio.read()
        client = speech.SpeechClient()
        audio = speech.RecognitionAudio(content=audio_content)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code="en-US",
        )
        response = client.recognize(config=config, audio=audio)
        transcript = ""
        for result in response.results:
            transcript += result.alternatives[0].transcript

        # Send transcript to Rasa
        rasa_response = requests.post(
            "http://localhost:5005/webhooks/rest/webhook",
            json={"sender": "user", "message": transcript},
            timeout=10
        ).json()

        # Get Rasa's response
        rasa_message = rasa_response[0]["text"] if rasa_response else "Sorry, I didn’t understand that."
        return {"transcript": transcript, "response": rasa_message}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")