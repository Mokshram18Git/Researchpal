from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
import textwrap
import os

def clean_text(text, width=80):
    """Clean and format text to be more readable"""
    text = ' '.join(text.split())
    return textwrap.fill(text, width=width)

def get_answer(question):
    """Get answer for question from vector database"""
    try:
        # Load embeddings and vector database
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vector_db = Chroma(persist_directory="./chromadb", embedding_function=embeddings)
        
        # Search for relevant documents
        relevant_docs = vector_db.similarity_search(question, k=3)
        
        if not relevant_docs:
            return "❌ No relevant information found in the document."
        
        # Build answer from relevant chunks
        answer = "Based on the research document:\n\n"
        source_pages = set()
        
        for i, doc in enumerate(relevant_docs):
            answer += f"**Section {i+1}:**\n"
            answer += clean_text(doc.page_content) + "\n\n"
            
            if hasattr(doc, 'metadata') and 'page' in doc.metadata:
                source_pages.add(doc.metadata['page'] + 1)
        
        if source_pages:
            answer += f"📚 **Source pages:** {', '.join(map(str, sorted(source_pages)))}"
        
        return answer
        
    except Exception as e:
        return f"❌ Error: {str(e)}"

def get_key_points():
    """Get key points from the document"""
    try:
        # Load embeddings and vector database
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vector_db = Chroma(persist_directory="./chromadb", embedding_function=embeddings)
        
        # Get some random chunks as key points
        relevant_docs = vector_db.similarity_search("key points summary", k=5)
        
        if not relevant_docs:
            return "❌ No content found in the document."
        
        # Build key points
        key_points = "🔑 **Key points from the document:**\n\n"
        source_pages = set()
        
        for i, doc in enumerate(relevant_docs):
            preview = doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content
            key_points += f"{i+1}. {clean_text(preview)}\n\n"
            
            if hasattr(doc, 'metadata') and 'page' in doc.metadata:
                source_pages.add(doc.metadata['page'] + 1)
        
        if source_pages:
            key_points += f"📚 **Source pages:** {', '.join(map(str, sorted(source_pages)))}"
        
        return key_points
        
    except Exception as e:
        return f"❌ Error: {str(e)}"

def start_query_interface():
    """Start the question-answering interface (for command line)"""
    print("Loading your knowledge database...")
    
    try:
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vector_db = Chroma(persist_directory="./chromadb", embedding_function=embeddings)
    except Exception as e:
        print(f"❌ Error loading database: {e}")
        print("Please process a PDF first using: python ingest.py")
        return
    
    print("✅ ResearchPal is ready! Ask me anything about your PDF!")
    print("Type 'exit' to quit\n")
    
    while True:
        question = input("🤔 Your question: ")
        
        if question.lower() == 'exit':
            print("👋 Goodbye!")
            break
        
        if question.strip() == "":
            continue
        
        print("🔍 Searching through your research...")
        
        try:
            answer = get_answer(question)
            print("\n" + "=" * 60)
            print("🎯 ANSWER:")
            print("=" * 60)
            print(answer)
            print("=" * 60 + "\n")
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    start_query_interface()