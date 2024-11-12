
import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    st.error("Google Gemini API key not found. Please add the key to the environment variables.")
    st.stop()

genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel("gemini-1.5-flash")



def summarize_document_gemini(processed_text, summary_type="concise"):
    try:
        if summary_type == "concise":
            prompt = (
                "Please provide a detailed yet concise summary of the following financial document, "
                "including key insights, important metrics, and significant announcements. Ensure the language is beginner-friendly.\n\n"
                f"{processed_text}"
            )
        elif summary_type == "detailed":
            prompt = (
                "Please provide a comprehensive and detailed summary of the following financial document, "
                "covering all key insights, financial performance metrics, significant announcements, notable financial activities, "
                "risks, strategies, and growth prospects. The summary should be in-depth to provide a complete understanding.\n\n"
                f"{processed_text}"
            )

        response = model.generate_content([prompt])
        return response.text

    except Exception as e:
        return f"Error during summarization with Gemini API: {e}"
