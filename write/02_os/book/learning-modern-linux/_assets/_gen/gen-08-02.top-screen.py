# 08-02 §5 — top 화면이 위에서 아래로 네 구역이고 정렬 키는 마지막 구역에 걸린다.
# 원문("Integrated Performance Monitors"): top 출력의 네 주석은 "Summary of system (compare with uptime
#       output)", "Task statistics", "CPU usage statistics (user, kernel, etc.; similar to vmstat
#       output)", "The dynamic process list, including details on a per-process level; comparable to
#       ps aux output" 다.
#       TIP 의 키 목록은 "? To list the help (including key mappings)", "V To toggle to and from process
#       tree view", "m To sort by memory usage", "P To sort by CPU consumption", "k To send a signal
#       (like to kill)", "q To quit" 다.
# 1차 자료(procps-ng top(1)): "m  :Memory/Swap-Usage toggle — This command affects the two summary area
#       lines dealing with physical and virtual memory. This command serves as a 4-way toggle" 이고,
#       정렬 키 표는 "M %MEM Yes" · "P %CPU Yes" · "N PID Yes" · "T TIME+ Yes" 다.
#       "V :Forest-View-Mode toggle" 도 그대로 있다.
# 주의: 소문자 m 은 요약 구역의 메모리 표시를 바꾸는 토글이고 정렬 키가 아니다. 정렬은 대문자 M 이다.
#       그래서 accent 를 프로세스 목록 구역과 그 키 줄에 건다. 같은 절이 그 표를 "For compatibility,
#       this top supports most of the former top sort keys. Since this is primarily a service to
#       former top users, these commands do not appear on any help screen." 라고 소개한다는 단서도 옮긴다.
# 타입 스펙: type-layers — 위아래로 쌓인 화면 구역. 각 구역이 무엇을 담는지와 어느 명령의 출력과 견줄
#           수 있는지를 같은 자리에 반복해 적는다. 축약: 대안 도구 비교는 본문 표가 맡는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 620
d = D(W, H, "LEARNING MODERN LINUX · 08-02 §5",
      "top 화면은 네 구역이고 정렬은 맨 아래에 걸린다",
      "저자가 top 출력에 붙인 네 주석을 화면 순서대로 쌓은 것. 오른쪽은 저자가 외워 두라고 꼽은 키이고, "
      "그중 하나가 실제 동작과 어긋난다.",
      "정렬 키는 소문자 m 이 아니라 대문자 M 입니다")

LX, LW, LH, GAP, Y0 = 24, 512, 68, 12, 116
layers = [
    ("시스템 요약", "uptime 출력과 견줄 수 있다", INFO, False),
    ("태스크 통계", "실행 · 수면 · 정지 · 좀비의 수", MUTED, False),
    ("CPU 사용 통계", "vmstat 출력과 비슷하다 — 사용자 · 커널 등", MUTED, False),
    ("동적 프로세스 목록", "ps aux 와 견줄 수 있다 — 정렬이 걸리는 자리", ACC, True),
]
for i, (name, note, col, focal) in enumerate(layers):
    y = Y0 + i * (LH + GAP)
    if focal:
        d.tone(LX, y, LW, LH, ACC, 8, "12", 1.4)
    else:
        d.box(LX, y, LW, LH, PAPER2, col, 1.2, 8)
    d.t(LX + 18, y + 28, name, 14, col, KR, "start", 600)
    d.t(LX + 18, y + 50, note, 11.5, MUTED, KR, "start")
    d.t(LX + LW - 18, y + 28, f"{i + 1}", 12, SOFT, MONO, "end", 600)

KX, KW = LX + LW + 20, W - (LX + LW + 20) - 24
KY, KH = Y0, 4 * (LH + GAP) - GAP
d.box(KX, KY, KW, KH, PAPER, RULE, 1.1, 8)
d.t(KX + 16, KY + 26, "저자가 꼽은 키", 12.5, INK, KR, "start", 600)
keys = [("?", "도움말", MUTED), ("V", "트리 보기 토글", MUTED),
        ("m", "메모리 정렬이라 적음", ACC), ("P", "CPU 사용률 정렬", OK),
        ("k", "시그널 보내기", MUTED), ("q", "끝내기", MUTED)]
for j, (k, desc, col) in enumerate(keys):
    y = KY + 52 + j * 32
    d.chip(KX + 32, y, k, col)
    d.t(KX + 56, y + 4, desc, 11.5, col, KR, "start", 600 if col is ACC else 400)

NY = Y0 + KH + 26
d.t(24, NY, "소문자 m 은 요약 구역의 메모리 두 줄을 바꾸는 4단 토글이고 정렬 키가 아닙니다.",
    12, INK, KR, "start", 600)
d.t(24, NY + 24, "top(1) 의 정렬 키 표에 있는 것은 대문자 M(%MEM) 과 P(%CPU) 이고, N(PID) 과 T(TIME+) 도 "
                 "같은 표에 있습니다.", 12, MUTED, KR, "start")
d.t(24, NY + 48, "그 표의 키들은 예전 top 사용자를 위한 호환 수단이라 어느 도움말 화면에도 나오지 않습니다.",
    12, MUTED, KR, "start")
d.t(24, NY + 72, "같은 man page 가 하나 더 알려 줍니다. 정렬에 영향을 주는 키를 누르면 V 로 켠 트리 보기가 꺼집니다.",
    12, SOFT, KR, "start")

d.legend(564, [("정렬이 걸리는 구역과 어긋난 키", ACC), ("uptime 과 견줄 구역", INFO),
                  ("실제로 정렬하는 키", OK), ("나머지 구역과 키", MUTED)])
d.save("08-02.top-screen.svg")
print("ok 08-02.top-screen")
