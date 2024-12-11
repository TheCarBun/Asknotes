import os, tempfile
import streamlit as st
import json
from streamlit import session_state as sst
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from streamlit_chat import message
from datetime import datetime
from io import BytesIO

OPENAI_API_KEY = st.secrets['OPENAI_API_KEY']

def get_timestamp():
  """Generates and returns a timestamp for the current time

  Returns:
      datetime: Current time in format of Hour:Minute:Second
  """
  return datetime.now().strftime("%H:%M:%S")

def initialize_log():
  """
  Initializes log message list
  """
  sst["log"] = [{
    "time" : get_timestamp(),
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
      sst.container.caption(f":orange[[{log_msg.get('time')}]] {log_msg.get('message')}")
    elif log_msg.get('status') == "success":
      sst.container.caption(f":orange[[{log_msg.get('time')}]] :green[{log_msg.get('message')}]")
    elif log_msg.get('status') == "error":
      sst.container.caption(f":orange[[{log_msg.get('time')}]] :red[{log_msg.get('message')}]")

def add_to_log(message:str, status="info"):
  """Adds message to List of log messages

  Args:
      message (str): log message
      status (str, optional): "info", "success" or "error". Status of log message. Defaults to "info".
  """
  if sst.show_bts:
    log_entry = {
      "time" : get_timestamp(),
      "status" : status,
      "message" : message
    }
    sst.log.insert(0, log_entry)
    sst.container.caption(f":orange[[now]] :grey-background[{message}]")
    
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

def prepare_download_file(format_type):
  
    """
    Prepare the chat history file based on the selected format.

    Args:
        format_type (str): 'JSON' or 'TXT'.

    Returns:
        tuple: Tuple containing the file content, file name, and file type.
        
    """
    if format_type == "JSON":
      
        add_to_log("Preparing chat history as JSON...")
        return BytesIO(json.dumps(sst.chat_history, indent=4).encode('utf-8')), "chat_history.json", "application/json"
    
    elif format_type == "TXT":
      
        add_to_log("Preparing chat history as TXT...")
        text_output = "\n\n--------------------------------------------------------------\n\n".join(
            [
                f"{'User' if msg['role'] == 'user' else 'AI'}: {msg['content']}"
                for msg in sst.chat_history
            ]
        )
        text_output = f"Chat History:\n{'=' * 40}\n\n{text_output}\n\n{'=' * 40}\nEnd of Chat"
        return BytesIO(text_output.encode('utf-8')), "chat_history.txt", "text/plain"
    
    return None, None, None
  
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

# ---- Navbar ----
  with st.container():
    app_col, home_col, about_col = st.columns(3)

    app_col.page_link(
    page='app.py',
    label='App',
    icon=':material/robot_2:'
    )
    home_col.page_link(
    page= "pages/home.py",
    label= "Home",
    icon= ':material/home:'
    )
    about_col.page_link(
    page='pages/about.py',
    label='About',
    icon=':material/star:',
    )
  st.markdown("---")

  # Title
  st.markdown("### 📝AskNotes.ai")

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
    if st.toggle("Advanced mode", help="Toggle advanced controls on/off"):
      with st.container(border=True):
        st.markdown("### Select LLM:")
        llm_model = st.radio(
          label="Select LLM",
          options=[
            'gpt-4o-mini', 
            'gpt-4o', 
            'o1-preview', 
            'o1-mini'
            ],
          captions=[
            'General Use($0.150 / 1M input tokens)', 
            'Advanced Vision and Context($2.50 / 1M input tokens)', 
            'Advanced Reasoning($15.00 / 1M input tokens)', 
            'Advanced Maths and Science($3.00 / 1M input tokens)'
            ],
            label_visibility='hidden'
                )
      with st.container(border=True):
        if "chat_history" in sst:
          st.markdown("### Refresh Chat:")
          if st.button("Clear Chat History", type='primary', use_container_width=True):
            initialize_chat_history()
        
        if "vectorstore" in sst:
          if st.button("Remake Vectorstore", use_container_width=True):
            sst.pop("vectorstore", None)

      with st.container(border=True):
        if "chat_history" in sst:
          st.markdown("### Download Chat History:")
          format_type = st.selectbox("Choose format for download",options=["JSON", "TXT"],index=0,help="Select the format to download chat history.")

          if format_type:
            file_data, file_name, mime_type = prepare_download_file(format_type)
            if file_data:
              st.download_button(
                  label=f"Download as {format_type}",
                  data=file_data,
                  use_container_width=True,
                  file_name=file_name,
                  mime=mime_type
              )  
          

    
    if st.toggle(label="Display backend activity", help="Enable/Disable detailed logging of backend processes for transparency and debugging."):
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

      # Modify prompt for teacher-like response
      teacher_prompt = (
          "You are an expert teacher with in-depth knowledge. When responding, explain your answer in detail, "
          "use examples if relevant, and structure your response as you would in a teaching environment. "
          "Reference relevant sections from the PDF. Here is the question: "
      ) + prompt
      with st.spinner("Generating response..."):
        add_to_log("Processing query..")
        llm = ChatOpenAI(model=llm_model, verbose=True, temperature=0.9)
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

