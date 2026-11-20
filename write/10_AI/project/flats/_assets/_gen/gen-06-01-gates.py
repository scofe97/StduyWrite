# 사실 출처: docs/gates.md:10-272 · docs/gates/runtime-discovery.md:1-30
# 타입 스펙: type-timeline
import pathlib
import sys

_HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))

from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, INFO, KR, MONO

W, H = 1000, 360
d = D(
    W, H,
    "PHASE GATES · VERIFICATION MILESTONES",
    "Flats 단계별 게이트 검증 이력",
    "기능 확장 단계마다 실행된 핵심 확인과 실측 합격 기준",
    lead="다중 노드 스파이크부터 무소스 에이전트 자율 배포까지 단계별 불변식을 검증합니다"
)

STAGES = [
    ("Phase 0", "스파이크", "다중노드", "tsnet·Portal 병합", OK, False),
    ("Phase 1", "MVP", "초기배포", "10MB 업로드·에이전트", OK, False),
    ("Phase 2", "서버 플랫", "DB보존", "SQLite·샌드박스", OK, False),
    ("Phase 3", "폴리시", "리다이렉트", "스냅샷·systemd", OK, False),
    ("Final review", "최종 리뷰", "37건해결", "4-lens 적대적 점검", OK, False),
    ("Runtime gate", "발견 게이트", "무소스작성", "MCP 단독 자율 배포", ACC, True),
]

Y_BASE = 200
X_START = 80
X_STEP = 168

# 가로 기준선
d.line(X_START - 20, Y_BASE, X_START + 5 * X_STEP + 40, Y_BASE, RULE, 1.2)

for i, (p_tag, p_name, key_word, detail, col, is_focal) in enumerate(STAGES):
    cx = X_START + i * X_STEP
    # 교차 틱 및 점
    r = 6 if is_focal else 4
    d.o.append(f'<circle cx="{cx}" cy="{Y_BASE}" r="{r}" fill="{col}" stroke="{PAPER}" stroke-width="2"/>')

    # 위쪽 카드 (Phase 이름 + 핵심 확인 한 단어)
    card_y = Y_BASE - 84
    card_w = 144
    card_h = 56
    stroke_c = col if is_focal else RULE
    fill_c = PAPER2
    d.box(cx - card_w / 2, card_y, card_w, card_h, fill=fill_c, stroke=stroke_c, sw=1.1 if is_focal else 0.9, r=4)
    d.line(cx, card_y + card_h, cx, Y_BASE - (r + 1), stroke_c, 1.0, dash="2,2")

    d.t(cx, card_y + 18, f"{p_tag} ({p_name})", 9.5, MUTED, KR, "middle")
    d.t(cx, card_y + 38, key_word, 13, col if is_focal else INK, KR, "middle", 600)

    # 아래쪽 라벨 (세부 확인 범위)
    d.t(cx, Y_BASE + 24, detail, 10, MUTED, KR, "middle")

d.legend(H - 40, [
    ("단계별 실측 합격", OK),
    ("무소스 자율 배포 게이트", ACC),
])

out_path = _HERE.parent / "06-01-gates.svg"
d.save(str(out_path))
print(f"saved {out_path}")
