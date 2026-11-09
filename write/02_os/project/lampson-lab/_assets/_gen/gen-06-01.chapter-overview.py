# 06-01 학습 목표 뒤 전체 지도 — 절 넷이 만료가 막는 것에서 알려진 한계까지 간다.
# 타입 스펙: type-process — 칸마다 같은 의미 슬롯(절 번호 · 다루는 일 · 그 절이 주는 것)이
#           반복되고 화살표가 읽는 순서를 나른다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 420
d = D(W, H, "LAMPSON LAB · 06-01",
      "만료돼도 열린 연결은 남는다 — 읽는 순서",
      "절 넷. 인증서 만료가 막는 것에서 시작해 호스트의 연결 상한, 끊기지 않는 것, 알려진 한계로 이어진다.",
      "두 번째 절이 이 편의 핵심이다 — 만료가 못 닫는 틈을 호스트의 연결 상한이 닫는다")

CW, CH, GAP, X0 = 404, 108, 24, 24
Y1, Y2 = 120, 252
cards = [
    ("§1", "만료가 막는 것 · 새 인증", "AC-19 거부 · AC-20 열린 세션 유지"),
    ("§2", "호스트의 연결 상한 · 60분", "session-reaper · EP-11"),
    ("§3", "끊기지 않는 것", "연결 위 새 세션 · PID 1 로 떨어진 프로세스"),
    ("§4", "알려진 한계 · 운영 보완", "토큰 로그 · 키 보호 · 신원 단위 · 재현성"),
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

d.t(24, 392, "짧은 인증서는 새 연결의 기간을 줄일 뿐 연결로 하는 일의 기간을 줄이지 않는다", 12, SOFT, KR, "start")
d.save("06-01.chapter-overview.svg")
