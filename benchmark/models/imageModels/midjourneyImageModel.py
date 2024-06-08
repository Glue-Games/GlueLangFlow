from benchmark.settings.modelsConfig import GOAPI_X_KEY
import time
import logging
import requests

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

IMAGINE_ENDPOINT = "https://api.midjourneyapi.xyz/mj/v2/imagine"
FETCH_ENDPOINT = "https://api.midjourneyapi.xyz/mj/v2/fetch"

class MidJourneyImageModel:
    def __init__(self, api_key):
        self.api_key = api_key

    def _fetch(self, task_id):
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
            
            if result["status"] == "failed":
                raise Exception("Failed create image")
            
            # Polling for result
            logger.info(f"Status: {result['status']}, retrying in 5 seconds...")
            time.sleep(5)

        return result

    def generate_image(self, prompt):
        headers = {
            "X-API-KEY": self.api_key
        }
        
        data = {
            "prompt": prompt,
            "aspect_ratio": "4:3",
            "process_mode": "turbo",
            "webhook_endpoint": "",
            "webhook_secret": ""
        }

        response = requests.post(IMAGINE_ENDPOINT, headers=headers, json=data)

        logger.info(response.status_code)
        imagine_response = response.json()

        return self._fetch(imagine_response["task_id"])

    def __str__(self):
        return __class__.__name__

midjourney_image_model = MidJourneyImageModel(api_key=GOAPI_X_KEY)
