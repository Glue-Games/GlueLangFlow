from benchmark.settings.levelConfigs import LEVEL_CAPTIONS

from benchmark.models.BackgroundModels.openaiBackgroundModel import openai_background_model

from urllib.request import urlretrieve
import logging
import requests
import os
from pathlib import Path
import pandas as pd
from PIL import Image
import openpyxl
import io
import time

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

def convert_to_bytes_io(img):
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    return img_byte_arr

def get_shrinked_image(image_path, save_middle_path):
    basewidth = 512
    img = Image.open(image_path)
    wpercent = (basewidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((basewidth, hsize), Image.LANCZOS)
    img = img.convert('RGBA')
    _, _, _, img_mask = img.split()

    # everything but the image should be transparent
    maskedImage = Image.new('RGBA', (1024, 1024), (255, 0, 0, 0))
    maskedImage.paste(img, (256, 0), img_mask)

    maskedImage.save(save_middle_path, format='PNG')

    return convert_to_bytes_io(maskedImage)

def run_picture_to_level_pipeline(pictures_folder, levels_folder, middle_output_dir):
    for image_name in os.listdir(pictures_folder):
        if os.path.isdir(image_name) or ".png" not in image_name:
            continue
        img_bytes = get_shrinked_image(Path.joinpath(pictures_folder, image_name), Path.joinpath(middle_output_dir, "middle_"+image_name), )
        logger.info(f"Image resized successfully")
        image_url = openai_background_model.fill_background_image(img_bytes)
        r = requests.get(image_url)
        image_dest = Path.joinpath(levels_folder, image_name)
        logger.info(f"Image Successful! saving image to: {image_dest}")
        with open(image_dest, 'wb') as outfile:
            outfile.write(r.content)


if __name__ == "__main__":
    timestr = time.strftime("test_results_%Y%m%d_%H%M%S")
    result_path = Path(f"./complete_levels/{timestr}")
    if not os.path.isdir(result_path):
        os.mkdir(result_path)

    logger.info(f"Test: {result_path}")
    output_doc = Path.joinpath(result_path, "results.xlsx")
    if output_doc.is_file():
        raise Exception(f"Cannot override existing results.xlsx! (path: {output_doc})")
    
    FileOutputHandler = logging.FileHandler(Path.joinpath(result_path, "test_log.log"))
    logger.addHandler(FileOutputHandler)

    pictures_folder = Path("./benchmark/results/test_results_20240415_090501/OpenAIPromptModel/OpenAIImageModel")
    middle_output_dir = Path.joinpath(result_path, "middle_pictures")
    if not os.path.isdir(middle_output_dir):
        os.mkdir(middle_output_dir)
    run_picture_to_level_pipeline(pictures_folder, result_path, middle_output_dir)