# 05-01 학습 목표 뒤 전체 지도 — 절 넷이 기대값에서 위협 지도까지 간다.
# 타입 스펙: type-process — 칸마다 같은 의미 슬롯(절 번호 · 테스트가 맡는 일 · 그 절이 주는 것)이
#           반복되고 화살표가 읽는 순서를 나른다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 420
d = D(W, H, "LAMPSON LAB · 05-01",
      "실패해야 할 것이 실패하는지 본다 — 읽는 순서",
      "절 넷. 기대값을 어디서 가져오는지에서 시작해 거부를 판정하는 법, 러너의 판정, 위협 지도로 이어진다.",
      "두 번째 절이 이 편의 핵심이다 — 거부는 정상 경로와 거부 사유가 함께 있어야 증거가 된다")

CW, CH, GAP, X0 = 404, 108, 24, 24
Y1, Y2 = 120, 252
cards = [
    ("§1", "기대값 · 계정표에서 옮긴다", "구현 설정을 읽지 않는다"),
    ("§2", "거부 · 양성 대조와 사유", "정상 경로 성공 · 로그에 남은 거부 문구"),
    ("§3", "러너 · 빠진 보고는 실패", "중간 종료 · 선언 항목 미보고 · 목록 항목 미보고"),
    ("§4", "위협 지도 · AC 가 막는 것", "발급 · 접속 · 만료 · 반복 · 비밀"),
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

d.t(24, 392, "통과 줄 하나보다 실패 줄 하나가 더 많은 것을 알려 준다", 12, SOFT, KR, "start")
d.save("05-01.chapter-overview.svg")
