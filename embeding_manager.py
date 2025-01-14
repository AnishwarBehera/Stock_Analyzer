import os
import openai
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
import streamlit as st
from document_loader import process_uploaded_files  
load_dotenv()



OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  
def vector_embedding(uploaded_files, document_type):
    try:
        embedding = OpenAIEmbeddings(model="text-embedding-3-small")

        documents = process_uploaded_files(uploaded_files, document_type)

        if not documents:
            st.error("No valid documents were extracted. Please check the uploaded files.")
            return None

        if document_type == "Annual Report":
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=3000, chunk_overlap=400)
        else:
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=300)

        split_docs = []
        problematic_docs = []  

        for i, doc in enumerate(documents):
            chunks = text_splitter.split_text(doc)
            if not chunks:
                problematic_docs.append(i + 1)  
                continue  
            split_docs.extend(chunks)

        if problematic_docs:
            st.warning(f"Documents {', '.join(map(str, problematic_docs))} could not be split properly. Skipping.")

        if not split_docs:
            raise ValueError("No text chunks were created from the documents.")

        st.write(f"Number of document chunks created: {len(split_docs)}")

        vectors = FAISS.from_texts(split_docs, embedding)
        st.session_state.vectors = vectors
        # st.success("Embeddings created successfully!")

        return vectors

    except Exception as e:
        st.error(f"Error during vector embedding: {e}")
        return None
