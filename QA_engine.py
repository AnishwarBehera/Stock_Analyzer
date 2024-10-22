from openai import OpenAI

import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def gpt_for_qa(question, context):
    try:
        response = client.chat.completions.create(model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an expert financial assistant analyzing company documents. Answer questions succinctly and accurately based on the context provided."},
            {"role": "user", "content": f"Context: {context}\nQuestion: {question}"}
        ],
        max_tokens=200,
        temperature=0.7)
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error during GPT-3.5 answer generation: {e}")
        return "Error generating answer."



def answer_question(question, document_type):
    if "vectors" not in st.session_state or st.session_state.vectors is None:
        return "ERROR: Please create vector embeddings first.", None

    retriever = st.session_state.vectors.as_retriever()
    response = retriever.get_relevant_documents(question)
    context = "\n".join([doc.page_content for doc in response])

    if context:
        answer = gpt_for_qa(question, context)
    else:
        answer = "No relevant context was retrieved to answer the question."

    return answer, response


