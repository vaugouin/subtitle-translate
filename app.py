import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import time
import os
import logging
import traceback
import sys
from datetime import datetime

# Logging configuration
logging_enabled = False  # Set to False to disable logging to files

# Set up logging
log_directory = "logs"
log_filename = None

if logging_enabled:
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)
    
    log_filename = os.path.join(log_directory, f"subtitle_translator_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    
    # Create file handler with immediate flushing
    file_handler = logging.FileHandler(log_filename, mode='w')
    file_handler.setLevel(logging.DEBUG)
    
    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

# Create console handler (always enabled)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# Get root logger and add handlers
root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)
if logging_enabled:
    root_logger.addHandler(file_handler)
root_logger.addHandler(console_handler)

# Create application logger
logger = logging.getLogger(__name__)
if logging_enabled:
    logger.info(f"Starting application. Logs will be saved to {log_filename}")
else:
    logger.info("Starting application. File logging is disabled.")
logger.info(f"Python version: {sys.version}")
logger.info(f"Current working directory: {os.getcwd()}")

st.set_page_config(page_title="Subtitle Translator", page_icon="🎬")
st.title("Subtitle Translator 🎬")

# Initialize session state for translations and errors
if 'translations' not in st.session_state:
    st.session_state.translations = []
    logger.info("Initialized empty translations in session state")
if 'errors' not in st.session_state:
    st.session_state.errors = []
    logger.info("Initialized empty errors in session state")

# Sidebar for API key
with st.sidebar:
    api_key = st.text_input("Enter OpenAI API Key", type="password")
    st.caption("Your API key is not stored and will be cleared when you refresh the page")
    
    # Add debug section in sidebar
    with st.expander("Debug Information"):
        if st.session_state.errors:
            st.write("Errors encountered:")
            for i, error in enumerate(st.session_state.errors):
                st.error(f"Error {i+1}: {error}")
        else:
            st.write("No errors encountered yet.")
        
        # Add log file information
        if logging_enabled and log_filename:
            st.write(f"Log file: {log_filename}")
            if os.path.exists(log_filename):
                if st.button("View Recent Logs"):
                    with open(log_filename, "r") as f:
                        log_content = f.readlines()
                        # Show last 20 lines of log
                        st.code("".join(log_content[-20:]), language="text")
                
                if st.button("Open Log File Location"):
                    try:
                        log_dir_abs = os.path.abspath(log_directory)
                        os.startfile(log_dir_abs)
                        st.success(f"Opened log directory: {log_dir_abs}")
                    except Exception as e:
                        st.error(f"Could not open log directory: {str(e)}")
        else:
            st.write("File logging is disabled.")

# Main interface
uploaded_file = st.file_uploader("Upload your SRT file", type=['srt'])
target_language = st.selectbox(
    "Select target language",
    ["French", "English", "Spanish", "German", "Italian", "Portuguese", "Polish", "Japanese", "Chinese", "Korean"]
)

# Add a translate button
translate_button = st.button("Translate")

if translate_button:
    logger.info(f"Translate button clicked. File uploaded: {uploaded_file is not None}, API key provided: {api_key != ''}")

if uploaded_file and api_key and translate_button:
    try:
        # Check file size
        file_size = len(uploaded_file.getvalue())
        logger.info(f"File size: {file_size} bytes")
        if file_size > 10 * 1024 * 1024:  # 10MB limit
            st.warning(f"File is very large ({file_size/1024/1024:.2f} MB). Processing may take longer.")
            
        logger.info(f"Starting translation process for file: {uploaded_file.name} to {target_language}")
        
        # Initialize OpenAI
        llm = ChatOpenAI(openai_api_key=api_key, model_name="gpt-4-turbo")
        logger.info("Initialized OpenAI LLM with model: gpt-4-turbo")
        
        # Read file content
        try:
            srt_text = uploaded_file.getvalue().decode('utf-8')
            logger.info(f"Read SRT file content, size: {len(srt_text)} characters")
            logger.info(f"First 100 characters: {srt_text[:100]}")
            logger.info(f"Last 100 characters: {srt_text[-100:] if len(srt_text) > 100 else srt_text}")
        except UnicodeDecodeError:
            # Try different encodings if UTF-8 fails
            try:
                srt_text = uploaded_file.getvalue().decode('cp1251')  # Cyrillic encoding
                logger.info(f"Successfully decoded with cp1251 encoding, size: {len(srt_text)} characters")
            except UnicodeDecodeError:
                try:
                    srt_text = uploaded_file.getvalue().decode('iso-8859-5')  # Another Cyrillic encoding
                    logger.info(f"Successfully decoded with iso-8859-5 encoding, size: {len(srt_text)} characters")
                except UnicodeDecodeError:
                    try:
                        srt_text = uploaded_file.getvalue().decode('utf-16')
                        logger.info(f"Successfully decoded with utf-16 encoding, size: {len(srt_text)} characters")
                    except UnicodeDecodeError:
                        error_msg = "Failed to decode subtitle file with multiple encodings. The file may be corrupted."
                        logger.error(error_msg)
                        st.error(error_msg)
                        raise
        
        # Text splitting
        text_splitter = CharacterTextSplitter(separator="\n\n", chunk_size=20, chunk_overlap=0)
        try:
            chunks = text_splitter.split_text(srt_text)
            logger.info(f"Split text into {len(chunks)} chunks with chunk_size=20")
            
            # Log some sample chunks for debugging
            if len(chunks) > 0:
                logger.info(f"First chunk: {chunks[0]}")
            if len(chunks) > 1:
                logger.info(f"Second chunk: {chunks[1]}")
            if len(chunks) > 2:
                logger.info(f"Third chunk: {chunks[2]}")
            if len(chunks) > 10:
                logger.info(f"10th chunk: {chunks[9]}")
            if len(chunks) > 100:
                logger.info(f"100th chunk: {chunks[99]}")
            if len(chunks) > 0:
                logger.info(f"Last chunk: {chunks[-1]}")
                
            # Check for empty chunks which might cause issues
            empty_chunks = [i for i, chunk in enumerate(chunks) if not chunk.strip()]
            if empty_chunks:
                logger.warning(f"Found {len(empty_chunks)} empty chunks at indices: {empty_chunks[:10]}...")
                
            # Check for very large chunks which might cause API issues
            large_chunks = [i for i, chunk in enumerate(chunks) if len(chunk) > 1000]
            if large_chunks:
                logger.warning(f"Found {len(large_chunks)} unusually large chunks (>1000 chars) at indices: {large_chunks[:10]}...")
                
        except Exception as e:
            error_msg = f"Error during text splitting: {str(e)}"
            logger.error(error_msg)
            st.error(error_msg)
            raise
        
        # Progress tracking
        progress_text = "Translation in progress..."
        progress_bar = st.progress(0)
        status_text = st.empty()
        error_placeholder = st.empty()
        
        # Prompt template
        translate_chunk_prompt_template = """You are an experienced translator to {target_language}. 
        Translate the following subtitle text to {target_language}.
        Do not add any comment to the answer, only the translated text. 
        Text: {chunk}"""
        translate_chunk_prompt = PromptTemplate.from_template(translate_chunk_prompt_template)
        translate_chunk_chain = translate_chunk_prompt | llm | StrOutputParser()
        logger.info("Created translation chain with prompt template")
        
        # Process chunks with progress tracking
        translations = []
        batch_size = 50
        logger.info(f"Starting translation with batch_size={batch_size}")
        
        for i in range(0, len(chunks), batch_size):
            batch_chunks = chunks[i:i+batch_size]
            logger.info(f"Processing batch {i//batch_size + 1}/{(len(chunks) + batch_size - 1)//batch_size} with {len(batch_chunks)} chunks")
            
            # Process each chunk to separate metadata (first two lines) from content
            processed_chunks = []
            metadata_lines = []
            
            for chunk in batch_chunks:
                lines = chunk.split('\n')
                # Store the first two lines (subtitle number and timestamp)
                if len(lines) >= 2:
                    metadata = '\n'.join(lines[:2])
                    content = '\n'.join(lines[2:])
                    processed_chunks.append(content)
                    metadata_lines.append(metadata)
                else:
                    # Handle case where chunk has fewer than 2 lines
                    processed_chunks.append(chunk)
                    metadata_lines.append("")
            
            logger.info(f"Separated metadata from content for {len(processed_chunks)} chunks")
            
            # Translate only the content parts with error handling for each chunk
            batch_translations = []
            try:
                logger.info(f"Processing batch {i//batch_size + 1} of {(len(chunks) + batch_size - 1)//batch_size}")
                logger.info(f"Batch contains {len(processed_chunks)} chunks")
                
                # Process each chunk individually to isolate errors
                for idx, chunk in enumerate(processed_chunks):
                    chunk_num = i + idx + 1
                    logger.info(f"Starting translation of chunk {chunk_num} of {len(chunks)}")
                    logger.info(f"Chunk {chunk_num} content preview: {chunk[:50]}...")
                    
                    try:
                        translation = translate_chunk_chain.invoke({
                            'chunk': chunk,
                            'target_language': target_language
                        })
                        batch_translations.append(translation)
                        logger.info(f"Successfully translated chunk {chunk_num}")
                        logger.info(f"Translation preview: {translation[:50]}...")
                        
                        # Force log flush after each translation
                        for handler in logger.handlers:
                            handler.flush()
                            
                    except Exception as chunk_error:
                        error_msg = f"Error translating chunk {chunk_num}: {str(chunk_error)}"
                        logger.error(error_msg)
                        st.session_state.errors.append(error_msg)
                        # Use original text if translation fails
                        batch_translations.append(chunk)
                        # Show error in UI but continue processing
                        error_placeholder.error(f"Error on chunk {chunk_num}: {str(chunk_error)}")
                        
                        # Force log flush after error
                        for handler in logger.handlers:
                            handler.flush()
                            
            except Exception as batch_error:
                error_msg = f"Error processing batch starting at chunk {i+1}: {str(batch_error)}"
                logger.error(error_msg)
                st.session_state.errors.append(error_msg)
                error_placeholder.error(error_msg)
                
                # Force log flush after batch error
                for handler in logger.handlers:
                    handler.flush()
            
            # Recombine metadata with translated content
            final_translations = []
            for j, translation in enumerate(batch_translations):
                if metadata_lines[j]:
                    final_translations.append(f"{metadata_lines[j]}\n{translation}")
                else:
                    final_translations.append(translation)
            
            translations.extend(final_translations)
            logger.info(f"Added {len(final_translations)} translated chunks to results")
            
            # Update progress
            progress = (i + len(batch_chunks)) / len(chunks)
            progress_bar.progress(progress)
            status_text.text(f"Processed chunks {i+1} to {i+len(batch_chunks)} of {len(chunks)}")
            logger.info(f"Progress: {progress*100:.1f}% complete")
            
            if i + batch_size < len(chunks):
                logger.info(f"Rate limiting: sleeping for 2 seconds before next batch")
                time.sleep(2)  # Rate limiting
        
        st.session_state.translations = translations
        logger.info(f"Completed all translations. Total chunks translated: {len(translations)}")
        
        # Join translations
        translation = '\n\n'.join(st.session_state.translations)
        translation += '\n\n'
        logger.info(f"Joined all translations. Final output size: {len(translation)} characters")
        
        # Download button
        output_filename = f"{uploaded_file.name.rsplit('.', 1)[0]}.{target_language}.srt"
        logger.info(f"Creating download button for file: {output_filename}")
        st.download_button(
            label="Download translated subtitles",
            data=translation,
            file_name=output_filename,
            mime="text/plain"
        )
        
        # Clear progress indicators
        progress_bar.empty()
        status_text.empty()
        logger.info("Cleared progress indicators")
        
        # Show summary of errors if any occurred
        if st.session_state.errors:
            logger.warning(f"Translation completed with {len(st.session_state.errors)} errors")
            st.warning(f"Translation completed with {len(st.session_state.errors)} errors. See debug section in sidebar for details.")
        else:
            logger.info("Translation completed successfully with no errors")
        
    except Exception as e:
        error_msg = f"A critical error occurred: {str(e)}\n{traceback.format_exc()}"
        logger.error(error_msg)
        st.session_state.errors.append(error_msg)
        st.error(error_msg)
else:
    if not api_key and translate_button:
        logger.warning("Translation attempted without API key")
        st.warning("Please enter your OpenAI API key in the sidebar.")
    if not uploaded_file and translate_button:
        logger.warning("Translation attempted without uploaded file")
        st.info("Please upload an SRT file to translate.")
    if not translate_button and uploaded_file and api_key:
        logger.info("File and API key provided, waiting for translate button click")
        st.info("Click the 'Translate' button to start the translation process.")
