# 04-01 학습 목표 뒤 전체 지도 — 파일을 여는 요청 하나가 사용자에서 파일까지 지나는 길.
# 근거: credentials(7) "These IDs determine who owns the process", "Linux uses the filesystem IDs"
#       (권한 검사는 프로세스의 ID 로 한다), seccomp(2) 필터는 시스템 콜 입구에서 거른다,
#       capabilities(7) "Privileged processes bypass all kernel permission checks" 를 단위로 나눈다.
#       노트의 「접근 요청 하나가 지나는 길」 표와 같은 다섯 단계. 칸 위 § 는 그 구간을 다루는 절.
# 타입 스펙: type-flowchart — 왼쪽에서 오른쪽으로 흐르는 단계와 두 개의 거부 출구.
#           accent 는 이 장의 제목이 가리키는 판정 칸 하나.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, BAD, PAPER, PAPER2, RULE, KR, MONO

W, H = 960, 470
d = D(W, H, "LEARNING MODERN LINUX · 04-01",
      "파일을 여는 요청이 지나는 길",
      "사용자는 프로세스를 띄우고, 프로세스가 낸 요청을 커널이 시스템 콜 입구와 권한 검사에서 "
      "두 번 거른 뒤에야 파일에 닿는다. capability 는 권한 검사의 일부를 단위로 건너뛰게 한다.",
      "칸 위의 번호가 그 구간을 다루는 절입니다")

BW, BH, GAP, X0, Y0 = 150, 100, 36, 24, 176
nodes = [
    ("§1 §3", "사용자", "UID · GID", INFO),
    ("§1 §5", "프로세스", "실제 · 유효 UID", INFO),
    ("§6", "시스템 콜 입구", "seccomp 필터", MUTED),
    ("§2 §4 §6", "권한 검사", "모드 · ACL · MAC", ACC),
    ("§4", "파일", "접근 허용", OK),
]
xs = [X0 + i * (BW + GAP) for i in range(len(nodes))]

for i, (sec, name, sub, c) in enumerate(nodes):
    x = xs[i]
    if c is ACC:
        d.tone(x, Y0, BW, BH, ACC, r=8, sw=1.4)
    else:
        d.box(x, Y0, BW, BH, PAPER2, c if c is not MUTED else RULE, 1.1, 8)
    d.t(x + BW / 2, Y0 - 12, sec, 12, ACC if c is ACC else SOFT, MONO, "middle", 600)
    d.t(x + BW / 2, Y0 + 44, name, 15, ACC if c is ACC else INK, KR, "middle", 600)
    d.t(x + BW / 2, Y0 + 70, sub, 12, MUTED, KR)
    if i < len(nodes) - 1:
        d.arrow([(x + BW, Y0 + BH / 2), (xs[i + 1] - 2, Y0 + BH / 2)], MUTED, "ar", 1.4)

# capability 가 권한 검사로 들어온다
cx = xs[3] + BW / 2
d.chip(cx, 112, "capability", ACC, 12)
d.arrow([(cx, 123), (cx, Y0 - 26)], ACC, "acc", 1.3)

# 거부 출구 둘
RY, RH = 350, 50
rx0, rx1 = xs[2], xs[3] + BW
d.box(rx0, RY, rx1 - rx0, RH, PAPER, BAD, 1.1, 8)
d.t((rx0 + rx1) / 2, RY + 30, "거부 · EPERM 또는 EACCES", 13, BAD, KR, "middle", 600)
for i in (2, 3):
    x = xs[i] + BW / 2
    d.arrow([(x, Y0 + BH), (x, RY - 2)], BAD, "bad", 1.3, "5 4")

d.legend(424, [("신원과 대리", INFO), ("이 장의 초점", ACC), ("허용", OK), ("거부", BAD)])
d.save("04-01.chapter-overview.svg")
print("ok 04-01.chapter-overview")
