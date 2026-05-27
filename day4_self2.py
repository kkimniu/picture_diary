# day4_self2.py — 상태 첫 조회
from pathlib import Path
import fal_client
from dotenv import load_dotenv
import time, requests
from pathlib import Path
from agents.video import status_kling, result_kling
from guardrails import check_max_iter, check_timeout, check_predicate, check_budget

load_dotenv()

task_id = Path("kling_task_id.txt").read_text().strip()
iteration = 0
start_ts = time.time()
status = ""
while True:
    # 여기에 4종 가드 적용 (check_max_iter(iteration) and check_timeout(start_ts) 모두 True면 계속,
    # 아니면 break)을 채워요.
    # 힌트: if not (check_max_iter(iteration) and check_timeout(start_ts)): print("[가드 발동] 중단") → break

    status = status_kling(task_id)
    print(f"[{iteration}] status: {status}")

    # 여기에 check_predicate(status)가 True면 break (완료 도달)를 채워요.

    iteration += 1
    time.sleep(5)  # 5초 간격 폴링

# 여기에 status가 "COMPLETED" 또는 "succeeded"일 때 result_kling으로 영상 URL을 받고
#   outputs/{오늘 날짜}/scene_1.mp4로 저장하는 코드를 채워요.
# 힌트: requests.get(video_url).content를 파일에 write.


print(f"self1에서 받은 task_id: {task_id}")

KLING_MODEL = "fal-ai/kling-video/v1/standard/image-to-video"
# 여기에 fal_client.status(KLING_MODEL, task_id, with_logs=False)를 호출하고
status = fal_client.status(KLING_MODEL, task_id, with_logs=False)
# status 객체와 status 문자열을 출력하는 코드를 채워요.
status_name = type(status).__name__
print(f"status:{status},status_name:{status_name}")