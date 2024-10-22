
import pandas as pd
import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain_openai import OpenAI
from dotenv import load_dotenv
from QA_engine import answer_question
from embeding_manager import vector_embedding
from summarization_engine import summarize_document_gemini
from document_loader import process_uploaded_files,classify_document,extract_text_from_pdf
from textblob import TextBlob
from table_extract import extract_table_from_pdf
from fetch_stock_info import fetch_company_info,generate_assessment,extract_company_name_from_pdf
import os
load_dotenv()




st.set_page_config(page_title="Document Analyzer", layout="wide")
st.markdown("""
    <style>
        :root {
            --primary-color: #1e90ff;         /* Dodger Blue */
            --secondary-color: #00bcd4;       /* Cyan */
            # --background-color: #121212;      /* Dark Background */
            --background-color: linear-gradient(135deg, #0d1117, #1a1f2b);
            --card-background: rgba(35, 39, 42, 0.85);  /* Dark Grey Card Background */
            --text-color: #e0e0e0;            /* Light Grey Text */
            --info-background: #2a3b4f;       /* Steel Blue */
        }



        /* Overall page styling */
        .stApp {
            background-color: var(--background-color);
            color: var(--text-color);
            font-family: 'Arial', sans-serif;
        }

        /* Header styling */
        .stHeader {
            text-align: center;
            margin-top: 1.5rem;
            margin-bottom: 2rem;
            background-color: #1a1f2b;  
            padding: 20px 0;
            border-radius: 12px;
            
        }

        .stHeader h1 {
            font-size: 3rem;
            font-weight: 800;
            color: var(--primary-color);
            text-align: center;  /* Ensure header is centered */
        }

        /* Section headers */
        .section-header {
            text-align: center;
            color: var(--text-color);
            font-size: 1.75rem;
            margin-bottom: 1rem;
        }

        /* Section container */
        .section-container {
            background-color: var(--card-background);
            border-radius: 50px;
            padding: 1.5rem;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
        }

     
        .stButton > button {
            width: 200px !important; /* Set a fixed width for consistency */
            height: 50px !important; /* Set a fixed height for all buttons */
            padding: 0.85rem !important; /* Consistent padding */
            background-color: var(--primary-color) !important;
            color: white !important;
            border: none !important;
            border-radius: 12px !important; /* Rounded corners for a polished look */
            font-weight: 500 !important;
            transition: all 0.3s ease !important;
            display: block !important;
            margin: 0 auto 15px auto !important; /* Center the button and add bottom margin */
        }

        /* Button hover animation */
        .stButton > button:hover {
            background-color: var(--secondary-color) !important;
            transform: translateY(-4px) scale(1.03); /* Slight bounce effect */
            box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2); /* Shadow to enhance visual feedback */
        }



        /* Radio button styling */
        .stRadio > div {
            display: flex !important;
            flex-direction: row !important;
            justify-content: center !important;
            gap: 1rem !important;
            margin-bottom: 1rem !important;
        }

        /* Center form labels and other form elements */
        .form-label {
            text-align: center;
            font-size: 1.2rem;
            color: var(--text-color);
            margin-bottom: 0.5rem;
        }
            
        @keyframes fadeInUp {
            0% {
                opacity: 0;
                transform: translateY(20px);
            }
            100% {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .how-to-use-container {
            animation: fadeInUp 1.7s ease-out;
        }
            details[open] > div {
            animation: fadeIn 0.7s ease-in-out;
        }

        @keyframes fadeIn {
            from { opacity: 0.4; }
            to { opacity: 1; }
        }




        [data-testid='stFileUploader'] {
            width: 60%;
            margin: 0 auto;
            padding: 20px;
            border-radius: 12px !important;
            border: 0.5px dashed #ffa600;
            # box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            background-color: rgba(37, 99, 235, 0.05) !important; /* Optional background color */
        }
        [data-testid='stFileUploader'] section + div {
            padding-top: 0;
            margin:5px 50px;
        }
            


            
        [data-testid="stTextInput"] {
        width: 60% !important; /* Set width to 60% */
        margin: 0 auto !important; /* Center the text input */
        padding: 10px !important;
        border-radius: 10px !important; /* Rounded corners for a polished look */
        color: #c9d6d2 !important; /* Text color for readability */
        border: 0.5px dashed #ffa600;
        # box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }

        [data-testid="stTextInput"] input {
            color: #c9d1d9 !important; /* Input text color for better contrast */
            margin: 2px;           
        }
    </style>
    <script>
        // JavaScript to add fade-in animation when the "How to Use" section is expanded
        document.addEventListener('DOMContentLoaded', function() {
            const detailsElement = document.querySelector('.how-to-use-container details');
            if (detailsElement) {
                detailsElement.addEventListener('toggle', function() {
                    if (detailsElement.open) {
                        detailsElement.querySelector('div').classList.add('fade-in');
                    }
                });
            }
        });
    </script> 
""", unsafe_allow_html=True)



# Main app header
st.markdown("""
<div class='stHeader' style="text-align: center;">
    <h1 style="font-size: 3rem; font-weight: 800; color: #00bcd4; margin: 0;">Document Analyzer</h1>
    <p style='font-size: 1.5rem; margin-top: 0.2rem;'>Interactive Q&A and Summarization Tool</p>
</div>
""", unsafe_allow_html=True)




# How to Use the app section
st.markdown("""
<div class='how-to-use-container' style="margin: 1.9rem 0rem; text-align: center; border-radius:15px; background-color: var(--info-background);">
    <details>
        <summary style="font-weight: bold; font-size: 1.2em; margin: 2px 0px;">ℹ️ How to Use Document Analyzer ℹ️</summary>
        <div style="margin: 10px ;padding:5px; text-align: left;">
            <p>Welcome to the Financial Report Analyzer! Here's a step-by-step guide on how to use the features effectively:</p>
            <ol>
                <li><b>Upload Document</b>: Use the 'Document Upload' section to upload a financial report in PDF format. You can choose between two types:
                    <ul>
                        <li><b>Annual Report</b>: If selected, you can upload annual reports and proceed with summarization or ask specific questions regarding the document.</li>
                        <li><b>Other Report</b>: Upload any other financial report. You will only be able to ask questions regarding this document.</li>
                    </ul>
                </li>
                <li><b>Automate Analysis</b>: Use the 'Automate Analysis' expander to get an overall opinion about the company. The AI will read the uploaded document, fetch relevant financial data from the web, and provide insights into the company's potential growth and investment opportunity.</li>
                <li><b>Summarization/Table Extraction</b>: The summarization feature is available for Annual Reports, while the table extraction feature is available for Other Reports. Depending on the document type, you will see options to either summarize the content or extract financial tables for analysis.</li>
                <li><b>Ask Questions</b>: Use the 'Ask Questions' section to ask specific questions about the uploaded document. The AI model will provide answers based on the document's content. Creating embeddings is required before using this feature. Click 'Create Embedding' to proceed.</li>
                <li><b>View Conversation History</b>: You can view previous interactions with the AI in the 'Conversation History' section. You can also clear the history whenever needed.</li>
                <li><b>Download Sample Financial Document</b>: If you are testing the app for the first time and need a financial document to upload, you can download a sample financial report from the following links:
                    <ul>
                        <li><a href="https://cdn-public.mappls.com/about-mappls/assets/investor_doc/Annual-Report-2023-24.pdf" target="_blank">Download Annual Report</a></li>
                        <li><a href="https://www.aavas.in/uploads/pdf/financia-results-july-25-2024-853887582.pdf" target="_blank">Download  Other Report</a></li>
                    </ul>
                </li>
            </ol>
        </div>
    </details>
</div>
""", unsafe_allow_html=True)


if 'llm' not in st.session_state:
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if openai_api_key is None:
        st.error("OpenAI API key is not set. Please add it to your environment variables.")
        st.stop()
    st.session_state.llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)

if 'memory' not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="response"
    )

if "vectors" not in st.session_state:
    st.session_state.vectors = None

if 'clear_history' not in st.session_state:
    st.session_state.clear_history = False





# Document upload section

st.markdown("<div class='section-container'>", unsafe_allow_html=True)
st.markdown("<h3 class='section-header'>📄 Document Upload</h3>", unsafe_allow_html=True)
st.markdown("<div class='form-label'>Select document type:</div>", unsafe_allow_html=True)
document_type = st.radio("", ("Annual Report", "Other Report"), key="doc_type")
st.markdown("<div class='form-label'>Upload PDF files:</div>", unsafe_allow_html=True)
uploaded_files = st.file_uploader("Upload your PDF files here:", type=["pdf"], accept_multiple_files=True)



if uploaded_files and len(uploaded_files) > 1:
            
    st.markdown(
    f"""
    <div style='
        text-align: center; 
        background-color: #ffb74d; 
        padding: 15px; 
        border-radius: 10px; 
        max-width: 800px; 
        margin: 15px auto; 
        color: #333333; 
        font-weight: bold; 
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
    '>
        ⚠️ You have uploaded multiple PDF files. The app is optimized for one document at a time. Uploading multiple or large PDFs may lead to unexpected behavior. Please try to avoid this.
    </div>
    """, unsafe_allow_html=True)

    single_file_uploaded = False
else:
    single_file_uploaded = True
if uploaded_files and single_file_uploaded:
    uploaded_file = uploaded_files[0] 
    detected_document_type = classify_document(uploaded_file)

    if detected_document_type != document_type:
        st.markdown(f"""
            <div style='
                text-align: center; 
                background-color: #ffb74d; 
                padding: 10px; 
                border-radius: 10px; 
                max-width: 800px; 
                margin: 15px auto; 
                color: #333;
                font-weight: bold;
            '>
                Document type detected: <span style='color: #000;'>{detected_document_type}</span><br>
                We will proceed considering the document as <span style='color: #000;'>{detected_document_type}</span> for optimal performance.
            </div>
        """, unsafe_allow_html=True)

        document_type = detected_document_type

    st.markdown(f"""
        <div style='
            text-align: center;
            background-color: #e3f2fd;
            padding: 7px;
            border-radius: 10px;
            max-width: 700px;
            margin: 10px auto;
            color: #000;
        '>
            Processing the document as: <strong>{document_type}</strong>
        </div>
    """, unsafe_allow_html=True)







#Automate analysis section

if uploaded_files and single_file_uploaded:
    uploaded_file = uploaded_files[0]
    
    with st.expander("🚀 Automate Analysis", expanded=False):
        st.markdown("""
        <div style='background-color: var(--info-background); padding: 15px; border-radius: 10px; margin-bottom: 1rem;'>
            <p><strong>What does Automate Analysis do?</strong></p>
            <p>The automate analysis feature will extract company-related information from the uploaded document, retrieve financial data about the company from the web, and generate an overall investment assessment using AI. This feature is designed to provide quick insights into the potential growth and investment opportunity of the company.</p>
            <p style='color: red;'><strong>Warning:</strong> This feature is in its early stages and may not provide a fully polished analysis. Please use this feature cautiously and do not make financial decisions solely based on this assessment.</p>
        </div>
        """, unsafe_allow_html=True)

        with st.spinner("Extracting company name from document..."):
            document_texts = process_uploaded_files(uploaded_files, document_type)
            document_text = " ".join(document_texts)  
            extracted_company_name = extract_company_name_from_pdf(document_text)

            if isinstance(extracted_company_name, str):
                extracted_company_name = extracted_company_name.strip()
            else:
                extracted_company_name = "Unknown"

        if extracted_company_name:
            st.markdown("<h3 class='section-header'>🏢 Company Information</h3>", unsafe_allow_html=True)
            company_name_input = st.text_input("Detected company name:", value=extracted_company_name, key="company_name_input")

            if st.button("Proceed with Analysis"):
                if company_name_input:
                    try:
                        with st.spinner(f"Fetching {company_name_input} information and performance metrics..."):
                            company_info = fetch_company_info(company_name_input)

                            if not isinstance(company_info, dict) or 'error' in company_info:
                                st.error(company_info.get('error', 'Unexpected error occurred while fetching company information.'))
                            else:
                                document_summary = summarize_document_gemini(document_text, summary_type="concise")
                                assessment = generate_assessment(company_name_input, document_summary, company_info)
                                st.markdown("#### 📝 Overall Assessment", unsafe_allow_html=True)
                                st.markdown(f"<div style='background-color: #1f2937; padding: 1rem; border-radius: 8px;'>{assessment}</div>", unsafe_allow_html=True)

                    except Exception as e:
                        st.error(f"Error: {str(e)}")
                else:
                    st.error("Please enter a valid company name")
        else:
            st.warning("Could not automatically detect the company name. Please provide the company information manually.")









# Summarization section

if document_type == "Annual Report":
    st.markdown("<div class='section-container'>", unsafe_allow_html=True)
    st.markdown("<h3 class='section-header'>📋 Summarization</h3>", unsafe_allow_html=True)
    st.markdown("<div class='form-label'>Select summarization type:</div>", unsafe_allow_html=True)
    summary_type = st.radio("", ("Concise Summarization", "Detailed Summarization"), key="summary_type")
    if st.button("Summarize Document"):
        if uploaded_files:
            try:
                with st.spinner("Processing document..."):
                    processed_text = process_uploaded_files(uploaded_files, document_type)
                    if not processed_text:
                        st.error("No content extracted.")
                    else:

                        summary_type_value = "concise" if summary_type == "Concise Summarization" else "detailed"
                        summary = summarize_document_gemini(processed_text, summary_type=summary_type_value)
                        
                        if not summary.strip() or "Error" in summary:
                            st.error("Summarization failed.")
                        else:
                            st.markdown("#### 📝 Summary", unsafe_allow_html=True)
                            st.markdown(f"<div style='background-color: #1f2937; padding: 1rem; border-radius: 8px;'>{summary[:1000]}...</div>", unsafe_allow_html=True)
                            
                            summary_file = summary.encode('utf-8')
                            st.download_button(
                                label="📥 Download Full Summary",
                                data=summary_file,
                                file_name=f"{summary_type_value}_summary.txt",
                                mime="text/plain"
                            )
            except Exception as e:
                st.error(f"Error: {str(e)}")
        else:
            st.error("Please upload a document first.")
    st.markdown("</div>", unsafe_allow_html=True)


 
# Table Extraction Section for "Other Report"
if document_type == "Other Report":
    st.markdown("<div class='section-container'>", unsafe_allow_html=True)
    st.markdown("<h3 class='section-header'>📋 Table Extraction & Summarization</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1rem; color: var(--text-color);'>Extract and summarize tables from the uploaded document below.</p>", unsafe_allow_html=True)

    if 'tables_extracted' not in st.session_state:
        st.session_state.tables_extracted = False

    extract_tables_button = st.button("Extract Tables")

    if extract_tables_button and not st.session_state.tables_extracted:
        try:
            with st.spinner("Extracting tables..."):
                st.session_state.tables = []

                for uploaded_file in uploaded_files:
                    uploaded_content = uploaded_file.read()  
                    tables = extract_table_from_pdf(uploaded_content)

                    if tables:
                        st.session_state.tables.extend(tables)

            if not st.session_state.tables:
                st.warning("No tables found in the document.")
            else:
                st.success("Tables have been successfully extracted.")
                st.session_state.tables_extracted = True

        except Exception as e:
            st.error(f"Error during table extraction: {str(e)}")

    if st.session_state.tables_extracted:
        st.markdown("<div style='display: flex; justify-content: center; align-items: center; flex-direction: column; width: 100%;'>", unsafe_allow_html=True)
        initial_tables = st.session_state.tables

        for idx, table in enumerate(initial_tables):
            with st.expander(f"Table {idx + 1}", expanded=False):
                st.markdown("""
                <div style='width: 100%; max-width: 900px; margin: 0 auto; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);'>
                """, unsafe_allow_html=True)
                
                table.columns = [col.strip() if isinstance(col, str) else col for col in table.columns]
                table.reset_index(drop=True, inplace=True)

                st.dataframe(table.style.format(precision=2))  
                
                csv_data = table.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label=f"📥 Download Table {idx + 1} as CSV",
                    data=csv_data,
                    file_name=f"table_{idx + 1}.csv",
                    mime="text/csv"
                )

                st.markdown("</div>", unsafe_allow_html=True)



        # Summarize Tables Section

        summarize_button = st.button("Summarize Tables")
        if summarize_button:
            try:
                with st.spinner("Summarizing tables..."):
                    combined_table_text = ""
                    for idx, table in enumerate(st.session_state.tables):
                        combined_table_text += f"Table {idx + 1}:\n{table.to_string(index=False)}\n\n"

                    summary = summarize_document_gemini(combined_table_text, summary_type="detailed")

                    if summary.strip():
                        st.markdown("#### 📝 Table Summary", unsafe_allow_html=True)
                        st.markdown(
                            f"<div style='max-height: 400px; overflow: auto; background-color: #1f2937; padding: 1rem; border-radius: 8px; text-align: left;'>{summary}</div>",
                            unsafe_allow_html=True
                        )

                        summary_file = summary.encode('utf-8')
                        st.download_button(
                            label="📥 Download Table Summary as Text",
                            data=summary_file,
                            file_name="table_summary.txt",
                            mime="text/plain"
                        )
                    else:
                        st.warning("Table summarization could not generate meaningful content.")

            except Exception as e:
                st.error(f"Error during table summarization: {e}")

    st.markdown("</div>", unsafe_allow_html=True)




# Q&A section

st.markdown("<div class='section-container'>", unsafe_allow_html=True)
st.markdown("<h3 class='section-header'>💬 Ask Questions</h3>", unsafe_allow_html=True)

if st.button("Create Embedding"):
    if uploaded_files:
        try:
            with st.spinner("Creating embeddings..."):
                st.session_state.vectors = vector_embedding(uploaded_files, document_type)
                st.success("Embeddings created successfully!")
        except Exception as e:
            st.error(f"Error: {str(e)}")
    else:
        st.error("Please upload PDF files first.")
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='form-label'>What would you like to know about the document?</div>", unsafe_allow_html=True)
question = st.text_input("", key="question")

if st.button("Enter"):
    if question:
        if st.session_state.vectors is not None:
            try:
                with st.spinner("Processing your question..."):
                    answer, source_documents = answer_question(question, document_type)

                    if answer.startswith("ERROR:"):
                        st.error(answer[7:])
                    else:
                        st.markdown("#### 🤖 AI Response", unsafe_allow_html=True)
                        st.markdown(f"<div style='background-color: #1f2937; padding: 1rem; border-radius: 8px;'>{answer}</div>", unsafe_allow_html=True)

                        if source_documents:
                            with st.expander("📚 View Source Sections"):
                                for i, doc in enumerate(source_documents, 1):
                                    st.markdown(f"**Source {i}**")
                                    st.markdown(f"<div style='background-color: #1f2937; padding: 0.5rem; border-radius: 4px; margin-bottom: 0.5rem;'>{doc.page_content}</div>", unsafe_allow_html=True)

                        st.session_state.memory.chat_memory.add_user_message(question)
                        st.session_state.memory.chat_memory.add_ai_message(answer)
            except Exception as e:
                st.error(f"Error: {str(e)}")
        else:
            st.error("Please create embeddings first.")
st.markdown("</div>", unsafe_allow_html=True)





st.markdown("<div class='section-container'>", unsafe_allow_html=True)
st.markdown("<h3 class='section-header'>📜 Conversation History</h3>", unsafe_allow_html=True)
if "memory" in st.session_state and st.session_state.memory.chat_memory and len(st.session_state.memory.chat_memory.messages) > 0:

    for message in st.session_state.memory.chat_memory.messages:
        is_user = message.type == "human"
        background_color = "#1f2937" if not is_user else "#fff5f7"
        text_color = "#c9d1d9" if not is_user else "#111827"

        st.markdown(f"""
        <div style='background-color: {background_color}; color: {text_color}; padding: 1rem; margin-bottom: 0.5rem; border-radius: 8px;'>
            <strong>{'User' if is_user else 'AI'}:</strong> {message.content}
        </div>
        """, unsafe_allow_html=True)

    if st.button("🗑️ Clear History"):
        st.session_state.memory.chat_memory.clear()
        st.session_state.clear_history = True
        st.success("Conversation history cleared!")
        st.experimental_rerun()

    st.markdown("</div>", unsafe_allow_html=True)





