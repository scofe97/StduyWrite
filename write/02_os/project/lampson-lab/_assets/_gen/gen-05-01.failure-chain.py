# 05-01 §5 — 이 맥에서 FAIL 한 세 항목의 원인 사슬.
# 타입 스펙: type-process — 원인에서 판정까지 칸이 화살표로 이어지고, 두 줄이 같은 슬롯
#           (호스트가 다른 것 · 테스트가 한 일 · 찍힌 판정)으로 반복된다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, INFO, KR, MONO

W, H = 880, 420
d = D(W, H, "LAMPSON LAB · 05-01 §5",
      "FAIL 세 항목의 원인 사슬",
      "AC-21 과 재실행한 AC-22 는 호스트 셸의 가정에서 나왔고, EP-11 은 AC-21 이 랩을 내린 채 끝난 연쇄였다.",
      "AC-22 사슬은 재실행 기준이다 — 본 실행의 AC-22 판정 줄은 gitleaks pull 출력이 원인이었다")

CW, CH, GAP, X0 = 184, 120, 32, 24

def card(x, y, head, l1, l2, l3, kind):
    if kind == "cause":
        d.tone(x, y, CW, CH, INFO, 8, "14", 1.2)
        hc = INFO
    elif kind == "focal":
        d.o.append(f'<rect x="{x}" y="{y}" width="{CW}" height="{CH}" rx="8" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
        hc = ACC
    else:
        d.box(x, y, CW, CH, PAPER2, RULE, 1.0, 8)
        hc = INK
    d.t(x + 14, y + 28, head, 12, hc, MONO, "start", 600)
    for j, ln in enumerate((l1, l2, l3)):
        d.t(x + 14, y + 56 + j * 22, ln, 11, MUTED, KR, "start")

def link(i, y):
    x1 = X0 + i * (CW + GAP) + CW
    d.arrow([(x1 + 3, y + CH / 2), (x1 + GAP - 4, y + CH / 2)], MUTED, "ar", 1.4)

R1, R2 = 104, 252
row1 = [
    ("원인 1", "BSD wc -l 은 숫자 앞에", "공백을 붙여 출력한다", "'0 containers' 와 달라진다", "cause"),
    ("AC-21 FAIL", "문자열 비교가 어긋나서", "make up 을 건너뛴다", "다음 사이클도 같다", "mid"),
    ("랩이 내려간 채", "AC-21 이 끝난 뒤", "컨테이너가 없다", "", "mid"),
    ("EP-11 FAIL", "SESSION_MAX_SECONDS", "is '', not 3600", "단독 재실행은 PASS", "focal"),
]
for i, (h, a, b, c, k) in enumerate(row1):
    card(X0 + i * (CW + GAP), R1, h, a, b, c, k)
    if i < 3:
        link(i, R1)

row2 = [
    ("원인 2", "/proc/sys/kernel/random", "/uuid 는 리눅스에만", "있다"),
    ("uuid() 네 곳이 빈 값", "agent.conf · value.txt", "spire.log · request.log", "에 심을 값이 비었다"),
    ("AC-22 FAIL", "the scan missed", "planted secrets: 다섯 개", "넷은 uuid, hidden 은 미상"),
]
for i, (h, a, b, c) in enumerate(row2):
    card(X0 + i * (CW + GAP), R2, h, a, b, c, "cause" if i == 0 else "mid")
    if i < 2:
        link(i, R2)

d.t(24, 396, "두 사슬은 서로 독립이다 — 한쪽을 고쳐도 다른 쪽 판정은 그대로 남는다", 12, SOFT, KR, "start")
d.save("05-01.failure-chain.svg")
