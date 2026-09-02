# 04-01 §5 — 호스트 테이블 한 줄에서 hosts 플러그인이 만들어 내는 레코드.
# 원문 근거: 표준 호스트 테이블 형식은 `<IP address> <canonical name> [aliases...]` 이고,
#            읽고 나면 (1) IPv4 항목마다 정규 이름과 별칭 전부를 그 주소로 잇는 A 레코드,
#            (2) IPv6 항목마다 같은 방식의 AAAA 레코드, (3) 주소를 정규 이름으로 되돌리는 PTR 하나를
#            만든다. "Note that the aliases become A or AAAA records, not canonical name (CNAME) records."
# 타입 스펙: type-tree — 한 줄이라는 부모에서 레코드 세 갈래로 갈라지는 생성 관계다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 940, 560
d = D(W, H, "LEARNING COREDNS · 04-01 §5",
      "호스트 테이블 한 줄이 만드는 것",
      "주소와 정규 이름과 별칭으로 된 한 줄에서 레코드 세 갈래가 나온다. "
      "별칭까지 주소로 이어지는 쪽과 주소에서 이름으로 되돌아오는 쪽이 다르다는 점이 이 절에서 걸리는 자리다.",
      "별칭은 CNAME 이 아니라 주소 레코드가 됩니다")

NW, NH = 200, 56
ROOT_Y, MID_Y, LEAF_Y = 96, 216, 312
BUS_Y = 184
CX = [208, 468, 728]

d.line(468, ROOT_Y + NH, 468, BUS_Y, MUTED, 1.0)
d.line(CX[0], BUS_Y, CX[2], BUS_Y, MUTED, 1.0)
for cx in CX:
    d.line(cx, BUS_Y, cx, MID_Y, MUTED, 1.0)
    d.line(cx, MID_Y + NH, cx, LEAF_Y, MUTED, 1.0)

d.box(468 - NW / 2, ROOT_Y, NW, NH, PAPER2, RULE, 1.0)
d.t(468, ROOT_Y + 26, "호스트 테이블 한 줄", 14, INK, KR, "middle", 600)
d.t(468, ROOT_Y + 46, "주소 · 정규 이름 · 별칭", 13, MUTED)

mids = [("A 레코드", "항목이 IPv4 일 때"),
        ("AAAA 레코드", "항목이 IPv6 일 때"),
        ("PTR 레코드", "주소당 하나")]
leaves = [("정규 이름과 별칭 전부", "별칭도 CNAME 이 아니다"),
          ("정규 이름과 별칭 전부", "A 와 같은 방식"),
          ("정규 이름만", "별칭으로는 안 돌아온다")]
for i, cx in enumerate(CX):
    nm, sub = mids[i]
    d.box(cx - NW / 2, MID_Y, NW, NH, PAPER2, RULE, 1.0)
    d.t(cx, MID_Y + 26, nm, 14, INK, MONO, "middle", 600)
    d.t(cx, MID_Y + 46, sub, 13, MUTED)
    nm, sub = leaves[i]
    focal = (i == 0)
    if focal:
        d.tone(cx - NW / 2, LEAF_Y, NW, NH, ACC, 6, "12", 1.4)
    else:
        d.box(cx - NW / 2, LEAF_Y, NW, NH, PAPER2, RULE, 0.8)
    d.t(cx, LEAF_Y + 26, nm, 13, ACC if focal else INK, KR, "middle", 600)
    d.t(cx, LEAF_Y + 46, sub, 12, ACC if focal else MUTED, KR)

d.t(12, MID_Y + 30, "무엇이 생기나", 12, SOFT, KR, "start")
d.t(12, LEAF_Y + 30, "누구를 가리키나", 12, SOFT, KR, "start")

d.t(20, 416, "no_reverse 를 주면 PTR 을 만들지 않고, ttl 기본값은 3600초다 — 단위 없이 정수로만 적는다", 13, MUTED, KR, "start")
d.t(20, 438, "이렇게 만든 존에는 SOA 가 없어 다른 서버로 전송할 수 없다 — 존 전체가 아니라 이름 몇 개를 싣는 용도다", 13, MUTED, KR, "start")

d.legend(458, [("별칭 처리가 갈리는 자리", ACC)])
d.save("04-01.hosts-records.svg")
