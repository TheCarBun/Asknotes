import streamlit as st
from streamlit import session_state as sst
from datetime import datetime
from io import BytesIO
from pathlib import Path
import json, os
from utils.logs import add_to_log

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


def load_css(path:Path= Path('static/styles.css')) -> str:
  """
  Loads a CSS stylesheet from a local file.

  Args:
      path (Path): Path to the CSS file (default: 'static/styles.css').

  Returns:
      str: The content of the CSS file if successfully loaded, otherwise an empty string.
  """
  # Load CSS stylesheet
  try:
    if not path.is_file():
      add_to_log(f"❗Error loading stylesheet: {path} does not exist.", "error")
      return ""
    with open(path) as f:
        custom_css = f.read()
    return custom_css
  except FileNotFoundError:
    add_to_log("❗Error loading stylesheet: File not found.", "error")
  except Exception as e:
    add_to_log("❗Error loading stylesheet.", "error")
