from pathlib import Path
from datetime import date
import json
from agents.image import batch_generate

scene_file = Path("scene_prompts.json")
with open(scene_file, "r", encoding="utf-8") as f:
    data = json.load(f)

scenes = data["scenes"]

today = date.today().isoformat()
output_dir = Path("outputs") / today

model = "dalle"
saved_paths = batch_generate(scenes[:4],model,output_dir)


for path in saved_paths:
    print(path)