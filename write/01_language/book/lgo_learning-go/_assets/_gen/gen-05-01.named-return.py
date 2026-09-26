# 05-01.named-return — 이름 붙은 결과 변수에 무엇이 들어갔다가 호출자에게 가는가
# 본문 요구(05-01 §4 「이름 붙은 반환 값」): 결과 변수는 제로 값으로 시작하고, 본문에서 20·30 을 넣어도
#           return 에 적은 값이 컴파일러에 의해 결과 변수에 다시 대입되어 호출자는 2 1 을 받는다. 그 사이에 defer 가
#           결과 변수를 읽고 고칠 수 있다(05-03 에서 쓴다). 참여자 셋 사이의 시간순 주고받음이다.
# 타입 스펙: type-sequence — 레인 3개(호출한 쪽 · 함수 본문 · 결과 변수), 시간은 위→아래, 메시지는 수평 화살표,
#           상태는 결과 변수 레인 위의 칩. dd.py Seq 는 라벨을 11px mono 로 고정하므로(계약 §프리미티브) 같은 모양을
#           13px·한글 분기로 직접 그린다. stride: 메시지 행 간격 56. focal 은 return 이 결과 변수를 덮어쓰는 칩 하나.
# 사실 출처: Learning Go 2판 5장 「Named Return Values」(divAndRemainderConfusing)·「defer」, go1.25.1 실행(2026-09-27) — 2 1 <nil>.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, PAPER2, KR, MONO

W, H = 984, 560
LANE_W = 232
LX = {"main": 152, "body": 492, "res": 832}
Y0, STRIDE = 104, 56


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


d = D(W, H, "SEQUENCE · 05-01 §4",
      "이름 붙은 결과 변수는 return 이 덮어쓴다",
      "divAndRemainder(5, 2) 한 번의 호출을 시간순으로 그린 시퀀스. 이름 붙은 결과 변수는 제로 값으로 시작하고, 본문이 20·30 을 넣어도 "
      "return 문에 적은 값이 결과 변수에 다시 대입된다. 함수가 끝나기 직전 defer 가 결과 변수를 읽고 고칠 수 있으며, 호출자는 그 뒤의 값 2 1 을 받는다.",
      lead="위에서 아래로 시간이 흐릅니다. 오른쪽 칩이 그 순간 결과 변수에 든 값입니다.")

names = [("main", "호출한 쪽", "main"), ("body", "함수 본문", "divAndRemainder"), ("res", "결과 변수", "result · remainder · err")]
for key, title, sub in names:
    x = LX[key]
    d.box(x - LANE_W // 2, Y0, LANE_W, 48)
    d.t(x, Y0 + 20, title, 14, INK, KR, "middle", 600)
    d.t(x, Y0 + 38, sub, 12, MUTED, MONO, "middle")
    d.line(x, Y0 + 56, x, 488, RULE, 1.0, "3 6")


def msg(a, b, label, y, c=MUTED, mk="soft"):
    x1, x2 = LX[a], LX[b]
    dr = 1 if x2 > x1 else -1
    d.arrow([(x1 + 8 * dr, y), (x2 - 10 * dr, y)], c, mk, 1.5)
    d.t((x1 + x2) / 2, y - 10, label, 13, c if c != MUTED else INK, kr(label), "middle", 600)


def chip(y, txt, c, focal=False):
    x = LX["res"]
    w = 176
    d.o.append(f'<rect x="{x - w // 2}" y="{y - 14}" width="{w}" height="28" rx="4" fill="#0D1117"/>')
    d.tone(x - w // 2, y - 14, w, 28, c, 4, "22" if focal else "14", 1.4 if focal else 1.0)
    d.t(x, y + 5, txt, 13, c, kr(txt), "middle", 600)


y = Y0 + 96
msg("main", "body", "divAndRemainder(5, 2)", y)
chip(y, "0 · 0 · nil", INFO)
y += STRIDE
msg("body", "res", "result, remainder = 20, 30", y)
chip(y + STRIDE // 2 - 4, "20 · 30 · nil", WARN)
y += STRIDE
msg("body", "res", "return 5/2, 5%2, nil", y + 12, ACC, "acc")
chip(y + 12 + STRIDE // 2, "2 · 1 · nil", ACC, focal=True)
y += STRIDE + 44
d.o.append(f'<rect x="{LX["body"] - 150}" y="{y - 18}" width="300" height="28" fill="#0D1117"/>')
d.t(LX["body"], y, "defer 실행 · 결과 변수 읽기·수정 가능", 13, MUTED, KR, "middle")
y += 40
msg("res", "main", "2 1 <nil>", y, OK, "ok")

d.legend(504, [("제로 값", INFO), ("본문이 넣은 값", WARN), ("return 이 덮어쓴 값", ACC), ("호출자가 받은 값", OK)])
d.save("05-01.named-return.svg")
print("ok 05-01 named-return")
