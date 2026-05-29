로컬 실행 시 생성됨

# 글로 쓰는 그림일기 — Picture Diary
일기 텍스트를 4장면 이미지와 영상으로 변환하는 멀티 AI 파이프라인 프로젝트입니다.

## 빠른 시작
```bash
uv venv && uv pip install -r requirements.txt
# .env에 OPENAI_API_KEY와 FAL_KEY 추가 후 실행
python pipeline.py
```

## 결과 미리보기
![scene\_1](outputs/2026-05-29/scene_1.mp4)

## 운영 지표
| Day | 모델 | 호출 수 | 합계 |
|-------------|----------------------|-----:|------:|
| Day 1       | gpt-image-1          |    1 | $0.04 |
| Day 2       | FLUX schnell         |    1 | $0.04 |
| Day 3       | gpt-image-1.5 / FLUX |    4 | $0.16 |
| Day 4       | Kling image-to-video |    1 | $0.20 |
| Day 5 self1 | FLUX A/B test        |    6 | $0.24 |
| 합계         |                     |   13 | $0.68 |
## A/B 테스트 요약
* 선택 도메인: travel
* seed A: 42
* seed B: 137
* A 호출 수: 3회
* B 호출 수: 3회
* p95_a: ab_test_results.json 참고
* p95_b: ab_test_results.json 참고

## 도메인 응용
<!-- # 여기에 Day 5 self1에서 선택한 도메인 결과를 채워요 -->
travel 도메인을 선택하여
비 오는 도시 아침, 젖은 도로 반사, 흐린 하늘 분위기의 여행 일기 스타일 이미지를 생성했습니다.


## 파일 구조
<!-- # 여기에 본인 프로젝트 파일 구조를 간단히 채워요 -->
```text
picture_diary/
├── pipeline.py
├── agents/
│   ├──__init__.py
│   ├── scene.py
│   ├── image.py
│   └── video.py
├── domains/
│   └── travel_prompts.json
├── ab_test.py
├── day5_self1.py
├── cost_report.md
├── ab_test_results.json
└── outputs/
```
## 라이선스
<!-- # 여기에 라이선스를 채워요 (예: MIT) -->
MIT
