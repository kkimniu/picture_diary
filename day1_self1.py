import os, base64
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv


def load_api_key() -> str:
    """`.env`에서 OPENAI_API_KEY를 로드하고 마스킹한 키 첫 5자를 출력합니다."""
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY", "")
    print(f"[API KEY] {api_key[:5]}*****")
    return api_key


def build_scene_prompt() -> str:
    """본인 일기 첫 문장을 영문으로 묘사한 프롬프트를 반환합니다."""
    prompt = (
        "rainy bus stop, dark cloudy sky," 
        "wet road, quiet morning," 
        "people with umbrellas, smartphone light," 
        "gloomy mood, watercolor diary illustration"
    )
    return prompt


def generate_image(client: OpenAI, prompt: str) -> str:
    """gpt-image-1로 이미지 1장 생성, URL을 반환합니다."""
    response = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1024",
        n=1
    )
    return response.data[0].b64_json


def save_image(b64_json: str, out_path: Path) -> None:
    """base64 문자열을 디코딩해 out_path에 저장합니다."""
    image_bytes = base64.b64decode(b64_json)
    out_path.write_bytes(image_bytes)


if __name__ == "__main__":
    load_api_key()
    client = OpenAI()
    prompt = build_scene_prompt()
    print(f"[프롬프트] {prompt}")
    b64_json = generate_image(client, prompt)
    print(f"[응답 b64] {b64_json[:60]}...")
    out_path = Path("outputs") / "scene01_gpt_image_1.png"
    out_path.parent.mkdir(exist_ok=True)
    save_image(b64_json, out_path)
    print(f"[저장 완료] {out_path}")