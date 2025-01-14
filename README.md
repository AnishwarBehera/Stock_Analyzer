# Quantum Finance

Quantum Finance is an interactive Streamlit application designed to analyze financial documents, summarize data, and provide insightful answers to questions about financial reports. With AI-driven automation, Quantum Finance helps users make informed decisions by providing a clear analysis of financial data, company performance, and the latest news.

## Features

### 1. Document Upload
Upload financial reports in PDF format to get started:
- **Annual Reports**: Analyze and summarize the document or ask questions about its content.
- **Other Financial Reports**: Extract and analyze financial tables.

### 2. Automate Analysis
Get an overall opinion of the company by extracting data from the uploaded document and combining it with real-time financial data from the web.

### 3. News Extraction
Stay updated with the latest news about the company. Quantum Finance automatically extracts the company name from your uploaded document and provides recent news articles.

### 4. Summarization/Table Extraction
- **Annual Report Summarization**: Generate a concise or detailed summary.
- **Other Report Table Extraction**: Extract financial tables for focused analysis.

### 5. Ask Questions
Ask specific questions about the uploaded document. Use the "Create Embedding" feature to get accurate responses based on the document content.

### 6. Conversation History
View past interactions with the AI to track and review questions and answers. Clear the history when needed.

### 7. Sample Financial Documents
Download sample financial documents to test the app:
- [Download Annual Report of Aavas Financiers Ltd](https://www.aavas.in/img/pdf/Annual_Report_for_the_Financial_Year_2023-24.pdf)
- [Download Q1 Report of MapMyIndia](https://cdn-public.mappls.com/about-mappls/assets/investor_doc/d-2024-25/BM_Outcome_08_Nov_2024.pdf)
- [Download Annual Report of Reliance](https://rilstaticasset.akamaized.net/sites/default/files/2024-08/RIL-Integrated-Annual-Report-2023-24.pdf)
- [Download Quarterly Report of Reliance](https://rilstaticasset.akamaized.net/sites/default/files/2024-10/14102024-Media-Release-RIL-Q2-FY2024-25-Financial-and-Operational-Performance.pdf)

## Installation
1. Clone the repository:
   git clone https://github.com/your-username/Stock_Analyzer.git

2. Navigate to the project directory:
   cd quantum-finance

3. Create a virtual environment and activate it:
   
   python -m venv venv
   source venv/bin/activate # On Windows use `venv\Scripts\activate`
   
4. Install the required dependencies:
   
   pip install -r requirements.txt

5. Set up environment variables for API keys:
   
   export NEWS_ID="your_bing_search_api_key"

## Running the App
Run the Streamlit app with the following command:
```sh
streamlit run app.py
```
Access the app in your web browser at `http://localhost:8501`.

## Technologies Used
- **Streamlit**: Framework for building the web application.
- **OpenAI API**: For natural language understanding and embedding.
- **Gemini API**: For enhanced summarization and analysis.
- **PyMuPDF (Fitz)**: To extract text from PDF documents.
- **Camelot**: To extract tables from PDF documents.
- **Bing Search API**: To fetch recent news about the company.

## How to Use
1. **Upload a Financial Document**: Use the "Document Upload" section to upload your financial report.
2. **Automate Analysis**: Click on the "Automate Analysis" expander to get an overview of the company.
3. **News Extraction**: Use the "Latest News about the Company" expander to get recent updates.
4. **Summarize or Extract Tables**: Summarize annual reports or extract tables from other reports.
5. **Ask Questions**: Use the "Ask Questions" section to interact with the AI and get specific information about the document.

## Contact
For any inquiries or support, contact [anishwarbehera@gmail.com].

