import unittest
import tempfile
import os
from pathlib import Path
from unittest.mock import MagicMock, patch
import streamlit as st
from app import get_loader, get_vectorstore
from io import BytesIO
import app

class TestPDFProcessing(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test"""
        # Create a temporary directory for test files
        self.test_dir = tempfile.mkdtemp()
        
        # Mock streamlit session state
        self.patcher = patch('streamlit.session_state', new_callable=MagicMock)
        self.mock_session_state = self.patcher.start()
        self.mock_session_state.show_bts = False  # Disable logging for tests

    def tearDown(self):
        """Clean up after each test"""
        # Stop the patcher
        self.patcher.stop()
        
        # Remove temporary directory and its contents
        for root, dirs, files in os.walk(self.test_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(self.test_dir)

    def create_test_pdf(self, content, filename="test.pdf"):
        """Helper function to create a test PDF file"""
        filepath = os.path.join(self.test_dir, filename)
        with open(filepath, 'wb') as f:
            f.write(content)
        return filepath

    @patch('streamlit.toast')
    @patch('app.PyPDFLoader')
    def test_valid_pdf_processing(self, mock_pdf_loader, mock_toast):
        """Test processing of a valid PDF with text content"""
        # Mock PDF loader behavior
        mock_page = MagicMock()
        mock_page.page_content = "Sample Text"
        mock_loader_instance = mock_pdf_loader.return_value
        mock_loader_instance.load.return_value = [mock_page]
        
        # Create mock PDF file object
        mock_pdf = MagicMock()
        mock_pdf.name = "test.pdf"
        mock_pdf.getvalue.return_value = b"mock pdf content"
        
        # Test PDF loading
        with patch('streamlit.spinner'):
            loader_list, temp_paths = get_loader([mock_pdf])
        
        # Assertions
        self.assertIsNotNone(loader_list)
        self.assertEqual(len(loader_list), 1)
        self.assertFalse(mock_toast.called)

    @patch('streamlit.toast')
    @patch('app.PyPDFLoader')
    def test_image_only_pdf_processing(self, mock_pdf_loader, mock_toast):
        """Test processing of a PDF containing only images"""
        # Mock PDF loader behavior for image-only PDF
        mock_page = MagicMock()
        mock_page.page_content = ""  # Empty content to simulate image-only PDF
        mock_loader_instance = mock_pdf_loader.return_value
        mock_loader_instance.load.return_value = [mock_page]
        
        # Create mock PDF file object
        mock_pdf = MagicMock()
        mock_pdf.name = "image_only.pdf"
        mock_pdf.getvalue.return_value = b"mock pdf content"
        
        # Test PDF loading
        with patch('streamlit.spinner'):
            loader_list, temp_paths = get_loader([mock_pdf])
        
        # Assertions
        self.assertIsNone(loader_list)
        mock_toast.assert_called_with(
            "Please upload PDFs with readable text content.",
            icon="⚠️"
        )

    @patch('streamlit.toast')
    @patch('app.PyPDFLoader')
    @patch('tempfile.NamedTemporaryFile')
    def test_multiple_pdfs_processing(self, mock_temp_file, mock_loader, mock_toast):
        """Test processing multiple PDFs with mixed content"""
        # Create mock pages with proper content
        mock_page_valid = MagicMock()
        mock_page_valid.page_content = "Sample Text Content"
        mock_page_empty = MagicMock()
        mock_page_empty.page_content = ""

        # Mock temporary file
        mock_temp = MagicMock()
        mock_temp.__enter__.return_value = mock_temp
        mock_temp.name = "/tmp/test.pdf"
        mock_temp_file.return_value = mock_temp

        # Set up the mock loader to handle different files
        mock_loader_instance = MagicMock()
        mock_loader_instance.load.return_value = [mock_page_valid]
        mock_loader.return_value = mock_loader_instance

        # Create mock PDFs
        mock_pdf1 = MagicMock()
        mock_pdf1.name = "valid.pdf"
        mock_pdf1.getvalue = lambda: b"content"

        mock_pdf2 = MagicMock()
        mock_pdf2.name = "image_only.pdf"
        mock_pdf2.getvalue = lambda: b"content"

        # Test processing multiple PDFs
        loader_list, temp_paths = app.get_loader([mock_pdf1, mock_pdf2])

        self.assertIsNotNone(loader_list)
        self.assertEqual(len(loader_list), 2)  # Both PDFs should be included
        mock_toast.assert_not_called()

    @patch('streamlit.toast')
    @patch('app.PyPDFLoader')
    def test_corrupted_pdf_processing(self, mock_pdf_loader, mock_toast):
        """Test processing of a corrupted PDF file"""
        # Mock PDF loader to raise an exception
        mock_loader_instance = mock_pdf_loader.return_value
        mock_loader_instance.load.side_effect = Exception("Invalid PDF file")
        
        # Create mock PDF file object
        mock_pdf = MagicMock()
        mock_pdf.name = "corrupted.pdf"
        mock_pdf.getvalue.return_value = b"corrupted content"
        
        # Test PDF loading
        with patch('streamlit.spinner'):
            loader_list, temp_paths = get_loader([mock_pdf])
        
        # Assertions
        self.assertIsNone(loader_list)
        mock_toast.assert_called_with(
            "Please upload PDFs with readable text content.",
            icon="⚠️"
        )

class TestPDFHandling(unittest.TestCase):
    def setUp(self):
        # Mock streamlit session state
        self.mock_session_state = {}
        st.session_state = self.mock_session_state
        
        # Create sample PDF files for testing
        self.text_pdf = MagicMock()
        self.text_pdf.name = "sample_text.pdf"
        self.text_pdf.getvalue = MagicMock(return_value=b"Sample PDF with text")
        
        self.image_pdf = MagicMock()
        self.image_pdf.name = "sample_image.pdf"
        self.image_pdf.getvalue = MagicMock(return_value=b"Sample PDF with image")

    @patch('streamlit.toast')
    @patch('app.PyPDFLoader')
    def test_pdf_with_text(self, mock_loader, mock_toast):
        # Mock successful text extraction
        mock_page = MagicMock()
        mock_page.page_content = "Sample text content"
        mock_loader.return_value.load.return_value = [mock_page]
        
        # Test processing a PDF with text
        loader_list, temp_paths = app.get_loader([self.text_pdf])
        
        self.assertIsNotNone(loader_list)
        self.assertEqual(len(loader_list), 1)
        mock_toast.assert_not_called()

    @patch('streamlit.toast')
    @patch('app.PyPDFLoader')
    def test_pdf_without_text(self, mock_loader, mock_toast):
        # Mock PDF with no text content
        mock_page = MagicMock()
        mock_page.page_content = ""
        mock_loader.return_value.load.return_value = [mock_page]
        
        # Test processing a PDF without text
        loader_list, temp_paths = app.get_loader([self.image_pdf])
        
        self.assertIsNone(loader_list)
        mock_toast.assert_called_once_with(
            "Please upload PDFs with readable text content.",
            icon="⚠️"
        )

    @patch('streamlit.toast')
    @patch('app.PyPDFLoader')
    @patch('tempfile.NamedTemporaryFile')
    def test_mixed_pdfs(self, mock_temp_file, mock_loader, mock_toast):
        # Mock temporary file
        mock_temp = MagicMock()
        mock_temp.__enter__.return_value = mock_temp
        mock_temp.name = "/tmp/test.pdf"
        mock_temp_file.return_value = mock_temp

        # Set up the mock loader to handle different files
        mock_loader_instance = MagicMock()
        mock_loader_instance.load.return_value = [MagicMock(page_content="Sample text content")]
        mock_loader.return_value = mock_loader_instance
        
        # Test processing multiple PDFs
        loader_list, temp_paths = app.get_loader([self.text_pdf, self.image_pdf])
        
        self.assertIsNotNone(loader_list)
        self.assertEqual(len(loader_list), 2)  # Both PDFs should be processed
        mock_toast.assert_not_called()

    @patch('streamlit.toast')
    @patch('app.PyPDFLoader')
    def test_pdf_loading_error(self, mock_loader, mock_toast):
        # Mock PDF loading error
        class MockLoader:
            def __init__(self, file_path, extract_images=False):
                raise Exception("PDF loading error")

        mock_loader.side_effect = MockLoader
        
        # Test processing a PDF that causes an error
        loader_list, temp_paths = app.get_loader([self.text_pdf])
        
        self.assertIsNone(loader_list)
        mock_toast.assert_called_once_with(
            "Error loading PDF. Please try a different file.",
            icon="⚠️"
        )

if __name__ == '__main__':
    unittest.main() 