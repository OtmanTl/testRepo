import streamlit as st
from llama_index.core import VectorStoreIndex, Settings
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core.chat_engine.types import ChatMode
from llama_index.llms.groq import Groq
from llama_index.embeddings.fastembed import FastEmbedEmbedding
from qdrant_client import QdrantClient
import logging
from PIL import Image

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize models
Settings.llm = Groq(model="llama3-70b-8192", api_key="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")
Settings.embed_model = FastEmbedEmbedding(model_name="jinaai/jina-embeddings-v2-base-en")

class ChatbotInterface:
    def __init__(self):
        self.collection_name = "user_collection"
        self.client = QdrantClient(url="http://72.144.113.188:6333/")
        self.initialize_chat_engine()

    def initialize_chat_engine(self):
        """Initialize the chat engine with the existing Qdrant collection"""
        try:
            vector_store = QdrantVectorStore(
                collection_name=self.collection_name,
                client=self.client,
                enable_hybrid=True,
            )
            index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
            return index.as_chat_engine(
                chat_mode=ChatMode.CONTEXT,
                verbose=True,
                streaming=True
            )
        except Exception as e:
            logger.error(f"Error initializing chat engine: {e}")
            raise

def main():
    #st.title("Policy Chatbot")
    # Initialize Streamlit interface
    st.set_page_config(page_title="Advanced Document Processing with LlamaIndex", page_icon="📚")
    # Logo and Navigation
    col1, col2, col3 = st.columns((1, 4, 1))
    with col2:
        logo = Image.open("hci_white_logo.png")
        st.image(logo)
        #st.image(Image.open("rub_logo.png"),width=200)
    st.title("AAdvanced Document Processing with LlamaIndex 📚")

    #st.markdown(("# 30 Days of Streamlit"))
    
    # Initialize session state for messages if it doesn't exist
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Initialize session state for chat engine if it doesn't exist
    if "chat_engine" not in st.session_state:
        try:
            chatbot = ChatbotInterface()
            st.session_state.chat_engine = chatbot.initialize_chat_engine()
        except Exception as e:
            st.error(f"Error connecting to the database: {str(e)}")
            return

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Chat input and response handling
    if prompt := st.chat_input("Ask about the policy document"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        with st.chat_message("assistant"):
            try:
                response_stream = st.session_state.chat_engine.stream_chat(prompt)
                response = "".join(chunk for chunk in response_stream.response_gen)
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.write(response)
            except Exception as e:
                st.error(f"Error generating response: {str(e)}")

if __name__ == "__main__":
    main()