from benchmark.settings.levelConfigs import LEVEL_CAPTIONS, NEW_LEVEL_CAPTIONS_BY_CATEGORY

from benchmark.models.promptModels.openaiPromptModel import openai_prompt_model
from benchmark.models.imageModels.openaiImageModel import openai_image_model
from benchmark.models.imageModels.midjourneyImageModel import midjourney_image_model

from urllib.request import urlretrieve
import logging
import requests
import os
from pathlib import Path
import pandas as pd
import openpyxl
import time

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

# logging.basicConfig(filename="./benchmark/results/current_test_log.txt",
#                     filemode='w',
#                     format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
#                     datefmt='%H:%M:%S',
#                     level=logging.INFO)

class Benchmark:
    def __init__(self, level_captions, prompt_models, image_models, results_dir, results_documentation):
        self.level_captions = level_captions
        self.prompt_models = prompt_models
        self.image_models = image_models
        self.results_documentation = results_documentation
        self.results_dir = results_dir
        self.global_id = 0
        self.result_dirs = {}
    
    def run(self):
        for prompt_model in self.prompt_models:
            self.create_results_dir(prompt_model)
            for level_category, level_captions in self.level_captions.items():
                for level_caption in level_captions:
                    for image_model in self.image_models:
                        output_dir = self.result_dirs[str(image_model)]
                        try:
                            image_prompt = prompt_model.generate_image_prompt(level_caption)
                            self.run_iteration(level_category, level_caption, prompt_model, image_model, image_prompt, output_dir)
                        except Exception:
                            if image_prompt:
                                logger.info(f"""Failed to generate entry:
                                            level_category: {level_category},
                                            level_caption: {level_caption},
                                            prompt_model: {prompt_model},
                                            image_model: {image_model},
                                            prompt: {image_prompt},
                                            """)
                            else:
                                logger.info(f"""Failed to generate entry:
                                            level_category: {level_category},
                                            level_caption: {level_caption},
                                            prompt_model: {prompt_model},
                                            image_model: {image_model},
                                            """)
                self.global_id += 1

    def create_results_dir(self, prompt_model):
        base_model_result = os.path.join(self.results_dir, str(prompt_model)) 
        if not os.path.isdir(base_model_result):
            os.mkdir(base_model_result)

        for image_model in self.image_models:
            full_result_path = os.path.join(base_model_result, str(image_model))
            if not os.path.isdir(full_result_path):
                    os.mkdir(full_result_path)
            self.result_dirs[str(image_model)] = full_result_path

    def run_iteration(self, level_category, level_caption, prompt_model, image_model, image_prompt, output_dir):
        logger.info(f"""Running - 
                    level_caption: {level_caption},
                    Prompt Model: {prompt_model},
                    Image Model: {image_model}""")
        new_entry = {
            "Level Caption": [level_caption],
            "Prompt Model": [prompt_model],
            "Image Model": [image_model]
        }
        new_entry["Image Prompt"] = [image_prompt]
        image_url = image_model.generate_image(image_prompt)
        # new_entry["image_url"] = image_url
        image_dest = Path(os.path.join(output_dir, "".join([level_category, " - ", level_caption, " id ", str(self.global_id), ".png"])))
        new_entry["Image Path"] = [image_dest.relative_to(self.results_dir)]
        new_entry["Image Filename"] = image_dest.name
        logger.info(f"""Finished
                    level_category: {level_category},
                    level_caption: {level_caption},
                    prompt_model: {prompt_model},
                    image_model: {image_model},
                    prompt: {image_prompt},
                    image_url: {image_url},
                    image_dest: {image_dest}
                    """)

        r = requests.get(image_url)
        with open(image_dest, 'wb') as outfile:
            outfile.write(r.content)

        self.log_output(new_entry)
    
    def log_output(self, new_entry):
        df_new = pd.DataFrame(new_entry)
        df_existing = pd.read_excel(self.results_documentation)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        df_combined.to_excel(output_doc, index=False)

if __name__ == "__main__":
    timestr = time.strftime("test_results_%Y%m%d_%H%M%S")
    result_path = Path(f"./benchmark/results/{timestr}")
    if not os.path.isdir(result_path):
        os.mkdir(result_path)

    logger.info(f"Test: {result_path}")
    output_doc = Path.joinpath(result_path, "results.xlsx")
    if output_doc.is_file():
        raise Exception(f"Cannot override existing results.xlsx! (path: {output_doc})")
    
    FileOutputHandler = logging.FileHandler(Path.joinpath(result_path, "test_log.log"))
    logger.addHandler(FileOutputHandler)
   
    df = pd.DataFrame([['<caption>',
                        '<prompt model>',
                        '<image model>',
                        '<image file name>',
                        '<image prompt>',
                        '<image file path>']], columns=[
                            'Level Caption',
                            'Prompt Model',
                            'Image Model',
                            'Image Filename',
                            'Image Prompt',
                            'Image Path'])

    df.to_excel(output_doc, index=False)

    benchmark_model = Benchmark(
        # LEVEL_CAPTIONS,
        NEW_LEVEL_CAPTIONS_BY_CATEGORY,
        [openai_prompt_model],
        [openai_image_model],
        result_path,
        output_doc)

    benchmark_model.run()