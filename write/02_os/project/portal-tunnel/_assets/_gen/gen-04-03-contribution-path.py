# 타입 스펙: type-flowchart
# 사실 출처: CONTRIBUTING.md:5-26, AGENTS.md:8-50,
#   portal/acme/certificate.go:238, .github/workflows/ci.yml:54-57, Makefile:41-57.
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, OK, WARN, BAD, INFO, ACC, KR, MONO

W, H = 1000, 680
d = D(W, H,
      "PORTAL-TUNNEL · CONTRIBUTION & VERIFICATION WORKFLOW",
      "포털 터널 기여 및 검증 경로",
      "마찰 식별부터 이슈 확인, 범위 판정(표면 vs 코어), 로컬 검증 및 메인테이너 리뷰까지의 절차",
      lead="표면 변경은 작은 PR로 신속히 개선하고 코어 변경은 설계 정당화와 e2e 재현을 선행합니다")

cx = 500

# 1. 시작 노드: 마찰 발견
y1 = 104
d.box(cx - 130, y1, 260, 42, fill=PAPER2, stroke=INFO, sw=1.2, r=6)
d.t(cx, y1 + 18, "마찰 및 개선점 식별", 12, INK, fam=KR, anchor="middle", weight=600)
d.t(cx, y1 + 34, "CLI · 로그 · 문서 · 인증서 실측", 10, MUTED, fam=KR, anchor="middle")

# 화살표 1 -> 2
d.arrow([(cx, y1 + 42), (cx, 174)], c=INFO, m="info", sw=1.4)

# 2. 판정 1: 기존 이슈 존재 여부
y2 = 174
d.box(cx - 130, y2, 260, 44, fill=PAPER2, stroke=WARN, sw=1.2, r=6)
d.t(cx, y2 + 18, "기존 이슈 존재 확인", 12, INK, fam=KR, anchor="middle", weight=600)
d.t(cx, y2 + 34, "GitHub Issues 검색", 10, MUTED, fam=KR, anchor="middle")

# 분기: Yes -> 오른쪽 기존 이슈 보강
d.arrow([(cx + 130, y2 + 22), (720, y2 + 22)], c=WARN, m="warn", sw=1.4)
d.t(cx + 155, y2 + 14, "있음", 10, WARN, fam=KR, anchor="middle", weight=600)

y_exist = 174
d.box(720, y_exist, 230, 44, fill=PAPER2, stroke=WARN, sw=1.0, r=6)
d.t(835, y_exist + 18, "기존 이슈에 맥락 보강", 12, INK, fam=KR, anchor="middle", weight=600)
d.t(835, y_exist + 34, "재현 로그 · 관측 사실 댓글 추가", 10, MUTED, fam=KR, anchor="middle")

# 분기: No -> 아래 신규 이슈 작성
d.arrow([(cx, y2 + 44), (cx, 246)], c=INFO, m="info", sw=1.4)
d.t(cx + 18, y2 + 56, "없음", 10, OK, fam=KR, anchor="middle", weight=600)

# 3. 신규 이슈 작성
y3 = 246
d.box(cx - 130, y3, 260, 42, fill=PAPER2, stroke=INFO, sw=1.2, r=6)
d.t(cx, y3 + 18, "신규 이슈 작성 등록", 12, INK, fam=KR, anchor="middle", weight=600)
d.t(cx, y3 + 34, "재현 환경 · 관측 사실 · 영향 범위", 10, MUTED, fam=KR, anchor="middle")

# 화살표 3 -> 4
d.arrow([(cx, y3 + 42), (cx, 316)], c=INFO, m="info", sw=1.4)

# 4. 판정 2: 기여 대상 범위 판정 (표면 vs 코어)
y4 = 316
d.box(cx - 140, y4, 280, 44, fill=PAPER2, stroke=ACC, sw=1.4, r=6)
d.t(cx, y4 + 18, "기여 대상 범위 판정", 12, INK, fam=KR, anchor="middle", weight=600)
d.t(cx, y4 + 34, "CONTRIBUTING.md 원칙 기준", 10, ACC, fam=KR, anchor="middle")

# 분기: 표면 (좌측)
lx = 240
d.arrow([(cx - 140, y4 + 22), (lx, y4 + 22), (lx, 388)], c=OK, m="ok", sw=1.4)
d.t(cx - 170, y4 + 14, "표면 계층", 10, OK, fam=KR, anchor="middle", weight=600)

y_surf = 388
d.box(lx - 130, y_surf, 260, 60, fill=PAPER2, stroke=OK, sw=1.2, r=6)
d.t(lx, y_surf + 18, "표면(Surface) 개선 PR", 12, OK, fam=KR, anchor="middle", weight=600)
d.t(lx, y_surf + 34, "CLI · 문서 · 진단 · 로컬 하네스", 10, MUTED, fam=KR, anchor="middle")
d.t(lx, y_surf + 50, "작은 변경 단위 · make 검증", 10, INK, fam=KR, anchor="middle")

# 분기: 코어 (우측)
rx = 760
d.arrow([(cx + 140, y4 + 22), (rx, y4 + 22), (rx, 388)], c=WARN, m="warn", sw=1.4)
d.t(cx + 170, y4 + 14, "코어 계층", 10, WARN, fam=KR, anchor="middle", weight=600)

y_core = 388
d.box(rx - 130, y_core, 260, 60, fill=PAPER2, stroke=WARN, sw=1.2, r=6)
d.t(rx, y_core + 18, "코어(Core) 프로토콜 PR", 12, WARN, fam=KR, anchor="middle", weight=600)
d.t(rx, y_core + 34, "프로토콜 · 신원 · 암호 · 전송 불변식", 10, MUTED, fam=KR, anchor="middle")
d.t(rx, y_core + 50, "설계 정당화 · e2e 재현 테스트 선행", 10, INK, fam=KR, anchor="middle")

# 합류: PR 제출 및 로컬 검증
y5 = 484
d.arrow([(lx, y_surf + 60), (lx, y5 + 24), (cx - 140, y5 + 24)], c=OK, m="ok", sw=1.4)
d.arrow([(rx, y_core + 60), (rx, y5 + 24), (cx + 140, y5 + 24)], c=WARN, m="warn", sw=1.4)

d.box(cx - 140, y5, 280, 48, fill=PAPER2, stroke=INFO, sw=1.2, r=6)
d.t(cx, y5 + 18, "풀 리퀘스트(PR) 제출", 12, INK, fam=KR, anchor="middle", weight=600)
d.t(cx, y5 + 36, "make vet · lint · test 통과 확인", 10, MUTED, fam=MONO, anchor="middle")

# 화살표 5 -> 6
d.arrow([(cx, y5 + 48), (cx, 560)], c=INFO, m="info", sw=1.4)

# 6. 최종 노드: CI 검증 및 리뷰
y6 = 560
d.box(cx - 150, y6, 300, 44, fill=PAPER2, stroke=RULE, sw=1.0, r=6)
d.t(cx, y6 + 18, "CI 통과 및 메인테이너 리뷰", 12, INK, fam=KR, anchor="middle", weight=600)
d.t(cx, y6 + 34, "GitHub Actions verify · tunnel-image · windows-acl", 9, MUTED, fam=MONO, anchor="middle")


# 범례
d.legend(636, [
    ("기본 진행 경로", INFO),
    ("표면 개선 (AI 권장)", OK),
    ("코어 검토 (인간 중심)", WARN),
    ("핵심 판정 관문 (Focal)", ACC),
])

out = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "04-03-contribution-path.svg"))
d.save(out)
print(f"saved: {out}")
