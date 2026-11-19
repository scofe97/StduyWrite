# 06-02 §2 요구 페이징 — 가상 주소를 읽을 때 페이지 테이블 엔트리와 RAM 상주 여부에 따라 세 갈래로 갈린다
# 근거: TLPI 6.4 — 엔트리가 RAM 위치 또는 디스크를 가리킴, 엔트리가 없으면 SIGSEGV, 비상주 페이지 접근 시 페이지 폴트와 적재
# 값 근거: 개념도라 값은 없다. 낱말은 6.4 본문(page fault, swap area, SIGSEGV, page-table entry).
# 타입 스펙: type-flowchart — 조회 두 번의 예·아니오 분기와 합류하는 적재 경로
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, BAD, PAPER, PAPER2, RULE, KR, MONO

W, H = 968, 392
d = D(W, H, "TLPI · 06-02 §2",
      "가상 주소 접근은 세 갈래로 갈린다",
      "페이지 테이블 엔트리가 있고 페이지가 RAM 에 있으면 그대로 실행되고, 없으면 SIGSEGV, 디스크에 있으면 페이지 폴트로 적재한 뒤 재개합니다.",
      "엔트리 조회와 RAM 상주 확인이 분기점입니다.")

NW, NH = 160, 64
COLS = [28, 216, 404, 592, 780]
Y1, Y2 = 116, 244


def node(col, y, title, sub, c):
    d.tone(COLS[col], y, NW, NH, c, 6, "14", 1.2)
    d.t(COLS[col] + NW / 2, y + 27, title, 14, c, KR, "middle", 600)
    d.t(COLS[col] + NW / 2, y + 48, sub, 12, MUTED, KR, "middle")


def right(col, y, c, m, label=None, dash=None):
    x1, x2 = COLS[col] + NW, COLS[col + 1]
    d.arrow([(x1 + 2, y + NH / 2), (x2 - 4, y + NH / 2)], c, m, 1.4, dash=dash)
    if label:
        d.t((x1 + x2) / 2, y + NH / 2 - 8, label, 12, MUTED, KR, "middle", 600)


node(0, Y1, "가상 주소 접근", "프로세스가 읽기·쓰기", INFO)
node(1, Y1, "엔트리 있음?", "페이지 테이블 조회", INFO)
node(2, Y1, "RAM 에 상주?", "엔트리가 가리키는 곳", INFO)
node(3, Y1, "프레임 접근", "정상 실행", OK)
right(0, Y1, SOFT, "soft")
right(1, Y1, OK, "ok", "예")
right(2, Y1, OK, "ok", "예")

node(1, Y2, "SIGSEGV", "엔트리 없음", BAD)
node(2, Y2, "페이지 폴트", "프로세스 실행 중단", WARN)
node(3, Y2, "페이지 적재", "디스크 → 프레임", INFO)
node(4, Y2, "실행 재개", "적재가 끝나면", OK)
right(2, Y2, WARN, "warn")
right(3, Y2, WARN, "warn")

# 아니오 분기 (아래로)
for col, c, m in ((1, BAD, "bad"), (2, WARN, "warn")):
    x = COLS[col] + NW / 2
    d.arrow([(x, Y1 + NH + 2), (x, Y2 - 4)], c, m, 1.4)
    d.t(x + 10, (Y1 + NH + Y2) / 2 + 4, "아니오", 12, MUTED, KR, "start", 600)

# 재개 뒤 프레임 접근으로 되돌아가는 경로
d.arrow([(COLS[4] + NW / 2, Y2 - 2), (COLS[4] + NW / 2, Y1 + NH / 2), (COLS[3] + NW + 4, Y1 + NH / 2)], OK, "ok", 1.4, dash="4 3")
d.t(COLS[4] + NW / 2 + 10, (Y1 + Y2) / 2 + 22, "적재 뒤", 12, MUTED, KR, "start", 600)

d.legend(H - 40, [("정상 경로", OK), ("페이지 폴트 경로", WARN), ("엔트리 없음", BAD), ("조회", INFO)])
d.save("06-02.page-fault-flow.svg")
print("ok 06-02.page-fault-flow.svg")
