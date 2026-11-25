# 05-01 학습 목표 뒤 전체 지도 — 실사용자 위험이 한 단계씩 줄어드는 사다리와 사다리 밖 아웃바운드 제어.
# 본문 근거: 05-01 핵심 요약·새 버전이 사용자에게 닿기까지·§1~§5.
# 값 근거: ch05.txt §5.2.5 (x-istio-cohort: internal), §5.3 (weight 90/10, 45s), §5.4 (mirror:, -shadow), §5.5 (ALLOW_ANY, REGISTRY_ONLY, ServiceEntry).
# 타입 스펙: type-architecture — 두 존(노출 사다리 · 사다리 밖 아웃바운드)과 직각 화살표로 단계적 위험 감소와 전제·곁가지를 보인다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 960, 588
d = D(W, H, "ISTIO IN ACTION · 05-01",
      "새 버전의 노출이 줄어드는 사다리",
      "실사용자 트래픽에 닿는 위험이 배포 분리(§1) → 다크 런치(§2) → 가중치 전환과 Flagger(§3) → 미러링(§4) 순으로 줄어든다. 메시를 떠나는 트래픽(§5)은 사다리 밖에서 기본 차단과 허용을 다룬다.",
      "아래로 내려갈수록 실사용자에게 닿는 위험이 줄고, §4 미러링에서 응답 영향이 0 이 됩니다")

# 존 1 — 노출 사다리
d.o.append(f'<rect x="24" y="108" width="612" height="416" rx="8" fill="rgba(245,245,245,0.02)" stroke="rgba(245,245,245,0.10)" stroke-width="0.8"/>')
d.o.append(f'<rect x="36" y="100" width="224" height="16" rx="2" fill="{PAPER}"/>')
d.t(44, 113, "노출 사다리 — 실사용자 위험 감소", 13, SOFT, KR, "start")

# 존 2 — 사다리 밖 · 전제
d.o.append(f'<rect x="664" y="108" width="272" height="416" rx="8" fill="rgba(245,245,245,0.02)" stroke="rgba(245,245,245,0.10)" stroke-width="0.8"/>')
d.o.append(f'<rect x="676" y="100" width="184" height="16" rx="2" fill="{PAPER}"/>')
d.t(684, 113, "사다리 밖 · 공통 전제", 13, SOFT, KR, "start")

# 화살표 (노드보다 먼저 그려 z-order 확보)
step_links = [
    (204, 234, "요청 헤더로 대상을 가르면"),
    (300, 330, "고른 부류에서 비율로 열려면"),
    (396, 426, "응답 영향을 없애려면"),
]
for y1, y2, lab in step_links:
    d.path(f"M 140 {y1} V {y2}", MUTED, 1.4, m="ar")
    d.t(152, (y1 + y2) / 2 + 5, lab, 13, MUTED, KR, "start")

# 사다리 밖 연결선 (점선)
d.path("M 636 316 H 650 V 172 H 792 Q 800 172 800 180 V 198", SOFT, 1.2, m="soft", dash="4 3")
d.t(672, 162, "방향을 밖으로 뒤집으면", 13, SOFT, KR, "start")

rungs = [
    ("§1", "배포와 릴리스 분리", "설치(트래픽 0)와 개방을 분리", "빅뱅 → 점진 기반", INFO, False),
    ("§2", "다크 런치", "x-istio-cohort · gateways: mesh", "고른 부류만 노출", OK, False),
    ("§3", "가중치 전환 · Flagger", "weight 10/90 · 45초마다 승격·롤백", "정한 비율만 노출", OK, False),
    ("§4", "미러링", "mirror: 복제 · -shadow · 응답 폐기", "응답 영향 0", ACC, True),
]

RX, RW, RH = 44, 572, 64
for i, (sec, title, sub, badge, col, focal) in enumerate(rungs):
    y = 140 + i * 96
    d.tone(RX, y, RW, RH, col, 8, "1e" if focal else "12", 1.4 if focal else 1.1)
    d.chip(RX + 28, y + 22, sec, col, 11)
    d.t(RX + 60, y + 27, title, 14, col if focal else INK, KR, "start", 600)
    fam = MONO if not any("가" <= ch <= "힣" for ch in sub) else KR
    d.t(RX + 60, y + 49, sub, 12 if fam == MONO else 13, MUTED, fam, "start")
    d.t(RX + RW - 16, y + 37, badge, 13, col, KR, "end", 600)

# §5 아웃바운드 제어 카드
OX, OY, OW, OH = 684, 200, 232, 152
d.box(OX, OY, OW, OH, PAPER2, RULE, 1.0, 8)
d.chip(OX + 26, OY + 22, "§5", MUTED, 11)
d.t(OX + 52, OY + 27, "외부 통신 차단 · 허용", 14, INK, KR, "start", 600)
for idx, line in enumerate(["기본값 ALLOW_ANY", "REGISTRY_ONLY 기본 차단", "ServiceEntry 로 허용 등록", "L3·L4 차단 병행"]):
    d.t(OX + OW / 2, OY + 60 + idx * 24, line, 13, SOFT if idx == 3 else MUTED, KR)

# 공통 전제 카드
PX, PY, PW, PH = 684, 376, 232, 128
d.box(PX, PY, PW, PH, PAPER2, RULE, 1.0, 8)
d.chip(PX + 46, PY + 22, "§2·§3·§4", SOFT, 11)
d.t(PX + 92, PY + 27, "앱 동시 실행 전제", 14, INK, KR, "start", 600)
for idx, line in enumerate(["v1 · v2 다중 버전 공존", "미러링은 미러 요청을 알아봄", "외부 상태 공유 시 주의"]):
    d.t(PX + PW / 2, PY + 60 + idx * 24, line, 13, MUTED, KR)

d.legend(544, [("전제 · 빅뱅 해소", INFO), ("단계적 노출 통제", OK), ("응답 영향 0 (핵심)", ACC), ("사다리 밖 · 전제", MUTED)])
d.save("05-01.chapter-overview.svg")
