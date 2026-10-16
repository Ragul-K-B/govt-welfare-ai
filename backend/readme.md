# Welfare AI — Backend Setup & Usage

## 1. Project Overview

Welfare AI is an AI-powered Government Welfare Scheme Discovery and Eligibility Assistant for India, initially focused on Tamil Nadu.

The backend uses:

- **Python** — application logic
- **FastAPI** — REST API
- **MongoDB Atlas** — scheme data storage
- **FAISS** — semantic scheme retrieval
- **Groq API** — LLM-powered profile extraction, intent classification, and conversational assistance
- **Deterministic eligibility engine** — evaluates eligibility using `PASS`, `FAIL`, or `UNKNOWN`
- **Console chatbot** — interactive interface for testing the complete workflow

The LLM does not make the final eligibility decision. Eligibility is evaluated by the Python decision engine.

## 2. Project Structure

```text
backend/
├── api/
│   └── routes.py
├── core/
│   └── config.py
├── db/
│   └── mongodb.py
├── eligibility/
│   └── engine.py
├── llm/
│   └── intent_classifier.py
├── retrieval/
│   ├── data/
│   ├── generate_embeddings.py
│   ├── faiss_index.py
│   └── search.py
├── schemas/
│   └── scheme.py
├── services/
│   ├── conversation.py
│   ├── discovery.py
│   ├── eligibility_service.py
│   └── relevance_service.py
├── main.py
├── console_chat.py
└── README.md
```

This is a representative structure. Some files and directories may differ as the project evolves.

## 3. Prerequisites

Before running the backend, ensure you have:

- Python installed
- The project's virtual environment
- MongoDB Atlas configured and accessible
- Required environment variables configured in the backend's `.env` file
- A valid Groq API key configured according to the existing application settings
- The FAISS index and scheme ID mapping available under `retrieval/data/`
- Required Python dependencies installed

The Groq integration uses the Free plan. Stay within the available usage limits.

**Security:** Never commit `.env` files, API keys, database credentials, or other secrets to GitHub.

## 4. Open the Backend Directory

Open Windows PowerShell and execute:

```powershell
cd R:\welfare_ai\backend
```

## 5. Activate the Virtual Environment

Activate the existing virtual environment:

```powershell
.\venv\Scripts\Activate.ps1
```

The terminal should display `(venv)` before the PowerShell prompt.

If the virtual environment does not exist, create it from the backend directory:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Install the project's dependencies using its existing dependency file, if available:

```powershell
python -m pip install -r requirements.txt
```

If the repository does not contain `requirements.txt`, install the dependencies listed by the project using the existing setup instructions.

## 6. Start the FastAPI Backend

**Terminal 1 — API server**

From `R:\welfare_ai\backend`, with the virtual environment activated, run:

```powershell
python -m uvicorn main:app --reload
```

The server should start at:

```text
http://127.0.0.1:8000
```

The `--reload` option automatically restarts the development server when Python files change.

### Verify the backend

Open these URLs in your browser:

- Backend health endpoint: http://127.0.0.1:8000/
- MongoDB connection test: http://127.0.0.1:8000/db-test
- FastAPI interactive documentation: http://127.0.0.1:8000/docs

The root endpoint should report that the backend is running. The database test should confirm a successful MongoDB connection.

Keep Terminal 1 running while using the console chatbot.

## 7. Run the Console Chatbot

**Terminal 2 — Interactive console**

Open a second PowerShell terminal. Run:

```powershell
cd R:\welfare_ai\backend
.\venv\Scripts\Activate.ps1
python console_chat.py
```

The console chatbot communicates with the running FastAPI server through its API endpoints.

The `requests` package must be installed in the active virtual environment.

If Python reports that `requests` is missing, install it:

```powershell
python -m pip install requests
```

Then start the console again:

```powershell
python console_chat.py
```

## 8. Using the Console Chatbot

Once the chatbot starts, enter a request in natural language.

For example:

```text
I am a 22-year-old diploma student from Tamil Nadu.
My family income is ₹2,00,000 per year.
I am looking for government scholarships and educational assistance.
```

The chatbot can:

1. Extract relevant attributes from the user's message.
2. Discover relevant schemes using semantic retrieval.
3. Evaluate eligibility using the deterministic engine.
4. Display scheme recommendations and available details.
5. Ask follow-up questions when required information is missing.
6. Update the citizen profile as the conversation continues.
7. Reevaluate eligibility after receiving additional information.
8. Answer general questions about government schemes.

Follow the chatbot's prompts to answer any follow-up questions.

You can continue asking questions or exploring schemes during the session. Enter `exit` when you want to leave the console.

## 9. Available API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Check whether the backend is running |
| GET | `/db-test` | Test the MongoDB connection |
| POST | `/api/discover` | Start scheme discovery |
| POST | `/api/continue` | Continue an existing conversation |

Use the FastAPI documentation at http://127.0.0.1:8000/docs to inspect the actual request schemas and test the endpoints.

## 10. Common Problems

### Backend connection refused

**Possible cause:** The FastAPI server is not running.

**Solution:** Start the server in Terminal 1:

```powershell
python -m uvicorn main:app --reload
```

### `ModuleNotFoundError`

**Possible cause:** A required Python dependency is missing or the wrong virtual environment is active.

**Solution:** Activate the backend virtual environment and install the project's dependencies.

### MongoDB connection failure

**Possible causes:**

- Incorrect MongoDB connection settings
- Missing environment variables
- Network access restrictions in MongoDB Atlas
- Invalid database credentials

**Solution:** Check the existing `.env` configuration and MongoDB Atlas network access settings. Never share database credentials in logs or screenshots.

### Groq API errors

**Possible causes:**

- Missing or invalid API key
- Free-plan rate limits
- Temporary provider errors

**Solution:** Verify the existing Groq configuration and check the account's usage limits. Do not upgrade to a paid plan as part of the current MVP setup.

### FAISS index or embedding errors

**Possible cause:** The required index, mapping file, or embedding dependencies are missing or inconsistent.

**Solution:** Verify that the expected files exist under `retrieval/data/` and inspect the error before rebuilding the index. MongoDB remains the source of truth for scheme records.

### Console chatbot does not respond

**Possible causes:**

- The FastAPI server is stopped
- An API request timed out
- A backend exception occurred
- An external service is unavailable

**Solution:** Check the console output and the FastAPI terminal logs before changing the application code.

## 11. Stopping the Application

Stop the console chatbot by entering:

```text
exit
```

Stop the FastAPI development server by pressing:

```text
Ctrl + C
```

Both processes can be stopped independently.

## 12. Important Architecture Notes

- MongoDB Atlas is the source of truth for scheme records.
- FAISS supports semantic retrieval of relevant schemes.
- The deterministic eligibility engine produces the final eligibility decision.
- The LLM supports conversational understanding and explanations but does not determine eligibility.
- The console chatbot uses the existing FastAPI endpoints.
- The frontend will use the same backend API rather than duplicating the Python business logic.

## 13. Quick Start Summary

Open two PowerShell terminals.

**Terminal 1 — Start the API**

```powershell
cd R:\welfare_ai\backend
.\venv\Scripts\Activate.ps1
python -m uvicorn main:app --reload
```

**Terminal 2 — Start the chatbot**

```powershell
cd R:\welfare_ai\backend
.\venv\Scripts\Activate.ps1
python console_chat.py
```

Keep the API server running while interacting with the console chatbot.

---

**Project:** Welfare AI — Government Welfare Scheme Discovery & Eligibility Assistant

**Repository:** https://github.com/Ragul-K-B/govt-welfare-ai

**Current interface:** Console chatbot

**Next phase:** React + Vite frontend integrated with the existing FastAPI backend.