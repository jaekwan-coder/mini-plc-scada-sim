"""
stats.py
--------
log.csv를 읽어서 요약 통계를 계산하는 모듈.
실제 SCADA 시스템의 '트렌드 분석 / 리포트' 기능을 아주 단순화해서 흉내 낸 것.
"""

import csv
import os
from collections import Counter

from logger import LOG_FILE


def compute_stats():
    """
    log.csv를 읽어서 다음 세 가지를 계산해 문자열로 돌려준다.
    - 총 기록 건수
    - 완료된 사이클 수
    - 가장 많이 거친 상태
    """
    if not os.path.exists(LOG_FILE):
        return "아직 기록이 없습니다. 먼저 시작 버튼을 눌러보세요."

    with open(LOG_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if not rows:
        return "아직 기록이 없습니다. 먼저 시작 버튼을 눌러보세요."

    cycle_count = sum(1 for r in rows if "사이클 종료" in r["메시지"])
    state_counter = Counter(r["상태"] for r in rows)
    most_common_state, most_common_count = state_counter.most_common(1)[0]

    return (
        f"총 스캔 기록: {len(rows)}건\n"
        f"완료된 사이클 수: {cycle_count}회\n"
        f"가장 많이 거친 상태: {most_common_state} ({most_common_count}회)"
    )
