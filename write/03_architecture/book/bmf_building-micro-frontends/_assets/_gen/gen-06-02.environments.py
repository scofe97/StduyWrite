# 06-02 §4 — 세 환경과 필요할 때 띄우는 환경 (원문 Environments Strategies).
# 각 존의 성격과 프로덕션에 붙는 두 통제, 온디맨드가 여는 셋은 모두 원문 서술 그대로다.
# 타입 스펙: type-deployment — 소프트웨어가 어디서 도는가. 존마다 그 안에서 도는 것과 접근 규칙이 붙는다.
#           축약: 상시 존 셋은 실선, 수명이 짧은 온디맨드 존은 점선 테두리로 갈랐다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W = 1240
ZW, ZH, GAP, X0, Y = 276, 264, 24, 40, 116
LEGEND_Y = Y + ZH + 36
H = LEGEND_Y + 44

d = D(W, H, "BUILDING MICRO-FRONTENDS · 06-02 §4",
      "세 환경과 필요할 때 띄우는 환경",
      "앞 셋은 상시로 서 있는 환경이고 마지막 하나는 작업이 끝나면 허무는 환경이다. 색이 붙은 존이 그 임시 환경이다.",
      "존마다 그 안에서 도는 것과 접근 규칙이 붙습니다")

zones = [
    ("TESTING", "테스트", "셋 중 가장 불안정하다",
     ["개발자가 빠르게 시도하는 자리"], False),
    ("STAGING", "스테이징", "프로덕션을 가능한 한 닮는다",
     ["승격 전에 확인하는 자리"], False),
    ("PRODUCTION", "프로덕션", "일부 인원만 접근한다",
     ["수동 접근을 막는 엄격한 통제", "승격과 배포의 신속한 수단"], False),
    ("ON-DEMAND", "온디맨드", "띄웠다가 끝나면 허문다",
     ["E2E · 시각적 회귀 테스트", "서브도메인 하나를 격리", "사업 쪽에 미리보기 제공", "스팟 인스턴스가 맞는 자리"], True),
]

for i, (eyebrow, name, desc, items, focal) in enumerate(zones):
    x = X0 + i * (ZW + GAP)
    if focal:
        d.o.append(f'<rect x="{x}" y="{Y}" width="{ZW}" height="{ZH}" rx="8" fill="{ACC}0A" '
                   f'stroke="{ACC}" stroke-width="1.4" stroke-dasharray="6 5"/>')
    else:
        d.o.append(f'<rect x="{x}" y="{Y}" width="{ZW}" height="{ZH}" rx="8" fill="{INK}04" '
                   f'stroke="{INK}30" stroke-width="1.0"/>')
    lw = len(eyebrow) * 6.4 + 16
    d.o.append(f'<rect x="{x + 20}" y="{Y - 6}" width="{lw}" height="12" rx="2" fill="{PAPER}"/>')
    d.t(x + 20 + lw / 2, Y + 3, eyebrow, 7.5, ACC if focal else SOFT, MONO)
    d.t(x + 20, Y + 34, name, 14, ACC if focal else INK, KR, "start", 600)
    d.t(x + 20, Y + 56, desc, 10.5, MUTED, KR, "start")
    for j, it in enumerate(items):
        by = Y + 76 + j * 44
        d.box(x + 20, by, ZW - 40, 34, PAPER2, RULE, 0.9, 5)
        d.t(x + 32, by + 22, it, 10, MUTED, KR, "start")

d.legend(LEGEND_Y, [("작업이 끝나면 허무는 환경", ACC)])
d.save("06-02.environments.svg")
print("h 필요:", LEGEND_Y + 40, " 실제:", H, " 우측끝:", X0 + 4 * ZW + 3 * GAP)
