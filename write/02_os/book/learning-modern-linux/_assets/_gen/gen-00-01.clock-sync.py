# 00-01 §2 시간과 날짜 — 시계 둘과 그 사이를 오가는 값, 그리고 타임존이 끼어드는 자리.
# 근거(hwclock(8), util-linux): Hardware Clock 은 "operates when the machine is powered off", System
#       Clock 은 "part of the Linux kernel ... the number of seconds since 00:00:00 January 1, 1970
#       UTC". "The Hardware Clock's basic purpose is to keep time when Linux is not running so that
#       the System Clock can be initialized from it at boot." 11 minute mode: 커널이 동기 상태일 때
#       "copies the System Time to the Hardware Clock every 11 minutes". --systohc: "Set the Hardware
#       Clock from the System Clock".
#     (localtime(5)): /etc/localtime 은 "used by applications for presentation to the user".
# 실행(debian:12, TZ=Asia/Seoul, 에포크 1794276000): date -u → 2026-11-10T02:00:00Z,
#       date +%FT%T%:z → 2026-11-10T11:00:00+09:00
# 타입 스펙: type-architecture — 구성요소 셋(RTC · 시스템 클럭 · NTP 데몬)과 그 사이 직교 연결, 아래에
#           시스템 클럭 값 하나가 세 표기로 나가는 자리. accent 는 모든 화살표가 모이는 시스템 클럭.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, BAD, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 436
d = D(W, H, "LEARNING MODERN LINUX · 00-01 §2",
      "시계는 둘이고 타임존은 표기에만 붙는다",
      "RTC 는 전원이 꺼져도 가는 하드웨어 시계이고 시스템 클럭은 커널이 1970-01-01 UTC 부터 세는 초다. "
      "부팅 때 RTC 값으로 시스템 클럭을 맞추고, NTP 데몬이 시스템 클럭을 보정하며, 동기 상태에서는 커널이 "
      "11분마다 그 값을 RTC 에 되적는다. 타임존은 같은 초를 화면에 적을 때만 쓰인다.",
      "에포크 1794276000 하나를 세 가지로 적은 값")

BY, BH, BW = 120, 92, 200
RX, KX, NX = 24, 340, 656

d.box(RX, BY, BW, BH, PAPER2, RULE, 1.0, 6)
d.t(RX + BW / 2, BY + 28, "RTC · 하드웨어 클럭", 14, INK, KR, "middle", 600)
d.t(RX + BW / 2, BY + 52, "전원이 꺼져도 유지", 12, MUTED)
d.t(RX + BW / 2, BY + 74, "hwclock --show", 12, INFO, MONO)

d.tone(KX, BY, BW, BH, ACC, 6, "1F", 1.5)
d.t(KX + BW / 2, BY + 28, "시스템 클럭 · 커널", 14, INK, KR, "middle", 600)
d.t(KX + BW / 2, BY + 52, "1970-01-01 UTC 부터 센 초", 12, MUTED)
d.t(KX + BW / 2, BY + 74, "1794276000", 13, ACC, MONO, "middle", 600)

d.box(NX, BY, BW, BH, PAPER2, RULE, 1.0, 6)
d.t(NX + BW / 2, BY + 28, "NTP 데몬", 14, INK, KR, "middle", 600)
d.t(NX + BW / 2, BY + 52, "NTP 서버 시각 수신", 12, MUTED)
d.t(NX + BW / 2, BY + 74, "systemd-timesyncd · chronyd", 11, INFO, MONO)

# RTC ↔ 시스템 클럭
d.t((RX + BW + KX) / 2, BY + 22, "부팅 때 읽기", 12, MUTED)
d.arrow([(RX + BW + 6, BY + 32), (KX - 8, BY + 32)], MUTED, "ar", 1.5)
d.arrow([(KX - 6, BY + 64), (RX + BW + 8, BY + 64)], MUTED, "ar", 1.5)
d.t((RX + BW + KX) / 2, BY + 84, "11분마다 기록", 12, MUTED)
# NTP → 시스템 클럭
d.t((KX + BW + NX) / 2, BY + 38, "보정", 12, OK)
d.arrow([(NX - 6, BY + 48), (KX + BW + 8, BY + 48)], OK, "ok", 1.5)

d.t(RX, BY + BH + 24, "손으로 되적기: hwclock --systohc", 12, MUTED, KR, "start")

# 시스템 클럭 → 세 표기
TY = 296
cells = [(24, "date +%s", "1794276000", "타임존과 무관"),
         (308, "date -u +%FT%TZ", "2026-11-10T02:00:00Z", "UTC 표기"),
         (592, "date +%FT%T%:z", "2026-11-10T11:00:00+09:00", "/etc/localtime 적용")]
CWD = 264
cx = KX + BW / 2
d.line(cx, BY + BH + 2, cx, 264, MUTED, 1.4)
d.line(24 + CWD / 2, 264, 592 + CWD / 2, 264, MUTED, 1.4)
d.t(cx + 12, 252, "같은 순간의 세 표기", 12, MUTED, KR, "start")
for x, cmd, val, cap in cells:
    d.arrow([(x + CWD / 2, 264), (x + CWD / 2, TY - 6)], MUTED, "ar", 1.4)
    d.box(x, TY, CWD, 76, PAPER2, RULE, 1.0, 6)
    d.t(x + CWD / 2, TY + 22, cmd, 12, INFO, MONO)
    d.t(x + CWD / 2, TY + 44, val, 13, INK, MONO, "middle", 600)
    d.t(x + CWD / 2, TY + 64, cap, 12, MUTED, MONO if cap.startswith("/") else KR)

d.legend(392, [("시스템 클럭", ACC), ("NTP 보정", OK), ("확인 명령", INFO)])
d.save("00-01.clock-sync.svg")
print("ok 00-01.clock-sync.svg")
