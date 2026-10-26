"""스킬 저장 위치와 이름 충돌 시 우선순위 결정 구조.

# 타입 스펙: type-nested
"""
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))

from dd import D, ACC, MUTED, INFO, INK, SOFT, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 500
d = D(
    W, H,
    "SKILL PRECEDENCE",
    "스킬 우선순위와 네임스페이스 격리",
    "엔터프라이즈 > 개인 > 프로젝트 순서의 이름 충돌 해결과 플러그인 고유 네임스페이스",
    lead="동일한 deploy 이름 충돌 시 개인 스킬이 프로젝트 스킬을 덮어씁니다"
)

# 좌측: 단일 이름 공간 충돌 영역
X0, Y0, W0, H0 = 24, 104, 588, 332
PADX, PADY = 28, 40

# Outer: 엔터프라이즈
d.box(X0, Y0, W0, H0, fill=PAPER2, stroke=RULE, sw=1.0, r=8)
d.t(X0 + 16, Y0 + 24, "엔터프라이즈 스킬", 13, INK, KR, "start", 600)
d.t(X0 + 140, Y0 + 24, "우선순위 1위", 12, MUTED, KR, "start")
d.t(X0 + W0 - 16, Y0 + 24, "조직 표준 정책 (미정의)", 12, SOFT, KR, "end")

# Middle: 개인 (focal)
x1, y1, w1, h1 = X0 + PADX, Y0 + PADY, W0 - 2 * PADX, H0 - 2 * PADY
d.tone(x1, y1, w1, h1, ACC, r=8, op="14", sw=1.4)
d.t(x1 + 16, y1 + 24, "개인 스킬", 13, ACC, KR, "start", 600)
d.t(x1 + 84, y1 + 24, "우선순위 2위", 12, ACC, KR, "start", 600)
d.t(x1 + w1 - 16, y1 + 24, "선택 실행", 12, ACC, KR, "end", 600)

d.t(x1 + 16, y1 + 52, "~/.claude/skills/deploy/", 12, INK, MONO, "start")
d.t(x1 + 16, y1 + 72, "/deploy 실행 (우선 적용)", 12, ACC, KR, "start")

# Inner: 프로젝트
x2, y2, w2, h2 = x1 + PADX, y1 + PADY + 44, w1 - 2 * PADX, h1 - PADY - 52
d.box(x2, y2, w2, h2, fill=PAPER, stroke=RULE, sw=0.9, r=6)
d.t(x2 + 16, y2 + 24, "프로젝트 스킬", 13, MUTED, KR, "start", 600)
d.t(x2 + 112, y2 + 24, "우선순위 3위", 12, MUTED, KR, "start")
d.t(x2 + w2 - 16, y2 + 24, "동일 이름 시 미실행", 12, SOFT, KR, "end")

d.t(x2 + 16, y2 + 52, ".claude/skills/deploy/", 12, SOFT, MONO, "start")
d.t(x2 + 16, y2 + 72, "개인 스킬에 의해 가려짐", 12, SOFT, KR, "start")

# 우측: 플러그인 독립 네임스페이스 영역
RX, RY, RW, RH = 636, 104, 260, 332
d.box(RX, RY, RW, RH, fill=PAPER2, stroke=INFO, sw=1.2, r=8)
d.t(RX + 16, RY + 24, "플러그인 스킬", 13, INFO, KR, "start", 600)
d.t(RX + RW - 16, RY + 24, "격리 공간", 12, INFO, KR, "end")

d.box(RX + 12, RY + 44, RW - 24, 76, fill=PAPER, stroke=RULE, sw=0.8, r=4)
d.t(RX + 24, RY + 68, "이름 공간: plugin:skill", 12, INK, MONO, "start")
d.t(RX + 24, RY + 92, "<plugin>/skills/deploy/", 12, MUTED, MONO, "start")

d.box(RX + 12, RY + 132, RW - 24, 100, fill=PAPER, stroke=RULE, sw=0.8, r=4)
d.t(RX + 24, RY + 156, "호출 명령", 12, INFO, KR, "start", 600)
d.t(RX + 24, RY + 180, "/myplugin:deploy", 13, INK, MONO, "start")
d.t(RX + 24, RY + 204, "독립 네임스페이스 (충돌 없음)", 12, INFO, KR, "start")

d.t(RX + 16, RY + 258, "skillOverrides 설정으로", 12, SOFT, KR, "start")
d.t(RX + 16, RY + 278, "스킬별 가시성 제어 (v2.1.129+)", 12, SOFT, KR, "start")

# 범례
d.legend(460, [("선택 실행 스킬 (focal)", ACC), ("가려짐 및 상위 위임", MUTED), ("격리된 네임스페이스", INFO)])
d.save("03-01.skill-precedence.svg")
