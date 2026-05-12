import streamlit as st
import sys
import os
import logging
from dotenv import load_dotenv

# Load env variables and setup logging
load_dotenv()
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)

# Ensure the root directory is in the path to find modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent.graph import run_agent

st.set_page_config(page_title="RailStay AI – Smart Retiring Room Finder", page_icon="🚆", layout="centered")

st.title("🚆 RailStay AI")
st.subheader("Smart IRCTC Retiring Room Finder")
st.write("Let the AI search hundreds of station combinations to find the best room for you!")

# Input fields
col1, col2 = st.columns(2)
with col1:
    city = st.text_input("City", value="Varanasi")
    date = st.date_input("Check-in Date")
with col2:
    duration = st.selectbox("Duration", ["6h", "12h", "24h"], index=1)
    room_type = st.selectbox("Room type", ["AC", "Non AC", "Dormitory"], index=0)

budget = st.text_input("Budget (optional)", placeholder="e.g. Under 500")

if st.button("Search Rooms", type="primary"):
    if not city:
        st.warning("Please enter a city.")
    else:
        with st.spinner("🤖 AI Agent is generating search plan and navigating IRCTC..."):
            try:
                # Running the LangGraph Agent Workflow
                logger.info(f"Initiating search with city={city}, date={date}, duration={duration}, room={room_type}")
                result = run_agent(
                    user="StreamlitUser",
                    city=city,
                    date=str(date),
                    duration=duration,
                    room_type=room_type,
                    budget=budget if budget else None
                )
                
                st.success("Search and AI Ranking Complete!")
                st.markdown("### Best Options Found:")
                st.info(result)
                
            except Exception as e:
                logger.error(f"UI Error occurred during workflow execution: {e}", exc_info=True)
                st.error(f"An error occurred during workflow execution: {e}")
