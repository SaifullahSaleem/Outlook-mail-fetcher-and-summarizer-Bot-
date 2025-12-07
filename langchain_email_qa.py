from langchain.chains import RetrievalQA
from langchain.memory import ConversationBufferMemory
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.docstore.document import Document

def create_langchain_pipeline(emails):
    # Converting emails to LangChain Documents
    docs = [Document(page_content=f"{e['subject']} {e['body']}", metadata=e) for e in emails]

    # Splitting large texts
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(docs)

    # Creating the embeddings & vectorstore
    embeddings = OpenAIEmbeddings()
    vectordb = Chroma.from_documents(chunks, embedding=embeddings, persist_directory="./chroma_db")

    # Initializing LLM and RetrievalQA
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    retriever = vectordb.as_retriever()
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, chain_type="stuff")

    return qa_chain
