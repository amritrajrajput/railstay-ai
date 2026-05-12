# RailStay AI – IRCTC Retiring Room Search Agent

This project builds an AI agent that automatically searches IRCTC retiring room availability across multiple nearby stations and room combinations using LangGraph, Playwright, Streamlit, and Google's Gemini API.

## Architecture

1. **User Input** starts at the **Streamlit UI** (`app.py`).
2. Input is passed to the **LangGraph Agent** (`agent/graph.py`).
3. **Planner Node**: Determines all nearby stations for a city (via Postgres/mock DB `database/stations.py`).
4. **Search Node**: Executes headless browser automation (`tools/irctc_search.py`) via Playwright in parallel.
5. **Ranking Node**: Uses Gemini API (`models/gemini_llm.py`) to analyze the results and rank them.
6. **Output**: The best combinations are sent back to the Streamlit UI.

## Getting Started

### 1. Requirements

- Python 3.9+
- A valid Google Gemini API Key

### 2. Installation

```bash
# Set up a virtual environment
python -m venv .venv

# Activate it
# Windows: .\.venv\Scripts\activate
# Mac/Linux: source .venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Install Playwright browsers
playwright install
```

### 3. Configuration

Copy the example environment file and update it with your settings:
```bash
# Windows
copy .env.example .env
# Linux/Mac
cp .env.example .env
```
Edit `.env` to configure your database connection and LLM model.

### 4. Setup Gemini API Key

Make sure you have created your Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey).
Add the API key to your `.env` file as `GEMINI_API_KEY`.

### 5. Run the Application

```bash
streamlit run app.py
```

This will launch the Web UI on `http://localhost:8501`.
