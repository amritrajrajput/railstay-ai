<div align="center">
  <h1>🚆 RailStay AI</h1>
  <p><strong>Intelligent IRCTC Retiring Room Search & Ranking Agent</strong></p>

  <!-- Badges -->
  <a href="https://python.org">
    <img src="https://img.shields.io/badge/Python-3.9+-blue.svg" alt="Python Version">
  </a>
  <a href="https://streamlit.io">
    <img src="https://img.shields.io/badge/UI-Streamlit-FF4B4B.svg" alt="Streamlit">
  </a>
  <a href="https://langchain.com">
    <img src="https://img.shields.io/badge/Framework-LangGraph-1C3C3C.svg" alt="LangGraph">
  </a>
  <a href="https://playwright.dev">
    <img src="https://img.shields.io/badge/Automation-Playwright-2EAD33.svg" alt="Playwright">
  </a>
  <a href="https://ai.google.dev">
    <img src="https://img.shields.io/badge/LLM-Gemini_API-8E75B2.svg" alt="Gemini API">
  </a>
</div>

<br />

RailStay AI is an autonomous, agentic system designed to take the friction out of booking IRCTC retiring rooms. Instead of manually checking hundreds of nearby stations and room combinations, this agent automatically maps out logical stations, executes headless browser searches in parallel, and leverages **Google's Gemini API** to analyze and rank the absolute best options for your stay.

## ✨ Features

- **🧠 Agentic Planning**: Intelligently determines all logical nearby railway stations based on your target city.
- **⚡ Automated Web Scraping**: Headless browsing via Playwright automatically simulates searches across multiple stations and dates.
- **🏆 AI-Powered Ranking**: Utilizes Google's Gemini API to evaluate hundreds of search results and rank them based on your exact budget, duration, and room type preferences.
- **🎨 Interactive UI**: A clean, modern Streamlit interface for effortless interaction.

## 🏗️ Architecture

The system operates on a directed graph workflow powered by **LangGraph**:

1. **User Input (`app.py`)**: The user provides trip details (City, Date, Duration, Room Type, Budget) via the Streamlit frontend.
2. **Planner Node (`agent/planner.py`)**: Queries the station database to build an exhaustive list of combinations to search.
3. **Search Node (`tools/irctc_search.py`)**: Deploys Playwright to autonomously scrape availability across all planned combinations.
4. **Ranking Node (`agent/ranking.py`)**: Passes raw scraped data to the **Gemini API** for contextual analysis and optimal ranking.
5. **Final Output**: The curated top 3 options are streamed back to the user interface.

## 🛠️ Tech Stack

- **Core/Agent**: Python, LangGraph, LangChain
- **LLM Engine**: Google Gemini API (`langchain-google-genai`)
- **Automation**: Playwright
- **Frontend**: Streamlit
- **Data**: PostgreSQL / Local mock database

---

## 🚀 Getting Started

### 1. Prerequisites

Before installing, ensure you have the following:
- **Python 3.9** or higher installed.
- A valid **[Google Gemini API Key](https://aistudio.google.com/app/apikey)**.

### 2. Installation

Clone the repository and set up your virtual environment:

```bash
# Clone the repository
git clone https://github.com/amritrajrajput/railstay-ai.git
cd railstay-ai

# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
# On Windows:
.\.venv\Scripts\activate
# On Mac/Linux:
source .venv/bin/activate

# Install the required dependencies
pip install -r requirements.txt

# Install Playwright browser binaries
playwright install
```

### 3. Configuration

Configure your environment variables by copying the example file:

```bash
# On Windows:
copy .env.example .env
# On Mac/Linux:
cp .env.example .env
```

Open the newly created `.env` file and **add your Gemini API Key**:
```env
GEMINI_API_KEY=your_actual_api_key_here
GEMINI_MODEL_NAME=gemini-1.5-pro
```

### 4. Running the Application

Once your environment is configured, start the Streamlit server:

```bash
streamlit run app.py
```

The web interface will automatically launch in your default browser at `http://localhost:8501`. Enter your travel details and let the AI find your perfect retiring room!

---

<div align="center">
  <i>Built with ❤️ for a smarter travel experience.</i>
</div>
