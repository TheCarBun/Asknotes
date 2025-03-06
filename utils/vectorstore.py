import streamlit as st
from streamlit import session_state as sst
from langchain.indexes import VectorstoreIndexCreator
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders.pdf import PyPDFLoader
from utils.logs import add_to_log
from utils.utils import delete_temp_files
import tempfile

def get_vectorstore():
    """
    Creates or retrieves an existing vectorstore from session state.
    Includes enhanced error handling for PDFs with graphics or no text content.

    Returns:
        Vectorstore object stored in session state.
    """
    add_to_log("Creating Vectorstore..")

    loader_list, temp_paths = get_loader(sst.pdf_files)
    try:
        with st.spinner("Creating Vectorstore..."):
            if not loader_list:
                # Clear PDF files from session state to allow fresh start
                if "vectorstore" in sst:
                    del sst.vectorstore
                return None
            
            embeddings = OpenAIEmbeddings()
            try:
                sst.vectorstore = VectorstoreIndexCreator(
                    vectorstore_cls=FAISS, 
                    embedding=embeddings
                ).from_loaders(loader_list)
                add_to_log("Created Vectorstore Successfully..", "success")
                return sst.vectorstore
            except Exception as e:
                st.toast(f"Error creating vectorstore. Try another PDF.", icon="⚠️")
                add_to_log(f"Error: Unable to create vectorstore - {str(e)}", "error")
                if "vectorstore" in sst:
                    del sst.vectorstore
                return None
    except Exception as e:
        st.toast("Unexpected error. Please try again with a different PDF.", icon="⚠️")
        add_to_log(f"Error: {str(e)}", "error")
        if "vectorstore" in sst:
            del sst.vectorstore
        return None
    finally:
        delete_temp_files(temp_paths)

def get_loader(pdf_files: list):
    """
    Creates PDF loaders from uploaded PDFs, saving each file temporarily.
    Includes enhanced error handling for PDFs with graphics.

    Args:
        pdf_files (list): List of uploaded PDFs.

    Returns:
        list: PDF loaders for processing.
        list: Temporary file paths for cleanup.
    """
    add_to_log("Processing PDFs..")
    pdf_loader_list = []
    temp_paths = []
    has_unreadable_pdfs = False
    
    try:
        with st.spinner("Loading PDFs..."):
            for pdf in pdf_files:
                try:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as f:
                        f.write(pdf.getvalue())
                        temp_paths.append(f.name)
                        # Create loader with enhanced error handling
                        loader = PyPDFLoader(
                            f.name,
                            extract_images=False  # Skip image extraction to avoid errors
                        )
                        # Test load to catch any immediate issues
                        try:
                            pages = loader.load()
                            # Only add loader if it successfully extracted text
                            if any(len(page.page_content.strip()) > 0 for page in pages):
                                pdf_loader_list.append(loader)
                                add_to_log(f"Successfully processed {pdf.name}", "success")
                            else:
                                has_unreadable_pdfs = True
                                add_to_log(f"No text content found in {pdf.name}", "error")
                        except Exception as e:
                            has_unreadable_pdfs = True
                            add_to_log(f"Error loading pages from {pdf.name}", "error")
                except Exception as e:
                    add_to_log(f"Error processing {pdf.name}", "error")
                    continue
            
            if pdf_loader_list:
                add_to_log("PDFs loaded successfully!", "success")
                if has_unreadable_pdfs:
                    st.toast("Some PDFs were skipped. Only PDFs with readable text were included.", icon="ℹ️")
                return pdf_loader_list, temp_paths
            else:
                add_to_log("No valid PDFs could be processed", "error")
                st.toast("Please upload PDFs with readable text content.", icon="⚠️")
                return None, temp_paths
            
    except Exception as e:
        add_to_log(f"Error: {str(e)}", "error")
        st.toast("Error loading PDFs. Please try again with different files.", icon="⚠️")
        return None, temp_paths
