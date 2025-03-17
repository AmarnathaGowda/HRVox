from fastapi import FastAPI, UploadFile, File, HTTPException
from google.cloud import speech_v1p1beta1 as speech,texttospeech
import io, requests
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from flask_cors import CORS
from flask import Flask

app = FastAPI(title="HRVox Backend", description="Backend for HRVox Chatbot", version="0.1.0")


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5000", "http://localhost:5000","http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app = Flask(__name__)
# CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})


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
    transcript = ""
    try:
        print("1. Creating client")
        client = speech.SpeechClient()
        print("2. Creating audio")
        audio = speech.RecognitionAudio(content=audio_content)
        print("3. Creating config")
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.MP3,
            sample_rate_hertz=48000,
            language_code="en-US",
        )
        print("4. Sending request to Google Cloud")
        
        try:
            response = client.recognize(config=config, audio=audio)
            print("5. Got response from Google Cloud")
            print(f"Response type: {type(response)}")
            print(f"Response content: {response}")
            
            if not response.results:
                return "No transcription available - empty results"
                
            for result in response.results:
                transcript += result.alternatives[0].transcript
            
            return transcript if transcript else "No transcription available - no text found"
            
        except Exception as api_error:
            print(f"Google Cloud API error: {str(api_error)}")
            raise HTTPException(status_code=500, detail=f"Google Cloud API error: {str(api_error)}")
            
    except Exception as e:
        print(f"General error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")


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

        with open("output1.mp3", "wb") as out:
            out.write(audio_content)
        print("Audio content written to 'output.mp3'")

        # print (audio_content)
        transcript = await transcribe_speech(audio_content)

        print("transcript")
        print(transcript)

        # Step 2: Send transcript to Rasa
        rasa_response = requests.post(
            "http://localhost:5005/webhooks/rest/webhook",
            json={"sender": "user", "message": transcript}
        ).json()

        # Step 3: Extract Rasa's text response
        rasa_message = rasa_response[0]["text"] if rasa_response else "Sorry, I didn’t understand that."

        print(rasa_message)

        # Step 4: Convert Rasa's text response to audio
        audio_response = await text_to_speech(rasa_message)

        with open("output2.mp3", "wb") as out:
            out.write(audio_response)
        print("Audio content written to 'output.mp3'")

        print("audio_response genarated")

        # Step 5: Return the audio as a streaming response
        return StreamingResponse(io.BytesIO(audio_response), media_type="audio/mpeg")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")