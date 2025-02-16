# AstroScan AI

AstroScan AI is an AI-powered application designed to provide structured recommendations for NASA technical documents. It utilizes Retrieval-Augmented Generation (RAG) to analyze and answer queries based on NASA Technical Bulletins and uploaded documents.

## 🚀 Features
- **QnA about NASA Tech Bulletins**: Retrieve insights from NASA's technical documents.
- **Analyze NASA Documents**: Upload and process custom PDFs.
- **Advanced RAG Pipeline**:
  - Retrieves NASA Tech Bulletin PDFs.
  - Splits document content into manageable chunks.
  - Embeds documents using the `sentence-transformers/all-MiniLM-L6-v2` model.
  - Stores embeddings in Pinecone (online vector database) and ChromaDB.
  - Retrieves answers using a GPT-4-powered RetrievalQA chain (via Clarifai API).

## 🛠️ Installation & Setup
### Clone the Repository
```sh
 git clone https://github.com/your-repo/AstroScanAI.git
 cd AstroScanAI
```

### Install Dependencies
```sh
pip install -r requirements.txt
```

### Set Up API Keys
To run the app locally, create a `.streamlit/secrets.toml` file in the root directory and add the following:
```
[secrets]
ClarifaiToken = "your_clarifai_token"
pinecone_apikey = "your_pinecone_api_key"
pinecone_env = "your_pinecone_environment"
```

## 🔍 Usage
### Running the App
```sh
streamlit run app.py
```

### QnA about NASA Tech Bulletins
- Check out `RAG_Data-Collection.ipynb` for the data collection process.
- The process involves:
  - Retrieving all PDF links from NASA Tech Bulletins.
  - Downloading and splitting PDFs into chunks with appropriate time intervals.
  - Generating embeddings using a Hugging Face model.
  - Uploading embeddings with metadata to Pinecone.
  - Deploying a RetrievalQA chain with GPT-4 via the Clarifai API.

### Analyzing Custom NASA Documents
- Upload your PDF file via the app interface.
- The system:
  - Splits the document into chunks.
  - Generates embeddings.
  - Stores embeddings in ChromaDB.
  - Uses prompt engineering with RetrievalQA to analyze the document.

## 📌 Acknowledgments
- Built with **LangChain**, **Pinecone**, **ChromaDB**, **Clarifai GPT-4**, and **Streamlit**.
- Inspired by **NASA Space Apps Challenge**.


---
🚀 *Developed for NASA Space Apps 2024*
