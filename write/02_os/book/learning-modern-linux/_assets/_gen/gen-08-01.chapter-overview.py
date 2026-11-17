# 08-01 전체 지도 — 로그 한 줄의 일생 다섯 단계 파이프라인.
# 원문 8장 서두: "To establish a common vocabulary, we'll first review different signal types you might
#       come across, such as system or application logs, metrics, and process traces. We'll also have a
#       look at how to go about troubleshooting and measuring performance. Next, we'll focus on logs
#       specifically, reviewing different options and semantics."
# 타입 스펙: type-data-flow — 파이프라인 단계마다 누가 무엇을 하고 데이터가 어디로 흐르는지 보인다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, INFO, PAPER2, RULE, KR, MONO

W, H = 880, 434
d = D(W, H, "LEARNING MODERN LINUX · 08-01",
      "로그 한 줄의 일생 — 다섯 단계 흐름",
      "로그 한 줄이 생산에서 수집·분배·조회·정리까지 다섯 단계를 거치는 전체 경로.",
      "journald 가 모든 줄을 먼저 받고 rsyslog 가 텍스트 파일로 나눕니다")

# 상단 파이프라인 카드 5개 (생산 → 수집 → 분배 → 조회 → 정리)
X0, Y0 = 24, 104
CW, CH = 144, 88
GAPX = 28
pos_x = [X0 + i * (CW + GAPX) for i in range(5)]  # [24, 196, 368, 540, 712]

cards = [
    ("1 생산", "앱과 커널", "/dev/log 소켓"),
    ("2 수집", "journald", "바이너리 저널"),
    ("3 분배", "rsyslog", "규칙 기반 라우팅"),
    ("4 조회", "사람", "필드 · 문자열 검색"),
    ("5 정리", "디스크 상한 관리", "회전과 정리"),
]

for i, (tag, who, where) in enumerate(cards):
    x = pos_x[i]
    focal = (i == 1)  # journald 수집이 focal
    if focal:
        d.tone(x, Y0, CW, CH, ACC, 6, "14", 1.4)
        d.t(x + 14, Y0 + 24, tag, 11, ACC, KR, "start", 600)
        d.t(x + 14, Y0 + 48, who, 13, ACC, MONO, "start", 600)
        d.t(x + 14, Y0 + 70, where, 11, MUTED, KR, "start")
    else:
        d.box(x, Y0, CW, CH, PAPER2, RULE, 1.0, 6)
        d.t(x + 14, Y0 + 24, tag, 11, SOFT, KR, "start", 600)
        d.t(x + 14, Y0 + 48, who, 13, INK, KR if i != 2 else MONO, "start", 600)
        d.t(x + 14, Y0 + 70, where, 11, MUTED, KR, "start")

# 카드 사이 수평 흐름 화살표 (축 정렬 148px)
for i in range(4):
    d.arrow([(pos_x[i] + CW, Y0 + CH / 2), (pos_x[i + 1] - 4, Y0 + CH / 2)], MUTED, "ar", 1.4)

# 하단 세부 상자 및 분기 (Y1 = 232, DH = 60)
Y1, DH = 232, 60

# 1 생산 세부 (직하 화살표)
cx0 = pos_x[0] + CW / 2
d.arrow([(cx0, Y0 + CH), (cx0, Y1 - 4)], MUTED, "ar", 1.3)
d.box(pos_x[0], Y1, CW, DH, PAPER2, RULE, 1.0, 6)
d.t(cx0, Y1 + 24, "앱 → /dev/log", 11, INK, MONO, "middle")
d.t(cx0, Y1 + 44, "커널 → 링 버퍼", 11, MUTED, KR, "middle")

# 2 수집 분기 — Storage= 가 둘 중 하나를 고른다. 경로 전체를 11px 로 쓰려고 두 상자를 세로로 쌓고,
#   아래 상자로 가는 갈래는 카드 사이 틈(오른쪽)으로 돌린다.
cx1 = pos_x[1] + CW / 2
SH, SG = 44, 8                       # 쌓은 상자 높이 · 사이
YB = Y1 + SH + SG
RX1 = pos_x[1] + CW + 12             # 오른쪽 우회 x (카드 사이 틈 28px 의 가운데쯤)
d.arrow([(cx1, Y0 + CH), (cx1, Y1 - 4)], INFO, "info", 1.3)
d.path(f"M {cx1} {Y0 + CH + 16} L {RX1} {Y0 + CH + 16} L {RX1} {YB + SH / 2} "
       f"L {pos_x[1] + CW + 4} {YB + SH / 2}", INFO, 1.3, m="info")
for y, path, note in ((Y1, "/run/log/journal", "메모리(휘발)"), (YB, "/var/log/journal", "디스크(영속)")):
    d.box(pos_x[1], y, CW, SH, PAPER2, INFO, 1.0, 6)
    d.t(cx1, y + 18, path, 11, INFO, MONO, "middle", 600)
    d.t(cx1, y + 35, note, 11, MUTED, KR, "middle")

# 3 분배 세부 (/var/log/* 텍스트 파일)
cx2 = pos_x[2] + CW / 2
d.arrow([(cx2, Y0 + CH), (cx2, Y1 - 4)], MUTED, "ar", 1.3)
d.box(pos_x[2], Y1, CW, DH, PAPER2, INFO, 1.0, 6)
d.t(cx2, Y1 + 24, "/var/log/* 파일", 11.5, INFO, MONO, "middle", 600)
d.t(cx2, Y1 + 44, "syslog · messages", 10.5, MUTED, MONO, "middle")

# 4 조회 세부 (저널 필드 매칭 vs 텍스트 검색)
cx3 = pos_x[3] + CW / 2
d.arrow([(cx3, Y0 + CH), (cx3, Y1 - 4)], MUTED, "ar", 1.3)
d.box(pos_x[3], Y1, CW, DH, PAPER2, RULE, 1.0, 6)
d.t(cx3, Y1 + 24, "journalctl 필드 매칭", 11, INK, KR, "middle")
d.t(cx3, Y1 + 44, "grep · zgrep 문자열", 11, MUTED, KR, "middle")

# 5 정리 분기 (텍스트 logrotate vs 저널 vacuum)
cx4 = pos_x[4] + CW / 2
d.line(cx4, Y0 + CH, cx4, Y0 + CH + 20, MUTED, 1.2)
d.line(pos_x[4] + 34, Y0 + CH + 20, pos_x[4] + 110, Y0 + CH + 20, MUTED, 1.2)
d.arrow([(pos_x[4] + 34, Y0 + CH + 20), (pos_x[4] + 34, Y1 - 4)], OK, "ok", 1.3)
d.arrow([(pos_x[4] + 110, Y0 + CH + 20), (pos_x[4] + 110, Y1 - 4)], OK, "ok", 1.3)

d.box(pos_x[4], Y1, 68, DH, PAPER2, OK, 1.0, 6)
d.t(pos_x[4] + 34, Y1 + 24, "logrotate", 11, OK, MONO, "middle", 600)
d.t(pos_x[4] + 34, Y1 + 44, "텍스트 회전", 11, MUTED, KR, "middle")

d.box(pos_x[4] + 76, Y1, 68, DH, PAPER2, OK, 1.0, 6)
d.t(pos_x[4] + 110, Y1 + 24, "journald", 11, OK, MONO, "middle", 600)
d.t(pos_x[4] + 110, Y1 + 44, "vacuum 정리", 11, MUTED, KR, "middle")

# 절 번호 라벨 (작게 표시)
Y2 = YB + SH + 24
d.t(cx0, Y2, "§2 첫 문단", 11, SOFT, KR, "middle")
d.t(cx1, Y2, "§2 · §4", 11, SOFT, KR, "middle")
d.t(cx2, Y2, "§2 · §3", 11, SOFT, KR, "middle")
d.t(cx3, Y2, "§3 · §5", 11, SOFT, KR, "middle")
d.t(cx4, Y2, "§4", 11, SOFT, KR, "middle")

# 범례
d.legend(Y2 + 38, [("최초 수집 주체 (journald)", ACC),
               ("저장소 및 분배 경로", INFO),
               ("정리 주체 분리 (텍스트 ≠ 저널)", OK)])

d.save("08-01.chapter-overview.svg")
print("ok 08-01.chapter-overview")
