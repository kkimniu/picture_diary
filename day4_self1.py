# day4_self1.py — Kling 영상 submit 1회 시범
from pathlib import Path

import fal_client

from agents.video import submit_kling

IMAGE_PATH = Path("outputs") / "2026-05-28" / "scene_1.png"
# 여기에 image_path를 fal.ai 임시 URL로 업로드하는 코드를 채워요.
# 힌트: fal_client.upload_file(str(IMAGE_PATH))는 fal.ai 임시 URL을 반환.
url = fal_client.upload_file(str(IMAGE_PATH))
PROMPT = "static shot, gentle smile, subtle breathing, cinematic lighting"  # 여기에 day4-s2에서 본 카메라 워크 어휘를 채워요.

# 여기에 submit_kling 호출 + task_id를 kling_task_id.txt에 저장하는 코드를 채워요.
task_id = submit_kling(url,PROMPT)

with open("kling_task_id.txt", "w", encoding="utf-8") as f:
    f.write(task_id)

print("[완료] task_id 저장:", task_id)