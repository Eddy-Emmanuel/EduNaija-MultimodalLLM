import os
from langchain_core.tools import Tool
from app.agents.prompts import rag_prompt
from langchain_classic.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from app.configurations.accesskeys import accesskeys_config
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders.parsers import LLMImageBlobParser

os.environ["OPENAI_API_KEY"] = accesskeys_config.OPENAI_API_KEY

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
llm = ChatOpenAI(model="gpt-5") 

# Global variable to store PDF path 
current_pdf_path = None

def set_pdf_path(path):
    """Call this from streamlit_app.py when PDF is uploaded"""
    global current_pdf_path
    current_pdf_path = path
    print(f"PDF path set to: {path}")

def CreateRetrieverQA(temp_path):
    loader = PyMuPDFLoader(
                file_path=temp_path,
                mode="page",
                images_inner_format="markdown-img",
                images_parser=LLMImageBlobParser(model=ChatOpenAI(model="gpt-4o", max_tokens=1024)),
            )

    docs = loader.load()
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )
    splits = splitter.split_documents(docs)

    vectordb = FAISS.from_documents(splits, embeddings)
    retriever = vectordb.as_retriever(search_kwargs={"k": 4})

    return RetrievalQA.from_chain_type(
                                        llm=llm,
                                        retriever=retriever,
                                        chain_type="stuff",
                                        chain_type_kwargs={"prompt": rag_prompt},  
                                        return_source_documents=True
                                    )
    
def rag_tool_func(query):
    global current_pdf_path
    if current_pdf_path:
        rag_chain = CreateRetrieverQA(current_pdf_path)
        result = rag_chain.invoke({"query": query})
        return result["result"]
    else:
        return "No PDF uploaded. Please upload a document first."
  
rag_tool = Tool(
    name="rag_search",
    description="Search and answer questions based on uploaded PDF documents",
    func=rag_tool_func,
)
