"""로컬 세션 스케줄과 클라우드 스케줄 작업의 생명주기 및 만료 상태 전이 상태 기계."""
# 타입 스펙: type-state
# 사실 출처: 05-03.Background Tasks.md:202-259 · 원문 09-advanced-features/README.md:191-250
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 960, 460
d = D(
    W, H,
    "SCHEDULED TASKS · STATE LIFECYCLE",
    "로컬 및 클라우드 예약 작업 생명주기와 상태 전이",
    "세션 종속 로컬 반복 작업과 클라우드 예약 작업의 활성화, 중단, 만료 전이와 API 키로 인한 /schedule 비활성",
    lead="로컬 작업은 세션과 함께 멈추고 7일 후 만료되며, API 키가 있으면 /schedule 이 꺼집니다",
)

# 1. 시작 및 종료 마커
# 시작 점
d.o.append(f'<circle cx="28" cy="242" r="6" fill="{INK}"/>')
d.arrow([(34, 242), (64, 242)], MUTED, "ar", 1.4)

# 2. 전이 화살표 (노드보다 먼저 그려 레이어 정리)
# 등록 접수 -> 로컬 세션 활성 (직각)
d.arrow([(204, 226), (248, 226), (248, 174), (290, 174)], ACC, "acc", 1.4)
d.t(240, 196, "/loop 등록", 11, ACC, MONO, "end")

# 등록 접수 -> 클라우드 활성 (직각)
d.arrow([(204, 258), (248, 258), (248, 314), (290, 314)], INFO, "info", 1.4)
d.t(240, 300, "/schedule 등록", 11, INFO, MONO, "end")

# 로컬 활성 자기 순환 (루프 실행)
d.path("M 336 140 L 336 102 L 408 102 L 408 140", ACC, 1.4, m="acc")
d.t(372, 92, "반복 실행 (지터 적용)", 11, ACC, KR, "middle")

# 로컬 활성 -> 세션 중단 (세션 종료)
d.arrow([(458, 160), (538, 160)], WARN, "warn", 1.4)
d.t(498, 148, "세션 종료", 11, WARN, KR, "middle")

# 세션 중단 -> 로컬 활성 (--resume 복구)
d.arrow([(538, 188), (458, 188)], OK, "ok", 1.4)
d.t(498, 204, "--resume", 11, OK, MONO, "middle")

# 로컬 활성 -> 만료 · 종료 (상단 우회: 7일 만료 또는 CronDelete)
d.arrow([(428, 140), (428, 66), (842, 66), (842, 210)], MUTED, "ar", 1.4)
d.t(635, 56, "7일 만료 / CronDelete", 11, MUTED, KR, "middle")

# 등록 접수 -> /schedule 사용 불가 (등록 단계 조건: API 키 있음)
d.arrow([(134, 274), (134, 330)], BAD, "bad", 1.4, "5 4")
d.t(126, 306, "API 키 있음", 11, BAD, KR, "end")


# 만료 · 종료 -> 종료 마커
d.arrow([(912, 242), (936, 242)], MUTED, "ar", 1.4)
# 종료 고리 점
d.o.append(f'<circle cx="944" cy="242" r="8" fill="none" stroke="{MUTED}" stroke-width="1.5"/>')
d.o.append(f'<circle cx="944" cy="242" r="4.5" fill="{INK}"/>')

# 3. 상태 노드
# State 0: 등록 접수
d.box(64, 210, 140, 64, fill=PAPER2, stroke=INFO, sw=1.0, r=8)
d.t(134, 236, "등록 접수", 12.5, INK, KR, "middle", 600)
d.t(134, 256, "/loop · /schedule", 10.5, INFO, MONO, "middle")

# State 1: 로컬 세션 활성 (Focal! ACC)
d.tone(290, 140, 168, 68, ACC, r=8, op="14", sw=1.4)
d.t(374, 166, "로컬 세션 활성", 13, ACC, KR, "middle", 600)
d.t(374, 188, "세션 반복 · 7일 만료", 11, INK, KR, "middle")

# State 2: 클라우드 활성
d.box(290, 280, 168, 68, fill=PAPER2, stroke=INFO, sw=1.0, r=8)
d.t(374, 306, "클라우드 활성", 13, INFO, KR, "middle", 600)
d.t(374, 328, "인프라 상시 실행", 11, MUTED, KR, "middle")

# State 3: 세션 중단 · 대기
d.box(538, 140, 160, 68, fill=PAPER2, stroke=WARN, sw=1.0, r=8)
d.t(618, 166, "세션 중단 · 대기", 12.5, WARN, KR, "middle", 600)
d.t(618, 188, "CLI 종료 대기", 11, MUTED, KR, "middle")

# State 4: /schedule 사용 불가 (등록 단계 조건, 점선)
d.o.append(f'<rect x="28" y="330" width="176" height="56" rx="8" fill="{PAPER2}" stroke="{BAD}" stroke-width="1.0" stroke-dasharray="5 4"/>')
d.t(116, 354, "/schedule 사용 불가", 12.5, BAD, KR, "middle", 600)
d.t(116, 374, "등록 단계 조건", 11, MUTED, KR, "middle")

# State 5: 만료 · 삭제
d.box(772, 210, 140, 64, fill=PAPER2, stroke=MUTED, sw=0.9, r=8)
d.t(842, 236, "만료 · 삭제", 12.5, INK, KR, "middle", 600)
d.t(842, 256, "종료 및 정리", 11, MUTED, KR, "middle")

# 4. 범례
d.legend(406, [
    ("로컬 활성", ACC),
    ("클라우드 활성", INFO),
    ("세션 대기", WARN),
    ("등록 불가 (점선)", BAD),
    ("재개 · 복구", OK),
    ("종료 · 정리", MUTED),
])

d.save("05-03.schedule-lifecycle.svg")
print("Saved 05-03.schedule-lifecycle.svg")
