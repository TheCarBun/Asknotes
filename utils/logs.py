from streamlit import session_state as sst
from datetime import datetime

timestamp = datetime.now().strftime("%H:%M:%S")

def initialize_log():
  """
  Initializes log message list
  """
  sst["log"] = [{
    "time" : timestamp,
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
  # Check if show_bts exists in session state, default to False if not
  show_bts = getattr(sst, 'show_bts', False)
  
  if show_bts:
    log_entry = {
      "time" : timestamp,
      "status" : status,
      "message" : message
    }
    sst.log.insert(0, log_entry)
    sst.container.caption(f":orange[[now]] :grey-background[{message}]")
  print(f"[{timestamp}] : {message}")
