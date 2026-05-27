## Day 1 self1
- 배운 점: .env에 API 키를 넣고 load_dotenv()로 읽으면 코드에 키를 직접 쓰지 않아도 된다.
- 막힌 점: 과제에서 모델을 dail-e 3으로 해야하는데 그것 안되어서 gpt-image-1로 변경해서 해결
- 내일 시도할 것: 조명을 추가해보는 것
- 강사 비유 연결: .env는 잠긴 서랍입니다. (강사 s1)

## Day 2 self1
- 완료 시각: 17:50
- 생성 파일: scene_prompts.json, day2_self2.py, outputs/scene01_fal.png
- FLUX vs DALL-E 차이: FLUX → “디테일하고 감성적인 이미지 생성”에 강함 DALL·E → “대화형 편집 + 안정적인 범용 생성”에 강함
- 막힌 부분: 없음

## Day 3 self1
- agents/scene.py로 diary.md에서 4장면 scenes JSON을 추출했다.
- scene_extracted.json을 Day 3 self2 이미지 생성 입력으로 사용할 준비를 했다.

## Day 3 self2
- 사용 모델: gpt-image-1.5 , flux
- COMMON_STYLE:     "watercolor diary illustration,soft rainy city palette,quiet rainy morning mood,consistent rainy bus stop atmosphere"
- 생성 결과: outputs/2026-05-27/scene_1~4.png
- 재시도한 장면: outputs/2026-05-28/scene_1~4.png
- Day 4 입력 가능 여부: 가능

## Day 4 self1
- 동기 vs 비동기 차이 1줄 + 가드레일 4종 의미 1줄 정리 : 동기 호출은 결과를 바로 기다리고, 비동기 호출은 task_id를 받아 나중에 status/result로 확인하고 가드레일 4종은 반복 횟수, 대기 시간, 완료 조건, 비용 상한을 제한해 무한 대기와 비용 초과를 막는다.

## Day 4 self2
- Kling은 submit 직후 영상 URL을 바로 주지 않기 때문에 status 폴링 후 result를 받아야 한다.
- picture_diary_pipeline(diary_text, model, animate_first)는 장면 추출(scene) → 이미지 생성(image) → 영상 생성(video) → 결과 저장(results)을 연결하는 통합 인터페이스다.
- 비동기 polling 구조를 사용하여 완료 상태를 반복 확인했다.
- guardrail(check_max_iter, check_timeout 등)을 통해 무한 실행과 비용 폭주를 방지했다.

## Day 5 self1 준비

- 내일은 pipeline()을 제품/이모티콘/여행 도메인 중 하나에 응용할 예정이다.
- cost_report.md를 이용해 이미지·영상 생성 비용을 기록한다.