# 06-06 §2 — 파이프라인 안에서 강제되는 여섯 겹 (원문 Fitness Functions 의 특성 목록).
# 특성 여섯과 그 설명은 원문 목록 그대로다. 아래에서 위로 "코드에서 사용자까지" 쌓은 것은 노트의 읽기다.
# accent 는 저자가 이 아키텍처 고유의 것으로 설명한 넷째(아키텍처 특성 테스트)에 준다.
# 타입 스펙: type-layers — 위아래로 쌓인 추상 수준. 통제가 어디서 강제되는지로 묶는 governance catalog 배치.
#           축약: 03-08.cache-layers 의 행 기하(인덱스 · 이름 · 오른쪽 설명 · 왼쪽 축)를 승계했다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W = 1240
AX = 60
BX, BW = 140, 1060
Y0, LH = 120, 68
N = 6
BOT = Y0 + N * LH
LEGEND_Y = BOT + 32
H = LEGEND_Y + 44

d = D(W, H, "BUILDING MICRO-FRONTENDS · 06-06 §2",
      "파이프라인 안에서 강제되는 여섯 겹",
      "아래가 코드를 재는 층이고 위로 갈수록 사용자가 겪는 것을 잰다. 색이 붙은 겹이 이 아키텍처 고유의 검사다.",
      "겹마다 저자가 든 특성과 그것이 재는 것이 붙습니다")

# 아래에서 위로 (인덱스 01 이 맨 아래)
layers = [
    ("01", "정적 분석", "SonarQube · 임계를 넘으면 리팩터링 전까지 파이프라인을 끝내지 않는다", False),
    ("02", "코드 커버리지", "공개 함수에 쓰인 테스트의 스냅숏 · 테스트의 품질은 알려 주지 않는다", False),
    ("03", "보안", "보안 팀이나 아키텍처 팀이 정의한 규정과 규칙을 위반하지 않는가", False),
    ("04", "아키텍처 특성 테스트", "조각 사이에 직접 의존이 없는가 · 승인된 공유 라이브러리만 쓰는가", True),
    ("05", "번들 크기", "조각마다 예산을 두고 초과 시점과 이유를 본다 · 공유 라이브러리도 함께", False),
    ("06", "성능 지표", "Lighthouse · WebPageTest 로 현재와 같거나 높은 기준인지 검증한다", False),
]

# 바깥 테두리
d.box(BX, Y0, BW, N * LH, f"{INK}03", RULE, 1.0, 6)

# 왼쪽 축
d.arrow([(AX, BOT - 8), (AX, Y0 + 8)], MUTED, "ar", 1.2)
d.o.append(f'<text x="{AX - 8}" y="{(Y0 + BOT) / 2}" text-anchor="middle" '
           f'font-family="{MONO}" font-size="8" letter-spacing="0.18em" fill="{SOFT}" '
           f'transform="rotate(-90 {AX - 8} {(Y0 + BOT) / 2})">TOWARD THE USER</text>')

# 겹 사이 구분선을 먼저 전부 긋고 — focal 상자가 자기 자리의 선을 덮는다
for k in range(1, N):
    d.line(BX, Y0 + k * LH, BX + BW, Y0 + k * LH, RULE, 0.8)

for i, (num, name, desc, focal) in enumerate(layers):
    y = Y0 + (N - 1 - i) * LH
    if focal:
        d.o.append(f'<rect x="{BX}" y="{y}" width="{BW}" height="{LH}" rx="6" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    d.t(BX + 32, y + LH / 2 + 4, num, 10, ACC if focal else SOFT, MONO, "start", 600)
    d.t(BX + 88, y + LH / 2 + 5, name, 13.5, ACC if focal else INK, KR, "start", 600)
    d.t(BX + BW - 24, y + LH / 2 + 5, desc, 10.5, MUTED, KR, "end")

d.legend(LEGEND_Y, [("이 아키텍처 고유의 검사", ACC)])
d.save("06-06.fitness-functions.svg")
print("h 필요:", LEGEND_Y + 40, " 실제:", H, " 우측끝:", BX + BW)
