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

def get_vectorstore(loader_list: list):
    try:
        embeddings = OpenAIEmbeddings()
        vectorstore = VectorstoreIndexCreator(vectorstore_cls=FAISS, embedding=embeddings).from_loaders(loader_list)
        return vectorstore
    except Exception as e:
        st.error(f"Error creating vectorstore: {e}")
        return None

def get_loader(pdf_files: list):
    pdf_loader_list = []
    temp_paths = []
    for pdf in pdf_files:
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as f:
                f.write(pdf.getvalue())
                pdf_loader_list.append(PyPDFLoader(f.name))
                temp_paths.append(f.name)
        except Exception as e:
            st.error(f"Error loading PDF {pdf.name}: {e}")
    return pdf_loader_list, temp_paths

def delete_temp_files(temp_paths: list):
    for path in temp_paths:
        try:
            os.remove(path)
        except Exception as e:
            st.warning(f"Failed to delete temp file {path}: {e}")


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
            with st.spinner("Processing..."):
                try:
                    loaders_list, temp_paths = get_loader(pdf_files)
                    if not loaders_list:
                        st.error("No valid PDF files could be processed.")
                        return

                    vectorstore = get_vectorstore(loaders_list)
                    delete_temp_files(temp_paths)

                    if vectorstore is None:
                        st.error("Failed to create a vectorstore.")
                        return

                    llm = ChatOpenAI(model='gpt-4', verbose=True, temperature=0.9)
                    try:
                        response = vectorstore.query(question=prompt, llm=llm)
                    except Exception as query_error:
                        st.error(f"Error querying the vectorstore: {query_error}")
                        response = "There was an error processing your query."

                    message(response)
                    sst.chat_history.append(
                      {
                      "role": "assistant", 
                      "content": response
                      }
                      )

                except Exception as e:
                    st.error(f"An error occurred: {e}")
    else:
        st.error("Attatch a PDF to start chatting")

if __name__ == '__main__':
    main()