# AstroScan AI

AstroScan AI is an AI-powered app designed for NASA to provide structured recommendations for technical requirements. It leverages document embeddings, vector search, and a language model to analyze and suggest improvements based on NASA's technical bulletins and user-uploaded documents.

## Features
- Retrieve technical recommendations from NASA's Technical Bulletin Database
- Upload custom documents (PDFs) for analysis
- Uses Clarifai GPT-4 for language understanding
- Pinecone for vector storage and search
- Streamlit interface for easy interaction

## Installation
Ensure you have Python 3.8+ installed. Then, clone this repository and install dependencies:

```sh
pip install -r requirements.txt
```

## Setup
You need to set up API keys in Streamlit secrets:

1. Create a `.streamlit/secrets.toml` file.
2. Add the following:

```toml
[secrets]
ClarifaiToken = "your_clarifai_api_key"
pinecone_apikey = "your_pinecone_api_key"
pinecone_env = "your_pinecone_environment"
```

## Usage
Run the Streamlit app:

```sh
streamlit run app.py
```

## Troubleshooting
If you encounter an import error related to `langchain.vectorstores`, make sure you have installed `langchain-community`:

```sh
pip install langchain-community
```


