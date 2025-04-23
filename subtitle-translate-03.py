from langchain_openai import ChatOpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import getpass
import time

strsrtfilename = "Mass 2021 1080p.sample.srt"
output_filename = "Mass 2021 1080p.sample French.srt"

OPENAI_API_KEY = getpass.getpass('Enter your OPENAI_API_KEY')

llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model_name="gpt-4o-mini")

with open(strsrtfilename, 'r', encoding='utf-8') as file:
    srt_text = file.read()

text_splitter = CharacterTextSplitter(separator="\n\n", chunk_size=1000, chunk_overlap=0)
chunks = text_splitter.split_text(srt_text)

translate_chunk_prompt_template = """You are an experienced translator to French. 
Translate the following subtitle text to French and leave the first two lines (subtitle numbers and timestamps) unchanged.
Do not add any comment to the answer, only the translated text. 
Also remove the original English text in the result. 
Text: {chunk}"""
translate_chunk_prompt = PromptTemplate.from_template(translate_chunk_prompt_template)
translate_chunk_chain = translate_chunk_prompt | llm | StrOutputParser()

# Process chunks with a delay to respect rate limits
translations = []
batch_size = 50  # adjust batch_size if still facing rate issues

for i in range(0, len(chunks), batch_size):
    batch_chunks = chunks[i:i+batch_size]
    batch_translations = translate_chunk_chain.batch([{'chunk': c} for c in batch_chunks])
    translations.extend(batch_translations)
    print(f"Processed chunks {i+1} to {i+len(batch_chunks)}")
    time.sleep(60)  # Wait for 60 seconds between batches (adjust if necessary)

# Join translations
translation = '\n\n'.join(translations)

# Save translation to file
with open(output_filename, 'w', encoding='utf-8') as f:
    f.write(translation)

print(f"Translation saved to {output_filename}")
