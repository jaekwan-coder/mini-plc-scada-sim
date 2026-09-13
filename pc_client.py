"""
pc_client.py
------------
[통신 버전] PC 클라이언트 - plc_server.py에 접속해서 명령을 보내고 상태를 받아오는 화면.

반드시 plc_server.py를 먼저 실행해둔 상태에서 이 파일을 실행해야 한다.
(서버가 안 켜져 있으면 "서버에 연결할 수 없습니다" 메시지가 뜬다.)
"""

import socket
import tkinter as tk

HOST = "127.0.0.1"
PORT = 5000


def send_command(command):
    """
    서버에 접속해서 명령 하나를 보내고, 응답을 받아서 돌려주는 함수.
    소켓 연결 -> 명령 전송 -> 응답 수신 -> 연결 종료, 이 네 단계가
    실제 PLC-PC 통신에서 항상 일어나는 기본 패턴이다.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(command.encode())
        response = s.recv(1024).decode()
    return response


class ClientApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PC 클라이언트 (통신 버전)")

        self.state_label = tk.Label(root, text="상태: -", font=("Arial", 16))
        self.state_label.pack(pady=10)

        tk.Button(root, text="시작", width=15, command=self.start).pack(pady=5)
        tk.Button(root, text="정지", width=15, command=self.stop).pack(pady=5)

        self.auto_refresh()

    def start(self):
        self._safe_send("START")

    def stop(self):
        self._safe_send("STOP")

    def _safe_send(self, command):
        try:
            send_command(command)
        except ConnectionRefusedError:
            self.state_label.config(text="서버에 연결할 수 없습니다.\nplc_server.py를 먼저 실행하세요.")

    def auto_refresh(self):
        """1초마다 자동으로 서버에 STATUS를 물어봐서 화면을 갱신한다."""
        try:
            state = send_command("STATUS")
            self.state_label.config(text=f"상태: {state}")
        except ConnectionRefusedError:
            self.state_label.config(text="서버에 연결할 수 없습니다.\nplc_server.py를 먼저 실행하세요.")
        self.root.after(1000, self.auto_refresh)


def main():
    root = tk.Tk()
    ClientApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
