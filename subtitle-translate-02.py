strsrtfilename = "Mass 2021 1080p sample.srt"

from langchain_openai import ChatOpenAI
#from langchain_text_splitters import TokenTextSplitter
from langchain.text_splitter import CharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnableParallel
import getpass

with open(strsrtfilename, 'r', encoding='utf-8') as file:
    srt_text = file.read()

OPENAI_API_KEY = getpass.getpass('Enter your OPENAI_API_KEY')

llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY,model_name="gpt-4o-mini")

# Split
text_chunks_chain = (
    RunnableLambda(lambda x: 
        [
            {
                'chunk': text_chunk, 
            }
            for text_chunk in 
               CharacterTextSplitter(separator="\n\n", chunk_size=20, chunk_overlap=0, length_function=len, is_separator_regex=False).split_text(x)
        ]
    )
)

# Map
translate_chunk_prompt_template = """You are an experienced translater to French. 
Translate the following subtitle text to French and leave the two first lines unchanged
Text: {chunk}"""
translate_chunk_prompt = PromptTemplate.from_template(translate_chunk_prompt_template)
translate_chunk_chain = translate_chunk_prompt | llm

translate_map_chain = (
    RunnableParallel (
        {
            'translation': translate_chunk_chain | StrOutputParser()        
        }
    )
)

# Reduce
translate_reduce_chain = (
    RunnableLambda(lambda x: '\n\n'.join([i['translation'] for i in x]))
)

map_reduce_chain = (
   text_chunks_chain
   | translate_map_chain.map()
   | translate_reduce_chain
)

translation = map_reduce_chain.invoke(srt_text)

