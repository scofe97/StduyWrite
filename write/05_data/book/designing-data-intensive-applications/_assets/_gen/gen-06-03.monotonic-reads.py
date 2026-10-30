# 06-03 §3 — 랙이 다른 두 팔로워를 차례로 조회할 때 첫 조회에서는 보였던 댓글이 두 번째 조회에서는 사라져 시간이 뒤로 가는 monotonic reads 위반 타임라인.
# 사실 출처: 06-03 §3(L56~L60), 원서 Ch.6 p.19~20 Figure 6-4
# 타입 스펙: type-timeline
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO

W = 880
AXIS_Y = 216
LEG = 466
H = LEG + 52

d = D(W, H, "06-03 · §3 MONOTONIC READS ANOMALY", "monotonic reads 이상 타임라인",
      "복제 지연 차이가 있는 두 팔로워를 순차 조회할 때 관찰자 시점에서 데이터가 사라지는 시간 역행 현상",
      "시간축 전개 · 팔로워별 복제 반영 시점 편차 · 관찰자 체감 상태 역행 · 단조 읽기 보장")

# 타임라인 메인 기준선 (가로 시간축)
d.line(60, AXIS_Y, 800, AXIS_Y, RULE, 1.2)
d.arrow([(790, AXIS_Y), (820, AXIS_Y)], MUTED, "ar", 1.4)
d.t(824, AXIS_Y + 4, "Time", 11, MUTED, MONO, "start")

# 눈금 및 시간 라벨
ticks = [
    (160, "t1", "리더 쓰기"),
    (290, "t2", "팔로워 1 복제"),
    (420, "t3", "1차 질의 (팔로워 1)"),
    (580, "t4", "2차 질의 (팔로워 2)"),
    (730, "t5", "팔로워 2 복제")
]

for tx, tlab, tdesc in ticks:
    d.line(tx, AXIS_Y - 5, tx, AXIS_Y + 5, RULE, 1.2)
    d.t(tx, AXIS_Y + 16, tlab, 11, INK, MONO, "middle", 600)
    d.t(tx, AXIS_Y + 30, tdesc, 11, SOFT, KR, "middle")

# 1. 상단 트랙: 리더 쓰기 및 팔로워 1 (정상 복제)
# t1: 리더 쓰기 박스
d.box(100, 118, 120, 68, PAPER2, ACC, 1.1)
d.t(160, 138, "t1: 리더 쓰기", 11, ACC, KR, "middle", 600)
d.t(160, 156, "댓글 55555 등록", 11, INK, KR, "middle")
d.t(160, 174, "리더 저장 완료", 11, SOFT, KR, "middle")
d.line(160, 186, 160, AXIS_Y - 5, ACC, 1.0, "3 3")

# t2: 팔로워 1 복제 완료
d.box(230, 118, 120, 68, PAPER2, OK, 1.1)
d.t(290, 138, "t2: 정상 복제", 11, OK, KR, "middle", 600)
d.t(290, 156, "댓글 55555 반영", 11, OK, KR, "middle")
d.t(290, 174, "최신 상태 일치", 11, SOFT, KR, "middle")
d.line(290, 186, 290, AXIS_Y - 5, OK, 1.0, "3 3")

# t3: 사용자 2345 1차 조회 (팔로워 1)
d.box(360, 118, 126, 68, PAPER2, INFO, 1.2)
d.t(423, 138, "t3: 1차 질의", 11, INFO, KR, "middle", 600)
d.t(423, 156, "결과: 댓글 표시", 11, OK, KR, "middle", 600)
d.t(423, 174, "사용자 2345 관찰", 11, SOFT, KR, "middle")
d.line(423, 186, 423, AXIS_Y - 5, INFO, 1.2)

# 2. 하단 트랙: 팔로워 2 복제 지연 및 시간 역행
# 지연 구간 음영 밴드
d.tone(160, 254, 570, 22, WARN, 4, "12", 0.9)
d.t(360, 269, "팔로워 2 복제 지연 구간 (댓글 미반영)", 11, WARN, KR, "middle")

# t4: 사용자 2345 2차 조회 (팔로워 2 · stale read)
d.box(516, 288, 128, 66, PAPER2, BAD, 1.3)
d.t(580, 308, "t4: 2차 질의", 11, BAD, KR, "middle", 600)
d.t(580, 326, "결과: 댓글 없음!", 11, BAD, KR, "middle", 600)
d.t(580, 344, "방금 본 댓글 소멸", 11, SOFT, KR, "middle")
d.line(580, AXIS_Y + 36, 580, 288, BAD, 1.2)

# t5: 팔로워 2 뒤늦은 복제
d.box(670, 288, 120, 66, PAPER2, RULE, 0.9)
d.t(730, 308, "t5: 지연 복제", 11, SOFT, KR, "middle", 600)
d.t(730, 326, "댓글 55555 도착", 11, MUTED, KR, "middle")
d.t(730, 344, "뒤늦게 일치 도달", 11, SOFT, KR, "middle")
d.line(730, AXIS_Y + 36, 730, 288, RULE, 1.0, "3 3")

# 3. 최하단: 체감 시간 역행 이상 & monotonic reads 해법 상자
# 이상 요약 상자
d.box(50, 374, 420, 72, PAPER2, BAD, 1.1)
d.t(260, 396, "체감 시간 역행 이상 (t3 확인 → t4 소멸)", 12, BAD, KR, "middle", 600)
d.t(260, 416, "새 데이터를 본 뒤 더 옛날 상태를 관찰해 시간 역행 체감", 11, SOFT, KR, "middle")
d.t(260, 432, "사용자에게 댓글이 저장됐다가 사라진 듯한 혼란 유발", 11, MUTED, KR, "middle")

# 해법 요약 상자
d.box(490, 374, 340, 72, PAPER2, OK, 1.1)
d.t(660, 396, "monotonic reads 보장: ID 해시 라우팅", 12, OK, KR, "middle", 600)
d.t(660, 416, "사용자 ID 해시 기반으로 동일 레플리카 고정 질의", 11, SOFT, KR, "middle")
d.t(660, 432, "옛 값을 읽을 수는 있으나 순차 조회 시 시간 역행 방지", 11, MUTED, KR, "middle")

d.legend(LEG, [("리더 쓰기", ACC), ("정상 복제", OK), ("1차 질의", INFO), ("지연 구간", WARN), ("시간 역행", BAD)])
d.save("06-03.monotonic-reads.svg")
