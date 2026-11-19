# 06-01 §1 「커널이 자원을 할당한 동적 실체」 — 디스크의 프로그램 파일 하나를 커널이 실행하면 PID·메모리·파일 서술자 테이블이 각자인 프로세스가 둘 생긴다.
# 본문 근거: 이 노트 「1. 프로그램과 프로세스의 구분」.
# 값 근거: 개념 도식이라 값은 없다. 프로세스 이름 A·B 는 구별용 표기다.
# 공식 근거: TLPI 6.1 — 프로그램은 런타임에 프로세스를 어떻게 구성할지 서술한 파일이고, 프로세스는 커널이 정의하며 시스템 자원이 할당되는 추상 개체다.
#           프로세스는 유저 공간 메모리와, 식별 번호·가상 메모리 테이블·열린 파일 서술자 테이블·시그널 정보·자원 한도·현재 작업 디렉터리를 담은 커널 자료구조로 이뤄진다.
# 타입 스펙: type-architecture — 왼쪽 디스크의 파일, 가운데 커널, 오른쪽 프로세스 둘. 연결은 직각 경로, focal 은 첫 프로세스 하나.
import sys
from pathlib import Path

sys.path.insert(0, ".")
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from dd import D, ACC, MUTED, INK, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 960, 500
d = D(W, H, "TLPI · 06-01 §1",
      "프로그램 파일 하나에서 독립된 프로세스 둘이 뜬다",
      "디스크의 프로그램 파일은 정적 명세이고, 커널이 실행하면 PID 와 자원을 따로 받은 프로세스가 생긴다.",
      "프로그램 파일 하나를 두 번 실행해 프로세스 A 와 B 가 생기는 구조")

# 왼쪽: 프로그램 파일
DX, DY, DW, DH = 24, 104, 272, 304
d.tone(DX, DY, DW, DH, MUTED, 6, "14", 1.0)
d.t(DX + DW / 2, DY + 28, "프로그램 파일", 14, INK, KR, "middle", 600)
d.t(DX + DW / 2, DY + 48, "디스크에 저장된 ELF 파일", 12, MUTED, KR)
d.line(DX + 12, DY + 60, DX + DW - 12, DY + 60, RULE, 0.8)
items = ["바이너리 형식 식별 정보", "기계어 인스트럭션", "진입점 주소", "초기화 데이터와 상수",
         "심볼·재배치 테이블", "공유 라이브러리 정보"]
for i, name in enumerate(items):
    iy = DY + 72 + i * 38
    d.box(DX + 12, iy, DW - 24, 30, PAPER, RULE, 0.8, 4)
    d.t(DX + 24, iy + 20, name, 13, INK, KR, "start", 500)

# 가운데: 커널
CX, BW, BH = 410, 116, 60
MY = DY + DH / 2
d.arrow([(DX + DW + 6, MY), (CX - BW / 2 - 4, MY)], MUTED, "ar", 1.4)
d.box(CX - BW / 2, MY - BH / 2, BW, BH, PAPER2, RULE, 1.0, 6)
d.t(CX, MY - 4, "커널", 14, INK, KR, "middle", 600)
d.t(CX, MY + 16, "PID·자원 부여", 12, MUTED, KR)

PX, PW, PH = 568, 368, 132
P1Y, P2Y = DY, DY + DH - PH
mid1, mid2 = P1Y + PH / 2, P2Y + PH / 2
d.path(f"M {CX + BW / 2 + 4} {MY - 12} H {PX - 36} Q {PX - 24} {MY - 12} {PX - 24} {MY - 24} V {mid1 + 12} "
       f"Q {PX - 24} {mid1} {PX - 12} {mid1} H {PX - 6}", ACC, 1.4, m="acc")
d.path(f"M {CX + BW / 2 + 4} {MY + 12} H {PX - 36} Q {PX - 24} {MY + 12} {PX - 24} {MY + 24} V {mid2 - 12} "
       f"Q {PX - 24} {mid2} {PX - 12} {mid2} H {PX - 6}", INFO, 1.4, m="info")
d.t(PX - 36, mid1 + 28, "처음 실행", 13, ACC, KR, "end")
d.t(PX - 36, mid2 - 20, "한 번 더 실행", 13, INFO, KR, "end")

rows = [("유저 메모리", "텍스트 · 데이터 · 힙 · 스택"),
        ("커널 자료구조", "가상 메모리 테이블 · 파일 서술자"),
        ("", "시그널 정보 · 작업 디렉터리")]
for py, name, c, pid in ((P1Y, "프로세스 A", ACC, "PID A"), (P2Y, "프로세스 B", INFO, "PID B")):
    d.tone(PX, py, PW, PH, c, 6, "18", 1.4)
    d.t(PX + 16, py + 28, name, 14, INK, KR, "start", 600)
    d.chip(PX + PW - 48, py + 24, pid, c, 12)
    d.line(PX + 12, py + 42, PX + PW - 12, py + 42, RULE, 0.8)
    for k, (lab, val) in enumerate(rows):
        ry = py + 66 + k * 26
        d.t(PX + 16, ry, lab, 12, MUTED, KR, "start")
        d.t(PX + 108, ry, val, 13, INK, KR, "start")

d.t(PX + PW / 2, (P1Y + PH + P2Y) / 2 + 5, "텍스트 영역은 공유 가능 · 나머지는 프로세스마다 독립", 13, MUTED, KR)

d.legend(H - 52, [("정적 명세 (디스크)", MUTED), ("프로세스 A", ACC), ("프로세스 B", INFO)])
d.save("06-01.program-vs-process.svg")
print("ok 06-01 program-vs-process")
