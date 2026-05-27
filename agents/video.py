# agents/video.py — Kling Image-to-Video 비동기 호출
import os
from dotenv import load_dotenv
import fal_client

load_dotenv()

KLING_MODEL = "fal-ai/kling-video/v2/master/image-to-video"  # 강사 day4-s3 시연 엔드포인트 일치

def submit_kling(image_url: str, prompt: str, duration: int = 5) -> str:
    # 여기에 fal_client.submit(KLING_MODEL, arguments={...})를 호출하고
    
    handler = fal_client.submit(
        KLING_MODEL,
        arguments={
            "prompt":prompt,
            "image_url":image_url,
            "duration":duration,
        }
    )
    #   handler.request_id를 반환하는 코드를 채워요.
    return handler.request_id  
    # 힌트: arguments = {"image_url": image_url, "prompt": prompt, "duration": duration}
    # 힌트: submit은 즉시 반환하고 영상은 백그라운드에서 생성됩니다.

# status_kling, result_kling 함수는 self2에서 작성
# agents/video.py (이어쓰기 — submit_kling 아래에 추가)

async def status_kling(request_id: str) -> str:
    """Kling status 1회 조회. 상태 문자열 반환."""
    # 여기에 fal_client.status_async(KLING_MODEL, request_id, with_logs=False)를 호출하고
    #   status 객체의 status 필드(예: "IN_PROGRESS", "COMPLETED")를 반환하는 코드를 채워요.
    status = await fal_client.status_async(KLING_MODEL, request_id, with_logs=False)
    return type(status).__name__

async def result_kling(request_id: str) -> str:
    """Kling 완료된 영상 결과 받기. 영상 URL 반환."""
    # 여기에 fal_client.result_async(KLING_MODEL, request_id)를 호출하고
    #   result["video"]["url"]을 반환하는 코드를 채워요.
    # 힌트: Kling 응답 구조는 result["video"]["url"] (DALL-E·FLUX와 다름).
    result = await fal_client.result_async(KLING_MODEL, request_id)
    return result["video"]["url"]