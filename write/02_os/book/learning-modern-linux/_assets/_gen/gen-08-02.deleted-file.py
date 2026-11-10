# 08-02 §4 — 지운 파일이 열린 fd 로 살아 있다가 0 으로 잘리거나 fd 가 닫히면 공간이 돌아온다.
# 실측: debian:12 컨테이너, 300MiB tmpfs /data (2026-11-10).
#   df -m /data → 0 · dd 200MiB app.log · tail -f app.log & → df 200 · rm app.log → ls 빈 폴더, df 200
#   lsof +L1 → "tail 3678 ... 209715200 NLINK 0 ... /data/app.log (deleted)"
#   : > /proc/3678/fd/3 → "tail: /data/app.log: file truncated", df 0
# 1차 자료: unlink(2) "the file will remain in existence until the last file descriptor referring to it is closed".
#           lsof(8) +L1 "will select open files that have been unlinked".
# 타입 스펙: type-state — 파일의 상태(이름·링크 수·df 사용량)와 전이를 일으키는 명령. 종료 경로는 man page 근거라 점선.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, RULE, KR, MONO

W, H = 960, 484
BW, BH, Y = 192, 112, 140
XS = [24, 264, 504, 744]
STATES = [
    ("빈 /data", ["파일 없음", "df 0 MiB"], SOFT, False),
    ("열린 파일", ["app.log · NLINK 1", "tail fd 3", "df 200 MiB"], INFO, False),
    ("지운 열린 파일", ["이름 없음 · NLINK 0", "(deleted) · fd 3", "df 200 MiB"], ACC, True),
    ("0 으로 잘린 파일", ["크기 0 · fd 3 유지", "df 0 MiB"], OK, False),
]

d = D(W, H, "LEARNING MODERN LINUX · 08-02 §4",
      "지운 뒤에도 남는 200MiB",
      "rm 은 이름만 떼고, 파일을 연 프로세스가 있으면 공간이 그대로 남는다. lsof +L1 이 그 파일을 "
      "보여 주고, /proc/PID/fd 로 크기를 0 으로 자르거나 fd 가 닫히면 df 가 0 으로 돌아온다.",
      "lsof +L1 의 NLINK 0 · (deleted) 줄이 공간을 쥔 프로세스입니다")

for x, (name, lines, c, focal) in zip(XS, STATES):
    d.tone(x, Y, BW, BH, c, 8, "2E" if focal else "14", 1.6 if focal else 1.1)
    d.t(x + BW / 2, Y + 26, name, 13, c if focal else INK, KR, "middle", 600)
    for j, ln in enumerate(lines):
        d.t(x + BW / 2, Y + 52 + j * 20, ln, 12, MUTED if j < len(lines) - 1 else c, MONO)

TR = [("dd · tail -f", INFO), ("rm app.log", ACC), (": > /proc/3678/fd/3", OK)]
for i, (lab, c) in enumerate(TR):
    x1, x2 = XS[i] + BW, XS[i + 1]
    d.arrow([(x1 + 4, Y + 56), (x2 - 6, Y + 56)], c, {INFO: "info", ACC: "acc", OK: "ok"}[c])
    d.t((x1 + x2) / 2, Y - 12, lab, 11, c, MONO)

# 종료 경로: 지운 열린 파일 → fd 닫힘
FY = 332
d.box(XS[3], FY, BW, 76, "#161B22", OK, 1.0, 8)
d.t(XS[3] + BW / 2, FY + 28, "fd 닫힌 파일", 13, INK, KR, "middle", 600)
d.t(XS[3] + BW / 2, FY + 54, "df 0 MiB", 12, OK, MONO)
cx = XS[2] + BW / 2
d.arrow([(cx, Y + BH + 4), (cx, FY + 38), (XS[3] - 6, FY + 38)], SOFT, "soft", 1.3, "5 4")
d.t(cx + 12, FY - 12, "프로세스 종료 · 재시작", 12, SOFT, KR, "start")
d.t(cx + 12, FY + 8, "unlink(2) 근거", 11, SOFT, KR, "start")

d.legend(H - 40, [("이름이 있는 상태", INFO), ("공간을 쥔 상태", ACC), ("공간이 돌아온 상태", OK),
                  ("man page 경로", SOFT)])
d.save("08-02.deleted-file.svg")
print("ok 08-02.deleted-file")
