"""
logger.py
---------
상태 전이 하나하나를 log.csv 파일에 기록하는 모듈.
실제 SCADA 시스템의 '데이터 로깅 / Historian' 기능을 아주 단순화해서 흉내 낸 것.

csv 파일은 엑셀로도 바로 열어볼 수 있는 표 형식 파일이다.
"""

import csv
import os
import time

LOG_FILE = "log.csv"


def init_log():
    """
    프로그램이 시작할 때 한 번 호출한다.
    log.csv 파일이 아직 없으면, 표의 첫 줄(헤더)을 만들어둔다.
    이미 있으면 그대로 둬서 이전 기록이 지워지지 않게 한다.
    """
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["시각", "상태", "메시지"])


def log_transition(state, message):
    """상태가 바뀔 때마다 호출한다. log.csv에 한 줄을 추가한다."""
    with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), state, message])
