# Harshit-Rana-wasserstoff-AiInternTask
 PDF Data Processor and Viewer is a web app that monitors a folder for new PDFs, extracts summaries and keywords, and displays results on a Streamlit interface. It uses MongoDB for data storage and Docker for streamlined deployment. Ideal for users needing quick, automated insights into PDF content.
# PDF Data Processor and Viewer

This project is a PDF data processing and viewing solution built with Python and Streamlit. It monitors a folder for new PDF files, extracts summaries and keywords, and saves the results to MongoDB. The Streamlit web interface allows you to view the summaries and keywords for each processed PDF.

## Table of Contents
- [System Requirements](#system-requirements)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [Solution Explanation](#solution-explanation)

---

## System Requirements
- Python 3.7 or later
- MongoDB (local instance or remote connection)
- Python libraries:
  - `PyPDF2`
  - `watchdog`
  - `nltk`
  - `pymongo`
  - `streamlit`
  - `altair`

## Setup Instructions

### 1. Install MongoDB
   - Ensure MongoDB is installed and running on `localhost:27017` (or modify the connection URI in the code to match your setup).

### 2. Clone the Repository
   - Clone or download the repository to your local machine:
     ```bash
     git clone https://github.com/yourusername/pdf-data-processor.git
     cd pdf-data-processor
     ```

### 3. Install Required Libraries
   - Use the following command to install required Python libraries:
     ```bash
     pip install -r requirements.txt
     ```

### 4. Set Up NLTK Resources
   - Run the following script to download required NLTK resources (`stopwords` and `punkt`):
     ```python
     import nltk
     nltk.download('stopwords')
     nltk.download('punkt')
     ```

### 5. Update Folder Path
   - Modify the `folder_path` variable in the script (`main.py`) to specify the folder path you want to monitor for PDF files:
     ```python
     folder_path = r"C:\Users\harshit rana\OneDrive\Desktop\pdfdataset"
     ```

### 6. Run the Application
   - Run the script to start both the monitoring service and the Streamlit app:
     ```bash
     streamlit run main.py
     ```
   - The Streamlit app will open in your browser at `http://localhost:8501`.

---

## Usage

1. **Folder Monitoring**: The application monitors a specified folder for new PDF files. When a PDF is added, it is automatically processed.
2. **PDF Processing**: For each PDF, the text is extracted, summarized, and keywords are identified.
3. **Data Storage**: The processed data (file name, summary, and keywords) is saved to MongoDB in a collection called `pdf_summaries`.
4. **Streamlit Web Interface**: The web interface allows you to view all processed summaries and keywords stored in MongoDB.

---

## Solution Explanation

This solution combines file monitoring, PDF processing, database storage, and a web interface in a streamlined Python application. Here's a breakdown of each component:

1. **PDF Monitoring and Processing**:
   - Using the `watchdog` library, the script monitors a specified folder. When a new PDF is added, it triggers processing via the `PDFHandler` class.
   - The PDF content is read and processed using `PyPDF2`, where text is extracted page by page.
   - Text is summarized based on sentence importance, and keywords are extracted using NLTK’s `stopwords` and Python’s `Counter` to identify the most common, meaningful words.

2. **Data Storage in MongoDB**:
   - Processed summaries and keywords are stored in MongoDB, making the data easy to retrieve and display.

3. **Streamlit Web Interface**:
   - The Streamlit interface displays PDF summaries and keywords in a user-friendly way, with each processed file’s data shown as a separate section. This provides easy access to the processed information directly from the MongoDB database.

This design keeps the PDF processing and the web interface loosely coupled, allowing each to run independently while sharing the MongoDB database. Using threads, the folder monitoring runs continuously in the background without interrupting the Streamlit interface.
