"""프롬프트마다 체크포인트가 생기고, 되감은 지점에서 대화가 다시 갈라지는 모습.

# 타입 스펙: type-timeline
"""
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))

from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 940, 480
d = D(
    W, H,
    "CHECKPOINT LIFECYCLE · BRANCH & REWIND",
    "프롬프트별 체크포인트 생성과 되감기 분기 구조",
    "프롬프트 입력 시점마다 자동 생성되는 스냅숏과 기준 체크포인트에서의 되감기 및 대안 분기",
    lead="첫 시도를 측정한 뒤 기준 체크포인트로 되감아 같은 출발점에서 다른 구현을 시도합니다"
)

# 1. 스냅숏 구성 상자 (좌측 하단 - 4개 요소 칩 배치)
d.box(48, 290, 248, 126, fill=PAPER2, stroke=RULE, sw=0.9, r=6)
d.t(172, 316, "체크포인트 스냅숏 구성", 12, INK, KR, "middle", 600)
d.line(64, 328, 280, 328, RULE, 0.8)
d.chip(112, 352, "대화 메시지", INFO, 11)
d.chip(230, 352, "파일 변경", OK, 11)
for _cx, _t in ((112, "도구 이력"), (230, "세션 컨텍스트")):
    d.o.append(f'<rect x="{_cx - 48}" y="378" width="96" height="20" rx="4" fill="{PAPER}" stroke="{SOFT}" stroke-width="0.8" stroke-dasharray="3 3"/>')
    d.t(_cx, 392, _t, 11, SOFT, KR, "middle")

# 2. 메인 타임라인 기준선 (y=210)
# CP1 전 구간
d.line(48, 210, 180, 210, RULE, 1.2)
# CP1 -> CP2 구간
d.line(180, 210, 420, 210, RULE, 1.2)
# CP2 -> CP3 구간 (시도 A)
d.line(420, 210, 660, 210, WARN, 1.2)
# CP3 -> 실패 중단 구간 (점선)
d.line(660, 210, 800, 210, WARN, 1.2, dash="4 4")

# 3. 되감기 곡선 화살표 (시도 A 실패 -> CP #2 기준점 복귀)
d.path("M 720 220 C 660 268, 480 268, 424 224", ACC, 1.4, m="acc")
d.chip(570, 252, "/rewind (Esc × 2)", ACC, 11)
d.t(570, 276, "기준 체크포인트로 복원", 11, MUTED, KR, "middle")

# 4. 시도 B 신규 분기 타임라인 (y=340)
# CP2 에서 분기하여 아래로 꺾여 진행
d.path("M 420 220 C 420 320, 460 340, 520 340", OK, 1.4)
d.line(520, 340, 830, 340, OK, 1.4)
d.path("M 822 340 L 834 340", OK, 1.4, m="ok")
d.t(904, 344, "진행 방향 →", 11, SOFT, KR, "end")

# 5. 타임라인 사건 노드 (상단 카드 & 눈금)
# 사건 1: 프롬프트 1 (CP #1)
d.box(88, 114, 184, 60, fill=PAPER2, stroke=RULE, sw=0.9, r=6)
d.t(180, 138, "프롬프트 1 전송", 12.5, INK, KR, "middle", 600)
d.t(180, 158, "체크포인트 생성", 11, MUTED, KR, "middle")
d.line(180, 174, 180, 206, RULE, 0.9)
d.o.append(f'<circle cx="180" cy="210" r="4" fill="{MUTED}"/>')
d.line(180, 204, 180, 216, RULE, 1.2)

# 사건 2: 프롬프트 2 (CP #2 - 기준 분기점, Focal!)
d.tone(316, 102, 208, 72, ACC, r=6, op="14", sw=1.4)
d.t(420, 128, "기준 체크포인트", 13.5, ACC, KR, "middle", 600)
d.t(420, 148, "분기점 (Branch Point)", 11.5, INK, KR, "middle", 600)
d.t(420, 165, "최적화 요청 시점", 11, MUTED, KR, "middle")
d.line(420, 174, 420, 201, ACC, 1.2)
d.o.append(f'<circle cx="420" cy="210" r="6" fill="{ACC}"/>')
d.o.append(f'<circle cx="420" cy="210" r="9" fill="none" stroke="{ACC}" stroke-width="1.2"/>')

# 사건 3: 프롬프트 3 (시도 A: 캐싱 계층 추가)
d.box(568, 114, 184, 60, fill=PAPER2, stroke=WARN, sw=1.0, r=6)
d.t(660, 138, "시도 A: 캐싱 추가", 12.5, WARN, KR, "middle", 600)
d.t(660, 158, "체크포인트 (시도 A)", 11, INK, KR, "middle")
d.line(660, 174, 660, 206, RULE, 0.9)
d.o.append(f'<circle cx="660" cy="210" r="4" fill="{WARN}"/>')
d.line(660, 204, 660, 216, RULE, 1.2)

# 시도 A 중단 표식
d.o.append(f'<circle cx="800" cy="210" r="4" fill="{WARN}"/>')
d.t(800, 194, "성능 측정", 11, MUTED, KR, "middle")
d.t(800, 228, "시도 A 되감기 (측정만)", 11, WARN, KR, "middle", 600)

# 사건 4: 프롬프트 3' (시도 B: 인덱스 튜닝 - 하단 분기)
d.box(568, 362, 184, 60, fill=PAPER2, stroke=OK, sw=1.1, r=6)
d.t(660, 386, "시도 B: 인덱스 튜닝", 12.5, OK, KR, "middle", 600)
d.t(660, 406, "체크포인트 (신규 분기)", 11, INK, KR, "middle")
d.line(660, 344, 660, 362, OK, 0.9)
d.o.append(f'<circle cx="660" cy="340" r="5" fill="{OK}"/>')

# 시도 B 확정 표식
d.o.append(f'<circle cx="800" cy="340" r="5" fill="{OK}"/>')
d.t(800, 362, "B 위에 캐싱 덧붙임", 11, OK, KR, "middle", 600)

# 6. 범례
d.legend(440, [
    ("기준 분기점 (Focal)", ACC),
    ("대안 B 채택 경로", OK),
    ("시도 A 되감기 경로", WARN),
    ("스냅숏 항목 (점선: 미확인)", INFO),
])

out_path = _HERE.parent / "05-01.checkpoint-snapshots.svg"
d.save(str(out_path))
print(f"saved: {out_path}")
