from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings, StorageContext, load_index_from_storage
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.agent.openai import OpenAIAgent
from image_describe import describe_image 
from context import pre_context, img_desc_msg, camera_engine_desc
from validating_agent import validation_agent
import os 




Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")
Settings.llm = OpenAI(model="gpt-4o-mini",api_key="", request_timeout=360.0, pre_context=pre_context)


PERSIST_DIR = "./camera_storage"
if not os.path.exists(PERSIST_DIR):
    documents = SimpleDirectoryReader("data").load_data()
    index = VectorStoreIndex.from_documents(documents)
    index.storage_context.persist(persist_dir=PERSIST_DIR)
else:
    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    index = load_index_from_storage(storage_context)


def camera_image_analyzing_agent(img_url):
    response_content = describe_image(img_url,img_desc_msg)
    query_engine = index.as_query_engine()
    # response = query_engine.query(response_content)
    query_engine_tools = [
        QueryEngineTool(
            query_engine,
            metadata=ToolMetadata(
                name="image_analyze_engine",
                description=(
                   camera_engine_desc
                ),
            ),
        )
    ]
    agent = OpenAIAgent.from_tools(query_engine_tools, verbose=False)
    res1 = agent.chat(response_content+"Provide only JSON Output")
    # print(res1)
    # print(res1)
    
    # val_res = validation_agent(res1.response, response_content)
    
    # res2 = validation_agent(response_content,res1)
    # print(res2)
    
    return res1


# response = camera_image_analyzing_agent("https://images.pexels.com/photos/7092454/pexels-photo-7092454.jpeg?auto=compress&cs=tinysrgb&w=600")
# print(response)