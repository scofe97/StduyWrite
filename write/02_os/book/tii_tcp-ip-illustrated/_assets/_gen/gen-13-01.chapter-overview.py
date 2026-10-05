# 13-01 학습 목표 뒤 전체 지도 — 이 편의 절 일곱을 두 묶음(연결의 생애 · 연결을 지키는 장치)으로 잇는다.
# 타입 스펙: type-process — 칸마다 같은 의미 슬롯(절 번호 · 이름 · 그 절이 답하는 물음)이 반복되고 화살표가 읽는 순서를 나른다.
#           축약: 주체(lane)가 없는 단계 지도라 §1 lanes 와 §2 공식을 쓰지 않고 카드 두 열 stride 로 놓는다
#           (visual-diagram-selection §알려진 공백 "주체 없는 단계 지도" 관례, 12-01 이전 편들과 같은 선택).
#           focal 은 로드맵의 빈 행(half-close)을 채우는 §3 한 칸.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 920, 600
d = D(W, H, "TCP/IP ILLUSTRATED VOL.1 · 13-01",
      "TCP 연결 수립과 종료 — 읽는 순서",
      "13.1·13.2 를 정리한 이 편의 절 일곱을 두 묶음으로 나눈 지도다. 왼쪽 열은 연결 하나가 열리고 닫히는 생애를, 오른쪽 열은 그 생애를 "
      "옛 세그먼트·응답 없는 상대·중간 장비로부터 지키는 장치를 따라간다. 칸 아래 줄이 그 절이 답하는 물음이다.",
      "왼쪽 열이 정상 경로, 오른쪽 열이 그 경로가 어긋나는 자리입니다")

CW, CH, GAP_X, GAP_Y = 420, 80, 32, 24
X = [24, 24 + CW + GAP_X]
Y0 = 132
COLS = [
    ("연결의 생애 · 13.2–13.2.2", [
        ("§1", "연결은 4-tuple 과 세 국면", "연결이란 정확히 무엇인가"),
        ("§2", "3-way handshake", "세 세그먼트가 무엇을 교환하나"),
        ("§3", "네 번의 닫기와 half-close", "한 방향만 닫으면 무엇이 남나"),
        ("§4", "동시 열기 · 동시 닫기", "양쪽이 함께 시작하면"),
    ]),
    ("연결을 지키는 장치 · 13.2.3–13.2.6", [
        ("§5", "초기 순서 번호 ISN", "옛 연결의 세그먼트를 어떻게 막나"),
        ("§6", "연결 수립 타임아웃", "상대가 없으면 몇 번, 얼마 간격으로"),
        ("§7", "NAT 와 연결 추적", "중간 장비는 연결을 어떻게 따라가나"),
    ]),
]
FOCAL = (0, 2)

def pos(c, r): return X[c], Y0 + 28 + r * (CH + GAP_Y)

# 연결선 먼저
for c, (_, cards) in enumerate(COLS):
    for r in range(len(cards) - 1):
        x, y = pos(c, r)
        d.arrow([(x + CW / 2, y + CH), (x + CW / 2, y + CH + GAP_Y - 4)], MUTED, "ar", 1.4)
# 왼쪽 열 끝 → 오른쪽 열 처음 (아래 corridor 로 돌아 위로)
xl, yl = pos(0, 3); xr, yr = pos(1, 0)
cy = yl + CH + 16
cx_mid = X[0] + CW + GAP_X / 2
d.arrow([(xl + CW / 2, yl + CH), (xl + CW / 2, cy), (cx_mid, cy), (cx_mid, yr + CH / 2), (xr - 4, yr + CH / 2)], MUTED, "ar", 1.4)

for c, (head, cards) in enumerate(COLS):
    d.t(X[c], Y0 + 12, head, 12, SOFT, KR, "start", 600)
    for r, (n, title, q) in enumerate(cards):
        x, y = pos(c, r)
        focal = (c, r) == FOCAL
        if focal:
            d.o.append(f'<rect x="{x}" y="{y}" width="{CW}" height="{CH}" rx="8" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
        else:
            d.box(x, y, CW, CH, PAPER2, RULE, 1.0, 8)
        d.t(x + 20, y + 30, n, 12, ACC if focal else SOFT, MONO, "start", 600)
        d.t(x + 64, y + 30, title, 15, ACC if focal else INK, KR, "start", 600)
        d.t(x + 64, y + 56, q, 13, MUTED, KR, "start")

d.save("13-01.chapter-overview.svg")
