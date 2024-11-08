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
  """
  Initialize chat history with a welcome message from AskNotes.ai.
  """
  sst["chat_history"] = [
    {
      'role': 'ai',
      'content': "Hi! I'm AskNotes.ai. Ask me anything about the uploaded PDF!"
    }
  ]

def show_chat(messages: list):
  """
  Display chat messages stored in session state.

  Args:
      messages (list): List of messages in the chat history.
  """
  for i, msg in enumerate(messages):
    message(
      message=msg['content'], 
      is_user=msg['role'] == 'user', 
      key=str(i)
    )

def add_to_chat(role, content):
  """
  Add a message to the chat history and display it.

  Args:
      role (str): 'user' or 'ai' to indicate message origin.
      content (str): Text content of the message.
  """
  sst.chat_history.append(
    {
      "role": role, 
      "content": content
    }
  )
  
  message(
    message=content, 
    is_user=(role == 'user')
  )

def get_vectorstore():
  """
  Creates or retrieves an existing vectorstore from session state.

  Returns:
      Vectorstore object stored in session state.
  """
  loader_list, temp_paths = get_loader(sst.pdf_files)
  try:
    with st.spinner("Creating Vectorstore..."):
      if not loader_list:
        st.error("No valid PDF files could be processed. Try uploading another PDF.")
        return
      
      embeddings = OpenAIEmbeddings()
      sst.vectorstore = VectorstoreIndexCreator(
        vectorstore_cls=FAISS, 
        embedding=embeddings
      ).from_loaders(loader_list)
      st.toast("Vectorstore created successfully!")
      st.rerun()
  except Exception as e:
    st.error(f"Error creating vectorstore: `{e}`. Try another PDF.")
    st.stop()
  finally:
    delete_temp_files(temp_paths)

def get_loader(pdf_files: list):
  """
  Creates PDF loaders from uploaded PDFs, saving each file temporarily.

  Args:
      pdf_files (list): List of uploaded PDFs.

  Returns:
      list: PDF loaders for processing.
      list: Temporary file paths for cleanup.
  """
  try:
    with st.spinner("Loading PDFs..."):
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
  except Exception as e:
    st.error("Error loading PDFs. Try uploading another PDF.")
    return
  finally:
    st.toast("PDFs loaded successfully!")

def delete_temp_files(temp_paths: list):
  """
  Deletes temporary files created during PDF loading.

  Args:
      temp_paths (list): Paths of temporary files to delete.
  """
  for path in temp_paths:
    try:
      os.remove(path)
    except Exception as e:
      st.warning(f"Failed to delete temp file {path}: {e}")

def main():
  # Set up the main page layout and title
  st.set_page_config(
    page_title="AskNotes.ai", 
    page_icon='📝', 
    layout="wide", 
    initial_sidebar_state='expanded'
  )
  st.title("📝AskNotes.ai")

  # ---- Sidebar Content ----
  with st.sidebar:
    pdf_files = st.file_uploader(
      label="Upload your PDF", 
      type='pdf',
      accept_multiple_files=True,
      label_visibility='hidden'
    )

    if "chat_history" in sst:
      if st.button("Clear Chat History"):
        initialize_chat_history()
    
    if "vectorstore" in sst:
      if st.button("Delete Vectorstore"):
        sst.pop("vectorstore", None)
  # ---- ---- ---- ---- ---- ----

  if pdf_files and st.sidebar.button("Process PDFs"):
    if "pdf_files" not in sst:
      sst.pdf_files = pdf_files
    
    if pdf_files != sst.pdf_files or "vectorstore" not in sst:
      sst.pdf_files = pdf_files
      get_vectorstore()
    else:
      st.toast("Reusing existing Vectorstore")

    if "chat_history" not in sst:
      initialize_chat_history()

    show_chat(sst.chat_history)
    
    # Capture User Prompt and Display AI Response
    prompt = st.chat_input("Enter your question:")
    if prompt:
      add_to_chat("user", prompt)  # Adds user message to chat history
      
      llm = ChatOpenAI(model='gpt-4', verbose=True, temperature=0.9)
      try:
        response = sst.vectorstore.query(question=prompt, llm=llm)
      except Exception as query_error:
        st.error(f"Error querying the vectorstore: {query_error}")
        response = "There was an error processing your query."

      add_to_chat("ai", response)

  else:
    st.info("Attach a PDF to start chatting")

if __name__ == '__main__':
  main()
