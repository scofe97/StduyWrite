# 02-01 §5 — www.example.com 질의 하나가 스텁 리졸버, 재귀 서버, 루트·TLD·권한 서버를 차례로 지나는 값의 흐름.
# 근거: RFC 9499 의 Stub resolver·Non-recursive query·Top-Level Domain 정의, 02-01 §6 의 재귀 설명,
#       01-01 §5 와 06-02 의 기본 Corefile(kubernetes 플러그인이 cluster.local 을 답하고 나머지는 forward).
# 타입 스펙: type-flowchart — 주체 사이를 가로로 잇는 한 방향 흐름이고, 질의 쪽 화살표와 답·참조 쪽 화살표를
#            선 모양과 라벨로 구분하는 것이 논지다. 시간순 왕복이 아니라 계층 분담이 요점이라 sequence 가 아니다(§6 이 sequence).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, OK, INFO, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO


def fam(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO


W, H = 896, 540
d = D(W, H, "LEARNING COREDNS · 02-01 §5",
      "스텁은 묻고 재귀 서버가 답을 완성한다",
      "www.example.com 질의 하나가 앱, 스텁 리졸버, 재귀 서버를 지나 루트·TLD·권한 서버까지 가는 순서. "
      "재귀 서버만 참조를 따라 내려가고, 쿠버네티스에서는 CoreDNS 가 클러스터 이름을 직접 답하고 나머지를 재귀 서버로 넘긴다.",
      "재귀 서버만 참조를 따라 내려갑니다")

CY = 222                       # 본 흐름의 중심 y
BH = 62                        # 왼쪽 상자 높이
APP = (24, 124)                # x, w
STUB = (208, 124)
REC = (392, 130)               # 재귀 서버는 오른쪽 세 상자 높이에 맞춰 키 큰 상자
SRV_X, SRV_W, SRV_H = 692, 180, 56
ROWS = [138, 222, 306]         # 루트·TLD·권한 중심 y


def node(x, w, cy, h, title, sub, focal=False):
    if focal:
        d.tone(x, cy - h / 2, w, h, INFO)
    else:
        d.box(x, cy - h / 2, w, h, PAPER2, RULE, 1.0)
    d.t(x + w / 2, cy - 2, title, 13, INK, KR, "middle", 600)
    d.t(x + w / 2, cy + 16, sub, 11, MUTED, fam(sub))


def pair(x1, x2, cy, out_lab, back_lab, back_c=MUTED, out_c=MUTED, back_mk="ar", dash="5 4"):
    """x1 → x2 질의(실선, 라벨 위)와 x2 → x1 답(점선, 라벨 아래)을 나란히 그린다."""
    mx = (x1 + x2) / 2
    d.arrow([(x1 + 2, cy - 8), (x2 - 2, cy - 8)], out_c, "ar", 1.5)
    d.t(mx, cy - 15, out_lab, 12, out_c, fam(out_lab), "middle", 600)
    d.arrow([(x2 - 2, cy + 8), (x1 + 2, cy + 8)], back_c, back_mk, 1.5, dash)
    d.t(mx, cy + 25, back_lab, 12, back_c, fam(back_lab), "middle", 600)


# 한 기계 안 표시
d.line(APP[0], 172, STUB[0] + STUB[1], 172, SOFT, 1.0)
d.t(APP[0] + (STUB[0] + STUB[1] - APP[0]) / 2, 164, "한 기계 안(OS)", 11, SOFT, KR)

node(*APP, CY, BH, "앱", "getaddrinfo()")
node(*STUB, CY, BH, "스텁 리졸버", "/etc/resolv.conf")
node(REC[0], REC[1], CY, 224, "재귀 서버", "캐시 확인 뒤 질의", focal=True)
d.t(REC[0] + REC[1] / 2, CY + 36, "참조를 따라감", 11, MUTED, KR)

pair(APP[0] + APP[1], STUB[0], CY, "요청", "답", back_c=ACC, back_mk="acc", dash=None)
pair(STUB[0] + STUB[1], REC[0], CY, "재귀 질의", "답", back_c=ACC, back_mk="acc", dash=None)

x1, x2 = REC[0] + REC[1], SRV_X
srv = [("루트 서버", "."), ("TLD 서버", "com"), ("권한 서버", "example.com")]
for cy, (t, s) in zip(ROWS, srv):
    node(SRV_X, SRV_W, cy, SRV_H, t, s)
pair(x1, x2, ROWS[0], "반복 질의", "참조 · com NS")
pair(x1, x2, ROWS[1], "반복 질의", "참조 · example.com NS")
pair(x1, x2, ROWS[2], "반복 질의", "답 · A 레코드", back_c=OK, back_mk="ok")

# 쿠버네티스 띠
d.line(24, 360, W - 24, 360, RULE, 1.0)
d.t(24, 380, "쿠버네티스 파드 안에서는", 11, SOFT, KR, "start")
BY = 424
node(APP[0], APP[1], BY, 56, "파드의 스텁", "resolv.conf 사용")
node(STUB[0], STUB[1], BY, 56, "CoreDNS", "클러스터 DNS")
d.arrow([(APP[0] + APP[1] + 2, BY), (STUB[0] - 2, BY)], MUTED, "ar", 1.5)
d.t((APP[0] + APP[1] + STUB[0]) / 2, BY - 8, "질의", 12, MUTED, KR, "middle", 600)

# CoreDNS → 재귀 서버(forward). 오른쪽으로 나가 재귀 서버 아래쪽으로 올라간다.
fx = REC[0] + REC[1] / 2
d.arrow([(STUB[0] + STUB[1] + 2, BY - 10), (fx, BY - 10), (fx, CY + 112 + 2)], MUTED, "ar", 1.5)
mx = (STUB[0] + STUB[1] + fx) / 2 - 4
d.t(mx, BY - 34, "상류 재귀 서버로", 12, MUTED, KR, "middle", 600)
d.t(mx, BY - 18, "그 밖 · forward", 12, MUTED, KR, "middle", 600)

# CoreDNS → 직접 답
node(SRV_X, SRV_W, BY + 10, 56, "직접 답", "kubernetes 플러그인")
d.arrow([(SRV_X - 2, BY + 10), (STUB[0] + STUB[1] + 2, BY + 10)], OK, "ok", 1.5, "5 4")
d.t((STUB[0] + STUB[1] + SRV_X) / 2, BY + 3, "cluster.local", 12, OK, MONO, "middle", 600)

# 범례: 색이 뜻이고 선 모양이 종류다. 상자 견본은 재귀 서버 상자 하나만 쓴다.
d.line(12, 480, W - 48, 480, RULE, 0.8)
d.t(12, 502, "LEGEND", 8, SOFT, MONO, "start")
lx = 100
for lab, c, mk, dash in [("질의", MUTED, "ar", None), ("참조", MUTED, "ar", "5 4"),
                         ("권한 서버·플러그인의 답", OK, "ok", "5 4"), ("스텁·앱에 돌아가는 답", ACC, "acc", None)]:
    d.arrow([(lx, 498), (lx + 34, 498)], c, mk, 1.5, dash)
    d.t(lx + 42, 502, lab, 11, MUTED, KR, "start")
    lx += 42 + len(lab) * 12 + 22
d.o.append(f'<rect x="{lx}" y="491" width="14" height="14" rx="2" fill="{INFO}22" stroke="{INFO}" stroke-width="1.1"/>')
d.t(lx + 22, 502, "재귀 서버", 11, MUTED, KR, "start")
d.save("02-01.resolver-roles.svg")
