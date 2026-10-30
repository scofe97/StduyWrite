# 타입 스펙: type-data-flow — 들어오는 패킷 하나가 지나는 다섯 층(NIC · 드라이버 · sk_buff 생성 · TC ingress · 네트워크 스택)을 가로로 놓고, 판정 코드마다 끝점이 달라지는 세로 목록을 층 아래에 붙인다. 나가는 쪽은 스택 아래의 TC egress 하나뿐이다.
# 사실 출처: 예제 저장소 lizrice/learning-ebpf chapter8 (HEAD 91ded4a) 의 hello.bpf.c·network.bpf.c,
#   linux v7.2 include/uapi/linux/bpf.h 6571~6582행(enum xdp_action: XDP_ABORTED=0, XDP_DROP=1, XDP_PASS=2, XDP_TX=3, XDP_REDIRECT=4)·6587~6596행(struct xdp_md),
#   include/uapi/linux/pkt_cls.h 63~71행(TC_ACT_UNSPEC=-1, TC_ACT_OK=0, TC_ACT_SHOT=2, TC_ACT_REDIRECT=7),
#   추출본 ebpf8.txt 459~475행(오프로드 XDP 는 드랍·되돌림을 호스트 CPU 없이 처리)·497~508행(TC 는 sk_buff, XDP 는 그 전)·529~533행(TC 는 양방향, XDP 는 들어오는 쪽).
# Layout conventions: 층 상자 152×72, 간격 44(x=32 시작), 판정 상자 160×44 stride 52, 레일 x=col_x+8. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 1000, 580
d = D(W, H, "LEARNING EBPF · 08-01",
      "들어오는 패킷 하나가 XDP 와 TC 의 판정을 차례로 거친다",
      "패킷은 NIC 의 오프로드 XDP, 드라이버의 네이티브 XDP, sk_buff 생성, TC ingress, 네트워크 스택 순으로 지난다. XDP 의 판정은 XDP_ABORTED 0, XDP_DROP 1, XDP_PASS 2, XDP_TX 3, XDP_REDIRECT 4 이고 TC 의 판정은 TC_ACT_OK 0, TC_ACT_SHOT 2, TC_ACT_REDIRECT 7 이다. 나가는 쪽은 TC egress 만 있다.",
      "판정마다 패킷이 멈추거나 되돌아가는 자리가 다릅니다")

NW, NH = 152, 72
COLX = [32, 228, 424, 620, 816]
TOP = 112
TW, TH, TS = 160, 44, 52

NODES = [
    ("NIC", "오프로드 XDP", None, MUTED),
    ("드라이버", "네이티브 XDP", "xdp_md", MUTED),
    ("sk_buff 생성", "XDP 이후", "TC 이전", MUTED),
    ("TC ingress", "분류기 · 동작", "__sk_buff", MUTED),
    ("네트워크 스택", "프로토콜 처리", None, OK),
]
for x, (nm, s1, s2, c) in zip(COLX, NODES):
    d.tone(x, TOP, NW, NH, c, 6, "12", 1.2)
    d.t(x + NW / 2, TOP + 24, nm, 14, c, KR, "middle", 600)
    d.t(x + NW / 2, TOP + 44, s1, 12, MUTED, KR)
    if s2:
        d.t(x + NW / 2, TOP + 62, s2, 12, MUTED, MONO if s2.startswith(("xdp_", "__")) else KR)
for i in range(4):
    y = TOP + NH // 2
    d.arrow([(COLX[i] + NW + 2, y), (COLX[i + 1] - 6, y)], MUTED, "ar", 1.5)

# 판정 목록: (코드, 값, 뜻, 색)
EXITS = {
    0: [("XDP_DROP", "1", "버림 · 호스트 CPU 0", BAD), ("XDP_TX", "3", "같은 포트로", INFO)],
    1: [("XDP_ABORTED", "0", "오류로 버림", WARN), ("XDP_DROP", "1", "버림", BAD),
        ("XDP_PASS", "2", "다음 층으로", OK), ("XDP_TX", "3", "들어온 장치로", INFO),
        ("XDP_REDIRECT", "4", "다른 장치로", INFO)],
    3: [("TC_ACT_OK", "0", "다음 층으로", OK), ("TC_ACT_SHOT", "2", "버림", BAD),
        ("TC_ACT_REDIRECT", "7", "다른 장치로", INFO)],
}
for col, items in EXITS.items():
    x = COLX[col]
    rail = x + 8
    y0 = TOP + NH + 28
    last = y0 + TS * (len(items) - 1) + TH // 2
    d.line(rail, TOP + NH, rail, last, RULE, 1.2)
    for k, (code, val, mean, c) in enumerate(items):
        y = y0 + TS * k
        d.arrow([(rail, y + TH // 2), (x + 20, y + TH // 2)], c, "info" if c == INFO else "ar", 1.3)
        d.tone(x + 24, y, TW, TH, c, 6, "12", 1.2)
        d.t(x + 24 + 10, y + 18, f"{code} · {val}", 12, c, MONO, "start", 600)
        d.t(x + 24 + 10, y + 35, mean, 11, MUTED, KR, "start")

# 나가는 쪽
ex = COLX[4]
d.arrow([(ex + NW / 2, TOP + NH + 2), (ex + NW / 2, TOP + NH + 40)], MUTED, "ar", 1.5)
d.tone(ex, TOP + NH + 44, NW, NH, ACC, 6, "1F", 1.4)
d.t(ex + NW / 2, TOP + NH + 44 + 28, "TC egress", 14, ACC, KR, "middle", 600)
d.t(ex + NW / 2, TOP + NH + 44 + 50, "__sk_buff", 12, MUTED, MONO)
d.chip(ex + NW / 2, TOP + NH + 44 + NH + 28, "XDP 는 들어오는 쪽만", ACC, 11)

d.legend(H - 56, [("버림", BAD), ("오류로 버림", WARN), ("다음 층", OK), ("되돌림·넘김", INFO), ("나가는 쪽", ACC)])
d.save("08-01.chapter-overview.svg")
