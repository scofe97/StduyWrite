"""다중 세션 간 영속 메모리 로드 및 갱신 흐름.

# 타입 스펙: type-timeline
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, OK, KR, MONO

W, H = 920, 520
d = D(
    W, H,
    "PERSISTENT MEMORY TIMELINE",
    "다중 세션 간 영속 메모리 로드 및 갱신 시점",
    "세션 1·2·3을 거치며 MEMORY.md 파일이 로드되고 누적 갱신되는 생명주기",
    lead="세션이 종료되어도 영속 메모리 디렉터리에 지식이 보존되어 다음 세션에 즉시 계승됩니다"
)

# 1. 세션 구간 태그
d.box(136, 104, 112, 24, fill=PAPER2, stroke=RULE, sw=0.8, r=4)
d.t(192, 120, "세션 1", 12, INK, KR, "middle", 600)

d.box(424, 104, 112, 24, fill=PAPER2, stroke=RULE, sw=0.8, r=4)
d.t(480, 120, "세션 2", 12, INK, KR, "middle", 600)

d.box(704, 104, 112, 24, fill=PAPER2, stroke=RULE, sw=0.8, r=4)
d.t(760, 120, "세션 3", 12, INK, KR, "middle", 600)

# 2. 타임라인 기준선 (y=268)
d.line(48, 268, 868, 268, RULE, 1.2)
d.path("M 860 268 L 872 268", MUTED, 1.2, m="ar")
d.t(872, 256, "시간 경과 →", 12, SOFT, KR, "end")

# 세션 경계 눈금 (Tick marks)
d.line(100, 260, 100, 276, RULE, 1.2)
d.line(388, 260, 388, 276, RULE, 1.2)
d.line(668, 260, 668, 276, RULE, 1.2)

# 3. 사건 1: 세션 1 시작 (위)
d.o.append(f'<circle cx="160" cy="268" r="4" fill="{MUTED}"/>')
d.line(160, 264, 160, 216, RULE, 1.0)
d.box(72, 148, 176, 68, fill=PAPER2, stroke=RULE, sw=1.0, r=6)
d.t(160, 176, "서브에이전트 시작", 13, INK, KR, "middle", 600)
d.t(160, 198, "기본 지침만 주입", 12, MUTED, KR, "middle")

# 4. 사건 2: 세션 1 종료 (아래)
d.o.append(f'<circle cx="244" cy="268" r="4" fill="{OK}"/>')
d.line(244, 272, 244, 320, RULE, 1.0)
d.box(156, 320, 176, 68, fill=PAPER2, stroke=OK, sw=1.1, r=6)
d.t(244, 348, "초기 지식 기록", 13, OK, KR, "middle", 600)
d.t(244, 370, "MEMORY.md 신규 생성", 12, INK, MONO, "middle")

# 5. 사건 3: 세션 2 시작 (위)
d.o.append(f'<circle cx="448" cy="268" r="4" fill="{INFO}"/>')
d.line(448, 264, 448, 216, RULE, 1.0)
d.box(360, 148, 176, 68, fill=PAPER2, stroke=INFO, sw=1.1, r=6)
d.t(448, 176, "영속 메모리 자동 로드", 13, INFO, KR, "middle", 600)
d.t(448, 198, "MEMORY.md 앞 200줄 주입", 12, INK, KR, "middle")

# 6. 사건 4: 세션 2 종료 (아래, Focal! ACC)
d.o.append(f'<circle cx="560" cy="268" r="6" fill="{ACC}"/>')
d.o.append(f'<circle cx="560" cy="268" r="9" fill="none" stroke="{ACC}" stroke-width="1.2"/>')
d.line(560, 277, 560, 320, ACC, 1.4)
d.tone(472, 320, 176, 68, ACC, r=6, op="14", sw=1.4)
d.t(560, 348, "지식 누적 및 갱신", 13, INK, KR, "middle", 600)
d.t(560, 370, "MEMORY.md 내용 업데이트", 12, ACC, KR, "middle")

# 7. 사건 5: 세션 3 시작 (위)
d.o.append(f'<circle cx="728" cy="268" r="4" fill="{INFO}"/>')
d.line(728, 264, 728, 216, RULE, 1.0)
d.box(640, 148, 176, 68, fill=PAPER2, stroke=INFO, sw=1.1, r=6)
d.t(728, 176, "누적 지식 계승", 13, INFO, KR, "middle", 600)
d.t(728, 198, "1·2세션 메모리 즉시 로드", 12, INK, KR, "middle")

# 8. 사건 6: 세션 3 진행 (아래)
d.o.append(f'<circle cx="828" cy="268" r="4" fill="{MUTED}"/>')
d.line(828, 272, 828, 320, RULE, 1.0)
d.box(748, 320, 160, 68, fill=PAPER2, stroke=RULE, sw=1.0, r=6)
d.t(828, 348, "연속 분석 수행", 13, INK, KR, "middle", 600)
d.t(828, 370, "재탐색 없이 작업 집중", 12, MUTED, KR, "middle")

# 9. 하단 영속 디스크 저장소 바
d.box(48, 412, 824, 40, fill=PAPER2, stroke=RULE, sw=0.8, r=6)
d.chip(112, 432, "영속 저장소", SOFT, 11)
d.t(440, 436, ".claude/agent-memory/<name>/MEMORY.md", 12, MUTED, MONO, "middle")
d.t(640, 436, "(project 범위)", 12, MUTED, KR, "start")

# 저장소 연결선 (사건 2 저장, 사건 4 갱신)
d.arrow([(244, 388), (244, 408)], OK, "ok", 1.2)
d.arrow([(560, 388), (560, 408)], ACC, "acc", 1.4)

# 10. 범례
d.legend(476, [
    ("세션 시작 (로드)", INFO),
    ("메모리 기록 (작업 중)", OK),
    ("지식 누적 및 갱신 (Focal)", ACC),
    ("영속 저장소", SOFT),
])

out = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "03-02.persistent-memory.svg"))
d.save(out)
print(f"saved: {out}")
