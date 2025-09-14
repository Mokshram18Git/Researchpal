from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
import os

def process_pdf(pdf_path=None):
    """Process the PDF and create vector database"""
    if not pdf_path:
        pdf_path = input("Enter the path to your PDF file: ").strip()
    
    if not os.path.exists(pdf_path):
        print(f"❌ Error: File {pdf_path} does not exist.")
        return None

    print(f"📄 Processing: {os.path.basename(pdf_path)}")
    
    # Load PDF
    loader = PyPDFLoader(pdf_path)
    print("Loading PDF content...")
    documents = loader.load()
    print(f"✅ Loaded {len(documents)} pages.")

    # Split text
    print("Splitting text into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"✅ Created {len(chunks)} text chunks.")

    # Create embeddings
    print("Creating embeddings...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # Store in ChromaDB
    print("Building knowledge database...")
    
    # Clear existing database if it exists
    if os.path.exists("./chromadb"):
        import shutil
        shutil.rmtree("./chromadb")
    
    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="./chromadb"
    )

    print("✅ PDF successfully processed and knowledge database created!")
    return vector_db

if __name__ == "__main__":
    process_pdf()