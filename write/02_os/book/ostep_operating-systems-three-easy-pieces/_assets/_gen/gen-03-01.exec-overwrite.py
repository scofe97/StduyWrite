# 03-01 「호출 한 번으로 프로그램이 바뀌기」 — execvp 호출 전후에 같은 프로세스의 코드와 정적 데이터는 wc 로 덮어써지고 힙과 스택은 다시 초기화된다.
# 본문 근거: 이 노트 「3. exec 으로 프로그램 덮어쓰기」.
# 값 근거: 5장 p3.c 실행 예의 자식 PID 29384. 직접 실행해 얻은 값이 아니다.
# 공식 근거: OSTEP 5장 §5.3 — exec 은 실행 파일을 읽어 현재 코드 구획과 정적 데이터를 덮어쓰고 힙·스택 등은 다시 초기화한다. 새 프로세스를 만들지 않는다. execve(2) — 기본적으로 파일 디스크립터는 열린 채 남는다.
# 타입 스펙: type-architecture-delta — Before · Changes · After 세 칸. 구획 이름은 두 상태에서 같고 내용만 바뀐다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, PAPER2, KR, MONO

W, H = 920, 580
d = D(W, H, "OSTEP · 03-01 §3",
      "exec 은 프로세스를 새로 만들지 않고 안의 프로그램만 바꾼다",
      "exec 호출 전의 자식은 p3 의 코드와 정적 데이터, 힙, 스택을 가진 PID 29384 프로세스다. 호출 뒤에도 PID 는 29384 이고 열린 파일도 그대로다. "
      "코드와 정적 데이터는 wc 의 것으로 덮어써지고 힙과 스택은 다시 초기화된다.",
      lead="Before 와 After 는 같은 프로세스입니다. 바뀐 칸에만 Δ 가 붙습니다.")

PW, SH, GAP = 300, 56, 12
BX, AX = 24, W - 24 - PW
LX0, LW = BX + PW + 12, AX - (BX + PW) - 24
Y0 = 112


def panel(x, title, rows):
    d.t(x + PW / 2, Y0 + 8, title, 13, INK, MONO, "middle", 600)
    d.box(x, Y0 + 24, PW, 40, PAPER2, RULE, 1.0)
    d.t(x + PW / 2, Y0 + 49, "프로세스 PID 29384", 13, INK, KR, "middle", 600)
    y = Y0 + 64 + GAP
    for name, sub, changed in rows:
        if changed:
            d.tone(x, y, PW, SH, ACC, 6, "14", 1.3)
            d.t(x + 18, y + 24, "Δ", 13, ACC, MONO, "middle", 600)
        else:
            d.box(x, y, PW, SH, PAPER2, RULE, 1.0)
        d.t(x + PW / 2, y + 23, name, 13, ACC if changed else INK, KR, "middle", 600)
        d.t(x + PW / 2, y + 43, sub, 12, MUTED, KR)
        y += SH + GAP


panel(BX, "exec 전 — p3", [
    ("코드", "p3 의 코드", False),
    ("정적 데이터", "p3 의 데이터", False),
    ("힙", "p3 가 쓰던 값", False),
    ("스택", "p3 가 쓰던 값", False),
    ("열린 파일", "표준 입력 · 출력 · 오류", False),
])
panel(AX, "exec 뒤 — wc", [
    ("코드", "wc 의 코드", True),
    ("정적 데이터", "wc 의 데이터", True),
    ("힙", "다시 초기화", True),
    ("스택", "다시 초기화", True),
    ("열린 파일", "표준 입력 · 출력 · 오류", False),
])

# 가운데 변경 목록
d.t(LX0 + LW / 2, Y0 + 8, "바뀐 것", 12, MUTED, KR, "middle", 600)
ents = [("CHANGED", "코드", "p3 → wc"), ("CHANGED", "정적 데이터", "p3 → wc"), ("CHANGED", "힙 · 스택", "다시 초기화")]
y = Y0 + 64 + GAP
for k, (tag, obj, diff) in enumerate(ents):
    d.box(LX0, y, LW, 2 * SH + GAP if False else SH, PAPER2, RULE, 1.0)
    d.t(LX0 + 10, y + 20, tag, 10, ACC, MONO, "start", 600)
    d.t(LX0 + 10, y + 38, obj + " " + diff, 11, INK, KR, "start")
    y += SH + GAP
d.chip(LX0 + LW / 2, Y0 + 64 + GAP + 3 * (SH + GAP) + 24, "PID · 열린 파일 그대로", OK, 11, 6)

d.legend(H - 40, [("덮어써짐 · 초기화(Δ)", ACC), ("그대로", OK)])
d.save("03-01.exec-overwrite.svg")
print("ok 03-01 exec-overwrite")
