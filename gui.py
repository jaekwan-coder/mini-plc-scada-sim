"""
gui.py
------
사람이 직접 보고 조작하는 화면 (GUI이자 HMI).
tkinter는 파이썬에 기본 내장되어 있어서 별도 설치가 필요 없다.

이 파일은 plc_logic.py를 '같은 프로그램 안에서' 직접 불러다 쓰는 기본 버전이다.
(서버-클라이언트로 분리된 통신 버전은 plc_server.py / pc_client.py를 참고)
"""

import threading
import time
import tkinter as tk

from plc_logic import PLC
from logger import init_log, log_transition
from stats import compute_stats


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("미니 PLC-PC 시뮬레이션 (HMI)")

        self.running = False
        self.plc = PLC(on_state_change=self.on_state_change)

        self.state_label = tk.Label(root, text="상태: IDLE", font=("Arial", 16))
        self.state_label.pack(pady=10)

        self.start_button = tk.Button(root, text="시작", width=15, command=self.toggle_run)
        self.start_button.pack(pady=5)

        self.stats_button = tk.Button(root, text="통계 보기", width=15, command=self.show_stats)
        self.stats_button.pack(pady=5)

        self.stats_label = tk.Label(root, text="", font=("Arial", 11), justify="left")
        self.stats_label.pack(pady=10)

        init_log()

    def on_state_change(self, state, message):
        """PLC 상태가 바뀔 때마다 자동으로 호출되는 함수 (콜백)."""
        self.state_label.config(text=f"상태: {state}  ({message})")
        log_transition(state, message)

    def toggle_run(self):
        self.running = not self.running
        self.start_button.config(text="정지" if self.running else "시작")
        if self.running:
            # 화면이 멈추지 않도록, PLC 스캔 반복은 별도의 스레드(동시 실행 흐름)에서 돌린다.
            threading.Thread(target=self.run_loop, daemon=True).start()

    def run_loop(self):
        while self.running:
            self.plc.scan()
            time.sleep(1)

    def show_stats(self):
        self.stats_label.config(text=compute_stats())


def main():
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
