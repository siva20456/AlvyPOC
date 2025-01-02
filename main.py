from langfuse import Langfuse
# from openai import OpenAI
# from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings, StorageContext, load_index_from_storage
# from llama_index.llms.openai import OpenAI
# from llama_index.core.tools import QueryEngineTool
# from llama_index.core.agent import ReActAgent
# from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import os
from langfuse.llama_index import LlamaIndexInstrumentor
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from camera_agent import camera_image_analyzing_agent
from screen_agent import screen_image_analyzing_agent
# from validating_agent import validation_agent
from chat_bot_agent import chatting_agent

# from image_describe import describe_image
# from context import pre_context


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins. Change to specific origins for production.
    allow_credentials=True,  # Allow cookies and credentials
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

@app.middleware("http")
async def add_keep_alive_header(request, call_next):
    response = await call_next(request)
    response.headers["Connection"] = "keep-alive"
    return response




os.environ["LANGFUSE_PUBLIC_KEY"] = ""
os.environ["LANGFUSE_SECRET_KEY"] = ""
os.environ["LANGFUSE_HOST"] = "http://localhost:3000"
os.environ["OPENAI_API_KEY"] = ""

langfuse_client = Langfuse(
    public_key=os.environ.get('LANGFUSE_PUBLIC_KEY'),
    secret_key=os.environ.get('LANGFUSE_SECRET_KEY'),
    host=os.environ.get('LANGFUSE_HOST')
)

instrumentor = LlamaIndexInstrumentor()
instrumentor.start()



class Req(BaseModel):
    img_url: str
    userId:str
    
class Sess_Req(BaseModel):
    userId:str
    
class ChatReq(BaseModel):
    query: str
    userId: str
    browserDetails: object

@app.post('/agent/camera')
def main_camera(obj: Req):
    # response = chat_function(obj.img_url,"Analyze the image and describe it. Describe it in paragraph with number of humans, objects detected, devices indicated, head direction of humans if any and hand guestures. output should not contain extra info about other thoughts and environments and hallucinations are not allowed.",obj.userId)
    # print(response,obj.userId)
    # return JSONResponse(response.response)
    trace = langfuse_client.trace(
        name = "Cam Img Analyzer",
        user_id = obj.userId,
        metadata = {
            "email": "user@langfuse.com",
        },
        session_id = "Session Cam by {}".format(obj.userId),
        tags = ["Python"],
        input = "Analyze " + obj.img_url
    )
    with instrumentor.observe(trace_id=trace.id, update_parent=False):
        cam_resp = camera_image_analyzing_agent(obj.img_url)
    trace.update(
        output=cam_resp.sources[0].content
    )
    res = {
        "img_url":obj.img_url,
        "camera":cam_resp.sources[0].content,
        # "validation_camera":validation_cam.response
    }
    return JSONResponse(res)

@app.post('/agent/screen')
def main_screen(obj: Req):
    # print(obj)
    trace = langfuse_client.trace(
        name = "Scrren Img Analyzer",
        user_id = obj.userId,
        metadata = {
            "email": "user@langfuse.com",
        },
        session_id = "Session Screen by {}".format(obj.userId),
        tags = ["Python"],
        input = "Analyze " + obj.img_url
    )
    with instrumentor.observe(trace_id=trace.id, update_parent=False):
        sc_resp = screen_image_analyzing_agent(obj.img_url)
    trace.update(
        output=sc_resp.sources[0].content
    )
    res = {
        "img_url":obj.img_url,
        "screen":sc_resp.sources[0].content,
        # "validation_screen":validation_screen.response
    }
    return JSONResponse(res)

@app.post('/agent/chat1')
def main_chat1(obj: ChatReq):
    trace = langfuse_client.trace(
        name = "KB Chat Bot",
        user_id = obj.userId,
        metadata = {
            "email": "user@langfuse.com",
        },
        session_id = "Session Chat by {}".format(obj.userId),
        tags = ["Python"],
        input = obj.query
    )
    with instrumentor.observe(trace_id=trace.id, update_parent=False):
        chat_response = chatting_agent(obj.query,obj.browserDetails,obj.userId)
    trace.update(
        output=chat_response.response
    )
    res = {
        "chat_bot": chat_response.response
    }
    return JSONResponse(res)

@app.post('/agent/chat')
def main_chat(obj: ChatReq):
    chat_response = chatting_agent(obj.query,obj.browserDetails,obj.userId)
    res = {
        "chat_bot": chat_response.response
    }
    return JSONResponse(res)
    

# @app.post('/agent/validate')
# def main_validate(obj: Sess_Req):
#     session_id = "Session Cam by {}".format(obj.userId)
#     traces = langfuse_client.get_traces(session_id=session_id)
#     for e in traces.data:
        
    


# @app.post('/sessions')
# def user_session(obj:Sess_Req):
#     session_id = "Session Llama Py by {}".format(obj.userId)
#     traces = langfuse_client.get_traces(session_id=session_id)
#     data = []
#     for e in traces.data:
#         data.append({
#             "id": e.session_id,
#             "output": e.output,
#             "input":e.input
#         })

#     return JSONResponse(data)

# print(response)
# session_id = "Session of Py by {}".format(user)
# sess = langfuse_client.fetch_sessions(session_id = session_id)
# traces = langfuse_client.get_traces(session_id=session_id)
# print(traces)
# print(traces.data)
# for e in traces.data:
#     print(e.session_id,e.input,e.output)