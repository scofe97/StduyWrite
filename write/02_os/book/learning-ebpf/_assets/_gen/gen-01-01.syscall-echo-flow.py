# 타입 스펙: type-data-flow — echo "hello" 실행 시 사용자 공간에서 시스템 콜을 거쳐 커널 및 터미널 출력으로 전달되는 데이터 흐름
# 사실 출처: 원문 ebpf1.txt 230-255(strace -c echo "hello" 출력 111회 호출, openat 30회, mmap 20회, write 1회)
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 460
d = D(W, H, "LEARNING EBPF · 01-01 §2", "echo 명령 실행 시의 시스템 콜 흐름과 eBPF 관측 지점",
      "단순한 문자열 출력도 예제 환경에서 111회 시스템 콜을 부릅니다",
      "strace -c 예제 출력: 총 111회 호출 · openat 30회 · mmap 20회 · write 1회")

# 상단: 4개 단계 박스 (Left to Right)
CW, GAP, X0, Y_TOP, CH = 196, 28, 28, 110, 140
steps = [
    ("01 실행 준비", "execve 1회", "echo 프로세스 기동", "바이너리 적재 시작", INFO),
    ("02 파일 열기·닫기", "openat 30회 · 12회 실패", "close 20회", "파일이 없으면 실패", WARN),
    ("03 메모리 매핑", "mmap 20회", "mprotect 4회", "가상 메모리 주소 매핑", WARN),
    ("04 화면 출력", "write 1회", "문자열 hello", "터미널로 전달", ACC),
]

for i, (title, c1, c2, c3, col) in enumerate(steps):
    x = X0 + i * (CW + GAP)
    cx = x + CW / 2
    if col == ACC:
        d.tone(x, Y_TOP, CW, CH, ACC, r=6, op="14", sw=1.3)
    else:
        d.box(x, Y_TOP, CW, CH, PAPER2, RULE, 0.9, 6)

    d.t(cx, Y_TOP + 24, title, 13, col, KR, "middle", 600)
    d.line(x + 10, Y_TOP + 36, x + CW - 10, Y_TOP + 36, RULE, 0.6)

    d.t(cx, Y_TOP + 60, c1, 14, col, MONO, "middle", 600)
    d.t(cx, Y_TOP + 84, c2, 12, INK, KR if "동반" in c2 or "출력" in c2 or "문자열" in c2 else MONO, "middle")
    d.t(cx, Y_TOP + 110, c3, 11, MUTED, KR, "middle")

    if i < len(steps) - 1:
        ax = x + CW
        d.arrow([(ax + 2, Y_TOP + CH / 2), (ax + GAP - 2, Y_TOP + CH / 2)], MUTED, "ar", 1.2)

# 하단: 커널 공간 및 eBPF 관측 레이어
KY, KH = 280, 128
d.tone(X0, KY, W - X0 * 2, KH, INFO, r=6, op="08", sw=1.1)
d.t(X0 + 16, KY + 24, "커널 공간 eBPF 관측 계층", 13, INFO, KR, "start", 600)
d.t(W / 2, KY + 116, "애플리케이션 수정 없이 시스템 콜 진입점(sys_enter)에서 관측", 11, MUTED, KR, "middle")

# eBPF 훅 카드 3개
HW = 176
hooks = [
    ("openat 진입점", "어떤 파일을 여는지", "호출 빈도 집계", OK),
    ("mmap 진입점", "메모리 매핑 호출 관측", "호출 빈도 집계", OK),
    ("write 진입점", "출력 호출 관측", "호출 빈도 집계", ACC),
]

for i, (fn, desc, effect, col) in enumerate(hooks):
    hcx = X0 + (i + 1) * (CW + GAP) + CW / 2
    hx = hcx - HW / 2
    d.box(hx, KY + 38, HW, 56, PAPER, RULE, 0.8, 4)
    d.t(hcx, KY + 58, fn, 12, col, KR, "middle", 600)
    d.t(hcx, KY + 78, desc, 11, MUTED, KR, "middle")

    # 상단 단계에서 하단 훅으로 화살표
    step_x = hcx
    d.arrow([(step_x, Y_TOP + CH), (step_x, KY + 34)], col, "acc" if col == ACC else "ok", 1.2, dash="3 3")

d.legend(420, [
    ("프로세스 시작", INFO),
    ("자원 준비 호출", WARN),
    ("최종 I/O 실행", ACC),
    ("eBPF 훅 관측", OK),
])
d.save("01-01.syscall-echo-flow.svg")
