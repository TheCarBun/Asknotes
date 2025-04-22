import streamlit as st
from streamlit import session_state as sst
from langchain_google_genai import ChatGoogleGenerativeAI
from utils.chat import initialize_chat_history, show_chat, add_to_chat
from utils.logs import initialize_log, display_log, add_to_log
from utils.vectorstore import get_vectorstore
from utils.ui import base_ui, promo
from utils.utils import load_css, prepare_download_file

GEMINI_API_KEY = st.secrets['GEMINI_API_KEY']


def main():
    base_ui()

    # Title
    st.markdown("### 📝AskNotes.ai")

    # Custom CSS
    st.markdown(f'<style>{load_css()}</style>', unsafe_allow_html=True)

    # ---- Sidebar Content ----
    if "show_bts" not in sst:
        sst.show_bts = False
    
    llm_model = 'gemini-2.0-flash-lite'
    
    with st.sidebar:
        pdf_files = st.file_uploader(
            label="Upload your PDF", 
            type='pdf',
            accept_multiple_files=True,
            label_visibility='hidden'
        )
        if st.toggle("Advanced controls", help="Toggle advanced controls on/off"):
            with st.container(border=True):
                st.markdown("### Select LLM:")
                llm_model = st.radio(
                    label="Select LLM",
                    options=[
                        'gemini-2.0-flash', 
                        'gemini-1.5-flash',
                    ],
                    captions=[
                        'Code execution, long context (15rpm, 1500rpd, 1mil)', 
                        'Fast and versatile (15rpm, 1500rpd, 1mil)'
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
        promo()

    if sst.show_bts:
        if "log" not in sst:
            initialize_log()
        
        display_log(sst.log)

    # Handle PDF processing and chat interface
    if pdf_files:
        if "pdf_files" not in sst or pdf_files != sst.pdf_files:
            sst.pdf_files = pdf_files
            if "vectorstore" in sst:
                del sst.vectorstore
            get_vectorstore()
        
        # Only proceed with chat if we have a valid vectorstore
        if "vectorstore" in sst:
            if "chat_history" not in sst:
                initialize_chat_history()
            
            show_chat(sst.chat_history)
            
            # Capture User Prompt and Display AI Response
            prompt = st.chat_input("Enter your question:", disabled=False)
            if prompt:
                add_to_chat("user", prompt)

                with st.spinner("Generating response..."):
                    add_to_log("Processing query..")
                    llm = ChatGoogleGenerativeAI(model=llm_model, temperature=0.9, google_api_key=GEMINI_API_KEY)
                    try:
                        response = sst.vectorstore.query(question=prompt, llm=llm)
                    except Exception as query_error:
                        st.toast("Error processing query. Please try again.", icon="⚠️")
                        response = "I apologize, but I encountered an error processing your query. Please try again."

                    add_to_chat("ai", response)
        else:
            # Show error state and disable chat input
            st.chat_input("Enter your question:", disabled=True)
            st.info("Please upload a PDF with readable text content to start chatting.")
    else:
        # Clear all states when no PDF is present
        if "vectorstore" in sst:
            del sst.vectorstore
        if "pdf_files" in sst:
            del sst.pdf_files
        if "chat_history" in sst:
            del sst.chat_history
        st.info("Attach a PDF to start chatting")

if __name__ == '__main__':
  main()

