"""
plc_logic.py
------------
실제 PLC 하드웨어 없이, PLC 안에서 도는 '로직'만 흉내 내는 모듈.

핵심 개념:
- PLC는 '지금 상태를 보고 다음에 뭘 할지 정하는 것'을 아주 빠르게 반복한다.
  이걸 스캔(scan)이라고 부른다. 여기서는 scan() 함수 한 번 호출 = 스캔 1회.
- 상태가 바뀔 때마다 무엇을 할지는 이 파일이 몰라도 된다.
  대신 on_state_change라는 '콜백 함수'를 미리 등록해두면,
  상태가 바뀔 때마다 그 함수가 자동으로 호출된다.
  (콜백 = "이 일이 생기면 이 함수를 대신 실행해줘"라고 미리 맡겨두는 함수)
  이렇게 분리해두면 GUI 버전이든 통신(서버) 버전이든 이 파일을 그대로 재사용할 수 있다.
"""


class PLC:
    # 이 리스트 순서대로 상태가 순환한다.
    STATES = ["IDLE", "MOVING", "DETECTED", "STOPPED", "PUSHING", "RETURNING"]

    def __init__(self, on_state_change=None):
        self.state = "IDLE"
        self.cycle_count = 0
        self.on_state_change = on_state_change

    def _set_state(self, new_state, message):
        """내부용: 상태를 바꾸고, 등록된 콜백이 있으면 호출해준다."""
        self.state = new_state
        if self.on_state_change:
            self.on_state_change(new_state, message)

    def scan(self):
        """
        PLC의 심장박동에 해당하는 함수.
        이 함수를 계속 반복 호출하면 IDLE -> MOVING -> ... -> IDLE 순서로 순환한다.
        """
        if self.state == "IDLE":
            self._set_state("MOVING", "부품 도착 감지 - 컨베이어 구동 시작")

        elif self.state == "MOVING":
            self._set_state("DETECTED", "컨베이어 구동 중 - 센서 위치로 이동 중")

        elif self.state == "DETECTED":
            self._set_state("STOPPED", "센서1 ON - 부품 감지됨")

        elif self.state == "STOPPED":
            self._set_state("PUSHING", "정지 위치 도달 - 컨베이어 정지")

        elif self.state == "PUSHING":
            self._set_state("RETURNING", "실린더 전진 - 부품 배출")

        elif self.state == "RETURNING":
            self.cycle_count += 1
            self._set_state("IDLE", f"실린더 후진 완료 - {self.cycle_count}번째 사이클 종료")
