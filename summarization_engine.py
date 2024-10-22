
import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
# Load environment variables
load_dotenv()

# Get Google Gemini API key from environment variables
gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    st.error("Google Gemini API key not found. Please add the key to the environment variables.")
    st.stop()

# Initialize the Gemini generative model
genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# Function to summarize a document using Google Gemini API
# def summarize_document_gemini(processed_text, summary_type="concise"):
#     try:
#         # Construct the summarization prompt
#         prompt = f"Please provide a {'concise' if summary_type == 'concise' else 'detailed'} summary of the following text:\n\n{processed_text}"

#         # Use Google Gemini API for summarization
#         response = model.generate_content([prompt])
#         summary = response.text

#         return summary

#     except Exception as e:
#         return f"Error during summarization with Gemini API: {e}"


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

        # Use Google Gemini API for summarization
        response = model.generate_content([prompt])
        return response.text

    except Exception as e:
        return f"Error during summarization with Gemini API: {e}"
