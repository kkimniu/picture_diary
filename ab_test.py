import time
import statistics
import math
from agents.image import generate_image

SEED_A = 42
SEED_B = 137

def time_one_call(prompt: str, seed: int, model: str = "flux") -> float:
    """이미지 1회 호출에 걸린 시간을 초 단위로 돌려주는 함수."""
    # 여기에 시작 시각을 time.perf_counter()로 기록해요
    start_time = time.perf_counter()
    # 여기에 generate_image(prompt=..., seed=..., model=...) 호출을 채워요
    generate_image(prompt=prompt,seed=seed,model=model)
    # 여기에 종료 시각을 time.perf_counter()로 기록해요
    end_time = time.perf_counter()
    # 여기에 종료 시각 - 시작 시각을 반환하도록 채워요
    return end_time- start_time


def run_ab_test(prompt: str, n_calls: int = 3) -> dict:
    """같은 prompt를 seed A/B로 나누어 여러 번 호출하는 함수."""
    # 여기에 seed A=42, seed B=137 값을 준비해요 (강사 day5-s3 시연 seed 일치)
    # 여기에 A 그룹 지연 시간을 담을 리스트를 만들어요
    # 여기에 B 그룹 지연 시간을 담을 리스트를 만들어요
    # 여기에 n_calls만큼 A 그룹 time_one_call을 반복해요
    # 여기에 n_calls만큼 B 그룹 time_one_call을 반복해요
    # 여기에 두 리스트를 dict로 묶어 반환하도록 채워요
    latencies_a = []
    latencies_b = []

    for i in range(n_calls):
        t_a = time_one_call(prompt, SEED_A)
        t_b = time_one_call(prompt, SEED_B)
        latencies_a.append(t_a)
        latencies_b.append(t_b)
        print(f"  [{i+1}/{n_calls}] A={t_a:.2f}s B={t_b:.2f}s")

    p95_a = compute_p95(latencies_a)
    p95_b = compute_p95(latencies_b)

    winner = "A (seed=42)" if p95_a < p95_b else "B (seed=137)"
    print(f"\n P95_A={p95_a:.2f}s | P95_B={p95_b:.2f}s → 승자: {winner}")

    return {
        "latencies_a": latencies_a,
        "latencies_b": latencies_b,
        "p95_a": p95_a,
        "p95_b": p95_b,
        "winner": winner,
    }


def compute_p95(latencies: list[float]) -> float:
    """지연 시간 목록에서 P95 값을 계산하는 함수."""
    # 여기에 빈 리스트일 때의 처리를 채워요
    # 여기에 statistics.quantiles 또는 정렬 기반 계산을 채워요
    # 여기에 초 단위 float 값을 반환하도록 채워요
    if not latencies:
        return 0.0
    sorted_latencies = sorted(latencies)        # 오름차순 정렬
    index = math.ceil(0.95 * len(sorted_latencies)) - 1  # P95 인덱스
    index = max(0, min(index, len(sorted_latencies) - 1))  # 범위 보정
    return sorted_latencies[index]
