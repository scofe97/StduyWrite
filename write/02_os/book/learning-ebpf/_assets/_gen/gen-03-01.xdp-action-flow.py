# 타입 스펙: type-flowchart — 네트워크 패킷 도착 시 XDP 진입부터 판정 반환값 분기까지의 실행 흐름
# 사실 출처: v7.2 include/uapi/linux/bpf.h L6576~6582, 《Learning eBPF》 Ch.3 L197~202, 본문 §2
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 960, 520
d = D(W, H, "LEARNING EBPF · 03-01 §2",
      "XDP Hello World 패킷 처리와 xdp_action 판정 분기",
      "네트워크 패킷이 도착하면 hello() 가 카운터를 올리고 XDP_PASS(2) 를 반환합니다",
      "패킷 수신 · bpf_printk 출력 · 전역 변수 증가 · 5가지 xdp_action 판정")

# 좌측 메인 실행 흐름 (세로)
LX, LW = 50, 320
STEPS = [
    ("패킷 수신", "네트워크 인터페이스(NIC) 도착", PAPER2, RULE, 110),
    ("hello(struct xdp_md *ctx)", "XDP 훅 진입점 실행", PAPER2, RULE, 178),
    ("bpf_printk()", "\"Hello World %d\" 출력", PAPER2, RULE, 246),
    ("counter++", "전역 카운터 1 증가", WARN, WARN, 314),
]

for title, sub, fill, stroke, y in STEPS:
    if fill == PAPER2:
        d.box(LX, y, LW, 46, PAPER2, RULE, 1.0, 6)
        d.t(LX + LW//2, y + 20, title, 13, INK, MONO if "(" in title else KR, "middle", 600)
        d.t(LX + LW//2, y + 36, sub, 11, MUTED, KR, "middle")
    else:
        d.tone(LX, y, LW, 46, stroke, 6, "12", 1.2)
        d.t(LX + LW//2, y + 20, title, 13, stroke, MONO if "(" in title or "++" in title else KR, "middle", 600)
        d.t(LX + LW//2, y + 36, sub, 11, MUTED, KR, "middle")

for i in range(len(STEPS) - 1):
    y1 = STEPS[i][4] + 46
    y2 = STEPS[i+1][4]
    d.arrow([(LX + LW//2, y1), (LX + LW//2, y2 - 2)], MUTED, "ar", 1.4)

# counter++ 에서 분기점으로 화살표
BY = 384
d.tone(LX + 40, BY, LW - 80, 44, ACC, 6, "15", 1.2)
d.t(LX + LW//2, BY + 20, "return 판정 분기", 13, ACC, KR, "middle", 600)
d.t(LX + LW//2, BY + 34, "enum xdp_action", 11, MUTED, MONO, "middle")
d.arrow([(LX + LW//2, 360), (LX + LW//2, BY - 2)], ACC, "acc", 1.4)

# 우측 xdp_action 5가지 분기
RX, RW, RH = 460, 450, 50
ACTIONS = [
    ("0: XDP_ABORTED", "오류로 버림", BAD, False),
    ("1: XDP_DROP", "버림", BAD, False),
    ("2: XDP_PASS", "네트워크 스택으로 전달", OK, True),
    ("3: XDP_TX", "들어온 인터페이스로 반송", INFO, False),
    ("4: XDP_REDIRECT", "다른 곳으로 전달", INFO, False),
]

AY0 = 110
A_STRIDE = 64

# 분기선
for i, (name, desc, c, is_pass) in enumerate(ACTIONS):
    ay = AY0 + i * A_STRIDE
    if is_pass:
        d.tone(RX, ay, RW, RH, c, 6, "18", 1.4)
        d.t(RX + 16, ay + 22, name, 13, c, MONO, "start", 700)
        d.t(RX + 16, ay + 40, desc, 11, INK, KR, "start")
        d.chip(RX + RW - 70, ay + 25, "예제 반환값", c, 11)
    else:
        d.box(RX, ay, RW, RH, PAPER2, RULE, 0.9, 6)
        d.t(RX + 16, ay + 22, name, 12, c, MONO, "start", 600)
        d.t(RX + 16, ay + 40, desc, 11, MUTED, KR, "start")

    # 연결 화살표 (엘보)
    mid_x = 420
    sy = BY + 22
    ey = ay + RH//2
    mc = c if is_pass else MUTED
    mk = "ok" if is_pass else "ar"
    sw = 1.6 if is_pass else 1.2
    d.arrow([(LX + LW - 40, sy), (mid_x, sy), (mid_x, ey), (RX - 4, ey)], mc, mk, sw)

d.legend(H - 46, [
    ("예제 반환값 PASS", OK),
    ("폐기 계열", BAD),
    ("카운터 갱신", WARN),
    ("전송·리다이렉트", INFO),
    ("실행 분기점", ACC),
])

d.save("03-01.xdp-action-flow.svg")
