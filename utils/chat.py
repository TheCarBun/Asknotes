from streamlit import session_state as sst
from streamlit_chat import message
from utils.logs import add_to_log
    
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
