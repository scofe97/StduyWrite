# 08-01 §3 「배운 것을 한 장면에 합치기」 — 서비스 하나를 재시작할 때 어느 프로세스가 어느 줄을 남기는가.
# 원문("journalctl"): "in one terminal we restart the service using systemctl restart apparmor, and in
#       another we execute the following command" 뒤의 `journalctl -f -u apparmor.service` 출력.
#       저자 주석은 "After systemd has stopped the service, here it comes back up again" 이다.
# 실제 값: 본문 출력 블록의 줄을 그대로 쓴다. 줄 끝 잘림(cle·al·rsy)과 줄임표 줄(...)은 원서 지면이
#       자르고 줄인 자리라 본문이 보존한 대로 둔다. 줄이 접힌 자리(Skipping profile in /
#       /etc/apparmor.d/disable: …)도 본문처럼 두 줄로 쓴다.
#       PID 13883 → 13904 와 타임스탬프 17:10:02 → 17:10:09 의 7초는 본문 해설이 짚은 값이다.
# 구조: 줄을 남기는 주체를 실제 프로세스 셋(systemd[1]·apparmor[13883]·apparmor[13904])으로 나눴다.
#       옛 프로세스는 자기 줄을 남기고 끝나고(×), 새 프로세스는 systemd 가 다시 올린 자리에서 생긴다.
#       오른쪽 창이 터미널 2 의 journalctl -f 화면이고, 줄마다 그 줄을 낸 프로세스에서 화살표가 온다.
# 축약: 행 간격은 시각에 비례하지 않는다(같은 초 안은 출력 순서만). 17:10:03 과 17:10:09 사이는
#       점선 끊김으로 표시했다. 줄이 journald 를 거쳐 저널에 쓰이는 단계는 §2 도식이 맡아 생략했다.
#       옛 프로세스의 끝(×)은 Stopped 줄보다 앞에 두었다 — 출력이 끝난 시각만 보여 줄 뿐 종료
#       시각 자체는 출력에 없다.
# 타입 스펙: type-sequence — 주체 넷 사이의 시간순 메시지. 프로세스 생성(13904)과 끝(13883)을
#           수명선의 시작과 끝으로 그린다. accent 는 systemd 가 다시 올리는 줄 하나.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 960, 700
d = D(W, H, "LEARNING MODERN LINUX · 08-01 §3",
      "재시작 한 번이 저널에 남기는 순서",
      "systemctl restart apparmor 를 친 뒤 journalctl -f -u apparmor.service 화면에 줄이 쌓이는 순서. "
      "옛 프로세스 apparmor[13883] 가 두 줄을 남기고 끝나고, systemd[1] 가 Stopped 와 Starting 을 남긴 뒤 "
      "새 프로세스 apparmor[13904] 를 올린다. 새 프로세스의 ...done. 은 Starting 에서 7초 뒤인 17:10:09 에 온다.",
      "같은 유닛 이름 아래 PID 가 13883 에서 13904 로 바뀐 자리가 재시작이다")

HY, HH, BW = 104, 44, 104
LX = {"t1": 96, "sd": 220, "old": 344, "new": 468}
PX0, PX1 = 556, 936                      # 터미널 2 창
ROW0, RS = 188, 34


def head(x, y, name, sub, col):
    d.box(x - BW / 2, y, BW, HH, PAPER2, col, 1.1, 6)
    d.t(x, y + 19, name, 12, INK if col == RULE else col,
        KR if any("가" <= c <= "힣" for c in name) else MONO, "middle", 600)
    d.t(x, y + 36, sub, 11, MUTED, KR if any("가" <= c <= "힣" for c in sub) else MONO)


# 행 y — 같은 초 안은 출력 순서대로 한 칸씩, 17:10:03 과 17:10:09 사이만 끊김 한 칸
Y = {}
y = ROW0
for k in ("restart", "c1", "c2", "dots", "stop", "start", "spawn", "p1", "p2"):
    Y[k] = y
    y += RS + (14 if k == "p2" else 0)
Y["gap"] = y + 4
y += RS + 10
for k in ("done", "started"):
    Y[k] = y
    y += RS
RAIL_END = Y["started"] + 16

# 수명선 — 먼저 그린다(글자와 화살표가 위에 오게)
d.line(LX["t1"], HY + HH, LX["t1"], Y["restart"] + 14, RULE, 1.0, "3 6")
d.line(LX["sd"], HY + HH, LX["sd"], RAIL_END, RULE, 1.0, "3 6")
OLD_END = Y["c2"] + 22
d.line(LX["old"], HY + HH, LX["old"], OLD_END, INFO, 1.2, "3 4")
d.line(LX["old"] - 7, OLD_END - 7, LX["old"] + 7, OLD_END + 7, INFO, 1.6)
d.line(LX["old"] - 7, OLD_END + 7, LX["old"] + 7, OLD_END - 7, INFO, 1.6)
d.t(LX["old"] + 14, OLD_END + 5, "끝", 12, INFO, KR, "start")
NEW_TOP = Y["spawn"] - HH / 2
d.line(LX["new"], NEW_TOP + HH, LX["new"], Y["done"] + 14, WARN, 1.2, "3 4")

head(LX["t1"], HY, "터미널 1", "명령을 친다", RULE)
head(LX["sd"], HY, "systemd[1]", "PID 1", RULE)
head(LX["old"], HY, "apparmor", "PID 13883", INFO)
head(LX["new"], NEW_TOP, "apparmor", "PID 13904", WARN)

# 터미널 2 창
PY0 = HY
PY1 = RAIL_END + 8
d.box(PX0, PY0, PX1 - PX0, PY1 - PY0, PAPER, RULE, 1.2, 8)
d.t(PX0 + 14, PY0 + 19, "터미널 2", 12, INK, KR, "start", 600)
d.t(PX0 + 80, PY0 + 19, "journalctl -f -u apparmor.service", 12, MUTED, MONO, "start")
d.line(PX0, PY0 + HH - 14, PX1, PY0 + HH - 14, RULE, 0.8)
TX = PX0 + 14


def pane(yy, txt, col=MUTED, w=400):
    d.t(TX, yy + 4, txt, 12, col, MONO, "start", w)


def emit(src, yy, txt, col, mk, w=400):
    d.arrow([(LX[src] + 8, yy), (PX0 - 6, yy)], col, mk, 1.3)
    d.o.append(f'<circle cx="{LX[src]}" cy="{yy}" r="4" fill="{col}"/>')
    pane(yy, txt, col if col != MUTED else INK, w)


pane(Y["restart"] - 22, "-- Logs begin at Sun 2021-01-24 14:36:30 GMT. --", SOFT)

# 터미널 1 → systemd
d.arrow([(LX["t1"] + 8, Y["restart"]), (LX["sd"] - 8, Y["restart"])], INK, "ar", 1.4)
d.t(24, Y["restart"] + 22, "systemctl restart apparmor", 11, MUTED, MONO, "start")

emit("old", Y["c1"], "17:10:02 All profile caches have been cle", INFO, "info")
emit("old", Y["c2"], "17:10:02 Unloading profiles will leave al", INFO, "info")
pane(Y["dots"], "...", SOFT)
emit("sd", Y["stop"], "17:10:02 Stopped AppArmor initialization.", MUTED, "ar")
emit("sd", Y["start"], "17:10:02 Starting AppArmor initialization...", ACC, "acc", 600)

# systemd 가 새 프로세스를 올림
d.arrow([(LX["sd"] + 8, Y["spawn"]), (LX["new"] - BW / 2 - 4, Y["spawn"])], WARN, "warn", 1.3)
d.t((LX["sd"] + LX["new"] - BW / 2) / 2, Y["spawn"] - 8, "다시 올림", 12, WARN, KR, "middle", 600)

emit("new", Y["p1"], "17:10:03 * Starting AppArmor profiles", WARN, "warn")
emit("new", Y["p2"], "17:10:03 Skipping profile in", WARN, "warn")
d.t(TX + 9 * 7.2, Y["p2"] + 20, "/etc/apparmor.d/disable: usr.sbin.rsy", 12, WARN, MONO, "start")

# 17:10:03 → 17:10:09 끊김
d.line(PX0 + 12, Y["gap"], PX1 - 12, Y["gap"], SOFT, 1.0, "2 5")
d.o.append(f'<rect x="{(PX0 + PX1) / 2 - 44}" y="{Y["gap"] - 10}" width="88" height="20" '
           f'rx="4" fill="{PAPER}" stroke="none"/>')
d.t((PX0 + PX1) / 2, Y["gap"] + 4, "6 초 뒤", 12, SOFT, KR)
d.line(LX["new"] - 10, Y["gap"], LX["new"] + 10, Y["gap"], SOFT, 1.2)

emit("new", Y["done"], "17:10:09 ...done.", OK, "ok", 600)
emit("sd", Y["started"], "17:10:09 Started AppArmor initialization.", MUTED, "ar")

# Starting → ...done. 의 7초
BX = 40
d.line(BX, Y["start"], BX, Y["done"], ACC, 1.2)
d.line(BX, Y["start"], BX + 8, Y["start"], ACC, 1.2)
d.line(BX, Y["done"], BX + 8, Y["done"], OK, 1.2)
MY = (Y["start"] + Y["done"]) / 2
d.t(BX + 10, MY - 4, "7 초", 14, INK, KR, "start", 600)
d.t(BX + 10, MY + 16, "프로파일 적재", 12, MUTED, KR, "start")

NY = PY1 + 26
d.t(24, NY, "줄 내용·잘림·줄임표는 본문 출력 그대로 · 행 간격은 시각 비례가 아니라 출력 순서", 11, SOFT, KR, "start")
d.legend(NY + 16, [("다시 올리는 줄", ACC), ("옛 PID 13883", INFO),
                   ("새 PID 13904", WARN), ("끝난 자리", OK)])
d.save("08-01.journal-restart.svg")
print("ok 08-01.journal-restart")
