📖 Overview
ResearchPal is an intelligent document analysis platform that transforms static PDF documents into interactive knowledge bases. Using advanced natural language processing and semantic search technologies, ResearchPal enables users to instantly extract insights, answer complex questions, and identify key information within research papers and documents.

✨ Features
🔍 Intelligent Document Processing
PDF Text Extraction: Advanced parsing of research papers and academic documents
Semantic Chunking: Context-aware text segmentation preserving document structure
Vector Embeddings: Transform text into numerical representations for intelligent search

💬 Interactive Query System
Natural Language Questions: Ask questions in plain English about your documents
Semantic Search: Find conceptually related content, not just keyword matches
Source Referencing: Track answers back to original document pages

🎨 Professional Web Interface
Modern UI/UX: Clean, responsive design optimized for research workflows
Drag & Drop Upload: Intuitive document management system
Real-time Processing: Instant feedback and status updates

🔒 Privacy-Focused Architecture
Local Processing: All analysis occurs on your hardware
No Cloud Dependencies: Complete offline functionality
Data Sovereignty: Your documents never leave your environment

🛠️ Technical Architecture
Core Technologies:
Python → Flask → LangChain → ChromaDB → Sentence Transformers

Component Breakdown:
Web Layer: Flask-based RESTful API with Jinja templating
Processing Engine: LangChain document pipelines with custom chunking strategies
Vector Storage: ChromaDB for high-performance similarity search
Embedding Model: Sentence Transformers for semantic understanding


📦 Installation
Prerequisites
Python 3.8 or higher
pip package manager

Quick Setup

# Clone the repository
git clone <https://github.com/Mokshram18Git/Researchpal>
cd researchpal

# Install dependencies
pip install -r requirements.txt

# Launch application
python app.py

required libraries:
flask==2.3.3          # Web framework
langchain==0.0.346    # AI chain orchestration
chromadb==0.4.15      # Vector database management
sentence-transformers==2.2.2  # Text embedding generation
pypdf==3.17.1         # PDF text extraction
werkzeug==2.3.7       # WSGI utilities

Auto-generated:
chromadb/ - Stores document embeddings (created automatically)
uploads/ - Temporary PDF storage (created automatically)

💡 How It Works
Upload PDF: Drag and drop your research paper
Processing: System extracts text and creates AI embeddings
Query: Ask questions in natural language
Results: Get precise answers with source page references
