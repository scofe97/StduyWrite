# 02-03 §5 — DNS 서버의 세 부류와 규모. 위로 갈수록 드물고 아래로 갈수록 많다.
# 수치는 원문 2.4.2 그대로다 — 루트는 13종의 사본이 약 2,000 인스턴스이고 12개 조직이 관리한다(2024년 기준).
# 로컬 DNS 서버를 피라미드 밖에 둔 것은 원문의 서술 그대로다 — "계층에 엄밀히 속하지 않지만 중심적".
# 타입 스펙: type-pyramid — 점이 위를 향하는 피라미드. 좁은 꼭대기가 가장 드물고 넓은 바닥이 기반이다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 596
APEX_X, APEX_Y = 400, 128
BASE_Y, HALF, HW_TOP = 428, 320, 148
BANDS = 3
BAND_H = (BASE_Y - APEX_Y) / BANDS

d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 02-03 §5",
      "DNS 서버는 세 부류입니다",
      "루트·TLD·권한 서버의 계층과 각 층의 규모. 로컬 DNS 서버는 이 계층에 속하지 않으면서 실제 질의의 대부분을 받는다.",
      "위로 갈수록 드물고 아래로 갈수록 많습니다")

def hw(y):  # 그 높이에서의 반폭. 꼭짓점을 잘라 사다리꼴로 두는 것은 라벨이 빗변을 넘지 않게 하기 위해서다.
    return HW_TOP + (HALF - HW_TOP) * (y - APEX_Y) / (BASE_Y - APEX_Y)

ROWS = [
    ("루트 DNS 서버", "TLD 서버의 주소를 준다", "13종 · 약 2,000 인스턴스 · 12개 조직", ACC),
    ("TLD 서버", "권한 서버의 주소를 준다", "com·net·edu·gov 와 모든 국가 코드", MUTED),
    ("권한 DNS 서버", "자기 조직 호스트의 주소를 준다", "공개 호스트를 가진 모든 조직", MUTED),
]
for i, (name, does, scale, c) in enumerate(ROWS):
    yt, yb = APEX_Y + i * BAND_H, APEX_Y + (i + 1) * BAND_H
    pts = f"{APEX_X - hw(yt)},{yt} {APEX_X + hw(yt)},{yt} {APEX_X + hw(yb)},{yb} {APEX_X - hw(yb)},{yb}"
    fill = f"{ACC}14" if c is ACC else PAPER2
    d.o.append(f'<polygon points="{pts}" fill="{fill}" stroke="{c if c is ACC else RULE}" '
               f'stroke-width="{1.4 if c is ACC else 1.0}"/>')
    cy = (yt + yb) / 2
    d.t(APEX_X, cy - 4, name, 12, c if c is ACC else INK, KR, "middle", 600)
    d.t(APEX_X, cy + 18, does, 11, SOFT, KR)
    d.line(APEX_X + hw(yb) + 6, cy, 730, cy, RULE, 0.8)
    d.t(742, cy + 4, scale, 11, MUTED, KR, "start")

# 계층 밖의 로컬 DNS 서버
d.box(64, 470, 872, 62, PAPER2, RULE, 0.9, 6)
d.t(84, 496, "로컬 DNS 서버", 12, INFO, KR, "start", 600)
d.t(84, 518, "계층에 엄밀히 속하지 않지만 DNS 구조에 중심적입니다. ISP 마다 하나씩 있고 보통 DHCP 로 주소를 받습니다.", 11, SOFT, KR, "start")
d.t(916, 496, "질의 대부분이 여기서 끝납니다", 11, INFO, KR, "end")

d.t(20, 452, "캐싱 덕분에 아주 작은 비율의 질의만이 루트 서버까지 갑니다 — 로컬 서버가 TLD 주소를 캐시해 꼭대기를 건너뜁니다.",
     11, MUTED, KR, "start")

d.legend(H - 40, [("캐싱으로 대개 건너뛰는 층", ACC), ("나머지 층", MUTED), ("계층 밖", INFO)])
d.save("02-03.dns-hierarchy.svg")
