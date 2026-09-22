# 05-02 §1 — DNS 세 구성 요소 중 이 편이 보는 자리는 리졸버 하나다.
# 본문 요구: "주요 구성 요소를 셋으로 나눕니다 — 이름 공간, 그 이름 공간을 제공하는 서버,
#            이름 공간에 대해 서버에 질의하는 리졸버(클라이언트). 그리고 범위를 못박습니다.
#            '이 주제는 리졸버 관점에 집중합니다.'"
#            불릿 셋은 나열일 뿐 어느 것이 이 편의 자리인지, 셋이 어떤 관계인지를 못 세운다.
# 타입 스펙: type-layers — 넓은 이름 공간 위에 서버가, 그 위에 질의하는 리졸버가 얹힌 관계.
#           focal 은 리졸버 하나 — 원문이 범위를 그리로 못박았고 캡처에 잡히는 자리도 거기다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, INFO, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 940, 560
d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 05-02 §1",
      "DNS 세 부분과 이 편이 보는 자리",
      "DNS 는 이름 공간과 그것을 제공하는 서버, 그리고 서버에 질의하는 리졸버 셋으로 이루어진다. "
      "원문은 범위를 리졸버 관점 하나로 못박는다. 캡처에 잡히는 것도 리졸버와 서버 사이의 "
      "질의 한 줄과 응답 여러 줄이다.",
      "캡처에 잡히는 구간은 리졸버와 서버 사이 한 곳입니다")

LX, LW = 132, 700
LH, STRIDE = 68, 88
Y0 = 120

LAYERS = [
    ("L3", "리졸버 (클라이언트)", "이 편이 보는 자리 · dns 필터 · UDP 53", ACC, True),
    ("L2", "이름 서버", "이름 공간을 제공 · 같은 질의에 여러 답", INFO, False),
    ("L1", "이름 공간", "계층적 이름의 전체 집합", MUTED, False),
]

for i, (tag, name, sub, col, focal) in enumerate(LAYERS):
    y = Y0 + i * STRIDE
    if focal:
        d.tone(LX, y, LW, LH, col, 8, op="14", sw=1.5)
    else:
        d.tone(LX, y, LW, LH, col, 8, op="0A", sw=1.1)
    d.t(LX - 16, y + 40, tag, 9, SOFT, MONO, "end", 600)
    d.t(LX + 24, y + 30, name, 15, col, KR, "start", 600)
    d.t(LX + 24, y + 52, sub, 12, MUTED, KR, "start")

d.t(44, Y0 + 20, "질의 ↑", 12, SOFT, KR, "start")
d.line(60, Y0 + 32, 60, Y0 + 2 * STRIDE + LH, RULE, 1.0, "3 6")
d.t(44, Y0 + 2 * STRIDE + LH + 4, "범위 ↓", 12, SOFT, KR, "start")

d.t(24, 412, "질의 섹션 — 레코드 타입 · 호스트명 · 클래스 IN", 12, SOFT, KR, "start")
d.t(24, 436, "응답 섹션 — 줄이 여럿이면 CNAME 체인이거나 주소가 여럿", 11, MUTED, KR, "start")
d.t(24, 458, "TCP 로 넘어가는 조건 — 존 전송(AXFR) · 응답이 한계 초과(OPT 크기 이하, 없으면 512)",
     11, MUTED, KR, "start")

d.legend(H - 44, [("원문이 못박은 범위", ACC), ("질의를 받는 쪽", INFO)])
d.save("05-02.dns-parts.svg")
