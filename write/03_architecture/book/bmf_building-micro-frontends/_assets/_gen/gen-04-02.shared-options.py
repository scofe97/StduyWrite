# 04-02 §2 — shared 객체에 줄 수 있는 옵션과 각각이 보장하는 것. 저자가 본문과 사이드바에 적은 것만 옮긴다.
# 타입 스펙: type-dp-security-matrix — 행(옵션) × 열(무엇을 지시하나 · 무엇을 막나 · 안 주면)의 격자.
#           축약: 권한 등급 어휘 대신 서술 값을 쓰고 열 폭을 넓혔다(한글 값 수용).
#           header_y 는 리드 줄을 쓰므로 스펙의 72 에서 100 으로 내렸다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

LEFT_PAD, COMP_W, GAP1, ROLE_W, ROLE_GAP, RIGHT_PAD = 12, 224, 12, 252, 16, 48
HEADER_Y, HEADER_H, ROW_H, ROW_STRIDE = 100, 52, 44, 48
ROW0 = HEADER_Y + 68
roles = [("무엇을 지시하나", "effect"), ("무엇을 막나", "prevents"), ("안 주면", "default")]
rows = [
    ("singleton", "true", ["같은 라이브러리를 하나만 로드", "두 벌이 메모리에 뜨는 일", "버전이 맞으면 재사용, 아니면 경고"], True),
    ("requiredVersion", "'18.2.0'", ["받아들일 버전 범위를 좁힌다", "semver 밖 버전이 섞이는 일", "셸의 package.json 버전을 쓴다"], False),
    ("shareScope", "'react17'", ["다른 스코프에 따로 붙인다", "기본 스코프와의 버전 충돌", "기본 스코프에 함께 붙는다"], False),
    ("import", "false", ["리모트가 이 의존성을 번들에 안 넣는다", "셸에 이미 있는 것을 또 받는 일", "리모트도 자기 몫을 번들한다"], False),
    ("eager", "true", ["동기로 미리 로드한다", "지연 로드에 따른 대기", "비동기 로드 (권장)"], False),
]
n = len(roles)
W = LEFT_PAD + COMP_W + GAP1 + n * ROLE_W + (n - 1) * ROLE_GAP + RIGHT_PAD
rows_bottom = ROW0 + (len(rows) - 1) * ROW_STRIDE + ROW_H
LEGEND_Y = rows_bottom + 28
H = LEGEND_Y + 44

d = D(W, H, "BUILDING MICRO-FRONTENDS · 04-02 §2",
      "shared 에 줄 수 있는 다섯 옵션",
      "공유 라이브러리를 별도 저장소로 빼는 대신 설정 한 줄로 끝내는 것이 이 플러그인의 값이다. 색이 붙은 행이 이 프로젝트가 세 라이브러리 모두에 준 옵션이다.",
      "행이 옵션이고 열이 그 옵션이 만드는 차이입니다")

def role_x(j): return LEFT_PAD + COMP_W + GAP1 + j * (ROLE_W + ROLE_GAP)

d.box(LEFT_PAD, HEADER_Y, COMP_W, HEADER_H, PAPER2, RULE, 0.8, 6)
d.t(LEFT_PAD + COMP_W / 2, HEADER_Y + 24, "옵션", 11, INK, KR, "middle", 600)
d.t(LEFT_PAD + COMP_W / 2, HEADER_Y + 42, "vs. 만드는 차이", 9, MUTED, KR)
for j, (ko, en) in enumerate(roles):
    x = role_x(j)
    d.o.append(f'<rect x="{x}" y="{HEADER_Y}" width="{ROLE_W}" height="{HEADER_H}" rx="6" fill="{INK}"/>')
    d.t(x + ROLE_W / 2, HEADER_Y + 24, ko, 11, PAPER, KR, "middle", 600)
    d.t(x + ROLE_W / 2, HEADER_Y + 40, en, 9, PAPER, MONO, "middle", 400, "0.85")

for i, (name, hint, cells, focal) in enumerate(rows):
    y = ROW0 + i * ROW_STRIDE
    d.box(LEFT_PAD, y, COMP_W, ROW_H, PAPER2, RULE, 0.8, 6)
    d.t(LEFT_PAD + 14, y + 20, name, 11.5, INK, MONO, "start", 600)
    d.t(LEFT_PAD + 14, y + 35, hint, 9, MUTED, MONO, "start")
    for j, val in enumerate(cells):
        x = role_x(j)
        if focal:
            d.o.append(f'<rect x="{x}" y="{y}" width="{ROLE_W}" height="{ROW_H}" rx="6" fill="{ACC}14" stroke="{ACC}" stroke-width="1.2"/>')
            d.t(x + ROLE_W / 2, y + 26, val, 9.5, ACC, KR, "middle", 600)
        else:
            d.box(x, y, ROLE_W, ROW_H, f"{INK}08", RULE, 0.8, 6)
            d.t(x + ROLE_W / 2, y + 26, val, 9.5, MUTED, KR)

d.legend(LEGEND_Y, [("이 프로젝트가 세 라이브러리 모두에 준 옵션", ACC)])
d.save("04-02.shared-options.svg")
print("h 필요:", LEGEND_Y + 40, " 실제:", H, " W:", W)
