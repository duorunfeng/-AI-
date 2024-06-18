# text_processor.py

import re
import warnings
from queue import Queue
from transformers import AutoTokenizer
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.vectorstores.utils import DistanceStrategy
from sentence_transformers import CrossEncoder
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate

warnings.simplefilter(action='ignore', category=FutureWarning)  # Ignore FutureWarnings for cleaner output

class Document:
    def __init__(self, page_content, metadata=None):
        self.page_content = page_content
        self.metadata = metadata or {}

def process_txt_files(txt_paths):
    pages_text = []
    for txt_path in txt_paths:
        with open(txt_path, 'r', encoding='utf-8') as file:
            page_text = file.read()
            if page_text:
                pages_text.append(Document(page_text))
    return pages_text

def get_all_queue_element(queue):
    result_str = ""
    while not queue.empty():
        result_str += queue.get() + "\n"
    return result_str

def remove_name_and_colon(text):
    return re.sub(r'^[A-Z][a-z]*\s*:\s*', '', text).strip()

def process_input(input_text):
    txt_paths = [r'Z:\PyCharmFire\webui\RAG\formatted_dialogues.txt']
    pages_text = process_txt_files(txt_paths)

    tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L12-v2")
    text_splitter = RecursiveCharacterTextSplitter.from_huggingface_tokenizer(
        tokenizer=tokenizer,
        chunk_size=256,
        chunk_overlap=16,
        strip_whitespace=True
    )
    chunks = text_splitter.split_documents(pages_text)

    bi_encoder = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L12-v2", model_kwargs={"device": "cuda"})
    faiss_db = FAISS.from_documents(chunks, bi_encoder, distance_strategy=DistanceStrategy.DOT_PRODUCT)

    cross_encoder = CrossEncoder("cross-encoder/ms-marco-TinyBERT-L-2-v2", max_length=768, device="cuda")

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "{system_prompt}"),
        ("human", "{input}")
    ])

    llm = Ollama(model="llama3", temperature=0.0)
    chat_history = []
    chat_queue = Queue(maxsize=4)

    user_prompt = get_all_queue_element(chat_queue) + input_text
    retrieved_chunks = faiss_db.similarity_search(user_prompt, k=5)
    reranked_chunks = cross_encoder.rank(
        user_prompt,
        [doc.page_content for doc in retrieved_chunks],
        top_k=1,  # Focus on the top document
        return_documents=True
    )

    context = reranked_chunks[0]["text"]  # Assume the most relevant context is selected
    lines = context.split('\n')
    answer_line = None
    found_vocabulary = False  # Flag to detect "Vocabulary" keyword

    for i, line in enumerate(lines):
        if "Vocabulary" in line:
            found_vocabulary = True
            break
        if input_text in line:  # Identify the line containing the question
            if i + 1 < len(lines):
                answer_line = lines[i + 1]  # Get the next line as the response
                break

    if found_vocabulary:
        answer_line = "The discussion on the current topic is complete. Let's start a new scenario dialogue. What scenario would you like to talk about?"

    if not answer_line:
        # Generate response if no direct answer is found
        generated_response = prompt_template | llm.invoke({
            "input": input_text,
            "chat_history": chat_history,
            "system_prompt": "You are an AI designed to help understand and respond using the conversation context.",
            "context": context
        })

        # Check the type of generated response
        if isinstance(generated_response, str):
            answer_line = generated_response
        else:
            answer_line = generated_response.get("content", "Sorry, I couldn't find a relevant response.")

    # Remove human names and colons from the response
    answer_line = remove_name_and_colon(answer_line)
    return answer_line
