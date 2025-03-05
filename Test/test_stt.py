from google.cloud import speech_v1p1beta1 as speech

def transcribe_audio(audio_file):
    client = speech.SpeechClient()
    with open(audio_file, "rb") as audio:
        content = audio.read()
    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )
    response = client.recognize(config=config, audio=audio)
    for result in response.results:
        print(f"Transcript: {result.alternatives[0].transcript}")

if __name__ == "__main__":
    transcribe_audio("sample_audio.wav")  # Replace with your audio file