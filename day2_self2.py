import os
import json
import requests
from pathlib import Path
from dotenv import load_dotenv
import fal_client


def load_keys() -> None:
    """.env에서 FAL_KEY와 OPENAPI_API_KEY를 로드합니다."""
    # 여기에 load_dotenv() 호출 + os.getenv("FAL_KEY") 가져오기 + 첫 5자 마스킹 출력을 채워요.
    load_dotenv()
    api_key: str | None = os.getenv("FAL_KEY")
    # 힌트: FAL_KEY가 없으면 fal-client가 작동하지 않아요.
    # 힌트: print(f"FAL_KEY: {key[:5]}...") 형태로 마스킹 출력해요.
    print(f"환경확인 | OPENAPI_API_KEY 첫 12자: {api_key[:5] if api_key else 'None - .env 위치 확인 필요!!!'}")
    pass


def load_first_prompt() -> str:
    """scene_prompts.json에서 첫 번째 장면의 prompt_en을 반환합니다."""
    data = json.loads(Path("scene_prompts.json").read_text(encoding="utf-8"))
    scenes = data.get("scenes", [])
    # 여기에 scene_prompts.json을 json.load로 읽고 scenes[0]["prompt_en"]을 반환하는 코드를 채워요.
    # 힌트: Path("scene_prompts.json").read_text(encoding="utf-8")로 파일을 읽어요.
    return scenes[0]["prompt_en"]


def call_flux_schnell(prompt: str) -> str:
    """FLUX-schnell로 이미지 1장 생성, URL을 반환합니다."""
    # 여기에 fal_client.subscribe("fal-ai/flux/schnell", arguments={"prompt": prompt, "num_images": 1})를 호출하고
    result = fal_client.subscribe("fal-ai/flux/schnell", arguments={"prompt": prompt, "num_images": 1})
    #   result["images"][0]["url"]을 반환하는 코드를 채워요.
    # 힌트: 응답 구조는 DALL-E와 다릅니다.
    #   OpenAI = response.data[0].url
    #   fal.ai = result["images"][0]["url"]
    fal_ai = result["images"][0]["url"]
    return fal_ai


def save_image(url: str, out_path: Path) -> None:
    """URL의 PNG 바이트를 내려받아 out_path에 저장합니다."""
    # 여기에 requests.get(url) + out_path.write_bytes(response.content) 코드를 채워요.
    # 힌트: day1_self1.py에서 작성한 패턴을 재사용해요.
    response = requests.get(url)
    out_path.write_bytes(response.content)
    pass


if __name__ == "__main__":
    load_keys()
    prompt = load_first_prompt()
    print(f"[프롬프트] {prompt[:60]}...")
    url = call_flux_schnell(prompt)
    print(f"[FLUX URL] {url[:60]}...")
    out_path = Path("outputs") / "scene01_fal.png"
    out_path.parent.mkdir(exist_ok=True)
    save_image(url, out_path)
    print(f"[저장 완료] {out_path}")
