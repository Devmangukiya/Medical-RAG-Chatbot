import os
from langchain_community.document_loaders import DirectoryLoader,PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from app.common.logger import get_logger
from app.common.custom_exception import CustomException

from app.config.config import DATA_PATH, CHUNK_OVERLAP, CHUNK_SIZE\
    
logger = get_logger(__name__)

def load_pdf_files():
    try:
        if not os.path.exists(DATA_PATH):
            raise CustomException("Data Path Does not Found...")
        
        logger.info("Loading files from {DATA_PATH}")

        loader = DirectoryLoader(DATA_PATH,glob="*.pdf",loader_cls=PyPDFLoader)

        documents = loader.load()

        if not documents:
            logger.info("No PDF are found..")
        else: 
            logger.info(f"Sucessfully fetched {len(documents)} documents")

        return documents
    
    except Exception as e:
        error_message = CustomException("Failed to load PDF",e)
        logger.error(str(error_message))
        return []
    
def create_text_chunks(documents):
    try:
        if not documents:
            raise CustomException("No Documents are found...")
        
        logger.info(f"Splitting {len(documents)} documents into chunks...")

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE,chunk_overlap = CHUNK_OVERLAP)
        text_chunks = text_splitter.split_documents(documents)

        logger.info(f"Generated {len(text_chunks)} text chunks")

        return text_chunks
    
    except Exception as e:
        error_message = CustomException("Failed to generate chunks",e)
        logger.error(str(error_message))
        return []