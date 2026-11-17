# 08-01 §3 「세부 — /var/log 배포판별 파일·바이너리 기록」 — /var/log 아래 항목을 누가 쓰고 무엇으로 읽는가.
# 원문("Logging") 의 `ls -al /var/log` 주석 열두 항목: auth.log, btmp, cups/, dpkg.log, apt/, dmesg,
#       installer/, journal/, kern.log, lastlog, ntpstats/, syslog.
# 실제 값(본문):
#   - 쓰는 쪽: "이름을 정하는 것은 커널도 systemd 도 아니고 §2 에서 본 rsyslog 의 기본 규칙"(syslog·auth.log·
#     kern.log, 본문 표 Debian 12 열), journald 의 바이너리 저널(journal/), "wtmp 를 고쳐 쓰는 login·init 같은
#     프로그램"(utmp(5), 로그인 기록 세 파일 표의 btmp·lastlog), 패키지 관리자(apt/·dpkg.log, 본문 표),
#     Ubuntu 의 /var/log/dmesg 는 "부팅 때 저장해 둔 사본".
#   - 소유자·권한: 본문 ls 출력 세 줄 — auth.log `-rw-r----- syslog adm`, btmp `-rw-rw---- root utmp`,
#     journal/ `drwxr-sr-x+ root systemd-journal`. 나머지 항목의 권한은 본문에 없어 적지 않았다.
#   - 읽는 쪽: tail -f /var/log/syslog, 회전본은 zgrep(§4), 저널은 journalctl, btmp 는 lastb, lastlog 는 lastlog,
#     dmesg 사본 뒤의 커널 메시지는 dmesg·journalctl -k.
# 축약: 묶음은 쓰는 쪽 기준으로 이 노트가 나눴다. cups/·installer/·ntpstats/ 는 본문이 쓰는 쪽을 다루지 않아
#       이름과 원문 주석 한 단어만 두었다.
# 타입 스펙: type-tree — /var/log/ 부모 아래 자식 항목 열둘. 왼쪽에 각 묶음을 쓰는 쪽, 오른쪽에 읽는 명령을
#           붙였다. 직교 연결만 쓴다. accent 는 이름을 정하는 rsyslog 규칙 하나(본문이 도식 바로 뒤에 짚는 점).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 668
d = D(W, H, "LEARNING MODERN LINUX · 08-01 §3",
      "/var/log 는 무엇이 어디 쌓이는지의 지도다",
      "Debian 계열 /var/log 의 주요 항목 열둘을 쓰는 쪽별로 묶은 지도. syslog·auth.log·kern.log 는 rsyslog 규칙이 "
      "이름을 정하고, journal/ 은 journald 가, btmp·lastlog 는 login·init 같은 프로그램이 쓴다. 바이너리 항목은 "
      "cat 대신 journalctl·lastb·lastlog 로 읽는다. 소유 그룹은 auth.log 가 adm, btmp 가 utmp, journal/ 이 "
      "systemd-journal 이다.",
      "파일 이름을 정하는 것은 커널도 systemd 도 아닌 rsyslog 규칙이다")


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


# 묶음: (쓰는 쪽, 부제, 색, [(이름, 권한·소유, 바이너리?, 읽는 법)])
groups = [
    ("rsyslog", "규칙이 이름을 정함", ACC, [
        ("syslog", "대부분의 시스템 메시지", False, ""),
        ("auth.log", "-rw-r----- syslog adm", False, ""),
        ("kern.log", "커널", False, "")]),
    ("journald", "바이너리 저널", INFO, [
        ("journal/", "drwxr-sr-x+ root systemd-journal", True, "journalctl")]),
    ("login · init 등", "고정 크기 레코드", INFO, [
        ("btmp", "-rw-rw---- root utmp", True, "lastb"),
        ("lastlog", "사용자마다 마지막 로그인", True, "lastlog")]),
    ("apt · dpkg", "패키지 관리자", MUTED, [
        ("apt/", "", False, ""),
        ("dpkg.log", "", False, "")]),
    ("부팅 때 저장", "Ubuntu 의 사본", MUTED, [
        ("dmesg", "", False, "그 뒤는 journalctl -k")]),
    (None, "", SOFT, [
        ("cups/", "인쇄", False, ""),
        ("installer/", "설치", False, ""),
        ("ntpstats/", "NTP", False, "")]),
]

WX0, WX1 = 24, 232                 # 쓰는 쪽
DX0, DX1 = 288, 664                # /var/log/
RX = 704                           # 읽는 쪽
TOP = 116
RS, GAP = 28, 14

d.t(WX0, TOP - 12, "쓰는 쪽", 12, SOFT, KR, "start", 600)
d.t(RX, TOP - 12, "읽는 명령", 12, SOFT, KR, "start", 600)

# 디렉터리 상자 높이를 먼저 센다
nrows = sum(len(g[3]) for g in groups)
DH = 48 + nrows * RS + (len(groups) - 1) * GAP + 8
d.box(DX0, TOP, DX1 - DX0, DH, PAPER2, RULE, 1.2, 8)
d.t(DX0 + 16, TOP + 26, "/var/log/", 15, INK, MONO, "start", 600)
d.t(DX0 + 112, TOP + 26, "ls -al 의 주요 항목 열둘", 12, MUTED, KR, "start")
d.line(DX0 + 10, TOP + 40, DX1 - 10, TOP + 40, RULE, 0.8)

y = TOP + 48
for wname, wsub, wcol, items in groups:
    gy0 = y
    for name, meta, binary, reader in items:
        cy = y + RS / 2
        ncol = INFO if binary else INK
        d.t(DX0 + 20, cy + 5, name, 13, ncol, MONO, "start", 600)
        if meta:
            d.t(DX0 + 120, cy + 5, meta, 11 if not kr(meta) == KR else 12,
                SOFT if kr(meta) == MONO else MUTED, kr(meta), "start")
        if reader:
            rc = INFO if binary else MUTED
            d.arrow([(DX1 + 4, cy), (RX - 6, cy)], rc, "info" if binary else "ar", 1.1)
            d.t(RX + 2, cy + 5, reader, 12, rc, kr(reader), "start", 600 if binary else 400)
        y += RS
    gy1 = y
    if wcol == ACC:                      # rsyslog 파일 묶음 전체에 읽는 법 하나
        gc = (gy0 + gy1) / 2
        d.line(DX1 + 8, gy0 + 4, DX1 + 8, gy1 - 4, MUTED, 1.2)
        d.arrow([(DX1 + 12, gc), (RX - 6, gc)], MUTED, "ar", 1.1)
        d.t(RX + 2, gc - 4, "tail -f · grep", 12, MUTED, MONO, "start")
        d.t(RX + 2, gc + 14, "회전본은 zgrep", 12, MUTED, KR, "start")
    if wname:
        gc = (gy0 + gy1) / 2
        bh = 44
        if wcol == ACC:
            d.tone(WX0, gc - bh / 2, WX1 - WX0, bh, ACC, 6, "14", 1.4)
        else:
            d.box(WX0, gc - bh / 2, WX1 - WX0, bh, PAPER2, wcol, 1.1, 6)
        d.t(WX0 + 14, gc - 3, wname, 13, wcol if wcol != MUTED else INK, kr(wname), "start", 600)
        d.t(WX0 + 14, gc + 14, wsub, 11, MUTED, kr(wsub), "start")
        # 묶음 괄호 + 쓰기 화살표
        d.line(DX0 - 8, gy0 + 4, DX0 - 8, gy1 - 4, wcol if wcol != MUTED else SOFT, 1.2)
        d.arrow([(WX1 + 4, gc), (DX0 - 12, gc)], wcol if wcol != MUTED else SOFT,
                "acc" if wcol == ACC else ("info" if wcol == INFO else "soft"), 1.3)
    else:
        d.t(WX0 + 14, (gy0 + gy1) / 2 + 4, "그 밖 · 본문 밖", 12, SOFT, KR, "start")
    y += GAP

NY = TOP + DH + 28
d.t(24, NY, "묶음은 쓰는 쪽으로 이 노트가 나눔 · 권한·소유는 본문 ls 세 줄만 · 파란 이름은 바이너리라 cat 으로 깨짐",
    11, SOFT, KR, "start")
d.legend(NY + 18, [("이름을 정하는 rsyslog 규칙", ACC), ("바이너리 · 전용 명령", INFO),
                   ("텍스트 · 그 밖의 쓰는 쪽", MUTED)])
d.save("08-01.var-log-tree.svg")
print("ok 08-01.var-log-tree")
