import streamlit as st
import tempfile

__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import pinecone
from langchain_community.vectorstores import Pinecone, Chroma
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain.llms import Clarifai
from langchain.chains import RetrievalQA

st.set_page_config('AstroScan AI', ':star:')

@st.cache_resource
def load_models(clarifai_token, pinecone_apikey, pinecone_env):
    embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

    try:
        llm = Clarifai(pat=clarifai_token, user_id='openai', 
                       app_id='chat-completion', model_id='GPT-4')
    except Exception as e:
        st.error(f"Error initializing Clarifai: {e}")
        return None, None, None

    try:
        pinecone.init(api_key=pinecone_apikey, environment=pinecone_env)
        index = pinecone.Index('nasa-rag')
        vectorstore = Pinecone(index, embedding_function, 'text')
    except Exception as e:
        st.error(f"Error initializing Pinecone: {e}")
        return None, None, None

    return embedding_function, llm, vectorstore

template = '''
You are Astro, an AI-powered app designed for NASA. Your goal is to
provide structured recommendations for technical requirements.
 The recommendations should include:
 - Section number and version letter of the document under review.
 - Current language from that section.
 - Identified issues.
 - Suggested modifications.
 - Sources of each recommendation.

Use the following pieces of context to answer the question in the structured format. 
{context}
If you don't know the answer, just say that you don't know, don't try to make up an answer.
Question: {question}
Answer in English
'''

prompt = PromptTemplate(
    template=template, input_variables=['context', 'question']
)

st.title('NASA Space Apps: :star: AstroScan AI')
st.write('Receive technical recommendations about NASA Documents.')

# Get API keys from user input
st.sidebar.header("Enter API Keys")
clarifai_token = st.sidebar.text_input("Clarifai Token", type="password")
pinecone_apikey = st.sidebar.text_input("Pinecone API Key", type="password")
pinecone_env = st.sidebar.text_input("Pinecone Environment")

if not clarifai_token or not pinecone_apikey or not pinecone_env:
    st.warning("Please enter all API keys in the sidebar.")
else:
    embedding_function, llm, pinecone_vectors = load_models(clarifai_token, pinecone_apikey, pinecone_env)

    if llm and pinecone_vectors:
        media = st.radio('What data you want to use?', ['NASA Technical Bulletin Database', 'Upload custom Document'])
        query = st.text_input('Query:')
        generate = st.button('Generate Response')

        if media == 'NASA Technical Bulletin Database':
            st.info('The Agent will strictly provide information from [NASA Technical Bulletins](https://www.nasa.gov/nesc/knowledge-products/nesc-technical-bulletins/)')

            if generate and query:
                rag_chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", 
                            retriever=pinecone_vectors.as_retriever(), 
                            chain_type_kwargs={"prompt": prompt})

                with st.spinner('Generating recommendations..'):
                    answer = rag_chain.run(query)
                    result = pinecone_vectors.similarity_search_with_score(query, k=1)

                st.write(answer)
                if result and result[0][1] > 0.5:
                    st.write(f'Source: {result[0][0].metadata["source"]}')

        else:
            st.info('Some documents may not be present in our database. Please upload them here.')
            pdf_file = st.file_uploader('', type=['pdf'])

            if pdf_file and generate and query:
                tfile = tempfile.NamedTemporaryFile(delete=False) 
                tfile.write(pdf_file.read())

                pdf_loader = PyPDFLoader(tfile.name)
                pdf_data = pdf_loader.load()

                text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
                docs = text_splitter.split_documents(pdf_data)
                
                pdf_vectors = Chroma.from_documents(documents=docs, embedding=embedding_function)

                rag_chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", 
                                    retriever=pdf_vectors.as_retriever(), 
                                    chain_type_kwargs={"prompt": prompt})

                with st.spinner('Generating recommendations..'):
                    report = rag_chain.run(query)
                st.write(report)
