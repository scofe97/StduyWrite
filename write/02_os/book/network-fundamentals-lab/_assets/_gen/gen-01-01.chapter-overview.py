# 01-01 학습 목표 뒤 전체 지도 — 절 셋을 읽는 순서로 잇는다.
# 타입 스펙: type-process — 칸마다 같은 의미 슬롯(절 번호 · 이름 · 그 절이 답하는 질문)이
#           반복되고 화살표가 읽는 순서를 나른다.
#           축약: 주체(lane)가 없는 단계 지도라 lanes 를 쓰지 않고 카드 한 줄 stride 로 놓는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 300
d = D(W, H, "NETWORK FUNDAMENTALS LAB · 01-01",
      "주소를 읽고 도구 셋을 든다 — 읽는 순서",
      "00장 노트의 절 셋을 읽는 순서로 이은 지도. 마스크 계산에서 출발해 주소가 둘인 이유를 지나 도구 셋으로 닫는다.",
      "앞 두 칸이 판단 기준을 세우고, 마지막 칸이 그 기준을 확인할 도구를 든다")

CW, CH, GAP, X0, Y = 261, 118, 24, 24, 120
cards = [
    ("§1", "마스크가 가른다", "이 둘은 직접 통하는가"),
    ("§2", "주소가 둘인 이유", "구간을 넘는 일과 건네는 일"),
    ("§3", "도구 셋", "설정 · 왕복 · 실제 지나간 것"),
]

def x_of(i):
    return X0 + i * (CW + GAP)

for i in range(2):
    d.arrow([(x_of(i) + CW, Y + CH / 2), (x_of(i + 1) - 4, Y + CH / 2)], MUTED, "ar", 1.4)

for i, (n, title, q) in enumerate(cards):
    x = x_of(i)
    focal = (i == 2)
    if focal:
        d.o.append(f'<rect x="{x}" y="{Y}" width="{CW}" height="{CH}" rx="8" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, Y, CW, CH, PAPER2, RULE, 1.0, 8)
    d.t(x + 18, Y + 30, n, 11, ACC if focal else SOFT, MONO, "start", 600)
    d.t(x + 18, Y + 60, title, 15, ACC if focal else INK, KR, "start", 600)
    d.t(x + 18, Y + 86, q, 12, MUTED, KR, "start")

d.t(24, 272, "세 칸을 다 지나면 01장 ARP 로 넘어간다", 12, SOFT, KR, "start")
d.save("01-01.chapter-overview.svg")
