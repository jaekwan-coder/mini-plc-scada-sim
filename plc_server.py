"""
plc_server.py
-------------
[통신 버전] PLC 서버 - 소켓(socket)을 열어두고 클라이언트(PC 프로그램)의 명령을 기다린다.

실행 순서가 중요하다:
    1. 이 파일(plc_server.py)을 먼저 실행해서 켜둔다. (터미널 창 1)
    2. 그 다음 pc_client.py를 실행한다. (터미널 창 2, 또는 다른 컴퓨터)

주고받는 명령:
    START   -> 클라이언트가 보내면, 서버가 자동 운전을 시작한다.
    STOP    -> 클라이언트가 보내면, 서버가 자동 운전을 멈춘다.
    STATUS  -> 클라이언트가 보내면, 서버가 지금 상태 글자를 돌려준다.

이게 실제 'PLC와 PC가 통신 케이블/네트워크로 대화하는 것'의 원리를
소켓(TCP)이라는 파이썬 기본 기능으로 그대로 재현한 것이다.
"""

import socket
import threading
import time

from plc_logic import PLC
from logger import init_log, log_transition

HOST = "127.0.0.1"  # 내 컴퓨터 자기 자신을 가리키는 주소 (localhost)
PORT = 5000         # 이 포트 번호로 클라이언트가 접속해온다

plc = PLC(on_state_change=lambda state, msg: log_transition(state, msg))
running = False  # 지금 자동 운전 중인지 여부


def scan_loop():
    """서버가 켜져 있는 동안 계속 도는 백그라운드 루프. running이 True일 때만 스캔한다."""
    while True:
        if running:
            plc.scan()
        time.sleep(1)


def handle_client(conn, addr):
    """클라이언트 한 명과 계속 대화하는 함수. 접속이 끊기면 자동으로 끝난다."""
    global running
    print(f"[연결됨] {addr}")
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break  # 클라이언트가 연결을 끊음

            command = data.decode().strip().upper()
            print(f"[요청 수신] {addr} -> {command}")

            if command == "START":
                running = True
                conn.sendall("OK: 시작됨".encode())
            elif command == "STOP":
                running = False
                conn.sendall("OK: 정지됨".encode())
            elif command == "STATUS":
                conn.sendall(plc.state.encode())
            else:
                conn.sendall("UNKNOWN COMMAND".encode())
    print(f"[연결 종료] {addr}")


def main():
    init_log()
    threading.Thread(target=scan_loop, daemon=True).start()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()
    print(f"=== PLC 서버 시작됨 ({HOST}:{PORT}) - 클라이언트 접속 대기 중... (Ctrl+C로 종료) ===")

    try:
        while True:
            conn, addr = server.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
    except KeyboardInterrupt:
        print("\n=== 서버 종료 ===")


if __name__ == "__main__":
    main()
