from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings, StorageContext, load_index_from_storage
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.memory import ChatMemoryBuffer,chat_memory_buffer
# from llama_index.storage.chat_store.redis import RedisChatStore
from image_describe import describe_image
from context import chat_desc_msg
import os 
import json


Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")
Settings.llm = OpenAI(model="gpt-4o-mini",api_key="", request_timeout=360.0)


memory_dict = {}

# chat_store = RedisChatStore(redis_url="redis://localhost:6379", ttl=300, password="myredissecret")


def chatting_agent(query,browserDetails,userId,memory,screen):
    
    # if userId not in memory_dict:
    #     memory_dict[userId] = ChatMemoryBuffer.from_defaults(token_limit=15000,chat_store_key=userId)
    
    if not memory:
        print('In')
        memory = ChatMemoryBuffer.from_defaults(token_limit=15000,chat_store_key=userId)
    else:
        memory = ChatMemoryBuffer.from_dict(memory)
    print(memory)
    
    img_desc = ''
    if screen is not None:
        img_desc = "Iam giving you a breif description on my screen just consider only issues that you know and visible. And dont consider unwanted description. "
        img_desc += describe_image(screen,chat_desc_msg)
        

    PERSIST_DIR = "./chat_bot_storage"
    if not os.path.exists(PERSIST_DIR):
        documents = SimpleDirectoryReader("chat_bot_kb").load_data()
        index = VectorStoreIndex.from_documents(documents)
        index.storage_context.persist(persist_dir=PERSIST_DIR)
    else:
        storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
        index = load_index_from_storage(storage_context)
    query_input = "My Browser Details are {} {} {}".format(
    browserDetails["browserName"],
    browserDetails["browserVersion"], 
    # browserDetails["platform"],  
    browserDetails["os"]) 
    chat_engine = index.as_chat_engine(
        chat_mode="context",
        memory=memory,
        system_prompt=(
            "You are a chatbot, able to have normal interactions, as well as talk"
            " issues while taking exam. "
            "Broswer and system details are {} use these for answering issues based on browser and system".format(query_input)
        ),
    )
    res1 = chat_engine.chat(query+img_desc)
    
    serial_mem = memory.to_string()
    
    
    
    return (res1,serial_mem)


# response = chatting_agent("My mic is not working what should i do?")
# print(response)   