# 타입 스펙: type-nested
# 사실 출처: NPG Ch.13 Event Logging (p.297-299)
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 880, 520
d = D(W, H, "EVENT LOGGING · THREE REDUCTION AXES",
      "이벤트 로그 볼륨을 줄이는 세 축: 레벨·구조화·샘플링",
      "무분별한 로깅은 CPU 와 디스크 I/O 병목을 부르고 탐색을 어렵게 만듭니다. "
      "레벨로 불필요한 저수준 출력을 거르고, 구조화로 필드 검색을 돕고, "
      "샘플링으로 루프 내 반복 폭주를 줄여 최적의 관측 비용을 유지합니다.",
      lead="외곽 상자는 전체 시스템 이벤트, 내포된 상자들은 로깅 부하를 줄이는 단계별 필터입니다.")

# 1. 외곽 컨테이너: 전체 런타임 발생 이벤트
OX, OY, OW, OH = 36, 100, 808, 380
d.box(OX, OY, OW, OH, fill=PAPER2, stroke=RULE, sw=1.0, r=8)
d.t(OX + 16, OY + 24, "시스템 런타임 전체 이벤트", 12, MUTED, KR, "start", 600)
d.t(OX + 240, OY + 24, "수많은 요청·루프 순회·상태 변화 (과도한 기록 시 I/O 병목)", 11, SOFT, KR, "start")

# 2. 중간 컨테이너: 이벤트 로그 대상 영역
LX, LY, LW, LH = 56, 140, 500, 320
d.tone(LX, LY, LW, LH, INFO, 6, "0c", 1.2)
d.t(LX + 16, LY + 24, "이벤트 로그 (개별 상태 기록)", 12, INFO, KR, "start", 600)

# 세 축 중첩 상자
# 축 1: 레벨 필터링 (Debug 제외)
C1_X, C1_Y, C1_W, C1_H = 76, 176, 460, 264
d.tone(C1_X, C1_Y, C1_W, C1_H, OK, 6, "10", 1.1)
d.t(C1_X + 14, C1_Y + 22, "축 1 · 레벨 필터링", 11, OK, KR, "start", 600)
d.t(C1_X + 150, C1_Y + 22, "DEBUG 억제 · ERROR / INFO 우선", 11, SOFT, KR, "start")

# 축 2: 구조화 로깅 (JSON 필드화)
C2_X, C2_Y, C2_W, C2_H = 96, 212, 420, 208
d.tone(C2_X, C2_Y, C2_W, C2_H, WARN, 6, "12", 1.1)
d.t(C2_X + 14, C2_Y + 22, "축 2 · 구조화 (Key-Value)", 11, WARN, KR, "start", 600)
d.t(C2_X + 180, C2_Y + 22, "msg · level · caller 필드 분리", 11, SOFT, KR, "start")

# 축 3: 샘플링 (반복 폭주 억제)
C3_X, C3_Y, C3_W, C3_H = 116, 248, 380, 152
d.tone(C3_X, C3_Y, C3_W, C3_H, ACC, 6, "18", 1.4)
d.t(C3_X + 14, C3_Y + 24, "축 3 · 샘플링 제어", 12, ACC, KR, "start", 600)
d.t(C3_X + 150, C3_Y + 24, "1초 틱 내 동일 메시지 솎아내기", 11, SOFT, KR, "start")

# 최심부: 최종 기록 로그
d.box(C3_X + 14, C3_Y + 44, 352, 88, fill=PAPER, stroke=ACC, sw=1.2, r=4)
d.t(C3_X + 190, C3_Y + 70, "최종 기록 로그", 12, INK, KR, "middle", 600)
d.t(C3_X + 190, C3_Y + 92, "{\"level\":\"error\",\"msg\":\"db down\"}", 11, OK, MONO, "middle")
d.t(C3_X + 190, C3_Y + 114, "최소 I/O 부하로 장애 진단 핵심 정보 확보", 11, MUTED, KR, "middle")

# 3. 우측 대비 컨테이너: 메트릭 관측 영역
MX, MY, MW, MH = 570, 140, 266, 320
d.tone(MX, MY, MW, MH, SOFT, 6, "10", 1.0)
d.t(MX + 14, MY + 24, "메트릭 영역 (집계 수치)", 12, INK, KR, "start", 600)
d.t(MX + 14, MY + 52, "개별 사건 문맥 대신 통계 집계", 11, MUTED, KR, "start")

# 메트릭 예시 상자들
d.box(MX + 8, MY + 72, 250, 68, fill=PAPER, stroke=RULE, sw=0.8, r=4)
d.t(MX + 14, MY + 94, "카운터 (Counter)", 11, INFO, KR, "start", 600)
d.t(MX + 14, MY + 118, "requests_total = 1420 (예시)", 11, INK, MONO, "start")

d.box(MX + 8, MY + 150, 250, 68, fill=PAPER, stroke=RULE, sw=0.8, r=4)
d.t(MX + 14, MY + 172, "게이지 (Gauge)", 11, WARN, KR, "start", 600)
d.t(MX + 14, MY + 196, "active_conns = 42 (예시)", 11, INK, MONO, "start")

d.box(MX + 8, MY + 228, 250, 68, fill=PAPER, stroke=RULE, sw=0.8, r=4)
d.t(MX + 14, MY + 250, "히스토그램 (Histogram)", 11, OK, KR, "start", 600)
d.t(MX + 14, MY + 274, "duration_bucket{le=\"0.1\"} 320 (예시)", 11, INK, MONO, "start")

svg_path = pathlib.Path(__file__).resolve().parent.parent / "13-01.event-logging-scope.svg"
d.save(str(svg_path))
print("ok 13-01 event-logging-scope")
