from serverLogic.settings import GO_API_KEY
import requests
import uvicorn
import logging
import time

logger = logging.getLogger("uvicorn")

IMAGINE_ENDPOINT = "https://api.midjourneyapi.xyz/mj/v2/imagine"
FETCH_ENDPOINT = "https://api.midjourneyapi.xyz/mj/v2/fetch"


def fetch(task_id):
    time.sleep(5)
    data = {
        "task_id": task_id
    } 

    logger.info(task_id)
    finished = False
    while not finished:
        response = requests.post(FETCH_ENDPOINT, json=data)
        logger.info(response.status_code)
        result = response.json()
        if result["status"] == "finished":
            return result["task_result"]["image_url"]
        
        # Polling for result
        logger.info(f"Status: {result['status']}, retrying in 5 seconds...")
        time.sleep(5)

    return result

def get_midjourney_image(prompt):
    headers = {
        "X-API-KEY": GO_API_KEY
    }
    
    data = {
        "prompt": prompt,
        "aspect_ratio": "4:3",
        "process_mode": "fast",
        "webhook_endpoint": "",
        "webhook_secret": ""
    }

    response = requests.post(IMAGINE_ENDPOINT, headers=headers, json=data)

    logger.info(response.status_code)

    imagine_response = response.json()

    return fetch(imagine_response["task_id"])
