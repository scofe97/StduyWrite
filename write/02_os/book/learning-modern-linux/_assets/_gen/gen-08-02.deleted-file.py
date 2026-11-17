# 08-02 §4 — 지운 파일이 열린 fd 로 살아 있는 실제 자리. lsof +L1 한 줄의 열(COMMAND·PID·FD /
#           SIZE/OFF·NLINK·NODE / NAME)이 각각 프로세스와 fd, 아이노드, 디렉터리 항목을 가리키고,
#           아이노드의 200 MiB 블록이 300 MiB tmpfs 를 차지해 df 가 200 을 센다.
# 실측: debian:12 컨테이너, 300MiB tmpfs /data (2026-11-10).
#   dd 200MiB app.log · tail -f app.log & · rm app.log → ls -la /data 는 . 와 .. 뿐(total 0)
#   df -m /data → "tmpfs 300 200 100 67% /data"
#   lsof +L1 → "tail 3678 root 3r REG 0,397 209715200 0 2 /data/app.log (deleted)"
#   : > /proc/3678/fd/3 → df 0
# 1차 자료: unlink(2) "the file will remain in existence until the last file descriptor referring to it is closed".
#           lsof(8) +L1 "will select open files that have been unlinked".
# 타입 스펙: type-architecture — lsof 출력의 열과 그 값을 가진 객체(프로세스 fd · 아이노드 · 디렉터리 ·
#           tmpfs 블록 · df)를 잇는 실제 구조. accent 는 공간을 쥔 fd 3.
# 축약: lsof 의 USER·TYPE·DEVICE 열은 뺐다. 막대는 300 MiB 를 그대로 비율로 그렸다(200 : 100).
#       종료·재시작으로 fd 가 닫히는 길은 unlink(2) 근거라 점선 줄로 둔다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, BAD, WARN, PAPER2, RULE, KR, MONO

W, H = 920, 640
d = D(W, H, "LEARNING MODERN LINUX · 08-02 §4",
      "이름은 사라졌는데 fd 3 이 200 MiB 를 쥐고 있다",
      "300 MiB tmpfs /data 에 200 MiB app.log 를 만들고 tail -f(PID 3678)로 연 채 rm 했다. "
      "ls -la /data 에는 . 와 .. 만 남지만 df -m 은 Used 200 을 보인다. lsof +L1 의 한 줄에서 "
      "COMMAND·PID·FD 는 프로세스와 fd 3 을, SIZE/OFF·NLINK·NODE 는 크기 209715200 바이트에 링크 수 0 인 "
      "아이노드 2 를, NAME 의 (deleted) 는 디렉터리에서 사라진 이름을 가리킨다. "
      ": > /proc/3678/fd/3 으로 크기를 0 으로 자르자 df 가 0 으로 돌아왔다.",
      "lsof +L1 한 줄의 열마다 그 값을 가진 객체가 있다 — 공간을 쥔 것은 fd 3 이다")

# ── 1줄: lsof +L1 출력의 열 ──────────────────────────────────
CY, CH = 116, 56
d.t(24, CY - 8, "$ lsof +L1", 12, MUTED, MONO, "start", 600)
cells = [  # (헤더, 값, x0, 폭, 값 색)
    ("COMMAND", "tail", 24, 72, INK), ("PID", "3678", 100, 56, INK), ("FD", "3r", 160, 48, ACC),
    ("SIZE/OFF", "209715200", 256, 104, INK), ("NLINK", "0", 364, 64, BAD), ("NODE", "2", 432, 56, INK),
    ("NAME", "/data/app.log (deleted)", 536, 232, BAD),
]
GROUPS = [(24, 208), (256, 488), (536, 768)]       # 프로세스 · 아이노드 · 디렉터리로 내려가는 묶음

# 묶음에서 객체로 내려가는 선은 상자보다 먼저
RY0, RY1 = 236, 356
for gx0, gx1 in GROUPS:
    cx = (gx0 + gx1) / 2
    d.line(cx, CY + CH + 2, cx, RY0 - 2, SOFT, 1.0, "3 3")

for head, val, x, w, c in cells:
    d.box(x, CY, w, CH, PAPER2, ACC if c is ACC else RULE, 1.4 if c is ACC else 0.9, 4)
    d.t(x + 8, CY + 18, head, 11, SOFT, MONO, "start")
    d.t(x + 8, CY + 42, val, 13, c, MONO, "start", 600)

# ── 2줄: 프로세스 · 아이노드 · 디렉터리 ─────────────────────
# 연결선 먼저
d.arrow([(198, 316), (253, 316)], ACC, "acc", 1.8)                 # fd 3 → 아이노드
d.line(546, 324, 490, 324, BAD, 1.2, "3 4")                        # 디렉터리 항목 → 아이노드: 끊김
d.t(512, 329, "✕", 14, BAD, MONO)
d.arrow([(372, RY1 + 2), (372, 400)], BAD, "bad", 1.4)             # 아이노드 → 블록

# 프로세스와 fd 테이블
d.box(24, RY0, 184, RY1 - RY0, PAPER2, RULE, 1.0, 8)
d.t(40, RY0 + 24, "PID 3678", 13, INK, MONO, "start", 600)
d.t(40, RY0 + 44, "tail -f", 12, MUTED, MONO, "start")
d.t(40, RY0 + 66, "fd 테이블", 12, SOFT, KR, "start")
d.o.append(f'<rect x="36" y="{RY0 + 76}" width="160" height="32" rx="4" '
           f'fill="{ACC}1F" stroke="{ACC}" stroke-width="1.4"/>')
d.t(48, RY0 + 97, "3r · 읽기", 13, ACC, MONO, "start", 600)

# 아이노드
d.tone(256, RY0, 232, RY1 - RY0, BAD, 8)
d.t(272, RY0 + 24, "아이노드 · NODE 2", 13, INK, KR, "start", 600)
d.t(272, RY0 + 52, "NLINK 0 · 이름 없음", 12, BAD, KR, "start")
d.t(272, RY0 + 76, "209715200 B", 13, INK, MONO, "start", 600)
d.t(272, RY0 + 96, "= 200 MiB", 12, MUTED, MONO, "start")

# 디렉터리 /data
d.box(536, RY0, 232, RY1 - RY0, PAPER2, INFO, 1.1, 8)
d.t(552, RY0 + 24, "디렉터리 /data", 13, INK, KR, "start", 600)
d.t(552, RY0 + 48, "ls -la → .  ..  (total 0)", 12, INFO, MONO, "start")
d.o.append(f'<rect x="548" y="{RY0 + 72}" width="208" height="32" rx="4" fill="{BAD}14" '
           f'stroke="{BAD}" stroke-width="1" stroke-dasharray="4 3"/>')
d.t(560, RY0 + 93, "app.log", 13, BAD, MONO, "start", 600)
d.line(558, RY0 + 88, 620, RY0 + 88, BAD, 1.4)
d.t(636, RY0 + 93, "rm → 이름만 삭제", 12, BAD, KR, "start")

# ── 3줄: tmpfs 블록 막대와 df ────────────────────────────────
BX0, BX1, BY, BH = 24, 712, 404, 40
used_x = BX0 + (BX1 - BX0) * 200 / 300
d.line(BX1 + 2, BY + BH / 2, 756, BY + BH / 2, WARN, 1.2, "3 3")    # df 가 막대 전체를 센다
d.o.append(f'<rect x="{BX0}" y="{BY}" width="{used_x - BX0:.1f}" height="{BH}" rx="4" '
           f'fill="{BAD}33" stroke="{BAD}" stroke-width="1.1"/>')
d.o.append(f'<rect x="{used_x + 2:.1f}" y="{BY}" width="{BX1 - used_x - 2:.1f}" height="{BH}" rx="4" '
           f'fill="none" stroke="{SOFT}" stroke-width="1" stroke-dasharray="4 3"/>')
d.t((BX0 + used_x) / 2 + 40, BY + 25, "200 MiB · 이름 없는 app.log 의 데이터", 12, INK, KR)
d.t((used_x + BX1) / 2, BY + 25, "100 MiB 빔", 12, MUTED, KR)
d.t(384, 384, "데이터", 12, BAD, KR, "start")
d.t(BX0, BY + BH + 20, "tmpfs /data · 크기 300 MiB", 12, SOFT, MONO, "start")

d.box(760, BY - 24, 136, 88, PAPER2, WARN, 1.2, 8)
d.t(776, BY - 2, "df -m /data", 12, WARN, MONO, "start", 600)
d.t(776, BY + 26, "Used 200", 18, WARN, MONO, "start", 600)
d.t(776, BY + 48, "Avail 100 · 67%", 12, MUTED, MONO, "start")

# ── 4줄: 공간을 돌려받는 길 ──────────────────────────────────
FY = 520
d.t(24, FY, ": > /proc/3678/fd/3", 13, OK, MONO, "start", 600)
d.t(208, FY, "fd 3 으로 크기를 0 으로 자름 → df 200 → 0 · 내용은 못 되살림", 13, OK, KR, "start")
d.line(24, FY + 24, 56, FY + 24, SOFT, 1.2, "4 3")
d.t(68, FY + 28, "fd 닫힘(종료 · 재시작) → 마지막 참조가 사라져 해제 · unlink(2)", 12, SOFT, KR, "start")

d.t(24, FY + 60, "PID·FD·크기·NLINK·NODE·df 값은 본문 실측 그대로 · lsof 의 USER·TYPE·DEVICE 열은 생략",
    11, SOFT, KR, "start")
LEG = FY + 76
d.legend(LEG, [("이름이 있던 자리", INFO), ("붙잡힌 공간", BAD), ("df 가 세는 자리", WARN), ("회수", OK)])
assert LEG + 40 <= H, (LEG, H)
d.save("08-02.deleted-file.svg")
print("ok 08-02.deleted-file")
