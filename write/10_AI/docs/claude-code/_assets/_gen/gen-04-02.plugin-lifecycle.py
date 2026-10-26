"""플러그인 수명 주기와 활성화 전이 흐름 상태 기계."""
# 타입 스펙: type-state
# 사실 출처: 04-02.Plugins.md:330-417 · 원문 07-plugins/README.md:798-840
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, KR, MONO

W, H = 960, 480
d = D(
    W, H,
    "PLUGIN LIFECYCLE · STATE MACHINE",
    "플러그인 수명 주기와 활성화 전이",
    "마켓플레이스 카탈로그부터 설치 대기, 즉시 활성, 비활성, 제거 상태 전이와 관리 명령",
    lead="캐시 보존 여부에 따라 즉시 활성화되거나 대기 상태를 거치며 비활성화 및 삭제로 전이됩니다",
)

# 1. 시작 및 종료 마커
# 시작 점
d.o.append(f'<circle cx="24" cy="256" r="6" fill="{INK}"/>')
d.arrow([(30, 256), (56, 256)], MUTED, "ar", 1.4)

# 2. 전이 화살표 (상태 박스보다 먼저 그린다)
# 미설치 → 설치 대기 (캐시 보존 시)
d.arrow([(128, 224), (128, 160), (276, 160)], WARN, "warn", 1.4)
d.t(202, 146, "/plugin install", 11, WARN, MONO, "middle")
d.t(202, 180, "캐시 보존 시", 11, MUTED, KR, "middle")

# 설치 대기 → 활성 (/reload-plugins)
d.arrow([(436, 160), (572, 160), (572, 220)], OK, "ok", 1.4)
d.t(504, 146, "/reload-plugins", 11, OK, MONO, "middle")
d.t(504, 180, "수동 반영", 11, MUTED, KR, "middle")

# 미설치 → 활성 (즉시 활성화)
d.arrow([(200, 256), (496, 256)], ACC, "acc", 1.4)
d.t(348, 244, "/plugin install", 11, ACC, MONO, "middle")
d.t(348, 276, "즉시 활성화", 11, MUTED, KR, "middle")

# 활성 → 비활성 (/plugin disable) — 상단 우회 경로
d.arrow([(616, 220), (616, 112), (840, 112), (840, 128)], MUTED, "ar", 1.4)
d.t(728, 102, "/plugin disable", 11, INK, MONO, "middle")

# 비활성 → 활성 (/plugin enable)
d.arrow([(768, 168), (596, 168), (596, 220)], OK, "ok", 1.4)
d.t(682, 158, "/plugin enable", 11, OK, MONO, "middle")

# 활성 자기 순환 (claude plugin update — 원문 README:1254 는 CLI 형태를 권함)
d.path("M 512 292 L 512 336 L 556 336 L 556 292", ACC, 1.4, m="acc")
d.t(534, 354, "plugin update", 11, ACC, MONO, "middle")
d.t(534, 372, "버전 갱신", 11, MUTED, KR, "middle")

# 활성 → 제거 (/plugin uninstall) — 하단 우회 경로
d.arrow([(624, 292), (624, 336), (768, 336)], MUTED, "ar", 1.4)
d.t(640, 326, "/plugin uninstall", 10.5, MUTED, MONO, "start")

# 비활성 → 제거 (/plugin uninstall) — 수직 드롭
d.arrow([(840, 192), (840, 304)], MUTED, "ar", 1.4)
d.t(832, 244, "/plugin uninstall", 11, MUTED, MONO, "end")
d.t(832, 262, "비활성 제거", 11, MUTED, KR, "end")

# 제거 → 종료 점
d.arrow([(912, 336), (928, 336)], MUTED, "ar", 1.4)
# 종료 고리 점
d.o.append(f'<circle cx="936" cy="336" r="8" fill="none" stroke="{MUTED}" stroke-width="1.5"/>')
d.o.append(f'<circle cx="936" cy="336" r="4.5" fill="{INK}"/>')

# 3. 상태 노드
# State 0: 미설치
d.box(56, 224, 144, 64, fill=PAPER2, stroke=INFO, sw=1.0, r=8)
d.t(128, 250, "미설치", 13, INK, KR, "middle", 600)
d.t(128, 270, "카탈로그 대기", 11.5, INFO, KR, "middle")

# State 1: 설치 대기 (Pending)
d.box(276, 128, 160, 64, fill=PAPER2, stroke=WARN, sw=1.0, r=8)
d.t(356, 154, "설치 대기 (Pending)", 13, WARN, KR, "middle", 600)
d.t(356, 174, "캐시 보존 지연", 11.5, MUTED, KR, "middle")

# State 2: 활성 (Active) [Focal! Accent!]
d.tone(496, 220, 152, 72, ACC, r=8, op="14", sw=1.4)
d.t(572, 248, "활성 (Active)", 14, ACC, KR, "middle", 600)
d.t(572, 270, "세션 도구 즉시 사용", 12, INK, KR, "middle")

# State 3: 비활성 (Disabled)
d.box(768, 128, 144, 64, fill=PAPER2, stroke=RULE, sw=1.0, r=8)
d.t(840, 154, "비활성 (Disabled)", 13, INK, KR, "middle", 600)
d.t(840, 174, "도구 호출 차단", 11.5, MUTED, KR, "middle")

# State 4: 제거 (Removed)
d.box(768, 304, 144, 64, fill=PAPER2, stroke=RULE, sw=1.0, r=8)
d.t(840, 330, "제거 (Removed)", 13, INK, KR, "middle", 600)
d.t(840, 350, "고립 의존성 prune", 11.5, MUTED, KR, "middle")

# 4. 범례
d.legend(416, [
    ("활성 상태 (Focal)", ACC),
    ("카탈로그 상태", INFO),
    ("설치 대기", WARN),
    ("재개 가능", OK),
    ("비활성 · 제거", MUTED),
])

d.save("04-02.plugin-lifecycle.svg")
