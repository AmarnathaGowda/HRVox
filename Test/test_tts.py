from google.cloud import texttospeech

def synthesize_text(text):
    client = texttospeech.TextToSpeechClient()
    input_text = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Wavenet-D",
    )
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    response = client.synthesize_speech(input=input_text, voice=voice, audio_config=audio_config)
    with open("output.mp3", "wb") as out:
        out.write(response.audio_content)
    print("Audio content written to 'output.mp3'")

if __name__ == "__main__":
    synthesize_text("Hello, this is a test of the text-to-speech API.")