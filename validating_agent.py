from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings, StorageContext, load_index_from_storage
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.agent.openai import OpenAIAgent
# from image_describe import describe_image 
from context import pre_context, validating_engine_desc
import os


Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")
Settings.llm = OpenAI(model="gpt-4o-mini",api_key="", request_timeout=360.0, pre_context=pre_context)


PERSIST_DIR = "./audit_storage"
if not os.path.exists(PERSIST_DIR):
    documents = SimpleDirectoryReader("audit_kb").load_data()
    index = VectorStoreIndex.from_documents(documents)
    index.storage_context.persist(persist_dir=PERSIST_DIR)
else:
    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    index = load_index_from_storage(storage_context)


def validation_agent(res,content):
    query_engine = index.as_query_engine()
    # req_op = query_engine.query(str(res))
    # response = query_engine.query(res)
    query_engine_tools = [
        QueryEngineTool(
            query_engine,
            metadata=ToolMetadata(
                name="validation_engine",
                description=(
                    validating_engine_desc
                ),
            ),
        )
    ]
    agent = OpenAIAgent.from_tools(query_engine_tools, verbose=False)
    res1 = agent.chat(res+content+"Provide only JSON output with validation")
    
    # print(response,"Agent",res1)
    
    return res1


