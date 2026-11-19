# 06-02 §1 프로세스 메모리 배치 — x86-32 가상 메모리 세그먼트와 경계 심볼
# 근거: TLPI 6.3 Figure 6-1 (PDF 8쪽 그림 대조), end(3) man page
# 값 근거: 그림 6-1 의 주소 0xC0000000·0x08048000·0x00000000 과 경계 심볼 &etext·&edata·&end, 표지 Top of stack·Program break.
# 타입 스펙: type-layers — 가상 주소 공간의 세그먼트를 위아래로 쌓고 경계 주소·심볼을 왼쪽 표지로 단다
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, PAPER, PAPER2, RULE, KR, MONO

W, H = 940, 544
BX, BW = 236, 690
d = D(W, H, "TLPI · 06-02 §1",
      "프로세스 가상 메모리 세그먼트 배치",
      "리눅스 x86-32 에서 프로세스가 보는 가상 주소 공간. 위쪽이 높은 주소이고 왼쪽 표지는 경계 주소와 심볼이다.",
      "책의 x86-32 기준 배치입니다. 주소는 커널 설정과 링크 옵션에 따라 달라집니다.")


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


# (이름, 높이, 설명, 칩, 색, 종류) — 위(높은 주소)에서 아래로
rows = [
    ("커널 (Kernel)", 48, "프로세스에 매핑되지만 프로그램은 접근 못 함", "/proc/kallsyms", SOFT, "soft"),
    ("argv, environ", 32, "명령행 인자와 환경 목록", None, PAPER2, "plain"),
    ("스택 (Stack)", 52, "아래 방향으로 자람 · 프레임이 쌓임", None, ACC, "focal"),
    ("미할당 영역", 44, "페이지 테이블 엔트리 없음", "SIGSEGV", PAPER, "gap"),
    ("힙 (Heap)", 52, "위 방향으로 자람 · 동적 할당", None, INFO, "tone"),
    ("미초기화 데이터 (BSS)", 36, "시작 전에 0 으로 채움", None, OK, "tone"),
    ("초기화된 데이터", 36, "실행 파일에서 초기값을 읽음", None, PAPER2, "plain"),
    ("텍스트 (프로그램 코드)", 40, "읽기 전용 · 프로세스끼리 공유", None, PAPER2, "plain"),
    ("미매핑", 32, "페이지 테이블 없음", None, PAPER, "gap"),
]
# 경계 표지: 행 번호(그 행의 위쪽 경계) → 라벨
marks = {1: "0xC0000000", 3: "스택 top", 4: "program break", 5: "&end", 6: "&edata", 7: "&etext", 8: "0x08048000"}

y = 104
bounds = []
for idx, (name, h, desc, chip, c, kind) in enumerate(rows):
    bounds.append(y)
    if kind == "focal":
        d.tone(BX, y, BW, h, c, 0, "1F", 1.5)
    elif kind == "tone":
        d.tone(BX, y, BW, h, c, 0, "1A", 1.0)
    elif kind == "gap":
        d.box(BX, y, BW, h, PAPER, RULE, 1.0, 0)
    elif kind == "soft":
        d.box(BX, y, BW, h, PAPER2, SOFT, 1.0, 0)
    else:
        d.box(BX, y, BW, h, PAPER2, RULE, 1.0, 0)
    ink = SOFT if kind == "gap" else INK
    d.t(BX + 16, y + h / 2 + 5, name, 13, ink, KR, "start", 600 if kind != "gap" else 500)
    d.t(BX + 262, y + h / 2 + 5, desc, 12, MUTED, KR, "start")
    if chip:
        d.chip(BX + BW - 18 - (len(chip) * 7.4 + 14) / 2, y + h / 2, chip, SOFT if kind != "gap" else MUTED, 12, 7)
    y += h
bounds.append(y)
for idx, label in marks.items():
    by = bounds[idx]
    d.line(BX - 12, by, BX, by, MUTED, 1.0)
    d.t(BX - 18, by + 4, label, 12, MUTED, kr(label), "end")
d.t(BX - 18, bounds[-1] + 4, "0x00000000", 12, MUTED, MONO, "end")
d.line(BX - 12, bounds[-1], BX, bounds[-1], MUTED, 1.0)

# 주소 증가 화살표
AX = 26
d.arrow([(AX, bounds[-1] - 8), (AX, 112)], MUTED, "ar", 1.4)
d.t(AX + 12, 290, "주소", 12, MUTED, KR, "start", 500)
d.t(AX + 12, 308, "증가", 12, MUTED, KR, "start", 500)

d.legend(H - 40, [("스택", ACC), ("힙", INFO), ("BSS", OK), ("커널 영역", SOFT)])
d.save("06-02.memory-segments.svg")
print("ok 06-02.memory-segments.svg")
