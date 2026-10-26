"""플러그인 폴더 안 매니페스트와 컴포넌트 실제 배치 구조."""
# 타입 스펙: type-tree
# 사실 출처: 04-02.Plugins.md:108-160 · 원문 07-plugins/README.md:16-30, 106-125
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, INFO, KR, MONO

W, H = 960, 460
d = D(
    W, H,
    "PLUGIN DIRECTORY STRUCTURE · TREE",
    "플러그인 내부 디렉터리 구조와 컴포넌트 배치",
    "패키지 매니페스트(선택)와 함께 스킬, 서브에이전트, 훅, MCP 및 언어 서버 설정의 실제 배치 구조",
    lead="매니페스트(선택)와 함께 스킬, 서브에이전트, 훅, MCP 설정이 표준 디렉터리에 배치됩니다",
)

# 1. 트리 연결선 (노드보다 먼저 그린다)
# Root 하향선
d.line(480, 144, 480, 172, RULE, 1.2)
# 수평 버스
d.line(112, 172, 848, 172, RULE, 1.2)
# 5개 가지 드롭선
for cx in (112, 296, 480, 664, 848):
    d.line(cx, 172, cx, 200, RULE, 1.2)

# 2. 루트 노드 (my-plugin/)
d.box(300, 96, 360, 48, fill=PAPER2, stroke=RULE, sw=1.0, r=6)
d.t(480, 116, "my-plugin/", 13, INK, MONO, "middle", 600)
d.t(480, 134, "플러그인 루트 디렉터리", 11.5, MUTED, KR, "middle")

# 3. 5개 단말 노드 (Leaves)
# Slot 0: 매니페스트 (Focal! Accent!)
d.tone(32, 200, 160, 144, ACC, r=6, op="14", sw=1.4)
d.chip(112, 222, "manifest", ACC, 11)
d.t(112, 248, ".claude-plugin/", 12, INK, MONO, "middle", 600)
d.t(112, 268, "plugin.json", 13, ACC, MONO, "middle", 600)
d.t(112, 294, "매니페스트 (선택)", 12, INK, KR, "middle")
d.t(112, 314, "신원 정보 · 대체 경로", 11.5, MUTED, KR, "middle")
d.t(112, 330, "의존성 선언", 11, SOFT, KR, "middle")

# Slot 1: 스킬 및 명령
d.box(216, 200, 160, 144, fill=PAPER2, stroke=INFO, sw=1.0, r=6)
d.chip(296, 222, "skills", INFO, 11)
d.t(296, 248, "skills/", 12, INK, MONO, "middle", 600)
d.t(296, 268, "SKILL.md", 13, INFO, MONO, "middle", 600)
d.t(296, 294, "작업 지침 · 프롬프트", 12, INK, KR, "middle")
d.t(296, 314, "commands/ 호환", 11.5, MUTED, KR, "middle")
d.t(296, 330, "명령 매핑", 11, SOFT, KR, "middle")

# Slot 2: 서브에이전트
d.box(400, 200, 160, 144, fill=PAPER2, stroke=INFO, sw=1.0, r=6)
d.chip(480, 222, "subagents", INFO, 11)
d.t(480, 248, "agents/", 12, INK, MONO, "middle", 600)
d.t(480, 268, "*.md", 13, INFO, MONO, "middle", 600)
d.t(480, 294, "전문 서브에이전트", 12, INK, KR, "middle")
d.t(480, 314, "독립 컨텍스트", 11.5, MUTED, KR, "middle")
d.t(480, 330, "권한 상향 제한", 11, SOFT, KR, "middle")

# Slot 3: 수명주기 훅
d.box(584, 200, 160, 144, fill=PAPER2, stroke=OK, sw=1.0, r=6)
d.chip(664, 222, "events", OK, 11)
d.t(664, 248, "hooks/", 12, INK, MONO, "middle", 600)
d.t(664, 268, "hooks.json", 13, OK, MONO, "middle", 600)
d.t(664, 294, "수명주기 훅", 12, INK, KR, "middle")
d.t(664, 314, "이벤트 자동 트리거", 11.5, MUTED, KR, "middle")
d.t(664, 330, "셸 명령 제어", 11, SOFT, KR, "middle")

# Slot 4: 외부 도구 및 언어 서버 설정
d.box(768, 200, 160, 144, fill=PAPER2, stroke=RULE, sw=1.0, r=6)
d.chip(848, 222, "config", MUTED, 11)
d.t(848, 248, ".mcp.json · .lsp.json", 12, INK, MONO, "middle", 600)
d.t(848, 268, "settings.json", 13, INK, MONO, "middle", 600)
d.t(848, 294, "도구 서버 연동", 12, INK, KR, "middle")
d.t(848, 314, "코드 인텔리전스", 11.5, MUTED, KR, "middle")
d.t(848, 330, "bin/ 실행 바이너리", 11, SOFT, MONO, "middle")

# 4. 범례
d.legend(388, [
    ("매니페스트 (Focal)", ACC),
    ("실행 컴포넌트", INFO),
    ("이벤트 제어", OK),
    ("도구 연동", MUTED),
])

d.save("04-02.plugin-layout.svg")
