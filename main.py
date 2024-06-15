from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import json
from serverAILibrary.AIInterface import AIInterface

import logging
import uvicorn

logger = logging.getLogger("uvicorn")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*", "POST"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="./client/dist",html = True), name="static")

# @app.post("/generate-text/")
# async def pipeline(request: Request):
#     global ai_interface
#     try:
#         context = await request.json()

#         if not context:
#             raise ValueError("Prompt cannot be empty.")

#         print("----------------------------------------------------------------")
#         print(context)
#         print("----------------------------------------------------------------")

#         ai_interface = AIInterface(context)

#         # Add your processing logic here
#         return {"message": "Data received successfully", "data": context}
#         # Call the ChatGPT API to generate the response
#         response = get_chat_gpt_prompt(context)

#         return JSONResponse(content=response, status_code=200)

#     except Exception as e:
#         logger.error(str(e))
#         return JSONResponse(content={"error": str(e)}, status_code=500)
    

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            context = json.loads(data)
            ai_interface = AIInterface(context)
            try:
                for step, data in enumerate(ai_interface.run_pipeline()):
                    # await websocket.send_text(f"Processing step: {step} data: {data}")
                    logger.info("trying to send json on ws")
                    await websocket.send_json({"step": step, "data": data})
                    logger.info("json sent successfully")
            except Exception as e:
                logger.error(str(e))
                await websocket.send_json({"step": -1, "data": "FAILED"})
                await websocket.close()
            else:
                await websocket.send_json({"step": -1, "data": "SUCCESS"})
                # await websocket.close()

    except WebSocketDisconnect:
        print("WebSocket connection closed")
