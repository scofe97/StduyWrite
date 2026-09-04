# 02-02.rule-token-gates — 규칙 한 줄을 토큰으로 쪼개면 패킷을 바꾸는 것은 하나뿐
# 본문 요구: "커널은 규칙을 토큰 단위로 왼쪽에서 오른쪽으로 훑습니다. 위 그림은
#            `iptables -t nat -S KUBE-SEP-2MJG2J3URJK2NCRL` 이 뱉은 문자열을
#            그 순서 그대로 늘어놓은 것입니다." → 가로 좌→우 순서가 본문이 정한 규격이다.
# 타입 스펙: type-flowchart.md — 관문을 한 줄로 세우고 조건 불일치 가지를 아래로 뺀다.
#           패킷을 실제로 바꾸는 칸 하나에만 focal.
# 2026-08-28 재작성: 앞 판은 원본 규칙 문자열이 도식에 없어 "무엇을 쪼갠 것인지"가 안 보였다
#           (학습자 피드백 — "저게 뭘 설명하는지 모르겠다"). 실제 한 줄을 맨 위에 그대로 싣고
#           번호 칩으로 아래 칸과 잇는다. 연결선을 쓰지 않는 것은 네 갈래가 한 통로에서
#           겹치고 비스듬해지기 때문 — 번호가 그 일을 대신한다(primitive-annotation).
# 좌표: Layout conventions 타입이라 공식이 없다 — 칸 stride 240, 전부 4의 배수.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 748
d = D(W, H, "ONE iptables RULE · GATES THEN ONE TARGET",
      "규칙 한 줄은 관문의 연속 — 조건은 통과 여부만 정하고 타깃 하나가 패킷을 바꾼다",
      "맨 위가 실제 규칙 한 줄이다. 번호가 그 토막과 아래 칸을 잇는다. "
      "앞의 셋은 통과 여부만 정하고, 헤더를 고치는 것은 마지막 -j 하나뿐이다.",
      lead="맨 위 한 줄이 원본 · 번호가 토막과 아래 칸을 잇는다 · 헤더를 고치는 것은 마지막 -j 하나뿐")

BW, BH, GAP = 184, 104, 62   # 코리도어 11px 수용
CX = [48 + BW // 2 + i * (BW + GAP) for i in range(4)]           # 140 380 620 860
CY, SKIP_CY = 372, 528
STRIP_Y = 208                                                     # 원본 한 줄의 baseline
CHIP_Y = 176                                                      # 번호 칩
BAR_Y = 220                                                       # 토막 밑줄

ddx.band(d, 104, 668, "iptables -t nat -S KUBE-SEP-2MJG2J3URJK2NCRL 이 뱉은 한 줄을 그대로 옮겼다")

# ── 원본 한 줄 — 토막마다 (문자열, 번호, 색) ────────────────────────────────
# mono 13px 기준 라틴 폭 0.62em 예산으로 x 를 누적한다. 토막 사이 18px.
SEG = [("-A KUBE-SEP-2MJG…",                        "1", SOFT),
       ("-p tcp",                                    "2", INFO),
       ('-m comment --comment "…"',                  "3", SOFT),
       ("-m tcp",                                    "3", SOFT),
       ("-j DNAT --to-destination 10.244.1.66:8080", "4", ACC)]

CW, SEG_GAP, X0 = 13 * 0.62, 18, 56
x = X0
for txt, num, c in SEG:
    w = len(txt) * CW
    d.o.append(f'<rect x="{x-6:.0f}" y="{BAR_Y-2}" width="{w+12:.0f}" height="3" rx="1.5" fill="{c}"/>')
    d.t(x, STRIP_Y, txt, 13, INK if c is ACC else MUTED, MONO, "start")
    d.chip(x + w / 2, CHIP_Y, num, c)
    x += w + SEG_GAP
assert x < W - 24, f"원본 한 줄이 캔버스를 넘는다: {x:.0f}px"

d.t(56, 152, "실제 규칙 한 줄", 11, SOFT, KR, "start", 600)

# ── 토막이 하는 일 ──────────────────────────────────────────────────────────
STAGE = ["어디에 넣을 규칙인가", "이 패킷이 조건에 맞나", "커널이 안 보는 토큰", "패킷을 바꾸는 자리"]
NODES = [("-A KUBE-SEP-2MJG…", "이 규칙이 놓일 체인", "조건도 동작도 아니다", False),
         ("-p tcp", "통과 여부만 정한다", "이 줄의 유일한 조건", False),
         ("-m comment · -m tcp", "판정에 영향이 없다", "사람용 메모와 빈 토큰", False),
         ("-j DNAT", "목적지를 바꾼다", "dst → 10.244.1.66:8080", True)]
EDGE = ["다음 토큰", "TCP 맞음", "조건 충족"]

for cx, s in zip(CX, STAGE):
    d.t(cx, 288, s, 12, SOFT, KR, "middle", 600)
for cx, (t, s, tag, focal), (_, num, c) in zip(CX, NODES, [SEG[0], SEG[1], SEG[2], SEG[4]]):
    x0, y0 = cx - BW // 2, CY - BH // 2
    if focal:
        d.o.append(f'<rect x="{x0}" y="{y0}" width="{BW}" height="{BH}" rx="6" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>'); tc = ACC
    else:
        d.box(x0, y0, BW, BH, PAPER2, RULE, 1.1, 6); tc = INK
    d.chip(x0 + 16, y0 - 12, num, c)                              # 위 토막과 같은 번호 — 테두리 위에 얹지 않고 바깥에 세운다
    d.t(cx, CY - 20, ddx.fit(t, 12, BW - 16, t), 12, tc, MONO, "middle", 600)
    d.t(cx, CY + 4, ddx.fit(s, 12, BW - 14, s), 12, MUTED, KR)
    d.t(cx, CY + 28, ddx.fit(tag, 11, BW - 12, tag), 11, ACC if focal else SOFT,
        MONO if all(ord(ch) < 128 or ch in '·-.:→' for ch in tag) else KR)
for i, lab in enumerate(EDGE):
    a, b = CX[i] + BW // 2, CX[i + 1] - BW // 2
    d.path(f"M {a+6} {CY} L {b-10} {CY}", MUTED, 1.5, m="ar")
    d.t((a + b) // 2, CY - 16, ddx.fit(lab, 11, GAP - 6, f"corridor {lab}"), 11, MUTED, KR)

# ── 조건이 어긋나면 뒤 토큰은 아예 평가되지 않는다 ─────────────────────────
d.box(CX[1] - 116, SKIP_CY - 44, 232, 88, PAPER2, RULE, 1.1, 6)
d.t(CX[1], SKIP_CY - 14, "규칙 전체를 건너뛴다", 13, MUTED, KR, "middle", 600)
d.t(CX[1], SKIP_CY + 8, "뒤 토큰은 평가되지 않는다", 11, MUTED, KR)
d.t(CX[1], SKIP_CY + 28, "헤더 불변 · 다음 줄로", 11, SOFT, KR)
d.path(f"M {CX[1]} {CY+BH//2+6} L {CX[1]} {SKIP_CY-44-10}", MUTED, 1.4, m="ar", dash="6 5")
d.t(CX[1] + 14, (CY + BH // 2 + SKIP_CY - 44) // 2 + 4, "TCP 아님", 11, MUTED, KR, "start")

# ── 걸렸을 때 실제로 무엇이 달라지는가 ────────────────────────────────────
BX, BY, BBW = 552, SKIP_CY, 176
for i, (lab, val, c) in enumerate((("규칙에 걸리기 전", "dst 10.96.192.224:8080", MUTED),
                                   ("걸린 뒤", "dst 10.244.1.66:8080", ACC))):
    x0 = BX + i * (BBW + 72)
    d.box(x0, BY - 44, BBW, 88, PAPER2, c if c is ACC else RULE, 1.1, 6)
    d.t(x0 + BBW // 2, BY - 12, lab, 12, c, KR, "middle", 600)
    d.t(x0 + BBW // 2, BY + 14, val, 11, c, MONO)
d.path(f"M {BX+BBW+8} {BY} L {BX+BBW+64} {BY}", ACC, 1.6, m="acc")
d.t(BX + BBW + 36, BY - 12, "-j DNAT", 11, ACC, MONO)

d.t(36, 620, "조건이 몇 개든 패킷을 바꾸는 것은 마지막 -j 하나뿐이다 — 규칙을 읽을 때 눈이 먼저 갈 자리가 거기다",
     12, MUTED, KR, "start")
d.t(36, 644, "-m comment 와 -m tcp 는 판정에 아무 영향이 없다. 읽는 사람만 헷갈리게 하는 토큰이다",
     12, MUTED, KR, "start")
d.legend(684, [("패킷을 바꾸는 자리", ACC), ("유일한 조건", INFO), ("판정 무관", SOFT)])
d.save("02-02.rule-token-gates.svg")
print("ok rule-token-gates")
