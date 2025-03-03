# HRVox
HRVox is a voice-interactive chatbot designed to streamline HR workflows. 

### Architecture ###
``` mermaid

graph TD
    subgraph "User Interaction"
        A[Employee] -->|Speaks| B[Web Frontend]
    end

    subgraph "Web Frontend"
        B -->|Captures Audio| C[Microphone Input]
        C -->|Sends Audio| D[FastAPI Backend]
    end

    subgraph "FastAPI Backend"
        D -->|Processes Audio| E[Google Cloud Speech-to-Text]
        E -->|Transcribes to Text| F[Rasa NLU]
        F -->|Identifies Intent & Entities| G[Rasa Core]
        G -->|Triggers Agent| H[Agent System]
    end

    subgraph "Agent System"
        H -->|Policy Agent| I[Query PostgreSQL Database]
        H -->|Leave Application Agent| J[Call Apply Leave API]
        I -->|Retrieves Policy Data| K[Response Generation]
        J -->|Submits Leave Request| K[Response Generation]
    end

    subgraph "Response Generation"
        K -->|Generates Response Text| L[Google Cloud Text-to-Speech]
        L -->|Converts to Audio| M[FastAPI Backend]
    end

    subgraph "Web Frontend"
        M -->|Sends Audio| N[Audio Playback]
        N -->|Plays Response| A[Employee]
    end

    subgraph "Database & External Services"
        O[PostgreSQL Database] -->|Stores HR Policies| I
        P[Apply Leave API] -->|Processes Leave Requests| J
    end

```
