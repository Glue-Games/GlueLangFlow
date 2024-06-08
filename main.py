from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from httpx import AsyncClient

import logging
from serverLogic.chatgpt import get_chat_gpt_response, get_chat_gpt_prompt
from serverLogic.openai_endpoint import get_create_image
from serverLogic.goapi_endpoint import get_midjourney_image
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

@app.post("/generate-text/")
async def pipeline(request: Request):
    try:
        context = await request.json()

        if not context:
            raise ValueError("Prompt cannot be empty.")

        print("----------------------------------------------------------------")
        print(context)
        print("----------------------------------------------------------------")

        # Log the received data for debugging purposes
        logger.info(f"Received data: {context}")
        # Add your processing logic here
        return {"message": "Data received successfully", "data": context}
        # Call the ChatGPT API to generate the response
        response = get_chat_gpt_prompt(context)

        return JSONResponse(content=response, status_code=200)

    except Exception as e:
        logger.error(str(e))
        return JSONResponse(content={"error": str(e)}, status_code=500)