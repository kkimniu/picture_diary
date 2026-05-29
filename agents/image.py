import os, requests, json , base64
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
import fal_client

load_dotenv()

COMMON_STYLE = (
    "watercolor diary illustration, "
    "soft rainy city palette, "
    "quiet rainy morning mood, "
    "consistent rainy bus stop atmosphere"
)  # ← 캐릭터 일관성 어휘 (§2에서 정한 화풍·색·인물 표현 1줄)

def call_dalle(client: OpenAI, prompt: str) -> str:
    """gpt-image-1.5로 1장 생성, URL 반환."""
    # 여기에 OpenAI() 클라이언트 + client.images.generate(...) 호출 코드를 채워요.
    # 힌트: gpt-image-1.5 는 seed 인자를 직접 받지 않으므로 prompt에 "seed: N" 텍스트로 표현하거나 무시.
    full_prompt = prompt
    result = client.images.generate(
        model="gpt-image-1.5",
        prompt=full_prompt,
        size="1024x1024",
        quality="auto",
        n=1,
        output_format="png"
    )
    b64_data = result.data[0].b64_json    
    return b64_data

def call_flux(prompt: str, seed: int = 42) -> str:
    """FLUX로 1장 생성, URL 반환. seed로 일관성 강화."""
    # 여기에 fal_client.run("fal-ai/flux/schnell", arguments={..., "seed": seed})를 호출하는 코드를 채워요.
    # 힌트: 응답 구조는 result["images"][0]["url"].
    full_prompt = prompt
    result = fal_client.run(
        "fal-ai/flux/schnell",
        arguments={
            "prompt": full_prompt,
            "seed" : seed, # 캐리기티 일관성을 위한 시드 고정
            "num_images" : 1,
            "image_size" : "square_hd"
        }
    )
    image_url = result["images"][0]["url"]    
    return image_url

def generate_image(prompt: str, model: str = "dalle", seed: int = 42) -> str:
    """모델 분기 함수. DALL-E 또는 FLUX 호출."""
    # 여기에 model 분기 (dalle/flux) 후 위 두 함수 호출 → URL 반환.
    if model == "dalle":
        client = OpenAI()
        return call_dalle(client,prompt)
    elif model == "flux":
        return call_flux(prompt,seed)

def save_image(url: str, out_path: Path, model: str = "dalle") -> None:
    # 여기에 requests.get + write_bytes 패턴 (day1_self1.py에서 가져온 재사용 코드).
    if model == "dalle":
        out_path.parent.mkdir(parents=True, exist_ok=True) # ./1/outputs/abc.png
        out_path.write_bytes(base64.b64decode(url))
    elif model == "flux":
        out_path.parent.mkdir(parents=True,exist_ok=True)
        result = requests.get(url,timeout=30)
        result.raise_for_status() # 다운로드 문제 여부 확인
        out_path.write_bytes(result.content)

def batch_generate(scenes: list[dict], model: str, out_dir: Path) -> list[Path]:
    """scenes 리스트를 받아 4장 일괄 생성 후 저장 경로 반환. try/except로 한 장 실패 시 격리."""
    # 여기에 for 루프 + try/except + generate_image + save_image 호출 패턴을 채워요.
    # 힌트: 각 scene["prompt_en"] + COMMON_STYLE 결합. seed는 scene_id로 고정.
    saved: list[Path] = []
    model = model.lower()
    for scene in scenes:
        try:
            image_data = generate_image(scene["prompt_en"]+ COMMON_STYLE,model,scene["scene_id"])
            save_path = out_dir / f"scene_{scene['scene_id']}.png"
            save_image(image_data,save_path,model)
            saved.append(save_path)

        except Exception as e:
            print(f"[ERROR] scene_{scene.get('scene_id', 'unknown')} 실패: {e}")
            continue

    return saved