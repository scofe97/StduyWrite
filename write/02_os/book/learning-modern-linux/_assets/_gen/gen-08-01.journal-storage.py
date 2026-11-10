# 08-01 §9 — Storage= 값과 디렉터리 하나가 저널 파일의 자리를 정한다.
# 1차 자료: journald.conf(5) Storage= 의 volatile·persistent·auto·none, SystemMaxUse= 기본 10%,
#   SystemKeepFree= 기본 15%, 둘 다 4G 상한, /run 쪽 Runtime*= 짝.
# 실측(Debian 12 컨테이너, systemd 252): /var/log/journal 을 지우고 재시작하면
#   /run/log/journal/<machine-id>/system.journal 에만 쓰고, 디렉터리를 만들고 재시작 + flush 하면 돌아온다.
# 타입 스펙: type-flowchart — 설정값 하나에서 네 갈래로 나뉘고 auto 만 판정 한 번을 더 거친다.
#           직교 연결, 갈래 이름은 선 위 칩. accent 는 auto 의 판정 하나.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, WARN, BAD, PAPER2, RULE, KR, MONO

W, H = 880, 512
d = D(W, H, "LEARNING MODERN LINUX · 08-01 §4",
      "Storage= 값과 디렉터리 하나가 저널의 자리를 정한다",
      "journald.conf 의 Storage= 네 값이 저널 파일을 어디에 쓰는지. Debian 12 기본값 auto 는 /var/log/journal "
      "디렉터리가 있는지로 영속과 휘발을 가른다.",
      "Debian 12 기본값 auto 에서는 디렉터리 하나가 재부팅 뒤 기록을 정합니다")

AX, AY, AW, AH = 24, 196, 140, 56
d.box(AX, AY, AW, AH, PAPER2, RULE, 1.1, 6)
d.t(AX + AW / 2, AY + 24, "Storage=", 13, INK, MONO, "middle", 600)
d.t(AX + AW / 2, AY + 44, "journald.conf", 11, MUTED, MONO)

DX, DY, DW, DH = 260, 196, 196, 56
d.tone(DX, DY, DW, DH, ACC, 6, "14", 1.4)
d.t(DX + DW / 2, DY + 24, "/var/log/journal", 12, ACC, MONO, "middle", 600)
d.t(DX + DW / 2, DY + 44, "디렉터리가 있나", 11, MUTED, KR)

RX, RW = 560, 296
R1Y, R2Y, R3Y = 96, 288, 392
d.box(RX, R1Y, RW, 80, PAPER2, OK, 1.2, 6)
d.t(RX + 14, R1Y + 26, "/var/log/journal/<id>/system.journal", 11, INK, MONO, "start", 600)
d.t(RX + 14, R1Y + 46, "영속 · 재부팅 뒤 -b -1 로 조회", 11, OK, KR, "start")
d.t(RX + 14, R1Y + 66, "SystemMaxUse 10% · KeepFree 15% · 각 4G", 11, SOFT, MONO, "start")
d.box(RX, R2Y, RW, 80, PAPER2, WARN, 1.2, 6)
d.t(RX + 14, R2Y + 26, "/run/log/journal/<id>/system.journal", 11, INK, MONO, "start", 600)
d.t(RX + 14, R2Y + 46, "휘발 · 재부팅에 사라짐", 11, WARN, KR, "start")
d.t(RX + 14, R2Y + 66, "RuntimeMaxUse= 등 Runtime 짝", 11, SOFT, MONO, "start")
d.box(RX, R3Y, RW, 48, PAPER2, BAD, 1.2, 6)
d.t(RX + 14, R3Y + 20, "저장 안 함", 11, BAD, KR, "start", 600)
d.t(RX + 14, R3Y + 38, "imjournal 이 읽을 파일 없음", 11, MUTED, KR, "start")

BUS = 196
d.line(AX + AW, AY + AH / 2, BUS, AY + AH / 2, MUTED, 1.3)
d.line(BUS, 128, BUS, 416, MUTED, 1.3)
d.path(f"M {BUS} 128 L {RX - 4} 128", MUTED, 1.3, m="ar")
d.chip(300, 128, "persistent", MUTED, 11)
d.t(372, 120, "없으면 만듦", 11, SOFT, KR, "start")
d.path(f"M {BUS} {DY + DH / 2} L {DX - 4} {DY + DH / 2}", MUTED, 1.3, m="ar")
d.chip(228, DY + DH / 2, "auto", MUTED, 11)
d.path(f"M {DX + DW} {DY + DH / 2} L 508 {DY + DH / 2} L 508 152 L {RX - 4} 152", OK, 1.3, m="ok")
d.chip(508, 188, "있음", OK, 11)
d.path(f"M {DX + DW / 2} {DY + DH} L {DX + DW / 2} 308 L {RX - 4} 308", WARN, 1.3, m="warn")
d.chip(DX + DW / 2, 280, "없음", WARN, 11)
d.path(f"M {BUS} 344 L {RX - 4} 344", MUTED, 1.3, m="ar")
d.chip(300, 344, "volatile", MUTED, 11)
d.path(f"M {BUS} 416 L {RX - 4} 416", MUTED, 1.3, m="ar")
d.chip(300, 416, "none", MUTED, 11)

d.legend(468, [("디렉터리 하나가 가르는 판정", ACC), ("재부팅 뒤 남음", OK),
               ("재부팅에 사라짐", WARN), ("저장 안 함", BAD)])
d.save("08-01.journal-storage.svg")
print("ok 08-01.journal-storage")
