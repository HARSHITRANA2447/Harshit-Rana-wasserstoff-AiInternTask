import os
import time
import PyPDF2
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import nltk
from nltk.corpus import stopwords
from collections import Counter
import re
from nltk.tokenize import sent_tokenize
from pymongo import MongoClient
import streamlit as st
from threading import Thread

# Download required NLTK data
nltk.download('stopwords')
nltk.download('punkt')

# MongoDB connection setup
client = MongoClient("mongodb://localhost:27017/")
db = client['pdf_data_db']
collection = db['pdf_summaries']

# Function to read a PDF and extract its text
def read_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text() + '\n'
        return text

# Extract keywords from text
def extract_keywords(text, num_keywords=10):
    text = text.lower()
    words = re.findall(r'\b[a-z]{3,}\b', text)
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if word not in stop_words]
    word_counts = Counter(filtered_words)
    return word_counts.most_common(num_keywords)

# Summarize text based on sentence scoring
def summarize_text(text, num_sentences=5):
    sentences = sent_tokenize(text)
    words = re.findall(r'\b[a-z]{3,}\b', text.lower())
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if word not in stop_words]
    word_counts = Counter(filtered_words)
    sentence_ranks = {}
    for sentence in sentences:
        sentence_words = re.findall(r'\b[a-z]{3,}\b', sentence.lower())
        sentence_score = sum([word_counts[word] for word in sentence_words if word in word_counts])
        sentence_ranks[sentence] = sentence_score
    
    top_sentences = sorted(sentence_ranks, key=sentence_ranks.get, reverse=True)[:num_sentences]
    summary = ' '.join(top_sentences)
    
    return summary

# Save processed PDF data to MongoDB
def save_to_mongo(file_name, keywords, summary):
    data = {
        'file_name': file_name,
        'keywords': keywords,
        'summary': summary
    }
    collection.insert_one(data)
    print(f"Data saved to MongoDB for file: {file_name}")

# Function to process PDF
def process_pdf(file_path):
    print(f"Processing PDF: {file_path}")
    text = read_pdf(file_path)
    summary = summarize_text(text)
    keywords = extract_keywords(summary)
    save_to_mongo(os.path.basename(file_path), keywords, summary)
    print(f"Processed PDF: {file_path}")

# Watchdog handler for monitoring new PDFs
class PDFHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return

        file_path = event.src_path
        if file_path.endswith('.pdf'):
            print(f"New PDF detected: {file_path}")
            process_pdf(file_path)

# Function to monitor folder for new PDFs
def monitor_folder(folder_path):
    event_handler = PDFHandler()
    observer = Observer()
    observer.schedule(event_handler, folder_path, recursive=False)
    observer.start()
    print(f"Monitoring folder: {folder_path}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

# Fetch PDF data from MongoDB
def fetch_pdf_data():
    return list(collection.find({}))

# Streamlit app function to display data
def run_streamlit_app():
    st.title("PDF Summary Viewer")
    st.markdown("This app displays the summaries and keywords generated from PDFs stored in MongoDB.")

    pdf_data = fetch_pdf_data()
    if pdf_data:
        for doc in pdf_data:
            st.subheader(f"File: {doc['file_name']}")
            st.write("**Summary:**")
            st.write(doc['summary'])
            st.write("**Keywords:**")
            st.write(", ".join([keyword[0] for keyword in doc['keywords']]))
            st.write("---")
    else:
        st.write("No data found in MongoDB.")

if __name__ == "__main__":
    # Define folder path for monitoring
    folder_path = r"C:\Users\harshit rana\OneDrive\Desktop\pdfdataset"

    # Start folder monitoring in a background thread
    Thread(target=monitor_folder, args=(folder_path,), daemon=True).start()

    # Run the Streamlit app
    run_streamlit_app()
