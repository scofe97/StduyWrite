# 08-01 §4 「저널 저장 위치와 보존 한도」 — Storage= 값과 디렉터리 하나가 저널 파일의 자리를 정한다.
# 1차 자료: journald.conf(5) Storage= 의 volatile·persistent·auto·none(persistent 는 없으면 만들고 부팅 초기에는
#   /run 에 썼다가 옮긴다), SystemMaxUse= 기본 10%, SystemKeepFree= 기본 15%, 둘 다 4G 상한, /run 쪽 Runtime*= 짝.
# 실측(Debian 12 컨테이너, systemd 252): /var/log/journal 을 지우고 재시작하면
#   /run/log/journal/<machine-id>/system.journal 에만 생기고, mkdir -p · systemd-tmpfiles --create ·
#   재시작 · journalctl --flush 를 주면 /run 의 항목이 /var/log/journal 로 옮겨진다.
# 구조: 오른쪽은 저널 파일이 실제로 놓이는 두 자리 — 디스크의 /var/log/journal 과 재부팅에 사라지는
#   /run/log/journal — 이고, 그 사이를 journalctl --flush 가 잇는다. <machine-id> 는 기계마다 다른 값이라
#   본문처럼 자리표시로 둔다.
# 타입 스펙: type-flowchart — 설정값 하나에서 네 갈래로 나뉘고 auto 만 판정 한 번을 더 거친다.
#           직교 연결, 갈래 이름은 선 위 칩. accent 는 auto 의 판정 하나.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, WARN, BAD, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 588
d = D(W, H, "LEARNING MODERN LINUX · 08-01 §4",
      "Storage= 값과 디렉터리 하나가 저널의 자리를 정한다",
      "journald.conf 의 Storage= 네 값이 저널 파일을 디스크의 /var/log/journal 과 메모리의 /run/log/journal 중 "
      "어디에 쓰는지. Debian 12 기본값 auto 는 /var/log/journal 디렉터리가 있는지로 갈린다. "
      "journalctl --flush 는 /run 쪽 항목을 /var 쪽으로 옮긴다.",
      "Debian 12 기본값 auto 에서는 디렉터리 하나가 재부팅 뒤 기록을 정합니다")

AX, AY, AW, AH = 24, 248, 136, 56
d.box(AX, AY, AW, AH, PAPER2, RULE, 1.1, 6)
d.t(AX + AW / 2, AY + 24, "Storage=", 13, INK, MONO, "middle", 600)
d.t(AX + AW / 2, AY + 44, "journald.conf", 11, MUTED, MONO)

DX, DY, DW, DH = 256, 248, 196, 56
d.tone(DX, DY, DW, DH, ACC, 6, "14", 1.4)
d.t(DX + DW / 2, DY + 24, "/var/log/journal", 12, ACC, MONO, "middle", 600)
d.t(DX + DW / 2, DY + 44, "디렉터리가 있나", 12, MUTED, KR)

ZX0, ZX1 = 556, 896


def zone(y0, y1, col, head, sub, path, limits):
    d.box(ZX0, y0, ZX1 - ZX0, y1 - y0, PAPER2, col, 1.3, 8)
    d.t(ZX0 + 16, y0 + 22, head, 13, col, KR, "start", 600)
    d.t(ZX0 + 76, y0 + 22, sub, 12, MUTED, KR, "start")
    d.t(ZX0 + 16, y0 + 48, path, 12, INK, MONO, "start", 600)
    d.box(ZX0 + 32, y0 + 58, 148, 24, PAPER, col, 1.0, 4)
    d.t(ZX0 + 106, y0 + 75, "system.journal", 12, col, MONO, "middle", 600)
    d.t(ZX0 + 16, y1 - 12, limits, 11, SOFT, MONO, "start")


DZ0, DZ1 = 112, 236
MZ0, MZ1 = 320, 440
zone(DZ0, DZ1, OK, "디스크", "재부팅 뒤 남음 · -b -1 로 조회",
     "/var/log/journal/<machine-id>/", "SystemMaxUse 10% · KeepFree 15% · 각 최대 4G")
zone(MZ0, MZ1, WARN, "메모리", "/run · 재부팅에 사라짐",
     "/run/log/journal/<machine-id>/", "RuntimeMaxUse= 등 Runtime 짝")

NB0, NB1 = 452, 492
d.box(ZX0, NB0, ZX1 - ZX0, NB1 - NB0, PAPER2, BAD, 1.2, 6)
d.t(ZX0 + 16, NB0 + 25, "저장 안 함", 12, BAD, KR, "start", 600)
d.t(ZX0 + 96, NB0 + 25, "imjournal 같은 독자가 읽을 것이 없음", 12, MUTED, KR, "start")

# /run → /var 로 옮기는 flush
FX = 860
d.arrow([(FX, MZ0 - 2), (FX, DZ1 + 4)], OK, "ok", 1.5)
d.t(FX - 12, 270, "journalctl --flush", 12, OK, MONO, "end", 600)
d.t(FX - 12, 290, "/run 의 항목을 옮김", 12, MUTED, KR, "end")

# 갈래
BUS = 196
YP, YA, YV, YN = 152, AY + AH / 2, 412, 472
d.line(AX + AW, YA, BUS, YA, MUTED, 1.3)
d.line(BUS, YP, BUS, YN, MUTED, 1.3)
d.path(f"M {BUS} {YP} L {ZX0 - 4} {YP}", MUTED, 1.3, m="ar")
d.chip(300, YP, "persistent", MUTED, 11)
d.t(372, YP - 8, "없으면 만듦", 12, SOFT, KR, "start")
d.path(f"M {BUS} {YA} L {DX - 4} {YA}", MUTED, 1.3, m="ar")
d.chip(226, YA, "auto", MUTED, 11)
d.path(f"M {DX + DW} {YA} L 508 {YA} L 508 196 L {ZX0 - 4} 196", OK, 1.3, m="ok")
d.chip(508, 232, "있음", OK, 11)
d.path(f"M {DX + DW / 2} {DY + DH} L {DX + DW / 2} 376 L {ZX0 - 4} 376", WARN, 1.3, m="warn")
d.chip(DX + DW / 2, 336, "없음", WARN, 11)
d.path(f"M {BUS} {YV} L {ZX0 - 4} {YV}", MUTED, 1.3, m="ar")
d.chip(300, YV, "volatile", MUTED, 11)
d.path(f"M {BUS} {YN} L {ZX0 - 4} {YN}", MUTED, 1.3, m="ar")
d.chip(300, YN, "none", MUTED, 11)

NY = NB1 + 28
d.t(24, NY, "Debian 12 실측 · 디렉터리 삭제 뒤 재시작 → /run 에만 생김 · 다시 만들고 --flush → /var 로 옮겨짐",
    11, SOFT, KR, "start")
d.legend(NY + 16, [("디렉터리 하나가 가르는 판정", ACC), ("재부팅 뒤 남음", OK),
                   ("재부팅에 사라짐", WARN), ("저장 안 함", BAD)])
d.save("08-01.journal-storage.svg")
print("ok 08-01.journal-storage")
