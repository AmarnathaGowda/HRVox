from fastapi import FastAPI, UploadFile, File, HTTPException
from google.cloud import speech_v1p1beta1 as speech,texttospeech
import io, requests
from fastapi.responses import StreamingResponse


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
    


async def transcribe_speech(audio_content: bytes) -> str:
    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(content=audio_content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )
    response = client.recognize(config=config, audio=audio)
    for result in response.results:
        return result.alternatives[0].transcript
    return "No transcription available"


async def text_to_speech(text: str) -> bytes:
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Wavenet-D",  # Choose a natural-sounding voice
    )
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    return response.audio_content

@app.post("/process_audio", summary="Transcribe audio, process with Rasa, and return TTS audio")
async def process_audio(audio: UploadFile = File(...)):
    try:
        # Step 1: Transcribe the audio
        audio_content = await audio.read()
        transcript = await transcribe_speech(audio_content)

        # Step 2: Send transcript to Rasa
        rasa_response = requests.post(
            "http://localhost:5005/webhooks/rest/webhook",
            json={"sender": "user", "message": transcript}
        ).json()

        # Step 3: Extract Rasa's text response
        rasa_message = rasa_response[0]["text"] if rasa_response else "Sorry, I didn’t understand that."

        # Step 4: Convert Rasa's text response to audio
        audio_response = await text_to_speech(rasa_message)

        print(audio_response)

        # Step 5: Return the audio as a streaming response
        return StreamingResponse(io.BytesIO(audio_response), media_type="audio/mpeg")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")