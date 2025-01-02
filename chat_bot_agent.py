from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings, StorageContext, load_index_from_storage
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.storage.chat_store.redis import RedisChatStore
import os 



Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")
Settings.llm = OpenAI(model="gpt-4o-mini",api_key="", request_timeout=360.0)


memory_dict = {}

chat_store = RedisChatStore(redis_url="redis://localhost:6379", ttl=300, password="myredissecret")


def chatting_agent(query,browserDetails,userId):
    
    # if userId not in memory_dict:
    #     memory_dict[userId] = ChatMemoryBuffer.from_defaults(token_limit=15000)
    memory = ChatMemoryBuffer.from_defaults(token_limit=15000,chat_store=chat_store,chat_store_key=userId)
    
    # memory = memory_dict[userId]
    # print(memory.get())

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
    res1 = chat_engine.chat(query)
    
    
    
    return res1


# response = chatting_agent("My mic is not working what should i do?")
# print(response)   