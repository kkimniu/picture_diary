# day4_self2.py — 상태 첫 조회
from pathlib import Path
from datetime import date
import fal_client
from dotenv import load_dotenv
import time, requests
from agents.video import status_kling, result_kling
from guardrails import check_max_iter, check_timeout, check_predicate, check_budget
import asyncio
from pipeline import picture_diary_pipeline

load_dotenv()
async def main():
    task_id = Path("kling_task_id.txt").read_text().strip()
    iteration = 0
    start_ts = time.time()
    status = ""
    while True:
        # 여기에 4종 가드 적용 (check_max_iter(iteration) and check_timeout(start_ts) 모두 True면 계속,
        # 아니면 break)을 채워요.
        # 힌트: if not (check_max_iter(iteration) and check_timeout(start_ts)): print("[가드 발동] 중단") → break
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

    # 여기에 status가 "COMPLETED" 또는 "succeeded"일 때 result_kling으로 영상 URL을 받고
    #   outputs/{오늘 날짜}/scene_1.mp4로 저장하는 코드를 채워요.
    # 힌트: requests.get(video_url).content를 파일에 write.
    if status == "COMPLETED" or status == "Completed" or status == "succeeded":
        video_url = await result_kling(task_id)
        output_dir = Path("outputs")/ date.today().isoformat()
        output_dir.mkdir(parents=True,exist_ok=True)
        output_path = output_dir/"scene_1.mp4"
        output_path.write_bytes(requests.get(video_url).content)

    print(f"self1에서 받은 task_id: {task_id}")

diary_text = Path("diary.md").read_text(encoding="utf-8")
# 여기에 picture_diary_pipeline(diary_text, animate_first=False)를 호출하고
# 결과를 출력하는 코드를 채워요.
result = asyncio.run(picture_diary_pipeline(diary_text,animate_first=False))

print(result)