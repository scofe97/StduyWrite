# 02-03 §6 「만들어진 규칙은 방향을 한쪽으로 가정합니다」 — 같은 SYN 에서 뽑은 두 줄이 어디서 갈리는가.
# 본문: "주석이 목적지라고 적은 두 줄에도 --source 와 --source-port 가 붙었습니다" · "이 공격 SYN 을 막는 줄은
# 첫 줄 --source 203.0.113.50/32 입니다. Destination port. 줄은 … 공격 SYN 의 출발지 포트는 51500 이라 지나갑니다."
# 규칙 조각은 Wireshark release-4.6 ui/firewall_rules.c 의 Netfilter 형식 문자열에 이 패킷 값을 넣은 것이다.
# 타입 스펙: type-flowchart — semantic-patterns 의 Paired policy-evaluation traces. 같은 순서의 단계
#           (값 꺼내기 → 옵션 붙이기 → 규칙 조각 → 공격 SYN 대조)를 두 트레이스로 적고 처음 갈리는 칸을 표시한다.
#           흐름은 스펙의 top→down 대신 좌→우로 편다(01-01 promiscuous-gates 와 같은 축약).
#           focal 은 목적지 값에 출발지 옵션이 붙는 칸 하나.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, BAD, INFO, PAPER2, RULE, KR, MONO

W, H = 880, 412
d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 02-03 §6",
      "같은 체크가 목적지 값에도 --source 를 붙입니다",
      "203.0.113.50 이 198.51.100.20 의 22번 포트로 보낸 SYN 에서 Firewall ACL Rules 가 만든 두 줄을 따라간다. Inbound 가 켜져 있으면 출발지 값이든 목적지 값이든 --source 계열 옵션이 붙어, 목적지 포트 줄은 공격 SYN 에 걸리지 않는다.",
      "위 줄은 공격 SYN 을 막고, 아래 줄은 목적지 값에 출발지 옵션이 붙어 지나보냅니다")

LABEL_X = 40
COLS = [(232, 112), (376, 152), (560, 208), (792, 64)]     # (x, w) — 칸 사이 corridor 32 · 24
RH = 56
HEAD = [("대화상자의 줄", "주석 이름"), ("꺼낸 값", "값의 출처"), ("붙은 옵션", "Inbound 켬"),
        ("규칙 조각", "iptables"), ("공격 SYN", "막히나")]
d.t(LABEL_X, 124, HEAD[0][0], 13, INK, KR, "start", 600)
d.t(LABEL_X, 142, HEAD[0][1], 12, MUTED, KR, "start")
for (x, w), (title, sub) in zip(COLS, HEAD[1:]):
    d.t(x + w / 2, 124, title, 13, INK, KR, "middle", 600)
    d.t(x + w / 2, 142, sub, 12, MUTED, MONO if sub == "iptables" else KR, "middle")
d.line(24, 160, 856, 160, RULE, 0.8)

# 처음 갈리는 칸 위에 괄호 막대와 이름
SPLIT_Y = 184
x, w = COLS[1]
d.line(x, SPLIT_Y + 6, x + w, SPLIT_Y + 6, INK, 1.2)
d.line(x, SPLIT_Y + 6, x, SPLIT_Y + 10, INK, 1.2); d.line(x + w, SPLIT_Y + 6, x + w, SPLIT_Y + 10, INK, 1.2)
d.t(x + w / 2, SPLIT_Y - 4, "여기서 처음 갈림", 12, INK, KR, "middle", 600)

ROWS = [  # (행 y, 줄 이름, 값 출처, [(상태, 값 글자, 글꼴)...])
    (200, "IPv4 source address.", "출발지 주소",
     [("info", "203.0.113.50", MONO), ("ok", "--source", MONO), ("ok", "--source 203.0.113.50/32", MONO), ("ok", "막힘", KR)]),
    (284, "Destination port.", "목적지 포트",
     [("info", "22", MONO), ("focal", "--source-port", MONO), ("bad", "--source-port 22", MONO), ("bad", "지나감", KR)]),
]
TONE = {"ok": OK, "bad": BAD, "focal": ACC, "info": INFO}

for ry, name, origin, cells in ROWS:
    cy = ry + RH / 2
    d.t(LABEL_X, cy - 3, name, 12, INK, MONO, "start", 600)
    d.t(LABEL_X, cy + 16, origin, 12, MUTED, KR, "start")
    d.arrow([(206, cy), (COLS[0][0] - 4, cy)], MUTED, "ar", 1.2)
    for j in range(3):
        x1 = COLS[j][0] + COLS[j][1]
        d.arrow([(x1, cy), (COLS[j + 1][0] - 4, cy)], MUTED, "ar", 1.4)
    for (x, w), (kind, text, fam) in zip(COLS, cells):
        c = TONE[kind]
        if kind == "focal":
            d.o.append(f'<rect x="{x}" y="{ry}" width="{w}" height="{RH}" rx="6" '
                       f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
        else:
            d.tone(x, ry, w, RH, c, 6)
        d.t(x + w / 2, cy + 5, text, 12 if fam == MONO else 13, c, fam, "middle", 600)

d.legend(364, [("목적지 값에 붙은 출발지 옵션", ACC), ("공격 SYN 을 막는 줄", OK), ("지나보내는 줄", BAD), ("패킷에서 꺼낸 값", INFO)])
d.save("02-03.acl-inbound.svg")
