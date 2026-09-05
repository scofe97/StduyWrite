# 08-01 §5 — /var/log 아래 무엇이 어디에 쌓이는가.
# 원문("Logging") 의 `ls -al /var/log` 주석: auth.log("Logs of all login attempts (successful and failed)
#       and authentication processes"), btmp("Failed login attempts"), cups/("Printing related logs"),
#       dpkg.log("Logs of the dpkg package manager"), apt/("Logs of the apt package manager"),
#       dmesg("Device driver logs; use dmesg to inspect"), installer/("System install logs (when the Linux
#       distro was originally installed)"), journal/("The journalctl location"), kern.log("The kernel
#       logs"), lastlog("All last logins of all users; use lastlog to inspect"), ntpstats/("NTP-related
#       logs"), syslog("The syslogd location").
# 주의: 묶음 다섯(인증 · 커널 · 패키지 · 로깅 시스템 · 그 밖)은 원문에 없다. 저자는 열두 항목을 한 줄씩
#       주석했을 뿐이고, 묶음은 이 노트가 읽기 쉬우라고 세운 것이라 legend 에 그렇게 적었다.
# 타입 스펙: type-tree — 부모에서 자식으로 내려가는 포함 관계. 실제 디렉터리 구조를 닮게 그린다.
#           직교 연결만 쓴다. accent 는 다음 절로 이어지는 자리 하나.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER2, RULE, KR, MONO

W, H = 880, 732
d = D(W, H, "LEARNING MODERN LINUX · 08-01 §5",
      "/var/log 는 무엇이 어디 쌓이는지의 지도다",
      "저자가 한 줄씩 주석한 열두 항목을 성격별로 묶어 트리로 세운 것. 묶음 이름은 원문에 없고 "
      "읽기 편하라고 이 노트가 붙였다.",
      "journal/ 만 디렉터리 권한이 다른데 그 이유가 다음 절로 이어집니다")

RX, RW, RH = 24, 132, 44
GX, GW, GH = 196, 168, 40
IX, IW, IH = 400, 456, 32
Y0, ISTRIDE = 112, 40

groups = [
    ("인증과 로그인", INFO, [
        ("auth.log", "로그인 시도 전부와 인증 과정"),
        ("btmp", "실패한 로그인 시도"),
        ("lastlog", "모든 사용자의 마지막 로그인 — lastlog 로 본다")]),
    ("커널과 장치", WARN, [
        ("kern.log", "커널 로그"),
        ("dmesg", "장치 드라이버 로그 — dmesg 로 본다")]),
    ("패키지 관리자", OK, [
        ("apt/", "apt 패키지 관리자 로그"),
        ("dpkg.log", "dpkg 패키지 관리자 로그")]),
    ("로깅 시스템이 사는 곳", ACC, [
        ("syslog", "syslogd 가 쓰는 자리"),
        ("journal/", "journalctl 이 읽는 자리 — drwxr-sr-x+")]),
    ("그 밖", MUTED, [
        ("cups/", "인쇄 관련 로그"),
        ("installer/", "배포판을 처음 설치할 때의 기록"),
        ("ntpstats/", "NTP 관련 로그")]),
]

d.box(RX, Y0, RW, RH, PAPER2, RULE, 1.1, 6)
d.t(RX + RW / 2, Y0 + 20, "/var/log/", 14, INK, MONO, "middle", 600)
d.t(RX + RW / 2, Y0 + 36, "중앙 로그 디렉터리", 10.5, MUTED, KR)

row = 0
gcenters = []
for gname, gcol, items in groups:
    gtop = Y0 + row * ISTRIDE
    gspan = len(items) * ISTRIDE
    gy = gtop + (gspan - GH) / 2
    d.box(GX, gy, GW, GH, PAPER2, gcol, 1.2, 6)
    d.t(GX + 14, gy + 24, gname, 12.5, gcol, KR, "start", 600)
    gcenters.append(gy + GH / 2)
    for k, (nm, note) in enumerate(items):
        iy = gtop + k * ISTRIDE + (ISTRIDE - IH) / 2
        focal = (nm == "journal/")
        if focal:
            d.tone(IX, iy, IW, IH, ACC, 5, "12", 1.3)
        else:
            d.box(IX, iy, IW, IH, PAPER2, RULE, 0.9, 5)
        d.t(IX + 14, iy + 21, nm, 12, ACC if focal else INK, MONO, "start", 600)
        d.t(IX + 132, iy + 21, note, 11.5, MUTED, KR, "start")
        d.path(f"M {GX + GW} {gy + GH / 2} L {(GX + GW + IX) / 2} {gy + GH / 2} "
               f"L {(GX + GW + IX) / 2} {iy + IH / 2} L {IX - 4} {iy + IH / 2}",
               gcol, 1.0, m=None)
    row += len(items)

BUS = (RX + RW + GX) / 2
d.line(BUS, Y0 + RH / 2, BUS, gcenters[-1], MUTED, 1.0)
d.path(f"M {RX + RW} {Y0 + RH / 2} L {BUS} {Y0 + RH / 2}", MUTED, 1.1)
for gc in gcenters:
    d.path(f"M {BUS} {gc} L {GX - 4} {gc}", MUTED, 1.1, m="ar")

NY = Y0 + row * ISTRIDE + 24
d.t(24, NY + 4, "저자는 읽기 좋게 줄인 출력이라고 밝힙니다. 파일마다 그룹이 갈려 있는 것이 눈에 띄는 대목입니다.",
    12, MUTED, KR, "start")
d.t(24, NY + 26, "auth.log 는 adm 그룹, btmp 는 utmp 그룹, journal/ 은 systemd-journal 그룹이 읽습니다.",
    12, MUTED, KR, "start")
d.t(24, NY + 48, "journal/ 의 권한 문자열 끝에 붙은 + 는 ACL 이 걸려 있다는 표시이고, 그룹 자리의 s 는 setgid 입니다.",
    12, SOFT, KR, "start")

d.legend(688, [("다음 절로 이어지는 자리", ACC), ("인증과 로그인", INFO),
                  ("커널과 장치", WARN), ("패키지 관리자", OK)])
d.save("08-01.var-log-tree.svg")
print("ok 08-01.var-log-tree")
