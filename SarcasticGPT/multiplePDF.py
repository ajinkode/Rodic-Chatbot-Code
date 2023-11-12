import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
# from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template
from langchain.llms import HuggingFaceHub
import os

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()
    # embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore


def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()
    # llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.5, "max_length":512})

    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain


def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)


def main():
    
    
    st.set_page_config(page_title="Chat with multiple PDFs",
                       page_icon=":books:")
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Chat with multiple PDFs :books:")
    
    st.markdown("Get your OpenAI API Key [here](https://platform.openai.com/account/api-keys) ")
    tempkey = st.text_input(":orange[Please enter your OpenAI API Key to start chatting]", type='password', placeholder='sk-xxxxx')
    
    if tempkey is not None:
        
        apikey = tempkey
    
        os.environ['OPENAI_API_KEY']=apikey
        
        if apikey:
            st.success("Successfully uploaded the key! Now please go ahead and upload your PDF.", icon="✅")
    
    
    
    pdf_docs = st.file_uploader(
            "Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
    if st.button("Process"):
        with st.spinner("Processing the PDF, please wait..."):
            # get pdf text
            raw_text = get_pdf_text(pdf_docs)

            # get the text chunks
            text_chunks = get_text_chunks(raw_text)

            # create vector store
            vectorstore = get_vectorstore(text_chunks)

            # create conversation chain
            st.session_state.conversation = get_conversation_chain(
                    vectorstore)
                
            st.success("PDF processed successfully. If you wish, you can add more PDFs, or you can ask questions from the existing PDFs.", icon="✅")
            
            
    
    user_question = st.text_input("Ask a question about your documents:")
    
    with st.spinner("Generating response, please wait..."):
        if user_question:
            handle_userinput(user_question)
            st.balloons()

    with st.sidebar:
        st.header("PDF Wizard 🤖💬")
        st.subheader("Effortlessly upload your PDFs and ask any questions related to the PDF.")
        
        st.subheader("How to use?")
        st.markdown('''
                    - Paste your OpenAI API Key. If you don't have one, generate it here https://platform.openai.com/account/api-keys.
                    - Upload your desired PDF.
                    - Ask questions related to the PDF!
                    ''')
        
        
        
    st.markdown("Made with ❤️ by [Ajinkya Kale](https://www.linkedin.com/in/ajinkode/) ", unsafe_allow_html=True)


if __name__ == '__main__':
    main()
