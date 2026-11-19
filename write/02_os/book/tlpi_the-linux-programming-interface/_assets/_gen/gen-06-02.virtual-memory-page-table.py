# 06-02 §2 가상 메모리와 페이지 테이블 — 같은 가상 페이지가 프로세스마다 다른 프레임으로, 코드 페이지는 같은 프레임으로 이어진다
# 근거: TLPI 6.4 Figure 6-2(PDF 9쪽 그림 대조), 가상 메모리의 이점 중 격리·공유, 스왑 영역과 SIGSEGV
# 값 근거: 프레임 번호와 페이지 용도는 설명용 예시다(그림 6-2 는 한 프로세스에 엔트리 4·2·7·0·3 을 보인다). 구조(엔트리가 RAM 또는 디스크를 가리키고, 엔트리가 없으면 SIGSEGV)는 6.4 본문이다.
# 타입 스펙: type-architecture — 두 프로세스의 페이지 테이블 엔트리가 물리 프레임 한 줄로 이어지는 구조
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, BAD, PAPER, PAPER2, RULE, KR, MONO

W, H = 980, 520
d = D(W, H, "TLPI · 06-02 §2",
      "페이지 테이블이 가상 페이지를 프레임에 잇는다",
      "프로세스 A·B 의 같은 가상 페이지가 서로 다른 프레임으로 이어지고, 같은 프로그램의 코드 페이지는 한 프레임을 함께 가리킵니다.",
      "프레임 번호와 페이지 용도는 설명용 예시입니다.")

ROW0, STRIDE, EH = 148, 52, 44
AX, AW = 36, 268        # A 엔트리
RAMX, RAMW = 388, 204
BXE, BWE = 688, 268     # B 엔트리


def ry(i):
    return ROW0 + i * STRIDE


def entry(x, w, i, text, c=None, bad=False):
    y = ry(i)
    if bad:
        d.tone(x, y, w, EH, BAD, 6, "14", 1.1)
    elif c:
        d.tone(x, y, w, EH, c, 6, "14", 1.1)
    else:
        d.box(x, y, w, EH, PAPER2, RULE, 1.0, 6)
    d.t(x + 14, y + EH / 2 + 5, text, 13, BAD if bad else (c or INK), MONO if text.isascii() else KR, "start", 500)


# 컨테이너
d.box(24, 108, 292, 268, PAPER, RULE, 1.0, 8)
d.t(36, 130, "프로세스 A 의 페이지 테이블", 14, INK, KR, "start", 600)
d.box(676, 108, 292, 268, PAPER, RULE, 1.0, 8)
d.t(688, 130, "프로세스 B 의 페이지 테이블", 14, INK, KR, "start", 600)
d.box(RAMX - 12, 108, RAMW + 24, 320, PAPER, RULE, 1.0, 8)
d.t(RAMX, 130, "물리 메모리 (페이지 프레임)", 14, INK, KR, "start", 600)

# RAM 프레임 5줄
frames = [("frame 2 · 공유 코드", ACC), ("frame 4 · A 데이터", OK), ("frame 7 · A 스택", OK),
          ("frame 5 · B 데이터", INFO), ("frame 9 · B 스택", INFO)]
for i, (t, c) in enumerate(frames):
    if c == ACC:
        d.tone(RAMX, ry(i), RAMW, EH, c, 6, "1F", 1.5)
    else:
        d.tone(RAMX, ry(i), RAMW, EH, c, 6, "14", 1.1)
    d.t(RAMX + RAMW / 2, ry(i) + EH / 2 + 5, t, 13, c, KR, "middle", 600)

# A 엔트리와 화살표 (모두 같은 줄로 곧게)
a_rows = [("page 0 (코드) → frame 2", ACC, 0), ("page 1 (데이터) → frame 4", OK, 1), ("page 2 (스택) → frame 7", OK, 2)]
for text, c, i in a_rows:
    entry(AX, AW, i, text, c)
    y = ry(i) + EH / 2
    d.arrow([(AX + AW + 2, y), (RAMX - 4, y)], c, {ACC: "acc", OK: "ok"}[c], 1.5)
entry(AX, AW, 3, "page 3 → 스왑 영역", WARN)
d.arrow([(AX + AW / 2, ry(3) + EH + 2), (AX + AW / 2, 404)], WARN, "warn", 1.5, dash="4 3")
d.box(24, 408, 292, 60, PAPER2, WARN, 1.0, 8)
d.t(36, 432, "디스크 스왑 영역", 14, WARN, KR, "start", 600)
d.t(36, 454, "RAM 에 없는 페이지의 사본", 12, MUTED, KR, "start")

# B 엔트리와 화살표 (3·4번째 프레임으로 내려가는 ㄷ 자 경로)
entry(BXE, BWE, 0, "page 0 (코드) → frame 2", ACC)
y0 = ry(0) + EH / 2
d.arrow([(BXE - 2, y0), (RAMX + RAMW + 4, y0)], ACC, "acc", 1.5)
b_rows = [(1, 3, 616, "page 1 (데이터) → frame 5"), (2, 4, 648, "page 2 (스택) → frame 9")]
for i, target, xc, text in b_rows:
    entry(BXE, BWE, i, text, INFO)
    ys, yt = ry(i) + EH / 2, ry(target) + EH / 2
    d.arrow([(BXE - 2, ys), (xc, ys), (xc, yt), (RAMX + RAMW + 4, yt)], INFO, "info", 1.5)
entry(BXE, BWE, 3, "page 3 · 엔트리 없음", bad=True)
d.chip(BXE + BWE - 56, ry(3) + EH / 2, "SIGSEGV", BAD, 12, 7)

d.legend(H - 40, [("공유 코드 프레임", ACC), ("A 전용", OK), ("B 전용", INFO), ("스왑에 있음", WARN), ("엔트리 없음", BAD)])
d.save("06-02.virtual-memory-page-table.svg")
print("ok 06-02.virtual-memory-page-table.svg")
