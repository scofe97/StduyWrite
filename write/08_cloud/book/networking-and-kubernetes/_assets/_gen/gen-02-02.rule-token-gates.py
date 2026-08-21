# 02-02.rule-token-gates — 규칙 한 줄은 관문의 연속
# 본문: "조건은 통과 여부만 정하고 타깃 하나가 패킷을 바꾼다"
# 타입 스펙: type-flowchart.md — 관문 넷을 한 줄로 세우고 조건 불일치 가지를 아래로 뺀다.
#           패킷을 실제로 바꾸는 칸 하나에만 focal.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 620
d = D(W, H, "ONE iptables RULE · GATES THEN ONE TARGET",
      "규칙 한 줄은 관문의 연속 — 조건은 통과 여부만 정하고 타깃 하나가 패킷을 바꾼다",
      "앞의 셋은 통과 여부만 정한다. 헤더를 실제로 고치는 것은 마지막 -j 하나뿐이다.",
      lead="앞의 셋은 통과 여부만 정하고, 헤더를 고치는 것은 마지막 -j 하나뿐이다")

BW, BH, GAP = 184, 104, 56
CX = [48 + BW // 2 + i * (BW + GAP) for i in range(4)]           # 140 380 620 860
CY, SKIP_CY = 304, 468
STAGE = ["① 놓일 자리", "② 조건 평가", "③ 판정 무관", "④ 타깃 실행"]
NODES = [("체인 지정", "-A KUBE-SEP-2MJG…", "평가 시점", False),
         ("조건 관문", "-p tcp", "유일한 조건", False),
         ("무동작", "-m comment", "-m tcp", False),
         ("변환", "-j DNAT", "10.244.1.66:8080", True)]
EDGE = ["다음 토큰", "TCP 맞음", "조건 충족"]

ddx.band(d, 104, 572, "토큰을 왼쪽부터 읽으면 어디까지가 조건이고 어디부터가 동작인지 갈린다")
for cx, s in zip(CX, STAGE):
    d.t(cx, 216, s, 12, SOFT, KR, "middle", 600)
for cx, (t, s, tag, focal) in zip(CX, NODES):
    x, y = cx - BW // 2, CY - BH // 2
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{BW}" height="{BH}" rx="6" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>'); tc = ACC
    else:
        d.box(x, y, BW, BH, PAPER2, RULE, 1.1, 6); tc = INK
    d.t(cx, CY - 22, ddx.fit(t, 13, BW - 16, t), 13, tc, KR, "middle", 600)
    d.t(cx, CY + 2, ddx.fit(s, 12, BW - 14, s), 12, MUTED, MONO)
    d.t(cx, CY + 28, ddx.fit(tag, 10, BW - 12, tag), 10, ACC if focal else SOFT,
        MONO if all(ord(ch) < 128 or ch in '·-.:' for ch in tag) else KR)
for i, lab in enumerate(EDGE):
    a, b = CX[i] + BW // 2, CX[i + 1] - BW // 2
    d.path(f"M {a+6} {CY} L {b-10} {CY}", MUTED, 1.5, m="ar")
    d.t((a + b) // 2, CY - 16, ddx.fit(lab, 10, GAP - 6, f"corridor {lab}"), 10, MUTED, KR)

# 조건이 어긋나면 아무것도 안 바꾸고 다음 줄로 간다
d.box(CX[1] - 110, SKIP_CY - 44, 220, 88, PAPER2, RULE, 1.1, 6)
d.t(CX[1], SKIP_CY - 14, "다음 규칙으로", 13, MUTED, KR, "middle", 600)
d.t(CX[1], SKIP_CY + 8, "조건 불일치", 11, MUTED, KR)
d.t(CX[1], SKIP_CY + 28, "헤더 불변", 10, SOFT, KR)
d.path(f"M {CX[1]} {CY+BH//2+6} L {CX[1]} {SKIP_CY-44-10}", MUTED, 1.4, m="ar", dash="6 5")
d.t(CX[1] + 14, (CY + BH // 2 + SKIP_CY - 44) // 2 + 4, "조건: TCP 아님", 11, MUTED, KR, "start")

d.t(36, 540, "-m comment 나 -m tcp 는 판정에 아무 영향이 없다 — 읽는 사람만 헷갈리게 하는 토큰이다",
     12, MUTED, KR, "start")
d.legend(588, [("패킷을 바꾸는 칸", ACC)])
d.save("02-02.rule-token-gates.svg")
print("ok rule-token-gates")
