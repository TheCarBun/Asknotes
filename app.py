import os, tempfile
import streamlit as st
from streamlit import session_state as sst
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from streamlit_chat import message
import time

OPENAI_API_KEY = st.secrets['OPENAI_API_KEY']

def initialize_log():
  """
  Initializes log message list
  """
  sst["log"] = [{
    "status" : "info",
    "message" : "Displaying background activity.."
  }]

def display_log(logs:list):
  """
  Display a log message in the sidebar when `show_bts` is active.

  Args:
      logs (list): List of log messages
  """
  for log_msg in logs:
    if log_msg.get('status') == "info":
      sst.container.caption(f"{log_msg.get('message')}")
    elif log_msg.get('status') == "success":
      sst.container.caption(f":green[{log_msg.get('message')}]")
    elif log_msg.get('status') == "error":
      sst.container.caption(f":red[{log_msg.get('message')}]")

def add_to_log(message:str, status="info"):
  """Adds message to List of log messages

  Args:
      message (str): log message
      status (str, optional): "info", "success" or "error". Status of log message. Defaults to "info".
  """
  if sst.show_bts:
    sst.log.append( {
      "status" : status,
      "message" : message
    })
    sst.container.caption(f":grey-background[{message}]")
    
def initialize_chat_history():
  """
  Initialize chat history with a welcome message from AskNotes.ai.
  """
  add_to_log("Initializing Chat History.")
  sst["chat_history"] = [
    {
      'role': 'ai',
      'content': "Hi! I'm AskNotes.ai. Ask me anything about the uploaded PDF!"
    }
  ]
  add_to_log("Chat History Initialized.", "success")

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
  add_to_log("Displaying Chat.")

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
  add_to_log("Message Added to Chat History..")
  
  message(
    message=content, 
    is_user=(role == 'user')
  )
  add_to_log("Displaying Message..")

def get_vectorstore():
  """
  Creates or retrieves an existing vectorstore from session state.

  Returns:
      Vectorstore object stored in session state.
  """
  add_to_log("Creating Vectorstore..")

  loader_list, temp_paths = get_loader(sst.pdf_files)
  try:
    with st.spinner("Creating Vectorstore..."):
      if not loader_list:
        st.error("No valid PDF files could be processed. Try uploading another PDF.")
        add_to_log("Error while processing PDFs..", "error")
        return
      
      embeddings = OpenAIEmbeddings()
      sst.vectorstore = VectorstoreIndexCreator(
        vectorstore_cls=FAISS, 
        embedding=embeddings
      ).from_loaders(loader_list)
      add_to_log("Created Vectorstore Successfully..", "success")
      st.rerun()
  except Exception as e:
    st.error(f"Error creating vectorstore: `{e}`. Try another PDF.")
    add_to_log("Error: Unable to create vectostore..", "error")
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
  add_to_log("Processing PDFs..")
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
          add_to_log("Error: Unable to load PDF..", "error")
          st.error(f"Error loading PDF {pdf.name}: {e}")
      add_to_log("PDFs loaded successfully!", "success")
      return pdf_loader_list, temp_paths
      
  except Exception as e:
    st.error("Error loading PDFs. Try uploading another PDF.")
    return

def delete_temp_files(temp_paths: list):
  """
  Deletes temporary files created during PDF loading.

  Args:
      temp_paths (list): Paths of temporary files to delete.
  """
  add_to_log("Deleting Temporary files..")
  for path in temp_paths:
    try:
      os.remove(path)
    except Exception as e:
      st.warning(f"Failed to delete temp file {path}: {e}")
      add_to_log("Error: Failed to delete temporary files..", "error")
  add_to_log("Temporary Files Deleted.", "success")


def load_css() -> str:
    """
    Loads CSS stylesheet and SVG background from local files.

    Returns:
    - str: The content of the CSS file.
    """
    # Load CSS stylesheet
    try:
        with open('static/styles.css') as f:
            custom_css = f.read()
        return custom_css
    except FileNotFoundError:
        add_to_log("❗Error loading stylesheet: File not found.", "error")
    except Exception as e:
        add_to_log("❗Error loading stylesheet.", "error")

def main():
  # Set up the main page layout and title
  st.set_page_config(
    page_title="AskNotes.ai", 
    page_icon='📝', 
    layout="wide", 
    initial_sidebar_state='expanded'
  )
  st.title("📝AskNotes.ai")

  # Custom CSS
  st.markdown(f'<style>{load_css()}</style>', unsafe_allow_html=True)

  # ---- Sidebar Content ----
  if "show_bts" not in sst:
    sst.show_bts = False
    
  with st.sidebar:
    pdf_files = st.file_uploader(
      label="Upload your PDF", 
      type='pdf',
      accept_multiple_files=True,
      label_visibility='hidden'
    )

    if "chat_history" in sst:
      if st.button("Clear Chat History", type='primary', use_container_width=True):
        initialize_chat_history()
    
    if "vectorstore" in sst:
      if st.button("Remake Vectorstore", use_container_width=True):
        sst.pop("vectorstore", None)

    
    if st.toggle(label="Display backend activity", help="Enable detailed logging of backend processes for transparency and debugging."):
      sst.show_bts = True
      with st.container():
        st.markdown("### Program Logs:")
        sst.container = st.container(height= 200)
    else:
      sst.show_bts = False
  # ---- ---- ---- ---- ---- ----

  if sst.show_bts:
    if "log" not in sst:
      initialize_log()
    
    display_log(sst.log)

  if pdf_files:
    if "pdf_files" not in sst:
      sst.pdf_files = pdf_files
    
    if pdf_files != sst.pdf_files or "vectorstore" not in sst:
      sst.pdf_files = pdf_files
      get_vectorstore()
    else:
      add_to_log("Reusing existing Vectorstore", "success")

    if "chat_history" not in sst:
      initialize_chat_history()

    show_chat(sst.chat_history)
    
    # Capture User Prompt and Display AI Response
    prompt = st.chat_input("Enter your question:")
    if prompt:
      add_to_chat("user", prompt)  # Adds user message to chat history
      
      # Progress Bar
      progress_text_list = ["Scanning PDF...", "Gathering info...", "Vectorizing gathered info...", "Preparing response..."]
      progress_bar = st.progress(value=0, text=progress_text_list[0])

      if sst.show_bts:
        st.sidebar.caption(":grey[Generating Response..]")


      # Modify prompt for teacher-like response
      teacher_prompt = (
          "You are an expert teacher with in-depth knowledge. When responding, explain your answer in detail, "
          "use examples if relevant, and structure your response as you would in a teaching environment. "
          "Reference relevant sections from the PDF. Here is the question: "
      ) + prompt
      
      llm = ChatOpenAI(model='gpt-4', verbose=True, temperature=0.9)
      try:
        response = sst.vectorstore.query(question=teacher_prompt, llm=llm)
      except Exception as query_error:
        st.error(f"Error querying the vectorstore: {query_error}")
        response = "There was an error processing your query."

        add_to_chat("ai", response)

  else:
    st.info("Attach a PDF to start chatting")

if __name__ == '__main__':
  main()
