# 07-01 §1 — "서버가 더 이상 요청을 받지 못한다"는 결과 하나에 모이는 네 갈래.
# 원문 The DOS attack 절의 첫 문장이 결과이고, 7장이 조사하는 갈래가 뼈다.
# 타입 스펙: type-fishbone — 관찰된 결과 하나, 조사한 갈래를 뼈로, 갈래마다 하위 근거 둘.
#           축약: 스펙 기준 캔버스(HEAD=1200 · viewBox 1440)는 이 책의 폭 규약(880~1000)을 넘으므로
#           60° 를 유지한 채 등축 축소한다 — dx/dy 를 96/168 에서 64/112 로(비 1.75 유지),
#           bone 간격 160 에서 132 로, HEAD 1200 에서 780 으로.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 1000, 512
CY, HEAD = 300, 780
DX, DY, STRIDE = 64, 112, 132

d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 07-01 §1",
      "서비스를 무너뜨리는 네 갈래",
      "원문 7장이 다루는 DoS 갈래를 결과 하나 아래 모은 것. 갈래마다 캡처에서 읽히는 근거가 다르고, 강조한 갈래는 원문의 예제 캡처가 실제로 확인해 주는 하나다.",
      "겨냥하는 층은 넷 다 다르지만 남기는 결과는 같습니다")

BONES = [
    ("L4 · SYN 홍수", "tcp.flags.syn", ["반쪽 연결이 쌓임", "FIN·PUSH 가 0"], False),
    ("L3 · ICMP 홍수", "icmp", ["echo reply 가 없음", "한 방향 대화 하나"], True),
    ("L7 · SSL 홍수", "tls", ["정상 트래픽과 닮음", "비용이 서버로 쏠림"], False),
    ("반사·증폭 · DrDoS", "udp", ["출발지가 위조됨", "공개 서버가 대신"], False),
]

d.arrow([(120, CY), (HEAD - 4, CY)], INK, "ar", 1.2)

for k, (label, sub, causes, focal) in enumerate(BONES, start=1):
    ax = HEAD - 60 - k * STRIDE
    up = -1 if k % 2 else 1
    fx, fy = ax - DX, CY + up * DY
    c = ACC if focal else MUTED
    d.line(ax, CY, fx, fy, c, 1.4 if focal else 1.1)
    for m in (1, 2):
        f = m / 3
        tx, ty = ax - DX * f, CY + up * DY * f
        d.line(tx, ty, tx - 32, ty, SOFT, 1.0)
        d.t(tx - 36, ty - 6 if up < 0 else ty + 14, causes[m - 1], 11, MUTED, KR, "end")

for k, (label, sub, causes, focal) in enumerate(BONES, start=1):
    ax = HEAD - 60 - k * STRIDE
    up = -1 if k % 2 else 1
    fx, fy = ax - DX, CY + up * DY
    if focal: d.tone(fx - 88, fy - 18, 176, 36, ACC, 4)
    else: d.box(fx - 88, fy - 18, 176, 36, PAPER2, RULE, 1.0, 4)
    d.t(fx, fy - 1, label, 12, ACC if focal else INK, KR, "middle", 600)
    d.t(fx, fy + 14, sub, 9, MUTED, MONO)

d.tone(HEAD, CY - 32, 200, 64, ACC, 8)
d.t(HEAD + 100, CY - 4, "서버가 더 이상", 12, ACC, KR, "middle", 600)
d.t(HEAD + 100, CY + 16, "요청을 받지 못합니다", 12, ACC, KR, "middle", 600)

d.legend(H - 60, [("원문 캡처가 확인한 갈래", ACC), ("장이 함께 다루는 갈래", MUTED)])
d.save("07-01.dos-families.svg")
