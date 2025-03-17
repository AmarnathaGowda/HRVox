# HRVox

HRVox is a voice-interactive chatbot designed to streamline HR workflows by enabling employees to interact with HR systems using natural speech. It leverages modern technologies like Google Cloud Speech-to-Text, Rasa, FastAPI, and PostgreSQL to process voice inputs, manage dialogues, execute HR-related tasks, and respond audibly.


---

## Table of Contents

- [Project Overview](#project-overview)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Setup](#setup)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## Project Overview

HRVox simplifies HR processes by providing a conversational interface for employees. It handles tasks like querying HR policies and submitting leave requests through voice commands, making it intuitive and efficient. The project integrates a web frontend for user interaction, a FastAPI backend for processing, and external services like Google Cloud and PostgreSQL for speech recognition and data management.

---

## Key Features

- **Voice Interaction**: Employees can speak to the chatbot, and it responds audibly.
- **Intent Recognition**: Uses Rasa NLU to understand user intents and entities.
- **HR Task Automation**: Supports querying HR policies and applying for leaves via agents.
- **Scalable Architecture**: Built with FastAPI and integrates with cloud services.
- **Natural Dialogue**: Powered by Rasa Core for conversational flow.

---


## Architecture

The HRVox architecture is modular with clear separation of concerns. Below is a Mermaid diagram illustrating the flow:

```mermaid
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

# Summary of the Flow

- **Employee Speaks**: Audio is captured by the Web Frontend.
- **Audio Processing**: Sent to the FastAPI Backend and transcribed to text using Google Cloud Speech-to-Text.
- **Intent Analysis**: Rasa NLU identifies the intent and entities, and Rasa Core manages the dialogue to trigger an agent.
- **Agent Action**: The agent either queries the PostgreSQL database (e.g., for HR policies) or calls an API (e.g., for leave requests).
- **Response Generation**: A text response is generated, converted to audio via Google Cloud Text-to-Speech, and sent back to the frontend.
- **Audio Playback**: The employee hears the response through the Web Frontend.

---
## Prerequisites

Before setting up HRVox, ensure you have the following installed:

- **Python (v3.8+)**: For running the FastAPI backend and Rasa components.
- **Node.js (v14+)**: For the Web Frontend.
- **Google Cloud SDK**: For speech-to-text and text-to-speech services.
- **PostgreSQL (v12+)**: For storing HR policies and data.
- **Git**: For cloning the repository.
- **pip**: Python package manager.
- **npm**: Node.js package manager.

You'll also need:

- A Google Cloud account with Speech-to-Text and Text-to-Speech APIs enabled.
- Credentials for Google Cloud (stored as a JSON key file).
- Access to an Apply Leave API (or a mock API for testing).

---

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/hrvox.git
cd hrvox
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Install Node.js Dependencies
```bash
cd frontend
npm install
```

### 4. Install Google Cloud SDK
Follow the official guide to install and authenticate the SDK.

### 5. Set Up PostgreSQL
Install PostgreSQL locally or use a hosted service.

Create a database named `hrvox_db`:
```sql
CREATE DATABASE hrvox_db;
```

Import the schema (if provided) or create tables for HR policies.

## Setup

### Configure Environment Variables
Create a `.env` file in the root directory with:
```plaintext
GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/google-credentials.json
DATABASE_URL=postgresql://username:password@localhost:5432/hrvox_db
LEAVE_API_URL=https://your-leave-api.com/apply
LEAVE_API_KEY=your-api-key
```

### Set Up Google Cloud Services
Enable Speech-to-Text and Text-to-Speech APIs in the Google Cloud Console.
Download your service account key and point to it in the `.env` file.

### Configure Rasa
Navigate to the rasa directory:
```bash
cd rasa
```

Train the Rasa model:
```bash
rasa train
```

### Build the FastAPI Backend
Ensure all dependencies are installed and the `.env` file is loaded.

Test the backend:
```bash
uvicorn main:app --reload
```

### Run the Web Frontend
From the frontend directory:
```bash
npm start
```

### Deploy Locally
Run the FastAPI backend, Rasa server, and frontend simultaneously (use separate terminals).

## Usage

### Access the Web Frontend
Open your browser to `http://localhost:3000` (or the port specified by the frontend).

### Interact with HRVox
Click the microphone button and speak a command, e.g., "What is the leave policy?" or "Apply for a leave on December 10th."
Listen to the audio response played back through the browser.

### Available Commands
- **Policy Queries**: "Tell me about sick leave," "What’s the vacation policy?"
- **Leave Requests**: "Apply for a leave tomorrow," "Request a day off next week."

### API Endpoints (for developers)
- **POST `/audio`**: Send audio data to the backend for processing.
  - **Response**: Audio file with the chatbot’s reply.

## Project Structure
```
hrvox/
├── frontend/           # Web frontend (React/Node.js)
│   ├── src/           # Source files
│   └── package.json   # Frontend dependencies
├── backend/           # FastAPI backend
│   ├── main.py        # Main application
│   └── requirements.txt # Python dependencies
├── rasa/              # Rasa NLU and Core setup
│   ├── data/         # Training data
│   └── models/       # Trained Rasa models
├── .env              # Environment variables
└── README.md         # This file
```

## Troubleshooting

- **Audio Not Captured**: Ensure microphone permissions are granted in the browser.
- **Google Cloud Errors**: Verify the credentials file path and API enablement.
- **Database Connection Failed**: Check the `DATABASE_URL` in `.env`.
- **Rasa Not Responding**: Ensure the Rasa server is running (`rasa run`).

For additional help, see the [Contact](#contact) section.

## Contributing

Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add your feature"
   ```
4. Push to the branch:
   ```bash
   git push origin feature/your-feature
   ```
5. Open a pull request.

Please follow the coding style and include tests where applicable.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact
For questions or support, reach out via:
- **Email**: amarnath1413@gmail.com
- **GitHub Issues**: Submit an issue

