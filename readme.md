Welfare AI
Welfare AI is an AI-powered web application that helps people discover
Indian government welfare schemes, understand scheme details, and check
their likely eligibility based on the information they provide.
Main features
- Discover relevant government welfare schemes.
- Show scheme benefits, eligibility conditions, required documents,
  application instructions, and official sources when available.
- Evaluate eligibility using a rule-based engine.
- Ask follow-up questions when information is missing.
- Use semantic search to find relevant schemes.
Technology used
- Frontend: React, Vite
- Backend: Python, FastAPI
- Database: MongoDB Atlas
- Scheme retrieval: Sentence embeddings and FAISS
- LLM: Used for selected language-understanding and response tasks
Requirements
Install these before running the project:
- Python 3.12 or a compatible version used by the project
- Node.js (a version compatible with the Vite project)
- npm
- Access to the project's MongoDB Atlas database
Run locally on Windows
The project folder is:
R:\welfare_ai
1. Start the backend
Open a PowerShell terminal and run:
cd R:\welfare_ai\backend
.\venv\Scripts\Activate.ps1
python -m uvicorn main:app --reload
The backend should be available at:
- API root: http://127.0.0.1:8000/
- API documentation: http://127.0.0.1:8000/docs
- Database test endpoint: http://127.0.0.1:8000/db-test
Keep this terminal open while using the application.

If the virtual environment does not exist, create it and install the
backend dependencies using the project's dependency file, if provided:
python -m venv venv
.\venv\Scripts\Activate.ps1
Then install the dependencies according to the backend's requirements
file.
2. Start the frontend
Open a second PowerShell terminal and run:
cd R:\welfare_ai\frontend
npm install
npm run dev
Open the local URL shown in the terminal, usually:

http://localhost:5173

Keep both terminals running while using the application.
Configuration notes
- The backend needs its environment variables configured in the
  appropriate local .env file. Use the variable names expected by
  the backend configuration; do not commit secrets to GitHub.
- MongoDB Atlas must allow connections from the public IP address of
  the network running the backend. If your public IP changes, you may
  need to update the Atlas Network Access list.
- Keep MongoDB credentials and any LLM API keys out of frontend code
  and source control.
- The FAISS index and its scheme-ID mapping are stored under
  backend/retrieval/data/ in the current project setup. If the
  scheme dataset changes, the retrieval index may need to be
  regenerated according to the project's retrieval scripts.
Troubleshooting
- Backend does not start: Confirm that the virtual environment is
  activated and that the backend dependencies are installed.
- Frontend does not start: Confirm that Node.js and npm are
  installed, then run npm install inside frontend.
- MongoDB connection fails: Check the .env configuration, Atlas
  credentials, database availability, and Atlas Network Access list.
- Frontend cannot reach the backend: Make sure the backend is
  running and check the API base URL used by the frontend.
Important
Eligibility results are guidance based on the scheme data and
information supplied by the user. They are not official government
approval. Users should verify scheme rules and application details
through the relevant official sources.