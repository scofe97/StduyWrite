# 13-02 학습 목표 뒤 전체 지도 — 옵션 다섯 갈래와 PMTUD 를 "무엇을 알리나" 로 잇는다.
# 타입 스펙: type-process — 칸마다 같은 의미 슬롯(절 번호 · 이름 · 그 옵션이 상대에게 알리는 것)이 반복되고 화살표가 읽는 순서를 나른다.
#           축약: 주체(lane)가 없는 단계 지도라 §1 lanes 와 §2 공식을 쓰지 않고 카드 두 열 stride 로 놓는다(13-01 지도와 같은 골격).
#           focal 은 로드맵 2단계 "MTU · MSS · PMTUD · PMTUD 블랙홀" 행을 채우는 §7 한 칸.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 920, 600
d = D(W, H, "TCP/IP ILLUSTRATED VOL.1 · 13-02",
      "TCP 옵션과 PMTUD — 읽는 순서",
      "13.3·13.4 를 정리한 이 편의 절 일곱을 두 묶음으로 나눈 지도다. 왼쪽 열은 SYN 에서 한 번 정하고 끝나는 옵션을, 오른쪽 열은 연결 내내 쓰이거나 "
      "연결 도중 세그먼트 크기를 바꾸는 장치를 따라간다. 칸 아래 줄이 그 장치가 상대에게 알리는 것이다.",
      "옵션 칸 40바이트 안에서, 각 옵션은 상대에게 한 가지씩을 알립니다")

CW, CH, GAP_X, GAP_Y = 420, 80, 32, 24
X = [24, 24 + CW + GAP_X]
Y0 = 132
COLS = [
    ("SYN 에서 정하는 것 · 13.3–13.3.3", [
        ("§1", "옵션의 생김새", "kind · len · 값 · 40바이트 상한"),
        ("§2", "MSS", "내가 받을 수 있는 가장 큰 세그먼트"),
        ("§3", "SACK", "구멍 뒤에 받아 둔 섬"),
        ("§4", "Window Scale", "창 칸을 몇 비트 밀어 읽을지"),
    ]),
    ("연결 내내 쓰는 것 · 13.3.4–13.4", [
        ("§5", "Timestamps 와 PAWS", "보낸 시각 · 한 바퀴 돈 번호 가려내기"),
        ("§6", "UTO 와 TCP-AO", "얼마나 기다릴지 · 세그먼트 인증"),
        ("§7", "TCP 의 PMTUD", "경로가 감당하는 크기로 줄이기"),
    ]),
]
FOCAL = (1, 2)

def pos(c, r): return X[c], Y0 + 28 + r * (CH + GAP_Y)

for c, (_, cards) in enumerate(COLS):
    for r in range(len(cards) - 1):
        x, y = pos(c, r)
        d.arrow([(x + CW / 2, y + CH), (x + CW / 2, y + CH + GAP_Y - 4)], MUTED, "ar", 1.4)
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

d.save("13-02.chapter-overview.svg")
