# 04-04 §3 — 클라이언트 사이드 렌더링 조각을 호스팅하는 세 방식. 저자가 팀들에게서 본 것만 옮긴다.
# 타입 스펙: type-dp-security-matrix — 행(방식) × 열(구성 · 언제 맞나 · 값)의 격자.
#           축약: 권한 등급 어휘 대신 서술 값을 쓰고 열 폭을 넓혔다(한글 값 수용).
#           header_y 는 리드 줄을 쓰므로 스펙의 72 에서 100 으로 내렸다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, WARN, KR, MONO

LEFT_PAD, COMP_W, GAP1, ROLE_W, ROLE_GAP, RIGHT_PAD = 12, 240, 12, 260, 16, 48
HEADER_Y, HEADER_H, ROW_H, ROW_STRIDE = 100, 52, 48, 52
ROW0 = HEADER_Y + 68
roles = [("어떻게 두나", "layout"), ("언제 맞나", "fit"), ("값", "cost")]
rows = [
    ("단일 스토리지 + CDN", "저자의 권고", ["버킷 하나에 모두 넣고 CDN 으로", "거버넌스가 하나로 묶인 조직", "설정과 관리가 가장 단순하다"], True),
    ("다중 스토리지 + 단일 CDN", "팀마다 버킷", ["팀마다 버킷 · 전달은 한 CDN", "자율적인 팀이 많은 큰 조직", "호환과 중복을 막을 조율이 든다"], False),
    ("보안 컨테이너", "규제 산업", ["VPN 안의 컨테이너로 서빙", "정적 파일의 공개 접근이 금지될 때", "컴퓨트를 낭비하고 복잡도가 크다"], False),
]
n = len(roles)
W = LEFT_PAD + COMP_W + GAP1 + n * ROLE_W + (n - 1) * ROLE_GAP + RIGHT_PAD
rows_bottom = ROW0 + (len(rows) - 1) * ROW_STRIDE + ROW_H
LEGEND_Y = rows_bottom + 28
H = LEGEND_Y + 44

d = D(W, H, "BUILDING MICRO-FRONTENDS · 04-04 §3",
      "조각을 어디에 둘 것인가",
      "저자가 팀들에게서 본 방식은 셋이다. 색이 붙은 행이 가능하면 이것을 쓰라고 권한 쪽이다.",
      "행이 호스팅 방식이고 열이 그 방식을 가르는 축입니다")

def role_x(j): return LEFT_PAD + COMP_W + GAP1 + j * (ROLE_W + ROLE_GAP)

d.box(LEFT_PAD, HEADER_Y, COMP_W, HEADER_H, PAPER2, RULE, 0.8, 6)
d.t(LEFT_PAD + COMP_W / 2, HEADER_Y + 24, "호스팅 방식", 11, INK, KR, "middle", 600)
d.t(LEFT_PAD + COMP_W / 2, HEADER_Y + 42, "vs. 가르는 축", 9, MUTED, KR)
for j, (ko, en) in enumerate(roles):
    x = role_x(j)
    d.o.append(f'<rect x="{x}" y="{HEADER_Y}" width="{ROLE_W}" height="{HEADER_H}" rx="6" fill="{INK}"/>')
    d.t(x + ROLE_W / 2, HEADER_Y + 24, ko, 11, PAPER, KR, "middle", 600)
    d.t(x + ROLE_W / 2, HEADER_Y + 40, en, 9, PAPER, MONO, "middle", 400, "0.85")

for i, (name, hint, cells, focal) in enumerate(rows):
    y = ROW0 + i * ROW_STRIDE
    d.box(LEFT_PAD, y, COMP_W, ROW_H, PAPER2, RULE, 0.8, 6)
    d.t(LEFT_PAD + 14, y + 22, name, 11.5, INK, KR, "start", 600)
    d.t(LEFT_PAD + 14, y + 38, hint, 8.5, MUTED, KR, "start")
    for j, val in enumerate(cells):
        x = role_x(j)
        last = (i == len(rows) - 1 and j == len(cells) - 1)
        if focal:
            d.o.append(f'<rect x="{x}" y="{y}" width="{ROLE_W}" height="{ROW_H}" rx="6" fill="{ACC}14" stroke="{ACC}" stroke-width="1.2"/>')
            d.t(x + ROLE_W / 2, y + 28, val, 10, ACC, KR, "middle", 600)
        else:
            d.box(x, y, ROLE_W, ROW_H, f"{INK}08", RULE, 0.8, 6)
            d.t(x + ROLE_W / 2, y + 28, val, 10, WARN if last else MUTED, KR)

d.legend(LEGEND_Y, [("가능하면 이것을 쓰라고 권한 쪽", ACC), ("저자가 강하게 말리는 값", WARN)])
d.save("04-04.hosting-options.svg")
print("h 필요:", LEGEND_Y + 40, " 실제:", H, " W:", W)
