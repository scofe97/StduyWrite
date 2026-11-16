# 06-01 §6 — 단위 파일 둘이 실제 파일 → 프로세스 → 저널 → 터미널 출력 한 줄이 되기까지.
# 원문("Example: scheduling greeter"): "let's assume we want to launch our greeter app every hour.
#       First, we define a systemd unit file of type service. ... Next, we define a timer unit to launch
#       the greeter service every hour. ... Now we copy both unit files to /run/systemd/system so that
#       systemd recognizes them."
#  실제 값 — 단위 파일 본문(greeter.service: Description=My Greeting Service, Type=oneshot,
#       ExecStart=/home/mh9/greeter.sh / greeter.timer: Description=Runs Greeting service at the top of
#       the hour, OnCalendar=hourly), ls 출력의 크기(117 · 107), status 출력("Active: active (waiting)
#       since Sun 2021-09-12 13:10:35 IST", "Trigger: Sun 2021-09-12 14:00:00 IST; 49min left"),
#       journalctl 출력("Sep 12 14:00:01 starlite systemd[1]: Starting My Greeting Service...",
#       "Sep 12 14:00:01 starlite greeter.sh[21071]: You are awesome!").
#       저자 노트 — "the stdout output is going directly to the logs". 본문 §5 — 저널은
#       systemd-journald 데몬이 관리하는 바이너리 파일.
# 타입 스펙: type-architecture — 디스크의 파일과 실행 중인 프로세스·저널을 존 둘로 나누고, 순서를 번호
#           붙은 화살표 1~4 로 싣는다. accent 는 systemd[1], 곧 로그의 [1] 이 가리키는 PID 1.
# 축약: timer 의 Description 은 앞부분만 적었다. 배포판별 활성화 차이(Debian 기본 · Red Hat 명시)는
#       구조가 아니라 본문 §6 에 맡겼다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, PAPER, PAPER2, RULE, KR, MONO, esc

W, H = 960, 666
d = D(W, H, "LEARNING MODERN LINUX · 06-01 §6",
      "단위 파일 둘이 로그 한 줄이 되기까지",
      "/run/systemd/system 에 복사한 greeter.timer(OnCalendar=hourly)와 greeter.service"
      "(Type=oneshot, ExecStart=/home/mh9/greeter.sh)를 systemd[1] 이 읽는다. 타이머는 active "
      "(waiting) 로 14:00:00 을 기다리다가 서비스를 띄우고, greeter.sh[21071] 의 표준 출력 "
      "You are awesome! 이 systemd-journald 의 저널로 간다. journalctl -f -u greeter.service 가 "
      "그 두 줄을 보여 준다.",
      "로그의 systemd[1] 이 부팅 넷째 단계의 그 PID 1 이다")


def zone(x, y, w, h, label, fam=KR):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{INK}05" '
               f'stroke="{SOFT}" stroke-width="1" stroke-dasharray="5 4"/>')
    d.t(x + 16, y + 22, label, 12, SOFT, fam, "start", 600)


zone(24, 104, 324, 312, "/run/systemd/system/", MONO)
zone(368, 104, 568, 312, "실행 중 — 사용자 공간")

# 연결선 — 글자보다 먼저
d.arrow([(332, 196), (386, 196)], INFO, "info", 1.5)
d.t(358, 186, "1", 13, INFO, KR, "middle", 600)
d.t(332, 126, "1. cp 뒤 인식", 12, INFO, KR, "end", 600)
d.path("M 332 340 L 460 340 L 460 260", INFO, 1.2, m="info")
d.t(470, 304, "읽음", 12, INFO, KR, "start")
d.arrow([(628, 196), (678, 196)], ACC, "acc", 1.5)
d.t(653, 186, "2. 실행", 12, ACC, KR, "middle", 600)
d.arrow([(800, 252), (800, 302)], OK, "ok", 1.5)
d.t(810, 282, "3. 표준 출력", 12, OK, KR, "start", 600)
d.path("M 560 260 L 560 352 L 678 352", MUTED, 1.2, m="ar")
d.t(572, 342, "시작 메시지", 12, MUTED, KR, "start")
d.arrow([(800, 398), (800, 454)], INFO, "info", 1.5)
d.t(810, 442, "4. journalctl -u", 12, INFO, MONO, "start", 600)


def unitfile(x, y, w, name, size, lines):
    h = 34 + len(lines) * 18 + 8
    d.box(x, y, w, h, PAPER, INFO, 1.2, 6)
    d.t(x + 12, y + 22, name, 13, INFO, MONO, "start", 600)
    d.t(x + w - 12, y + 22, size, 12, SOFT, MONO, "end")
    d.line(x + 8, y + 32, x + w - 8, y + 32, RULE, 1)
    for i, ln in enumerate(lines):
        d.t(x + 12, y + 50 + i * 18, ln, 12, INK if "=" in ln else MUTED, MONO, "start")
    return h


unitfile(40, 140, 292, "greeter.timer", "107 B",
         ["[Unit]", "Description=Runs Greeting …", "[Timer]", "OnCalendar=hourly"])
unitfile(40, 268, 292, "greeter.service", "117 B",
         ["[Unit]", "Description=My Greeting Service", "[Service]", "Type=oneshot",
          "ExecStart=/home/mh9/greeter.sh"])

# systemd[1] — 타이머를 쥐고 기다린다
SX, SY, SW, SH = 388, 140, 240, 118
d.o.append(f'<rect x="{SX}" y="{SY}" width="{SW}" height="{SH}" rx="8" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(SX + 14, SY + 20, "PID 1", 12, ACC, KR, "start")
d.t(SX + 14, SY + 44, "systemd[1]", 15, ACC, MONO, "start", 600)
d.t(SX + 14, SY + 68, "greeter.timer", 12, INK, MONO, "start")
d.t(SX + 14, SY + 86, "active (waiting)", 12, MUTED, MONO, "start")
d.t(SX + 14, SY + 106, "Trigger 14:00:00 · 49min left", 12, MUTED, MONO, "start")

# greeter.sh[21071] — 실행하고 끝나는 프로세스
d.box(680, 140, 240, 112, PAPER2, OK, 1.2, 8)
d.t(694, 164, "greeter.sh[21071]", 14, OK, MONO, "start", 600)
d.t(694, 188, "/home/mh9/greeter.sh", 12, MUTED, MONO, "start")
d.t(694, 212, "oneshot · 실행하고 끝남", 12, MUTED, KR, "start")
d.t(694, 236, "You are awesome!", 12, INK, MONO, "start")

# 저널
d.box(680, 304, 240, 94, PAPER2, OK, 1.2, 8)
d.t(694, 328, "저널", 14, OK, KR, "start", 600)
d.t(694, 352, "systemd-journald", 12, MUTED, MONO, "start")
d.t(694, 376, "바이너리 파일 · 중앙 저장소", 12, MUTED, KR, "start")

# 터미널 — journalctl 출력 그대로
TY = 456
d.box(24, TY, W - 48, 118, PAPER, MUTED, 1.0, 8)
d.t(40, TY + 24, "$ sudo journalctl -f -u greeter.service", 13, INFO, MONO, "start", 600)
d.t(40, TY + 50, "-- Logs begin at Sun 2021-01-24 14:36:30 GMT. --", 12, SOFT, MONO, "start")


def logline(y, who, msg, c):
    d.o.append(f'<text x="40" y="{y}" text-anchor="start" font-family="{MONO}" font-size="13" '
               f'fill="{MUTED}">Sep 12 14:00:01 starlite <tspan fill="{c}" font-weight="600">'
               f'{esc(who)}</tspan>: <tspan fill="{INK}">{esc(msg)}</tspan></text>')


logline(TY + 76, "systemd[1]", "Starting My Greeting Service...", ACC)
logline(TY + 100, "greeter.sh[21071]", "You are awesome!", OK)

d.t(24, 602, "timer 의 Description 은 앞부분만 · 시각 값은 status · journalctl 출력 그대로", 11, SOFT, KR, "start")
d.legend(618, [("단위 파일 · 사람이 하는 일", INFO), ("PID 1", ACC), ("표준 출력이 로그가 되는 길", OK)])
d.save("06-01.greeter-timer.svg")
print("ok 06-01.greeter-timer")
