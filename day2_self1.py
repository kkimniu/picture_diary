from pathlib import Path
import re
REQUIRED_FIELDS = ["scene_kr", "shot", "angle", "light", "composition", "lens", "prompt_en"]
def load_draft(path: Path) -> str:
    """scene_draft.md를 읽어 본문을 반환."""
    # 여기에 path.read_text(encoding='utf-8') 반환 코드를 채워요.
    return path.read_text(encoding='utf-8')
def count_scenes(text: str) -> int:
    """본문에서 '## 장면 N' 헤딩 수를 카운트."""
    # 여기에 re.findall + 길이 반환 코드를 채워요.
    # 힌트: 정규식 r'^## 장면 \d+' (re.M 플래그).
    return len(re.findall(r'^## 장면 \d+',text,re.M))
def check_fields(text: str, scene_idx: int) -> list[str]:
    """주어진 장면 인덱스에 빠진 필드 목록 반환. 모두 있으면 빈 리스트."""
    # 여기에 본문에서 '## 장면 {scene_idx}' 섹션을 잘라낸 후
    #   REQUIRED_FIELDS 각각 'field:' 패턴이 있는지 검사하고 누락 목록을 반환하는 코드를 채워요.
    pattern = rf"## 장면 {scene_idx}(.*?)(?=## 장면 \d+|$)"
    match = re.search(pattern, text, re.S)
    if not match:
        return REQUIRED_FIELDS
    scene_text = match.group(1)
    missing = []
    for field in REQUIRED_FIELDS:
        if f"- {field}:" not in scene_text:
            missing.append(field)
    return missing

if __name__ == "__main__":
    draft = load_draft(Path("scene_draft.md"))
    n = count_scenes(draft)
    print(f"[검출] 장면 수: {n}")
    # 여기에 1~4 각 장면에 대해 check_fields 호출 + 누락 출력 코드를 채워요.
    for i in range(1, 5):
        missing = check_fields(draft, i)
        if len(missing) == 0:
            print(f"장면 {i}: OK")
        else:
            print(f"장면 {i}: 누락 -> {missing}")   
    print("[완료] 모든 장면 OK이면 self2로 진행하세요.")
