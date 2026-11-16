# 05-01 §8 — 유니온 마운트 실습 구조. 컨테이너 A·B 가 image 한 벌을 lowerdir 로 같이 쓰고
#           upperdir 만 따로 갖는 실제 폴더 트리와 du 값을 보인다. 기존 3연산 도식(05-01.union-mount)
#           앞에 두어 "공유 이미지"를 먼저 보이게 한다.
# 타입 스펙: type-layers — 위에서 아래로 merged(view) · upperdir(upper) · lowerdir(image) 세 층.
#           가로로 컨테이너 A·B 두 열, image 층은 두 열을 가로지르는 상자 하나. accent 는 image 한 벌.
# 근거: 학습 실습(OrbStack lml-ubuntu, 2026-11-16) 의 mount 두 줄, `tree -h` 출력, `du -sh` 결과
#       (image 201M · a-upper 0 · b-upper 0). 원 요청서 relay-w3-union-mount-20261116-2138.md.
#       트리의 행 순서만 usr/ 를 etc/ 위로 올렸다 — 비쳐 보임 화살표와 위층 화살표가 엇갈리지 않게.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, PAPER2, RULE, KR, MONO

W, H = 880, 656
d = D(W, H, "LEARNING MODERN LINUX · 05-01 §8",
      "이미지 한 벌, 컨테이너 둘",
      "컨테이너 A 와 B 가 같은 image 폴더를 lowerdir 로 겹쳐 마운트한 실제 구조다. 맨 아래 image "
      "(etc/motd, usr/big.bin 200M) 는 두 열을 가로지르는 상자 하나이고 du 로 201M 이다. 그 위에 "
      "컨테이너마다 upperdir 가 따로 있다. a-upper 에는 A 에서 새로 만든 etc/hello 만 있고, b-upper 는 "
      "비어 있으며 둘 다 du 0 이다. 맨 위 a-view 와 b-view 는 각 컨테이너가 보는 / 다. 두 view 의 "
      "big.bin 200M 과 motd 는 image 에서 비쳐 보이는 것이지 복사본이 아니고, A 의 hello 만 a-upper 에서 온다.",
      "디스크에는 image 한 벌만 있고, 컨테이너마다 위층(upperdir)만 따로 얹는다")

LX = 24                         # 층 이름 열
AX, BX, COLW = 176, 528, 328    # 컨테이너 A·B 열
UPW = 232                       # upper 상자 폭
IND, ROW = 24, 20               # 트리 들여쓰기 · 행 간격
CW = 7.8                        # mono 13px 글자 폭(0.6em)
VY, VH = 128, 140               # view 층: 루트 + 5행
UY, UH = VY + VH + 48, 80       # upper 층: 루트 + 2행
IY, IH = UY + UH + 48, 120      # image 층: 루트 + 4행
HC_A = AX + 268                 # A 위층 화살표가 오르는 세로선
BC_A, BC_B = AX + 300, BX + 300 # image 에서 비쳐 보임 화살표의 세로선


def tx(col_x):
    return col_x + 20


def base(top, i):               # i 번째 행의 글자 기준선
    return top + 24 + i * ROW


def end_x(col_x, level, name):  # 행 글자의 오른쪽 끝
    return tx(col_x) + level * IND + len(name) * CW


def mid(top, i):                # 행 글자의 세로 가운데(화살표 높이)
    return base(top, i) - 4


def guides(col_x, top, rows):
    """트리 선 — 부모의 세로선과 자식으로 가는 가로 눈금."""
    for i, (lv, _, _) in enumerate(rows):
        if lv == 0:
            continue
        p = max(j for j in range(i) if rows[j][0] == lv - 1)
        gx = tx(col_x) + (lv - 1) * IND + 4
        d.line(gx, base(top, p) + 5, gx, mid(top, i), SOFT, 0.9)
        d.line(gx, mid(top, i), tx(col_x) + lv * IND - 6, mid(top, i), SOFT, 0.9)


def labels(col_x, top, rows):
    for i, (lv, name, c) in enumerate(rows):
        w = 600 if lv == 0 else 400
        d.t(tx(col_x) + lv * IND, base(top, i), name, 13, c, MONO, "start", w)


VIEW_A = [(0, "a-view/", INK), (1, "usr/", MUTED), (2, "big.bin [200M]", INFO),
          (1, "etc/", MUTED), (2, "hello", OK), (2, "motd", INFO)]
VIEW_B = [(0, "b-view/", INK), (1, "usr/", MUTED), (2, "big.bin [200M]", INFO),
          (1, "etc/", MUTED), (2, "motd", INFO)]
UP_A = [(0, "a-upper/", INK), (1, "etc/", MUTED), (2, "hello", OK)]
UP_B = [(0, "b-upper/", INK)]
IMG = [(0, "image/", INK), (1, "usr/", MUTED), (2, "big.bin [200M]", INK),
       (1, "etc/", MUTED), (2, "motd", INK)]

# 층 이름 — 본문 용어(merged·upperdir·lowerdir)와 실습 이름을 잇는다
for y, name, term, note in ((VY, "보이는 /", "merged", "컨테이너가 보는 /"),
                            (UY, "위층", "upperdir", "컨테이너마다 따로"),
                            (IY, "이미지", "lowerdir", "공유 · 읽기만")):
    d.t(LX, y + 26, name, 14, INK, KR, "start", 600)
    d.t(LX, y + 44, term, 12, MUTED, MONO, "start")
    d.t(LX, y + 62, note, 12, SOFT, KR, "start")

# 열 머리
for x, name in ((AX, "컨테이너 A"), (BX, "컨테이너 B")):
    d.t(x, VY - 16, name, 14, INK, KR, "start", 600)

# 상자 — 화살표보다 먼저(채움이 화살표를 덮지 않게)
for x in (AX, BX):
    d.box(x, VY, COLW, VH, PAPER2, RULE, 1.0, 6)
    d.box(x, UY, UPW, UH, PAPER2, RULE, 1.0, 6)
d.tone(AX, IY, BX + COLW - AX, IH, ACC, 6, "1F", 1.4)

# 트리 선
for col_x, top, rows in ((AX, VY, VIEW_A), (BX, VY, VIEW_B), (AX, UY, UP_A), (AX, IY, IMG)):
    guides(col_x, top, rows)

# 화살표 — A 의 hello 는 a-upper 에서 (실선)
d.arrow([(end_x(AX, 2, "hello") + 6, mid(UY, 2)), (HC_A, mid(UY, 2)),
         (HC_A, mid(VY, 4)), (end_x(AX, 2, "hello") + 8, mid(VY, 4))], OK, "ok", 1.4)
# big.bin 은 image 한 벌이 두 view 에 비쳐 보인다 (점선)
big = "big.bin [200M]"
d.arrow([(end_x(AX, 2, big) + 6, mid(IY, 2)), (BC_A, mid(IY, 2)),
         (BC_A, mid(VY, 2)), (end_x(AX, 2, big) + 8, mid(VY, 2))], INFO, "info", 1.4, "4 3")
d.arrow([(BC_A, mid(IY, 2)), (BC_B, mid(IY, 2)),
         (BC_B, mid(VY, 2)), (end_x(BX, 2, big) + 8, mid(VY, 2))], INFO, "info", 1.4, "4 3")
d.t(end_x(AX, 2, big) + 8, mid(IY, 2) + 30, "비쳐 보임 · 복사본 아님", 12, INFO, KR, "start")

# 트리 글자
for col_x, top, rows in ((AX, VY, VIEW_A), (BX, VY, VIEW_B), (AX, UY, UP_A), (BX, UY, UP_B), (AX, IY, IMG)):
    labels(col_x, top, rows)
d.t(tx(BX) + IND, base(UY, 1), "(비어 있음)", 12, SOFT, KR, "start")

# du 실측값
for x in (AX, BX):
    d.t(x + UPW - 14, base(UY, 0), "du 0", 13, MUTED, MONO, "end")
d.t(BC_B - 20, base(IY, 0), "du 201M", 13, ACC, MONO, "end", 600)

FOOT = IY + IH + 28
d.t(AX, FOOT, "workdir  a-work · b-work — OverlayFS 내부 작업용 빈 폴더", 12, SOFT, KR, "start")
LEG = FOOT + 20
d.legend(LEG, [("upper 에서 온 파일", OK), ("image 에서 비쳐 보임", INFO), ("디스크의 image 한 벌", ACC)])
assert LEG + 40 <= H, (LEG, H)
d.save("05-01.union-mount-shared.svg")
print("ok 05-01.union-mount-shared")
