# 10-01 §3 — 지연 여섯 가지가 각각 타임라인의 어느 구간을 재는가.
# 타입 스펙: type-process — 칸마다 같은 의미 슬롯(무엇을 재나 · 무엇이 섞이나)이 반복되고
#           가로 위치가 연결 수립의 시간 순서를 나른다.
#           축약: 주체(lane)가 없는 구간 지도라 §1 lanes 와 §2 공식을 쓰지 않고
#           눈금 x 를 stride 로 고정해 막대를 놓는다
#           (visual-diagram-selection §알려진 공백 "주체 없는 단계 지도" 관례, cntd 01-04 와 동일).
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, INFO, PAPER, PAPER2, RULE, KR, MONO



W, H = 976, 560
X0, XE = 132, 928
AXIS = 128          # 눈금 라벨 기준선
BAR_Y, BAR_H, BAR_STRIDE = 168, 32, 44

# 시간 순서 눈금 — 4의 배수로 고정
T = {"start": 132, "syn": 244, "est": 372, "byte": 468, "close": 560}

d = DK(W, H, "SYSTEMS PERFORMANCE · 10-01 §3",
      "지연 여섯 가지 — 어디서 무엇을 재는가",
      "클라이언트가 서버에 연결할 때의 지연. 여섯은 서로 다른 구간을 재고, 그중 첫 바이트 지연만 서버의 think time 을 품는다.",
      "여럿을 같이 재야 '느리다' 가 네트워크 탓인지 서버 탓인지 갈립니다")

# 눈금선
for k in ("start", "syn", "est", "byte", "close"):
    d.line(T[k], AXIS + 8, T[k], BAR_Y + 6 * BAR_STRIDE + 8, RULE, 1.0, "3 6")

for k, lab in (("start", "이름 해석 시작"), ("syn", "SYN 전송"), ("est", "연결 수립"),
               ("byte", "첫 바이트"), ("close", "연결 종료")):
    d.t(T[k], AXIS, lab, 13, SOFT, KR, "middle")

# (라벨, 시작, 끝, 무엇이 섞이나, 색)
BARS = [
    ("이름 해석", "start", "syn", "DNS 조회 — 타임아웃이면 수십 초", None),
    ("연결", "syn", "est", "TCP 핸드셰이크 — SYN 드롭 시 재전송 1초+", None),
    ("첫 바이트 (TTFB)", "est", "byte", "서버 think time 이 들어온다", ACC),
    ("연결 수명", "start", "close", "수립부터 종료까지 — keep-alive 로 늘린다", None),
]

for i, (name, a, b, note, c) in enumerate(BARS):
    y = BAR_Y + i * BAR_STRIDE
    x1, x2 = T[a], T[b]
    if c: d.tone(x1, y, x2 - x1, BAR_H, c, 6)
    else: d.box(x1, y, x2 - x1, BAR_H, PAPER2, RULE, 1.0, 6)
    d.t(x1 - 12, y + 21, name, 12, c if c else INK, KR, "end", 600)
    # 주석은 막대 밖 오른쪽에 둔다 — 짧은 막대 안에 넣으면 변을 넘는다
    d.t(x2 + 12, y + 21, note, 13, c if c else MUTED, KR, "start")

# ping · RTT 는 연결 수립과 무관한 왕복 한 번 — 시간축에서 떼어 별도 행으로 둔다
y = BAR_Y + 4 * BAR_STRIDE + 12
d.t(T["start"] - 12, y + 21, "ping · RTT", 13, INFO, KR, "end", 600)
d.tone(T["start"], y, 104, BAR_H, INFO, 6)
d.t(T["start"] + 12, y + 21, "왕복 한 번", 13, INFO, KR, "start")
d.t(T["start"] + 128, y + 21, "ICMP echo — 전파 + 홉마다의 처리. 라우터가 우선순위를 달리 줄 수 있습니다",
    13, MUTED, KR, "start")

y2 = y + BAR_STRIDE + 16
d.t(X0 - 12, y2, "서버 think time 이 섞이는 것은 TTFB 하나뿐입니다 — ping·연결 지연과 TTFB 의 차이가 네트워크와 서버를 가릅니다",
    13, MUTED, KR, "start")
d.t(X0 - 12, y2 + 24, "localhost ping 을 1초로 잡으면 — 같은 서브넷 10GbE 4초 · Wi-Fi 1분 · SF→뉴욕 13분 · SF→호주 1시간",
    13, SOFT, KR, "start")

d.legend(y2 + 48, [("서버 think time 을 품는 지연", ACC), ("네트워크만 재는 왕복", INFO), ("구간 지연", MUTED)])
d.save("10-01.network-latency-types.svg")
