# 08-01 §9 「줄일 때는 vacuum」 — 저널 디스크 사용량이 회전과 vacuum 으로 바뀌는 순서.
# 실측(Debian 12 컨테이너, systemd 252): journalctl --disk-usage 8.0M → logger 로 채운 뒤 36.7M →
#   journalctl --rotate → journalctl --vacuum-size=16M 이 보관 파일 하나(21.6M)를 지움 →
#   --disk-usage 15.1M. 36.7 − 21.6 = 15.1.
# 1차 자료: journalctl(1) --disk-usage·--rotate·--vacuum-size(보관 파일만 지운다).
# 타입 스펙: type-waterfall — 사용량 막대가 단계마다 어떻게 오르내리는지 실제 값으로 보인다.
#           세로축은 MB 선형 눈금, 16M 목표선은 점선. accent 는 vacuum 이 지운 구간 하나.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, PAPER2, RULE, KR, MONO

W, H = 880, 496
d = D(W, H, "LEARNING MODERN LINUX · 08-01 §4",
      "저널 사용량은 rotate 뒤 vacuum 으로 줄어든다",
      "컨테이너에서 저널을 채운 뒤 --disk-usage, --rotate, --vacuum-size=16M 을 차례로 돌린 값. "
      "vacuum 은 보관 파일만 지운다.",
      "vacuum 이 21.6M 짜리 보관 파일 하나를 지워 15.1M 이 남았습니다")

BASE, TOP, MAXM = 380, 140, 40
SC = (BASE - TOP) / MAXM          # 1 MB 당 6 px
def y(mb):
    return BASE - mb * SC

AXX = 96
d.line(AXX, TOP, AXX, BASE, RULE, 1.0)
d.line(AXX, BASE, 800, BASE, RULE, 1.0)
for mb in (0, 10, 20, 30, 40):
    d.line(AXX - 4, y(mb), AXX, y(mb), RULE, 1.0)
    d.t(AXX - 8, y(mb) + 4, f"{mb}M", 11, SOFT, MONO, "end")

BW, X0, STRIDE = 120, 120, 176
bars = [
    ("8.0M", 0, 8.0, MUTED, "처음", "--disk-usage"),
    ("36.7M", 0, 36.7, INFO, "logger 로 채운 뒤", "--disk-usage"),
    ("−21.6M", 15.1, 36.7, ACC, "보관 파일 삭제", "--vacuum-size=16M"),
    ("15.1M", 0, 15.1, OK, "정리 뒤", "--disk-usage"),
]
for i, (val, lo, hi, col, lab, cmd) in enumerate(bars):
    x = X0 + i * STRIDE
    d.tone(x, y(hi), BW, y(lo) - y(hi), col, 4, "22" if col != ACC else "33", 1.2)
    d.t(x + BW / 2, y(hi) - 8, val, 12, col, MONO, "middle", 600)
    d.t(x + BW / 2, BASE + 24, lab, 11, MUTED, KR)
    d.t(x + BW / 2, BASE + 42, cmd, 11, SOFT, MONO)
    if i in (1, 2):
        nx = X0 + (i + 1) * STRIDE
        lvl = 36.7 if i == 1 else 15.1
        d.line(x + BW, y(lvl), nx, y(lvl), MUTED, 1.0, "3 4")

RXM = X0 + STRIDE + BW + (STRIDE - BW) / 2
d.chip(RXM, TOP - 16, "--rotate", MUTED, 11)
d.t(RXM, TOP + 4, "활성 → 보관", 11, MUTED, KR)
d.line(RXM, TOP + 12, RXM, BASE, RULE, 1.0, "2 4")

d.line(AXX, y(16), 800, y(16), SOFT, 1.0, "6 4")
d.t(804, y(16) + 4, "16M", 11, SOFT, MONO, "start")

d.legend(452, [("vacuum 이 지운 보관 파일", ACC), ("채운 뒤", INFO), ("정리 뒤", OK)])
d.save("08-01.journal-vacuum.svg")
print("ok 08-01.journal-vacuum")
