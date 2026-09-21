# 04-02 학습 목표 뒤 전체 지도 — 절 넷을 "가른다 → 뚫린다 → 만든다 → 수명" 순으로 잇는다.
# 절 배열은 학습 순서다. 두 서명을 가르고(§1), 서명이 빠졌을 때 뚫리는 자리를 보고(§2),
# 그 인증서가 만들어지는 과정을 따라간 뒤(§3), 키의 수명을 가른다(§4).
# 타입 스펙: type-process — 칸마다 같은 의미 슬롯(절 번호 · 이름 · 그 절이 답하는 것)이 반복되고
#           화살표가 읽는 순서를 나른다. 주체가 없는 단계 지도라 lanes 를 쓰지 않는다.
#           focal 은 이 편의 중심 주장이 서는 칸 하나(§1 두 서명)다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, BAD, PAPER2, RULE, KR, MONO

W, H = 880, 400
d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 04-02",
      "인증서와 두 서명 — 읽는 순서",
      "핸드셰이크 한 번에 서명이 두 번 나온다. 인증서 안의 CA 서명과 ServerKeyExchange 의 서버 서명을 "
      "먼저 가르고, 뒤의 서명이 빠졌을 때 무엇이 뚫리는지 본다. 그다음 그 인증서가 만들어지는 세 걸음을 "
      "따라가고, 마지막으로 장기 키와 세션 키의 수명을 가른다.",
      "TLS 1.2 인증서 기반 핸드셰이크를 기준으로 읽습니다")

CW, CH, GAP, X0 = 400, 80, 24, 24
ROW, Y0 = 112, 116
cards = [
    ("§1", "서명이 둘인데 이름이 하나",  "주인 보증과 소유 증명",       "focal"),
    ("§2", "서명을 빼면 뚫리는 자리",    "인증서는 통과 · 값만 교체",   BAD),
    ("§3", "인증서는 어떻게 만들어지는가", "키 · CSR · 서명 세 걸음",    None),
    ("§4", "같은 키 파일과 매번 새 키",   "장기 키와 세션 키의 수명",    None),
]

def pos(i):
    return X0 + (i % 2) * (CW + GAP), Y0 + (i // 2) * ROW

for i, (num, title, q, mark) in enumerate(cards):
    x, y = pos(i)
    if mark == "focal":
        d.o.append(f'<rect x="{x}" y="{y}" width="{CW}" height="{CH}" rx="8" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
        col = ACC
    elif mark:
        d.tone(x, y, CW, CH, mark, 8); col = mark
    else:
        d.box(x, y, CW, CH, PAPER2, RULE, 1.0, 8); col = INK
    d.t(x + 20, y + 32, num, 12, SOFT, MONO, "start", 600)
    d.t(x + 56, y + 32, title, 14, col, KR, "start", 600)
    d.t(x + 56, y + 56, q, 13, MUTED, KR, "start")

for i in range(len(cards) - 1):
    x0, y0 = pos(i); x1, y1 = pos(i + 1)
    if y0 == y1:
        d.arrow([(x0 + CW, y0 + CH / 2), (x1 - 6, y1 + CH / 2)], MUTED, "ar", 1.4)
    else:
        d.arrow([(x0 + CW / 2, y0 + CH), (x0 + CW / 2, y0 + CH + 16),
                 (x1 + CW / 2, y0 + CH + 16), (x1 + CW / 2, y1 - 6)], MUTED, "ar", 1.4)

d.t(24, 344, "범위: TLS 1.2 인증서 기반 · TLS 1.3 은 CertificateVerify 로 자리가 옮겨감",
     12, SOFT, KR, "start")

d.legend(H - 40, [("이 편의 중심", ACC), ("서명이 없을 때", BAD)])
d.save("04-02.chapter-overview.svg")
