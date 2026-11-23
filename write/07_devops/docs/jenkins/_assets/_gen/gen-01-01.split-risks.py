# 타입 스펙: type-architecture
# 1절 분리가 막는 세 위험 — 빌드를 Controller 에서 돌릴 때와 Agent 로 뗀 뒤를 나란히 놓고 위험이 옮겨 가는 자리를 보인다
"""01-01 분리가 막는 세 위험 — 도식 생성기.

실행: cd ~/runners-high/write/07_devops/docs/jenkins/_assets && python3 -B _gen/gen-01-01.split-risks.py
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import (D, PAPER, PAPER2, INK, MUTED, RULE, ACC,  # noqa: E402
                OK, WARN, INFO, KR, MONO)

W, H = 960, 496

d = D(
    W, H,
    "JENKINS · CONTROLLER VS AGENT BUILD",
    "빌드를 Controller 에서 돌릴 때와 Agent 로 뗀 뒤",
    "Controller 한 곳에서 제어와 빌드를 함께 돌리면 자원 경쟁, 파일 접근, 수직 확장의 세 위험이 생기고 빌드를 Agent 로 떼면 위험이 Agent 쪽으로 옮겨 간다",
    lead="왼쪽은 한 프로세스에 모인 제어와 빌드, 오른쪽은 빌드를 Agent 로 뗀 뒤의 같은 일"
)


def fam(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO


def zone(x, y, w, h, label):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" '
               f'fill="{INK}05" stroke="{INK}1A" stroke-width="0.8"/>')
    han = sum(1 for c in label if "가" <= c <= "힣")
    lw = han * 13.0 + (len(label) - han) * 8.2 + 16
    d.o.append(f'<rect x="{x + 12}" y="{y + 6}" width="{lw}" height="18" rx="2" fill="{PAPER}"/>')
    d.t(x + 20, y + 20, label, 13, MUTED, fam(label), "start", 600)


def row(x, y, w, title, sub, c, op="14"):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="40" rx="6" fill="{c}{op}" stroke="{c}" stroke-width="1.2"/>')
    d.t(x + 16, y + 25, title, 13, c, fam(title), "start", 600)
    d.t(x + 112, y + 25, sub, 13, INK, fam(sub), "start")


# 존
zone(24, 100, 440, 340, "Controller 에서 빌드")
zone(496, 100, 440, 340, "Agent 로 뗀 뒤")

# 왼쪽: Controller 한 상자 안에 제어 일과 빌드 일
d.box(44, 136, 400, 132, PAPER2, RULE, 1.0, 6)
d.t(60, 158, "Controller", 14, INK, MONO, "start", 600)
d.tone(60, 168, 368, 40, INFO, r=6)
d.t(244, 193, "웹 UI · 스케줄링 · 잡 정의와 설정 · 빌드 기록", 13, INK, KR)
d.tone(60, 216, 368, 40, WARN, r=6)
d.t(244, 241, "체크아웃 · 컴파일 · 테스트 · 패키징", 13, INK, KR)

# 오른쪽: 제어는 Controller, 빌드는 Agent
d.box(516, 136, 168, 132, PAPER2, RULE, 1.0, 6)
d.t(532, 158, "Controller", 14, INK, MONO, "start", 600)
d.tone(532, 168, 136, 40, INFO, r=6)
d.t(600, 193, "웹 UI · 스케줄링", 12, INK, KR)
d.tone(532, 216, 136, 40, INFO, r=6)
d.t(600, 241, "설정 · 빌드 기록", 12, INK, KR)
d.arrow([(684, 202), (748, 202)], INFO, "info", 1.4)
d.t(716, 190, "지시", 13, MUTED, KR)
d.box(748, 136, 168, 132, PAPER2, RULE, 1.0, 6)
d.t(764, 158, "Agent", 14, INK, MONO, "start", 600)
d.tone(764, 168, 136, 88, OK, r=6)
d.t(832, 200, "체크아웃", 13, INK, KR)
d.t(832, 224, "컴파일 · 테스트", 13, INK, KR)
d.t(832, 248, "패키징", 13, INK, KR)

# 위험 세 줄(왼쪽) → 옮겨 간 자리(오른쪽)
rows = [
    (296, "자원 경쟁", "「안정성」 풀이: CPU·메모리 공유", WARN, "그 Agent 만 영향"),
    (344, "파일 접근", "파일시스템에 같은 수준 접근", ACC, "파일을 직접 열 수 없음"),
    (392, "수직 확장", "머신의 코어·디스크 키우기뿐", WARN, "Agent 를 더 붙임"),
]
for y, t, s, c, after in rows:
    row(44, y, 400, t, s, c)
    d.arrow([(444, y + 20), (516, y + 20)], MUTED, "ar", 1.3)
    d.o.append(f'<rect x="516" y="{y}" width="400" height="40" rx="6" fill="{OK}14" stroke="{OK}" stroke-width="1.2"/>')
    d.t(532, y + 25, after, 13, INK, KR, "start")

d.legend(452, [
    ("공식 문서가 직접 말함", ACC),
    ("이 문서의 풀이", WARN),
    ("제어 쪽 일", INFO),
    ("Agent 쪽 일", OK),
])

out = pathlib.Path(__file__).resolve().parent.parent / "01-01.split-risks.svg"
d.save(str(out))
print("saved", out)
