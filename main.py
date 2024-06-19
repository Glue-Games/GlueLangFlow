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

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            context = json.loads(data) # context => { context-0: "aldsfjalskdf", ..., intput-2: "adsfasdf" }
            ai_interface = AIInterface(context)
            try:
                for step, data in enumerate(ai_interface.run_pipeline()):
                    # await websocket.send_text(f"Processing step: {step} data: {data}")
                    logger.info(f"step: {step}, data: {data}")
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
