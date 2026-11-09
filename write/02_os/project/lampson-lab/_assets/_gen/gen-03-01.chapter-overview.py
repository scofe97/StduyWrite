# 03-01 학습 목표 뒤 전체 지도 — 절 넷이 토큰 검증에서 한계까지 간다.
# 타입 스펙: type-process — 칸마다 같은 의미 슬롯(절 번호 · 국면 · 그 절이 주는 것)이
#           반복되고 화살표가 읽는 순서를 나른다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 420
d = D(W, H, "LAMPSON LAB · 03-01",
      "principal 은 클라이언트가 고르지 않는다 — 읽는 순서",
      "절 넷. 요청이 어떻게 검증되는지에서 시작해 매핑이 principal 을 정하는 곳을 지나, 거부 경로와 남는 한계로 닫힌다.",
      "두 번째 절이 이 편의 핵심이다 — principal 은 요청이 아니라 SVID 의 신원에서 정해진다")

CW, CH, GAP, X0 = 404, 108, 24, 24
Y1, Y2 = 120, 252
cards = [
    ("§1", "검증 · X5C 토큰", "SVID 로 서명한 요청 · 체인 · 한 번만 사용"),
    ("§2", "결정 · 신원에서 principal 로", "매핑 한 행 · 요청은 대조만 · KeyID = SPIFFE ID"),
    ("§3", "거부 · 막는 층 넷", "토큰 · 템플릿 · policy · 수명"),
    ("§4", "한계 · 수명과 add-user", "인증서 수명 5분 상한 · 템플릿을 거치지 않는 인증서"),
]

def pos(i):
    return X0 + (i % 2) * (CW + GAP), (Y1 if i < 2 else Y2)

for i in range(3):
    x1, y1 = pos(i); x2, y2 = pos(i + 1)
    if y1 == y2:
        d.arrow([(x1 + CW, y1 + CH / 2), (x2 - 4, y2 + CH / 2)], MUTED, "ar", 1.4)
    else:
        cy = Y1 + CH + 16
        d.path(f"M {x1 + CW / 2} {y1 + CH} V {cy} H {X0 + CW / 2} V {y2 - 4}", MUTED, 1.4, m="ar")

for i, (n, title, mark) in enumerate(cards):
    x, y = pos(i)
    focal = (i == 1)
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{CW}" height="{CH}" rx="8" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y, CW, CH, PAPER2, RULE, 1.0, 8)
    d.t(x + 20, y + 30, n, 11, ACC if focal else SOFT, MONO, "start", 600)
    d.t(x + 20, y + 58, title, 15, ACC if focal else INK, KR, "start", 600)
    d.t(x + 20, y + 84, mark, 12, MUTED, KR, "start")

d.t(24, 392, "앞 편은 신원을 SVID 로 만들었다 — 이 편은 그 신원이 SSH 인증서가 되는 규칙이다", 12, SOFT, KR, "start")
d.save("03-01.chapter-overview.svg")
