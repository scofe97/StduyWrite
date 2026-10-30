# 06-01 §4 신규 팔로워 — 잠금 없는 일관 스냅샷과 복제 로그 위치 연계를 통한 무중단 팔로워 셋업 프로세스.
# 사실 출처: 06-01 본문 §4(L65~L76), DDIA 2판 6장 "Setting Up New Followers" (p.7~8)
# 타입 스펙: type-process
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 880
PY = 104
PH = 296
LEG = 468
H = LEG + 56

d = D(W, H, "06-01 · §4 PROCESS", "다운타임 없는 신규 팔로워 셋업 프로세스",
      "클라이언트 쓰기를 중단하지 않고, 리더의 잠금 없는 일관 스냅샷을 복사한 뒤 복제 로그 위치(LSN·GTID) 이후의 변경분을 요청·적용하여 팔로워를 따라잡는다.",
      "일관 스냅샷 생성 · 스냅샷 파일 복사 · 로그 위치 연계 · 변경분 스트림 처리 · 따라잡음")

COL_W = 192
GAP = 14
X0 = 36
xs = [X0 + i * (COL_W + GAP) for i in range(4)]

steps = [
    ("01 · 일관 스냅샷", "전체 잠금 없는 시점 캡처", INFO),
    ("02 · 파일 복사", "신규 팔로워 노드 전송", INFO),
    ("03 · 변경분 요청", "스냅샷 이후 로그 연계", ACC),
    ("04 · 따라잡음", "실시간 스트림 전환", OK),
]

for i, (chip_t, sub_t, c) in enumerate(steps):
    x = xs[i]
    d.chip(x + COL_W / 2, PY + 14, chip_t, c, 11)
    d.t(x + COL_W / 2, PY + 38, sub_t, 12, MUTED, KR, "middle")

Y_CARD = PY + 52
H_CARD = 236

# 단계 1: 일관 스냅샷
d.box(xs[0], Y_CARD, COL_W, H_CARD, PAPER2, RULE, 0.9)
d.t(xs[0] + COL_W / 2, Y_CARD + 24, "리더 시점 캡처", 13, INK, KR, "middle", 600)
d.tone(xs[0] + 10, Y_CARD + 38, COL_W - 20, 50, INFO, 4, "16", 0.9)
d.t(xs[0] + COL_W / 2, Y_CARD + 58, "잠금 없는 일관 스냅샷", 12, INFO, KR, "middle")
d.t(xs[0] + COL_W / 2, Y_CARD + 74, "클라이언트 쓰기 지속 처리", 11, MUTED, KR, "middle")

d.tone(xs[0] + 10, Y_CARD + 98, COL_W - 20, 68, ACC, 4, "18", 0.9)
d.t(xs[0] + COL_W / 2, Y_CARD + 118, "복제 로그 위치 기록", 12, ACC, KR, "middle", 600)
d.t(xs[0] + COL_W / 2, Y_CARD + 136, "PostgreSQL: LSN", 11, INK, MONO, "middle")
d.t(xs[0] + COL_W / 2, Y_CARD + 152, "MySQL: binlog · GTID", 11, INK, MONO, "middle")

d.box(xs[0] + 10, Y_CARD + 180, COL_W - 20, 42, PAPER, RULE, 0.8)
d.t(xs[0] + COL_W / 2, Y_CARD + 198, "서드파티 도구", 11, SOFT, KR, "middle")
d.t(xs[0] + COL_W / 2, Y_CARD + 214, "Percona XtraBackup", 11, INK, MONO, "middle")

# 단계 2: 파일 복사
d.box(xs[1], Y_CARD, COL_W, H_CARD, PAPER2, RULE, 0.9)
d.t(xs[1] + COL_W / 2, Y_CARD + 24, "스냅샷 노드 전송", 13, INK, KR, "middle", 600)
d.tone(xs[1] + 10, Y_CARD + 38, COL_W - 20, 50, INFO, 4, "16", 0.9)
d.t(xs[1] + COL_W / 2, Y_CARD + 58, "스토리지 파일 복사", 12, INFO, KR, "middle")
d.t(xs[1] + COL_W / 2, Y_CARD + 74, "새 팔로워 노드로", 11, MUTED, KR, "middle")

d.tone(xs[1] + 10, Y_CARD + 98, COL_W - 20, 68, INFO, 4, "16", 0.9)
d.t(xs[1] + COL_W / 2, Y_CARD + 118, "팔로워에 스냅샷", 12, INFO, KR, "middle", 600)
d.t(xs[1] + COL_W / 2, Y_CARD + 136, "스냅샷 시점 데이터 적재", 12, INK, KR, "middle")
d.t(xs[1] + COL_W / 2, Y_CARD + 152, "로그 위치와 연결됨", 11, MUTED, KR, "middle")

d.box(xs[1] + 10, Y_CARD + 180, COL_W - 20, 42, PAPER, RULE, 0.8)
d.t(xs[1] + COL_W / 2, Y_CARD + 198, "1·2단계 대안", 11, SOFT, KR, "middle")
d.t(xs[1] + COL_W / 2, Y_CARD + 214, "WAL-G · Litestream", 11, INK, MONO, "middle")

# 단계 3: 변경분 요청 (FOCAL)
d.box(xs[2], Y_CARD, COL_W, H_CARD, PAPER2, ACC, 1.4)
d.t(xs[2] + COL_W / 2, Y_CARD + 24, "로그 위치 연계 요청", 13, INK, KR, "middle", 600)
d.tone(xs[2] + 10, Y_CARD + 38, COL_W - 20, 50, ACC, 4, "20", 0.9)
d.t(xs[2] + COL_W / 2, Y_CARD + 58, "스냅샷 이후 변경분 요청", 12, ACC, KR, "middle")
d.t(xs[2] + COL_W / 2, Y_CARD + 74, "기준 LSN / GTID 위치 전송", 11, INK, KR, "middle")

d.tone(xs[2] + 10, Y_CARD + 98, COL_W - 20, 68, ACC, 4, "20", 0.9)
d.t(xs[2] + COL_W / 2, Y_CARD + 118, "백로그 순차 처리", 12, ACC, KR, "middle", 600)
d.t(xs[2] + COL_W / 2, Y_CARD + 136, "누적된 변경 로그 재생", 12, INK, KR, "middle")
d.t(xs[2] + COL_W / 2, Y_CARD + 152, "리더와 동일 순서 반영", 11, MUTED, KR, "middle")

d.box(xs[2] + 10, Y_CARD + 180, COL_W - 20, 42, PAPER, ACC, 0.8)
d.t(xs[2] + COL_W / 2, Y_CARD + 198, "요청 범위", 11, ACC, KR, "middle")
d.t(xs[2] + COL_W / 2, Y_CARD + 214, "스냅샷 이후 모든 변경", 11, INK, KR, "middle")

# 단계 4: 따라잡음
d.box(xs[3], Y_CARD, COL_W, H_CARD, PAPER2, OK, 1.2)
d.t(xs[3] + COL_W / 2, Y_CARD + 24, "따라잡음 (Caught Up)", 13, INK, KR, "middle", 600)
d.tone(xs[3] + 10, Y_CARD + 38, COL_W - 20, 50, OK, 4, "16", 0.9)
d.t(xs[3] + COL_W / 2, Y_CARD + 58, "밀린 변경 처리 완료", 12, OK, KR, "middle")
d.t(xs[3] + COL_W / 2, Y_CARD + 74, "리더 최신 사본과 일치", 11, MUTED, KR, "middle")

d.tone(xs[3] + 10, Y_CARD + 98, COL_W - 20, 68, OK, 4, "16", 0.9)
d.t(xs[3] + COL_W / 2, Y_CARD + 118, "실시간 복제 전환", 12, OK, KR, "middle", 600)
d.t(xs[3] + COL_W / 2, Y_CARD + 136, "실시간 변경 스트림 수신", 12, INK, KR, "middle")
d.t(xs[3] + COL_W / 2, Y_CARD + 152, "변경 발생 즉시 처리", 11, MUTED, KR, "middle")

d.box(xs[3] + 10, Y_CARD + 180, COL_W - 20, 42, PAPER, OK, 0.8)
d.t(xs[3] + COL_W / 2, Y_CARD + 198, "이후", 11, OK, KR, "middle")
d.t(xs[3] + COL_W / 2, Y_CARD + 214, "리더 변경을 계속 처리", 11, INK, KR, "middle")

# 단계 간 수평 연결 화살표
y_arr = Y_CARD + H_CARD / 2
for i in range(3):
    x1 = xs[i] + COL_W
    x2 = xs[i + 1]
    d.arrow([(x1 + 1, y_arr), (x2 - 3, y_arr)], MUTED, "ar", 1.4)

# 하단 핵심 원리 배너
d.tone(24, 418, W - 48, 34, INFO, 4, "12", 0.9)
d.t(W / 2, 439, "핵심 원리: 복제 로그 위치(LSN·GTID)와 스냅샷을 연계하여 무중단 데이터 정합성 보장", 12, INK, KR, "middle", 500)

d.legend(LEG, [("로그 위치 연계 (focal)", ACC), ("스냅샷 생성 및 전송", INFO), ("따라잡음", OK)])
d.save("06-01.new-follower-setup.svg")
