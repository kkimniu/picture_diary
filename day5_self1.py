# day5_self1.py
import json
from pathlib import Path

from ab_test import compute_p95, run_ab_test


BASE_DIR = Path(__file__).parent
DOMAIN_NAME = "travel"
N_CALLS = 3


def main() -> None:
    # Step 1. 도메인 프롬프트 JSON 로드
    domain_path = BASE_DIR / "domains" / f"{DOMAIN_NAME}_prompts.json"
    # 여기에 domain_path에서 JSON을 읽는 코드를 채워요
    data = json.loads(domain_path.read_text(encoding="utf-8"))
    # 여기에 scenes 목록에서 사용할 장면 1개를 고르는 코드를 채워요
    scenes = data.get("scenes", [])
    scene = scenes[0]
    # 여기에 scene_prompts.json을 json.load로 읽고 scenes[0]["prompt_en"]을 반환하는 코드를 채워요.
    # 힌트: Path("scene_prompts.json").read_text(encoding="utf-8")로 파일을 읽어요.
    scene_path = json.loads(Path("scene_prompts.json").read_text(encoding="utf-8"))
    prompt_en = scene_path["scenes"][0]["prompt_en"]        
    # 여기에 diary_sentence와 prompt_addons를 합쳐 prompt를 만드는 코드를 채워요
    prompt = (scene["diary_sentence"]+ ", " + ", ".join(scene["prompt_addons"]))
    print(prompt)
    # Step 2. A/B 실행 + P95 계산
    # 여기에 run_ab_test(prompt, n_calls=N_CALLS)를 호출해요
    ab_result = run_ab_test(prompt, n_calls=N_CALLS)
    # 여기에 A 그룹 지연 목록을 꺼내요
    group_a =ab_result["latencies_a"]
    # 여기에 B 그룹 지연 목록을 꺼내요
    group_b = ab_result["latencies_b"]
    # 여기에 compute_p95로 p95_a와 p95_b를 계산해요
    p95_a = compute_p95(group_a)
    p95_b = compute_p95(group_b)
    # Step 3. ab_test_results.json 저장
    result_path = BASE_DIR / "ab_test_results.json"
    # 여기에 domain, seed, latencies, p95 값을 dict로 묶어요
    result_data = {
        "domain": DOMAIN_NAME,
        "prompt": prompt,
        "seed_a": 42,
        "seed_b": 137,
        "a_latencies": group_a,
        "b_latencies": group_b,
        "p95_a": p95_a,
        "p95_b": p95_b,
        "n_calls": N_CALLS,
    }
    # 여기에 result_path에 JSON을 저장하는 코드를 채워요
    result_path.write_text(
        json.dumps(
            result_data,
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf-8"
    )
    print(f"[저장 완료] {result_path}")
    # Step 4. cost_report.md 작성
    report_path = BASE_DIR / "cost_report.md"
    # 여기에 5일 누적 비용 표를 문자열로 만들어요
    # 여기에 P95 지연 섹션을 문자열로 만들어요
    # 여기에 report_path에 markdown을 저장하는 코드를 채워요
    IMAGE_COST_USD = 0.04
    VIDEO_COST_USD = 0.20

    day1_calls = 1
    day2_calls = 1
    day3_calls = 4
    day4_calls = 1
    day5_calls = N_CALLS * 2

    day1_cost = day1_calls * IMAGE_COST_USD
    day2_cost = day2_calls * IMAGE_COST_USD
    day3_cost = day3_calls * IMAGE_COST_USD
    day4_cost = day4_calls * VIDEO_COST_USD
    day5_cost = day5_calls * IMAGE_COST_USD

    total_calls = day1_calls + day2_calls + day3_calls + day4_calls + day5_calls
    total_cost_usd = day1_cost + day2_cost + day3_cost + day4_cost + day5_cost

    cost_per_image = IMAGE_COST_USD
    p95_latency_s = max(p95_a, p95_b)

    report = f"""# 그림일기 파이프라인 5일 누적 비용 보고서

    ## 기본 정보

    | 항목 | 값 |
    |---|---|
    | 작성 세션 | Day 5 self1 |
    | 선택 도메인 | {DOMAIN_NAME} |
    | A seed | 42 |
    | B seed | 137 |
    | A/B 호출 수 | A {N_CALLS}회 / B {N_CALLS}회 |

    ## 5일 누적 비용

    | Day | 주요 작업 | 호출 수 | 단가 또는 추정 단가 | 합계 |
    |---|---|---:|---:|---:|
    | Day 1 | 환경 확인과 첫 호출 | {day1_calls} | ${IMAGE_COST_USD:.2f} | ${day1_cost:.2f} |
    | Day 2 | 장면 JSON 생성/FLUX 테스트 | {day2_calls} | ${IMAGE_COST_USD:.2f} | ${day2_cost:.2f} |
    | Day 3 | 이미지 생성 | {day3_calls} | ${IMAGE_COST_USD:.2f} | ${day3_cost:.2f} |
    | Day 4 | 영상 생성 | {day4_calls} | ${VIDEO_COST_USD:.2f} | ${day4_cost:.2f} |
    | Day 5 self1 | 도메인 A/B 테스트 | {day5_calls} | ${IMAGE_COST_USD:.2f} | ${day5_cost:.2f} |
    | 합계 |  | {total_calls} |  | ${total_cost_usd:.2f} |

    ## P95 지연

    | 그룹 | seed | 호출 수 | P95 지연 |
    |---|---:|---:|---:|
    | A | 42 | {N_CALLS} | {p95_a:.2f}초 |
    | B | 137 | {N_CALLS} | {p95_b:.2f}초 |

    ## README로 옮길 값

    | 항목 | 값 |
    |---|---:|
    | p95_latency_s | {p95_latency_s:.2f} |
    | cost_per_image | ${cost_per_image:.2f} |
    | total_cost_usd | ${total_cost_usd:.2f} |
    """

    report_path.write_text(report, encoding="utf-8")

    print(f"[저장 완료] {report_path}")

if __name__ == "__main__":
    main()