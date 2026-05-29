# 그림일기 프로젝트 — 5일 결과 회고 (week7_retrospective.md)

## Day별 핵심 산출물
| Day   | 강의 트랙              | 셀프 트랙                                     | 실행 확인 |
| ----- | ---------------------- | --------------------------------------------- | :--------:|
| Day 1 | OpenAI 이미지 생성 기초   | 첫 그림일기 이미지 생성                    |   ✅     |
| Day 2 | 장면 추출 JSON 구조화     | FLUX 기반 장면 이미지 생성                 |   ✅     |
| Day 3 | 멀티 장면 이미지 파이프라인    | batch_generate 기반 4장 이미지 생성   |   ✅     |
| Day 4 | Kling 영상 생성 비동기 처리 | 상태 폴링 및 mp4 저장                    |   ✅     |
| Day 5 | 도메인 A/B 테스트        | travel 도메인 성능 측정 및 cost_report 작성 |   ✅     |

## 잘 된 점
OpenAI API와 FAL API를 연동하여 이미지 생성 파이프라인을 구축했다.

## 개선할 점
비용 계산을 실제 API 사용량 기준으로 자동 집계하도록 개선하고 싶다.

## 다음 주 시도할 것
제품(Product) 도메인 추가

## GitHub 저장소
https://github.com/kkimniu/picture_diary