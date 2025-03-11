from fastapi import FastAPI

app = FastAPI(title="HRVox Backend", 
              description="Backedn for HRVox Chatbot",
              version="0.1.0")

@app.get("/health", summary="Check Server status")
async def health_check():
    return {"status": "healthy", "message": "HRVox backend is up and running!"}