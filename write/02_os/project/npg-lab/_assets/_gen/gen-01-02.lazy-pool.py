# 01-02-lazy-pool — 게으른 연결 풀의 단일 연결 수명주기와 보관 초과 시 TIME_WAIT 전이
# 본문 요구: 요청 도착 시에만 새로 맺고, 호스트당 기본 2칸 초과 반환 시 닫혀 TIME_WAIT 로 출발 포트를 점유하는 연결 상태 머신
# 타입 스펙: type-state
# 사실 출처: ch08-port-exhaustion-time-wait.md:5,23,24,26,45,49,91, ADR 0012:14,32,82,86
import sys
from pathlib import Path

# _assets 및 _gen 경로 등록
ASSETS_DIR = Path(__file__).resolve().parent.parent
GEN_DIR = Path(__file__).resolve().parent
if str(ASSETS_DIR) not in sys.path:
    sys.path.insert(0, str(ASSETS_DIR))
if str(GEN_DIR) not in sys.path:
    sys.path.insert(0, str(GEN_DIR))

from dd import D, INK, MUTED, SOFT, RULE, PAPER, PAPER2, ACC, OK, BAD, INFO, KR, MONO

W = 960
H = 488

d = D(
    W,
    H,
    "STATE MACHINE · CH08 LAZY POOL & PORT EXHAUSTION",
    "게으른 연결 풀과 TIME_WAIT 전이",
    "요청 도착 시점에만 새로 맺고 기본 2칸 초과 반환 시 프록시가 먼저 닫아 TIME_WAIT 60초 동안 출발 포트를 점유하는 상태 머신",
    lead="기본 보관 2칸을 초과한 연결은 프록시가 능동 종료(FIN)하여 TIME_WAIT 60초 동안 출발 포트(28,232개)를 점유합니다.",
)

# 시작 점 (Start Dot)
sx, sy = 32, 196
d.o.append(f'<circle cx="{sx}" cy="{sy}" r="6" fill="{INK}"/>')
d.t(sx, 168, "시작", 13, SOFT, KR, "middle", 600)

# 시작 -> State 1 화살표
d.arrow([(40, sy), (72, sy)], MUTED, "ar", 1.4)

# 1. State 1: 새로 맺음
s1_x, s1_y, s1_w, s1_h = 76, 156, 176, 80
d.tone(s1_x, s1_y, s1_w, s1_h, INFO, r=8, op="14", sw=1.2)
d.t(s1_x + s1_w // 2, s1_y + 26, "새로 맺음", 15, INFO, KR, "middle", 600)
d.t(s1_x + s1_w // 2, s1_y + 48, "요청 시점에만 생성", 14, INK, KR, "middle")
d.t(s1_x + s1_w // 2, s1_y + 68, "미리 채우지 않음", 14, MUTED, KR, "middle")

# State 1 -> State 2 화살표
d.arrow([(s1_x + s1_w, sy), (368, sy)], MUTED, "ar", 1.4)
d.t(310, 184, "연결 수립", 14, MUTED, KR, "middle")

# 2. State 2: 사용 중
s2_x, s2_y, s2_w, s2_h = 372, 156, 176, 80
d.tone(s2_x, s2_y, s2_w, s2_h, OK, r=8, op="14", sw=1.2)
d.t(s2_x + s2_w // 2, s2_y + 26, "사용 중", 15, OK, KR, "middle", 600)
d.t(s2_x + s2_w // 2, s2_y + 48, "HTTP 왕복 처리", 14, INK, KR, "middle")
d.t(s2_x + s2_w // 2, s2_y + 68, "동시 50 요청 처리", 14, MUTED, KR, "middle")

# State 2 -> State 3 화살표 (정상 반환)
d.arrow([(s2_x + s2_w, sy), (664, sy)], MUTED, "ar", 1.4)
d.t(606, 184, "반환 [idle < 2]", 14, MUTED, KR, "middle")

# 3. State 3: 빈 연결 보관
s3_x, s3_y, s3_w, s3_h = 668, 156, 176, 80
d.tone(s3_x, s3_y, s3_w, s3_h, INFO, r=8, op="14", sw=1.2)
d.t(s3_x + s3_w // 2, s3_y + 26, "빈 연결 보관", 15, INFO, KR, "middle", 600)
d.t(s3_x + s3_w // 2, s3_y + 48, "호스트당 기본 2칸", 14, INK, KR, "middle")
d.t(s3_x + s3_w // 2, s3_y + 68, "MaxIdleConnsPerHost", 14, MUTED, MONO, "middle")

# State 3 -> State 2 재사용 루프 (U-turn loop)
d.arrow([(s3_x + s3_w // 2, s3_y), (s3_x + s3_w // 2, 120), (s2_x + s2_w // 2, 120), (s2_x + s2_w // 2, s2_y - 4)], OK, "ok", 1.4)
d.t(608, 110, "다음 요청에 재사용", 14, OK, KR, "middle", 600)

# Focal 분기: State 2 바닥 -> State 4 상단 (수직 하강)
d.arrow([(s2_x + s2_w // 2, s2_y + s2_h), (s2_x + s2_w // 2, 316)], ACC, "acc", 1.6)
d.t(s2_x + s2_w // 2 + 12, 280, "보관 칸 가득 [idle ≥ 2]", 14, ACC, KR, "start", 600)

# 4. State 4: 닫힘 (능동 종료, Focal State)
s4_x, s4_y, s4_w, s4_h = 372, 320, 176, 80
d.tone(s4_x, s4_y, s4_w, s4_h, ACC, r=8, op="16", sw=1.6)
d.t(s4_x + s4_w // 2, s4_y + 26, "닫힘 (능동 종료)", 15, ACC, KR, "middle", 600)
d.t(s4_x + s4_w // 2, s4_y + 48, "초과 48개 소켓 닫음", 14, INK, KR, "middle")
d.t(s4_x + s4_w // 2, s4_y + 68, "프록시가 FIN 전송", 14, MUTED, KR, "middle")

# State 4 -> State 5 화살표 (Focal 연결, 우측 수평 이동)
d.arrow([(s4_x + s4_w, 360), (664, 360)], ACC, "acc", 1.6)
d.t(606, 348, "FIN 전송", 14, ACC, KR, "middle", 600)

# 5. State 5: TIME_WAIT
s5_x, s5_y, s5_w, s5_h = 668, 320, 176, 80
d.tone(s5_x, s5_y, s5_w, s5_h, BAD, r=8, op="14", sw=1.2)
d.t(s5_x + s5_w // 2, s5_y + 26, "TIME_WAIT", 15, BAD, KR, "middle", 600)
d.t(s5_x + s5_w // 2, s5_y + 48, "60초 동안 소켓 점유", 14, INK, KR, "middle")
d.t(s5_x + s5_w // 2, s5_y + 68, "포트 28,232개 고갈", 14, MUTED, KR, "middle")

# State 5 -> End Dot 화살표
d.arrow([(s5_x + s5_w, 360), (904, 360)], MUTED, "ar", 1.4)
d.t(874, 348, "60초", 13, MUTED, KR, "middle")

# 종료 점 (End Ringed Dot)
ex, ey = 916, 360
d.o.append(f'<circle cx="{ex}" cy="{ey}" r="8" fill="none" stroke="{MUTED}" stroke-width="1.4"/>')
d.o.append(f'<circle cx="{ex}" cy="{ey}" r="5" fill="{MUTED}"/>')
d.t(ex, 384, "포트 반환", 13, SOFT, KR, "middle")

# 범례
d.legend(440, [
    ("정상 연결·재사용", OK),
    ("게으른 생성·보관", INFO),
    ("보관 초과 닫힘 (focal)", ACC),
    ("포트 고갈 위험", BAD),
])

out_path = ASSETS_DIR / "01-02-lazy-pool.svg"
d.save(str(out_path))
print(f"saved: {out_path}")
