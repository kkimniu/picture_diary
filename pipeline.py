import json
from datetime import date
from pathlib import Path
import fal_client
import time, requests
from agents.scene import extract_scenes      # Day 3 self1
from agents.image import batch_generate     # Day 3 self2
from agents.video import submit_kling, status_kling, result_kling
from guardrails import check_max_iter, check_timeout, check_predicate, check_budget
import asyncio

async def picture_diary_pipeline(diary_text: str, model: str = "flux", animate_first: bool = True) -> dict:
    """그림일기 통합 파이프라인. diary 텍스트 → scenes → images → (선택) 첫 장면 영상 → results.json."""
    today = date.today().isoformat()
    out_dir = Path("outputs") / today
    out_dir.mkdir(parents=True, exist_ok=True)

    # 1) 여기에 scenes = extract_scenes(diary_text) 호출 + 결과 출력 코드를 채워요.
    scenes = extract_scenes(diary_text)
    print(f"결과[scenes]:{scenes}")
    # 2) 여기에 image_paths = batch_generate(scenes, model, out_dir) 호출 코드를 채워요.
    image_paths = batch_generate(scenes, model, out_dir)
    task_id = None
    video_path = None
    status = ""    
    # 3) (animate_first=True일 때) 여기에 image_paths[0]을 fal.ai에 업로드 + submit_kling 호출
    #    + 폴링 루프 + result_kling으로 영상 URL → 저장 코드를 채워요.
    #    힌트: Day 4 self2 §3 폴링 루프 패턴을 그대로 함수 내부에 흡수.
    if animate_first==True:

        image_url = fal_client.upload_file(str(image_paths[0]))
        prompt = scenes[0]["prompt_en"]
        task_id = submit_kling(image_url,prompt)
        iteration = 0
        start_ts = time.time()

        while True:
            if not (check_max_iter(iteration) and check_timeout(start_ts)): 
                print("[가드 발동] 중단") 
                break
            status = await status_kling(task_id)
            print(f"[{iteration}] status: {status}")

            # 여기에 check_predicate(status)가 True면 break (완료 도달)를 채워요.
            if check_predicate(status) == True:
                print("(완료 도달)") 
                break

            iteration += 1
            await asyncio.sleep(5)  # 5초 간격 폴링

    if status == "COMPLETED" or status == "Completed" or status == "succeeded":
        video_url = await result_kling(task_id)
        output_dir = Path("outputs")/ date.today().isoformat()
        output_dir.mkdir(parents=True,exist_ok=True)
        video_path = output_dir/"scene_1.mp4"
        video_path.write_bytes(requests.get(video_url).content)

    # 4) 여기에 results.json에 메타데이터(diary 첫 줄, scenes, image_paths, video_path)를 저장 코드를 채워요.

    return {"scenes": scenes, "images": image_paths, "video": video_path}
