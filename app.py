import os, tempfile
import streamlit as st
from streamlit import session_state as sst
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from streamlit_chat import message

OPENAI_API_KEY = st.secrets['OPENAI_API_KEY']

def initialize_chat_history():
    sst["chat_history"] = [
        {
            'role':'ai',
            'content': "Hi! I'm AskNotes.ai. Ask me anything about the uploaded PDF!"
        }
    ]

def show_chat(messages:list):
  for i, msg in enumerate(messages):
    message(
        message=msg['content'], 
        is_user=msg['role'] == 'user', 
        key=str(i)
        )

def get_vectorstore(loader_list:list):
    embeddings = OpenAIEmbeddings()
    vectorstore = VectorstoreIndexCreator(vectorstore_cls=FAISS, embedding=embeddings).from_loaders(loader_list)
    return vectorstore

def get_loader(pdf_files:list):
    pdf_loader_list = []
    temp_paths = []
    for pdf in pdf_files:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as f:
            f.write(pdf.getvalue())  # Write PDF content to file
            pdf_loader_list.append(PyPDFLoader(f.name))  # Append loader
            temp_paths.append(f.name)  # Save path for later cleanup
    return pdf_loader_list, temp_paths

def delete_temp_files(temp_paths:list):
    for path in temp_paths:
        os.remove(path)


def main():
    # Front end
    st.set_page_config(
        page_title="Asknotes.ai", 
        layout="wide", page_icon='📝', 
        initial_sidebar_state='expanded'
        )
    st.title("📝AskNotes.ai")

    # ---- Sidebar Content ----
    with st.sidebar:
        # File Uploader
        pdf_files = st.file_uploader(
            label="Upload your PDF", 
            type='pdf',
            accept_multiple_files=True,
            label_visibility='hidden'
            )

        if st.button("Clear Chat History"):
            initialize_chat_history()
    # ----  ----  ----  ----  ----

    if pdf_files:

        if "chat_history" not in sst:
            initialize_chat_history()

        show_chat(sst.chat_history)
        
        # User Prompt
        prompt = st.chat_input("Enter your question:")
        if prompt:
            message(prompt,is_user=True) # Displays user message
            sst.chat_history.append({"role": "user", "content": prompt}) # Adds to chat history
            
            # AI Response
            with st.spinner():
                #Get Vectorstore
                loaders_list, temp_paths = get_loader(pdf_files)
                vectorstore = get_vectorstore(loaders_list)
                delete_temp_files(temp_paths)
                llm = ChatOpenAI(model='gpt-4', verbose=True, temperature=0.9)
                response = vectorstore.query(question=prompt, llm=llm)

            message(response) # Generated response
            sst.chat_history.append(
                {
                "role": "assistant", 
                "content": response
                }
                ) # Adds to chat history
    else:
        st.error("Attatch a PDF to start chatting")

if __name__ == '__main__':
    main()