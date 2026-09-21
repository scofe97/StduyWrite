# README 「읽는 순서」 — 장 열을 읽는 순서로 잇고, 설계 문제로 빠지는 지점을 옆에 건다.
# 본문이 "기준을 먼저 잡고, 요청이 데이터에 닿는 순서로 내려간 다음 옆으로 넓히며, 줄이 끝날 때마다 문제를 하나 푼다"고 말한다.
# 타입 스펙: type-process — 장마다 같은 의미 슬롯(번호 · 이름 · 담는 것)이 반복되고 화살표가 읽는 순서를 나른다.
#           축약: 주체(lane)가 없는 단계 지도라 §1 lanes 와 §2 공식을 쓰지 않고 카드 stride 로 놓는다
#           (visual-diagram-selection §알려진 공백 "주체 없는 단계 지도" 관례).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, PAPER2, RULE, KR, MONO

W, H = 880, 624
d = D(W, H, "THE SYSTEM DESIGN PRIMER · READING ORDER",
      "기준을 먼저, 그다음은 요청이 내려가는 순서로",
      "01 · 02 장으로 기준을 잡고, 03 → 04 → 05 장으로 요청이 데이터에 닿는 길을 따라 내려간 뒤, 06 → 07 → 08 장으로 넓히고 09 장으로 닫는 읽기 순서. 줄이 끝나는 자리마다 10 장의 설계 문제로 빠진다.",
      "줄이 끝날 때마다 오른쪽의 설계 문제를 하나씩 풉니다")

CW, CH, SX, SY, X0, Y0 = 188, 72, 212, 120, 24, 112     # 카드 · stride
rows = [
    ("먼저 잡는 기준", [("01", "접근법", "4단계 · 규모 추정"), ("02", "트레이드오프", "CAP · 일관성 · 가용성")]),
    ("요청이 데이터에 닿기까지", [("03", "진입 경로", "DNS · CDN · 로드 밸런서"), ("04", "애플리케이션 계층", "마이크로서비스 · 디스커버리"), ("05", "데이터베이스", "복제 · 샤딩 · NoSQL")]),
    ("빠르게 하고 떼어 놓기", [("06", "캐시", "계층 · 갱신 전략"), ("07", "비동기", "큐 · 백프레셔"), ("08", "통신", "HTTP · RPC · REST")]),
    ("닫기", [("09", "보안", "암호화 · 검증 · 최소 권한")]),
]
probs = {1: ["Pastebin · Bit.ly"], 2: ["Twitter 타임라인", "웹 크롤러"], 3: ["수백만 사용자 on AWS"]}
BX, BW = 672, 184

def xy(r, c): return X0 + c * SX, Y0 + r * SY

# 연결선 먼저
for r, (_, cards) in enumerate(rows):
    for c in range(len(cards) - 1):
        x, y = xy(r, c)
        d.arrow([(x + CW, y + CH / 2), (x + SX, y + CH / 2)], MUTED, "ar", 1.4)
    if r < len(rows) - 1:                                  # 줄바꿈 — ㄷ자
        x, y = xy(r, len(cards) - 1); nx, ny = xy(r + 1, 0)
        d.arrow([(x + CW / 2, y + CH), (x + CW / 2, y + CH + 16), (nx + CW / 2, y + CH + 16), (nx + CW / 2, ny)], MUTED, "ar", 1.4)
    if r in probs:                                         # 문제로 빠지는 점선
        x, y = xy(r, len(cards) - 1)
        d.arrow([(x + CW, y + CH / 2 + 16), (BX, y + CH / 2 + 16)], INFO, "info", 1.0, "4 3")

# 카드
for r, (lab, cards) in enumerate(rows):
    x, y = xy(r, 0)
    lx, _ = xy(r, len(cards) - 1)
    if len(cards) < 3: d.t(lx + CW + 16, y + CH / 2 + 4, lab, 12, SOFT, KR, "start")
    else: d.t(lx + CW, y - 10, lab, 12, SOFT, KR, "end")
    for c, (n, title, sub) in enumerate(cards):
        x, y = xy(r, c); focal = n == "02"
        if focal:
            d.o.append(f'<rect x="{x}" y="{y}" width="{CW}" height="{CH}" rx="8" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
        else:
            d.box(x, y, CW, CH, PAPER2, RULE, 1.0, 8)
        d.t(x + 14, y + 22, n, 11, ACC if focal else SOFT, MONO, "start", 600)
        d.t(x + 40, y + 23, title, 14, ACC if focal else INK, KR, "start", 600)
        d.t(x + 14, y + 52, sub, 12, MUTED, KR, "start")

# 10장 띠
by = Y0 + SY
d.tone(BX, by - 40, BW, 2 * SY + CH + 40 + 16, INFO, 8, "10", 1.0)
d.t(BX + 14, by - 16, "10", 11, INFO, MONO, "start", 600)
d.t(BX + 40, by - 15, "설계 문제 풀이", 14, INK, KR, "start", 600)
for r, items in probs.items():
    _, y = xy(r, 0)
    for i, it in enumerate(items):
        d.t(BX + 14, y + CH / 2 + 20 + i * 20, it, 12, MUTED, KR, "start")

d.legend(568, [("읽는 순서", MUTED), ("문제로 빠지는 자리", INFO), ("모든 장의 기준", ACC)])
d.save("00-00.reading-order.svg")
