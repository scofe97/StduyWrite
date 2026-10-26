"""슬래시 명령의 네 가지 출처와 이름 공간 체계."""
# 타입 스펙: type-tree
import sys
from pathlib import Path

sys.path.insert(0, ".")
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, KR, MONO

W, H = 960, 496
d = D(
    W, H,
    "COMMAND SOURCES · NAMESPACE TOPOLOGY",
    "슬래시 명령의 네 가지 출처와 이름 공간 체계",
    "내장·스킬·플러그인·MCP의 네 가지 출처별 식별자 형식과 실제 호출 예시",
    lead="출처에 따라 단일 식별자와 접두어 체계(/<플러그인>:<명령>, /mcp__<서버>__<프롬프트>)로 나뉩니다",
)

# 1. 연결선 (노드보다 먼저 그린다: type-tree 규약)
# 루트 → 버스
d.line(184, 256, 216, 256, SOFT, 1.0)
# 수직 버스
d.line(216, 124, 216, 388, SOFT, 1.0)

# 버스 → 4개 브랜치 & 브랜치 → 리프
ys = [124, 212, 300, 388]
for y in ys:
    d.line(216, y, 248, y, SOFT, 1.0)
    d.line(456, y, 488, y, SOFT, 1.0)

# 2. 루트 노드 (좌측)
d.box(24, 224, 160, 64, PAPER2, RULE, 1.0)
d.t(104, 250, "슬래시 명령", 14, INK, KR, "middle", 600)
d.t(104, 270, "/<identifier>", 12, MUTED, MONO, "middle")

# 3. 4개 출처 브랜치 (중앙 열)
branches = [
    ("내장 명령", "런타임 번들", False),
    ("사용자·프로젝트 스킬", "SKILL.md 파일", False),
    ("플러그인 명령", "설치 플러그인", True),
    ("MCP 프롬프트", "연결 MCP 서버", False),
]

for (title, sub, is_focal), y_top in zip(branches, [96, 184, 272, 360]):
    if is_focal:
        d.tone(248, y_top, 208, 56, ACC, 6, "14", 1.4)
        d.t(352, y_top + 24, title, 13, ACC, KR, "middle", 600)
    else:
        d.box(248, y_top, 208, 56, PAPER2, RULE, 1.0)
        d.t(352, y_top + 24, title, 13, INK, KR, "middle", 600)
    d.t(352, y_top + 43, sub, 11.5, MUTED, MONO if "." in sub else KR, "middle")

# 4. 리프 노드 (우측 열: 식별자 체계 및 실제 호출 예시)
leaves = [
    ("단일 식별자 /명령", "/help · /clear · /model", INFO),
    ("단일 식별자 (~/.claude/ 우선)", "/optimize · /pr", INFO),
    ("접두어 /<플러그인>:<명령>", "/frontend-design:frontend-design", ACC),
    ("접두어 /mcp__<서버>__<프롬프트>", "/mcp__github__list_prs", INFO),
]

for (schema, eg, c), y_top in zip(leaves, [96, 184, 272, 360]):
    d.box(488, y_top, 448, 56, PAPER, RULE, 0.9)
    d.t(504, y_top + 24, schema, 12.5, c, MONO if "mcp" in schema else KR, "start", 600)
    d.t(504, y_top + 43, eg, 12, MUTED, MONO, "start")

# 5. 범례
d.legend(452, [("접두어 이름 공간 적용", ACC), ("단일 식별자 체계", INFO)])

d.save("02-01.command-sources.svg")
