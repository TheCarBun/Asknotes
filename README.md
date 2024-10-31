# AskNotes.ai

AskNotes is an interactive learning application designed for students to upload their study materials (in PDF format) and get AI-powered assistance in understanding the content. Built using Streamlit and LangChain, AskNotes provides a question-and-answer interface to query the content within PDF files, offering a personalized learning experience.
### Deployed at : https://asknotes.streamlit.app/
---

## Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Error Handling](#error-handling)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)

---

## Features
- **Upload Study Materials**: Students can upload one or multiple PDFs containing study materials.
- **Interactive Q&A**: Ask questions about the uploaded content, and AskNotes will provide relevant answers.
- **Session-based Chat**: Tracks chat history during each session, allowing users to refer back to previous interactions.
- **Secure and Temporary Storage**: Uploaded PDFs are temporarily stored for processing and deleted automatically after use.
- **Streamlit UI**: A user-friendly chat interface for engaging with AskNotes, implemented using `streamlit_chat`.

---

## Tech Stack
- **Frontend**: Streamlit for UI.
- **Backend**: LangChain (for Q&A processing), FAISS (for efficient vector storage and retrieval).
- **Embeddings and Language Models**: OpenAI embeddings and ChatGPT (gpt-4) for natural language understanding and answer generation.

---

## Getting Started

### Prerequisites
- Python 3.8+
- OpenAI API Key (for embeddings and GPT-4 model)

### Installation
1. **Clone the repository**:
    ```bash
    git clone https://github.com/TheCarBun/Asknotes.git
    cd Asknotes
    ```
   
2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Set up OpenAI API key**:
   Add your OpenAI API key to Streamlit secrets by creating a `secrets.toml` file in the `.streamlit` folder:
    ```toml
    [OPENAI_API_KEY]
    key = "your_openai_api_key_here"
    ```

4. **Run the app**:
    ```bash
    streamlit run app.py
    ```

---

## Usage
1. **Upload PDFs**:
   - Use the sidebar file uploader to upload one or more PDF files.
   - Files will be processed and used to create a searchable vector store.

2. **Ask Questions**:
   - Type a question in the chat input related to the PDF content.
   - The app will display responses based on the contents of the uploaded materials.

3. **Clear Chat History**:
   - Use the "Clear Chat History" button in the sidebar to reset the chat for a fresh session.

---

## Project Structure

    ├── asknotes.py             # Main application file
    ├── requirements.txt         # Python dependencies
    ├── .streamlit/
    │   └── secrets.toml         # API keys and secrets
    ├── README.md                # Project documentation
    └── ...                      # Additional project files and configurations

---

## Error Handling

The app includes exception handling for better stability:
- **API Key Missing**: Displays an error if the OpenAI API key is not configured correctly.
- **File Loading**: Catches errors when loading PDFs and warns the user if a file cannot be processed.
- **Vectorstore Creation**: Handles issues during vectorstore creation, providing user feedback on errors.
- **Query Processing**: Informs the user if an error occurs while querying the vectorstore.
- **Temp File Deletion**: Any issues with file deletion after processing are logged to avoid storage issues.

These exceptions ensure a more resilient app and a smoother user experience.

---

## Future Enhancements
- **Support for Additional File Types**: Extend support to handle TXT, DOCX, and EPUB files for broader usability.
- **Answer Summarization**: Include a summarization option for longer responses.
- **Enhanced NLP**: Add fine-tuning capabilities to improve relevance and answer quality based on specific course material.
- **User Authentication**: Implement session tracking with user authentication to store user chat history for later review.

---

## Contributing
We welcome contributions! Please follow these steps to contribute:
1. Fork the project.
2. Create your feature branch (`git checkout -b feature/your-feature-name`).
3. Commit your changes (`git commit -m 'Add your message'`).
4. Push to the branch (`git push origin feature/your-feature-name`).
5. Open a Pull Request.

Please ensure your code follows the existing style and includes comments where necessary.

---

Enjoy using AskNotes.ai for your interactive learning journey! Feel free to reach out for any questions or issues with the project.