# 08-02 §5 — top 화면이 위에서 아래로 네 구역이고, 정렬 키는 마지막 구역(프로세스 목록)에 걸린다.
# 실측: debian:12 컨테이너, nice 10 무한 반복문을 띄운 채 `top -b -n 1` (2026-11-10). 구역마다 실제 줄을 옮겼다.
# 1차 자료(procps-ng top(1)): "m :Memory/Swap-Usage toggle — This command affects the two summary area
#       lines dealing with physical and virtual memory. This command serves as a 4-way toggle",
#       정렬 키 표 "M %MEM Yes" · "P %CPU Yes" · "N PID Yes" · "T TIME+ Yes",
#       "these commands do not appear on any help screen", "V :Forest-View-Mode toggle".
# 타입 스펙: type-layers — 위아래로 쌓인 화면 구역. 구역마다 이름 · 견줄 명령 · 실제 줄을 같은 자리에 반복한다.
#           오른쪽 열은 키와 그 키가 바꾸는 구역. focal 은 정렬이 걸리는 프로세스 목록과 M 키.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, PAPER, PAPER2, RULE, KR, MONO

W, H = 900, 500
LX, LW, GAP, Y0 = 24, 548, 10, 112
layers = [
    ("1 시스템 요약", "uptime 과 같음", ["top - 05:02:54 up 2:50, load average: 1.82, 1.64, 1.41"], INFO, 64),
    ("2 태스크 통계", "실행 · 수면 · 정지 · 좀비", ["Tasks: 6 total, 2 running, 4 sleeping, 0 zombie"], MUTED, 64),
    ("3 CPU 사용 통계", "vmstat 의 CPU 축 · 아래 두 줄은 free",
     ["%Cpu(s): 1.4 us, 0.5 sy, 14.8 ni, 81.9 id, 0.1 wa",
      "MiB Mem: 8004.2 total, 5286.1 free, 1884.1 used"], MUTED, 88),
    ("4 프로세스 목록", "ps aux 와 견줌 · 정렬 대상",
     ["3078 root 30 10 R 100.0 0.0 0:02.15 sh"], ACC, 64),
]

d = D(W, H, "LEARNING MODERN LINUX · 08-02 §5",
      "top 화면의 네 구역과 정렬 키",
      "nice 10 반복문이 CPU 하나를 다 쓰는 동안 찍은 top 화면을 구역별로 쌓았다. 오른쪽은 화면에서 쓰는 키다.",
      "메모리 정렬은 대문자 M, 소문자 m 은 메모리 두 줄의 표시 토글입니다")

y = Y0
for name, note, lines, col, lh in layers:
    focal = col is ACC
    if focal:
        d.tone(LX, y, LW, lh, ACC, 8, "12", 1.4)
    else:
        d.box(LX, y, LW, lh, PAPER2, col, 1.1, 8)
    d.t(LX + 16, y + 24, name, 13.5, ACC if focal else INK, KR, "start", 600)
    d.t(LX + LW - 16, y + 24, note, 11.5, MUTED, KR, "end")
    for j, ln in enumerate(lines):
        d.t(LX + 16, y + 48 + j * 24, ln, 11.5, col if col in (INFO, ACC) else MUTED, MONO, "start")
    y += lh + GAP
LBOT = y - GAP

KX = LX + LW + 20
KW = W - KX - 24
d.box(KX, Y0, KW, LBOT - Y0, PAPER, RULE, 1.1, 8)
d.t(KX + 16, Y0 + 26, "키", 12.5, INK, KR, "start", 600)
keys = [("?", "키 매핑 도움말", MUTED), ("V", "트리 보기 토글", MUTED),
        ("M", "%MEM 순 정렬", ACC), ("P", "%CPU 순 정렬", OK),
        ("k", "시그널 보내기", MUTED), ("q", "끝내기", MUTED),
        ("N T", "PID · TIME+ 정렬, 도움말에 없음", SOFT), ("m", "메모리 두 줄 표시 4단 토글", SOFT)]
for j, (k, desc, col) in enumerate(keys):
    ky = Y0 + 52 + j * 32
    d.chip(KX + 34, ky, k, col)
    d.t(KX + 64, ky + 4, desc, 11.5, col if col is not MUTED else INK, KR, "start", 600 if col is ACC else 400)

d.legend(H - 44, [("정렬이 걸리는 구역과 키", ACC), ("uptime 과 같은 줄", INFO),
                  ("CPU 정렬 키", OK), ("숨은 키와 토글", SOFT)])
d.save("08-02.top-screen.svg")
print("ok 08-02.top-screen")
