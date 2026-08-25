# 02-02.ipvs-forwarding-modes — 세 포워딩 방식이 패킷의 어느 부분을 바꾸는가
# 본문 요구: "NAT 는 주소 재작성 / DR 은 IP 그대로 목적지 MAC 만 / IP 터널링은 원본을
#           다른 IP 데이터그램으로 감쌈" — 셋이 건드리는 자리가 다르다는 것이 논점.
#           책이 DR 과 터널링 설명을 뒤바꿔 인쇄했으므로 focal 은 DR 의 MAC 셀에 건다.
# 타입 스펙: 비교 행렬 — 행이 방식, 열이 패킷의 구성부. 공식 없는 타입이라 stride 로 배치.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, WARN, INFO, PAPER2, KR, MONO

W, H = 1000, 576
d = D(W, H, "IPVS · FORWARDING MODES",
      "세 포워딩 방식은 패킷의 어느 부분을 바꾸는가",
      "NAT 는 IP 를, DR 은 목적지 MAC 만 바꾸고, IP 터널링은 원본을 그대로 둔 채 새 IP 헤더로 감싼다.",
      lead="바꾸는 자리가 다르다 — NAT 는 L3, DR 은 L2, 터널링은 겉을 한 겹 더 씌운다")

X0, TXTX, CELLX = 24, 48, 380      # stride 4 배수
CW, GAP, CH = 176, 16, 56
BANDS = [108, 244, 380]            # 높이 120, 간격 16
BH = 120

ROWS = [
    ("NAT", ["주소를 재작성합니다"],
     [("MAC 헤더", "그대로", INFO, CW),
      ("IP 헤더", "목적지 재작성", WARN, CW),
      ("페이로드", "그대로", INFO, CW)]),
    ("DR — Direct Routing", ["IP 는 그대로 둔 채 목적지 MAC 만", "바꿔 백엔드로 넘깁니다"],
     [("MAC 헤더", "목적지 재작성", ACC, CW),
      ("IP 헤더", "그대로", INFO, CW),
      ("페이로드", "그대로", INFO, CW)]),
    ("IP 터널링", ["원본 패킷을 다른 IP 데이터그램으로", "감싸 보냅니다"],
     [("새 IP 헤더", "바깥에 씌운다", WARN, CW),
      ("원본 패킷 그대로", "MAC · IP · 페이로드", INFO, CW * 2 + GAP)]),
]

for y0, (name, lines, cells) in zip(BANDS, ROWS):
    ddx.band(d, y0, y0 + BH, name, x=X0, w=W - 2 * X0, focal=False)
    for i, ln in enumerate(lines):
        d.t(TXTX, y0 + 68 + i * 22, ddx.fit(ln, 12, CELLX - TXTX - 24, ln), 12, MUTED, KR, "start")
    x = CELLX
    for label, note, c, w in cells:
        y = y0 + 44
        if c is ACC:
            d.tone(x, y, w, CH, ACC, 6, "12", 1.4)
        else:
            d.box(x, y, w, CH, PAPER2, c, 1.1, 6)
        d.t(x + w // 2, y + 24, ddx.fit(label, 12, w - 20, label), 12, c, KR, "middle", 600)
        d.t(x + w // 2, y + 43, ddx.fit(note, 11, w - 20, note), 11,
            MUTED if c is not ACC else ACC,
            MONO if all(ord(ch) < 128 or ch in '·' for ch in note) else KR)
        x += w + GAP

d.t(X0 + 12, 524, "책은 DR 을 \"캡슐화\", 터널링을 \"MAC 재작성\"으로 인쇄했지만 둘이 뒤바뀐 것이다",
    12, MUTED, KR, "start")
d.legend(536, [("그대로", INFO), ("바뀌는 자리", WARN), ("책이 뒤바꿔 설명한 곳", ACC)])
d.save("02-02.ipvs-forwarding-modes.svg")
print("ok ipvs-forwarding-modes")
