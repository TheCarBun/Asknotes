# 📝 AskNotes.ai - AI Teacher
![GitHub commit activity](https://img.shields.io/github/commit-activity/t/TheCarBun/Asknotes?style=for-the-badge) 
![GitHub Issues or Pull Requests](https://img.shields.io/github/issues-raw/TheCarBun/Asknotes?style=for-the-badge) 
![GitHub Issues or Pull Requests](https://img.shields.io/github/issues-pr-raw/TheCarBun/Asknotes?style=for-the-badge) 
![GitHub Issues or Pull Requests](https://img.shields.io/github/issues-closed-raw/TheCarBun/Asknotes?style=for-the-badge) 
![GitHub Issues or Pull Requests](https://img.shields.io/github/issues-pr-closed-raw/TheCarBun/Asknotes?style=for-the-badge)
![GitHub last commit](https://img.shields.io/github/last-commit/TheCarBun/Asknotes?style=for-the-badge)
![GitHub forks](https://img.shields.io/github/forks/TheCarBun/Asknotes?style=for-the-badge)
![GitHub Repo stars](https://img.shields.io/github/stars/TheCarBun/Asknotes?style=for-the-badge)

## ✨ About
Asknotes is crafted to revolutionize the way students engage with their study materials. By seamlessly reading PDF notes, Asknotes transforms passive information into active learning, making study sessions more effective and enjoyable.

Asknotes is an innovative AI application built with Langchain that leverages the power of RAG(Retrieval Augmented Generation).

With Asknotes, students can effortlessly extract key insights from their PDF notes and receive personalized study guidance, ensuring they grasp concepts with confidence.

### ✨Try for free --> : [https://asknotes.streamlit.app/](https://asknotes.streamlit.app/home)

![image](https://github.com/user-attachments/assets/a87d9508-9e56-4a50-aa16-e981f717cf05)


## Inspiration for this project:
During my university days, one of the biggest challenges I faced was studying from notes provided in the form of PDFs. Whether it was preparing for term exams or solving previous year's question papers, the process was time-consuming and often frustrating. Scrolling through countless pages just to find relevant answers felt like looking for a needle in a haystack. 🕵️‍♂️ <br>
That’s why I built AskNotes—an AI-powered tool designed to make studying faster, smarter, and more efficient! 🚀<br>
With AskNotes, you can:<br>
 ✅ Upload your notes in PDF format.<br>
 ✅ Ask specific questions about the content.<br>
 ✅ Get instant, accurate answers in just a few seconds.<br>
No more wasting hours flipping through pages. Let AskNotes do the heavy lifting so you can focus on what matters most—understanding and learning.

---

## Table of Contents
- [About](#about)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Error Handling](#error-handling)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)

---
## About
AskNotes is an interactive learning application designed for students to upload their study materials (in PDF format) and get AI-powered assistance in understanding the content. Built using Streamlit and LangChain, AskNotes provides a question-and-answer interface to query the content within PDF files, offering a personalized learning experience.

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
