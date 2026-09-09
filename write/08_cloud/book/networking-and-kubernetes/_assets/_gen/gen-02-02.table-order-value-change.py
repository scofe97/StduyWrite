# 02-02.table-order-value-change — 한 체인 안에서 값이 어떻게 바뀌는가
# 본문 요구: §1 은 "체인이 먼저이고 그 안에서 Raw → Mangle → NAT → Filter 로 평가된다"를
#           문장으로만 적는다. 왜 그 순서여야 하는지는 값이 바뀌는 것을 봐야 잡히는데,
#           chain-then-table 도식은 어느 칸이 있고 없는지만 보이고 값은 담지 않는다.
#           학습자가 Phase 1 에서 스스로 세운 "값을 바꾸는 놈이 먼저, 그 값으로 결정하는 놈이 나중"을
#           패킷 필드의 실제 변화로 보이는 것이 이 그림의 몫이다.
# 타입 스펙: type-state.md — 테이블이 전이(입력), 패킷이 상태, 상태 안의 필드값이 결과다.
#           세로로 쌓아 전이 옆에 규칙 전문을 실을 자리를 준다.
#           coral 은 마지막 하나 — 바뀐 값으로 판정이 내려지는 자리.
#           각 상태에서 바뀐 필드만 상자 색으로 집어, 무엇이 달라졌는지를 눈으로 찾지 않게 한다.
#           정본 대조: 시작 점·끝 링 표식과 `event [guard] / action` 라벨 형식은 쓰지 않았다.
#           상자에 든 것이 유한 상태가 아니라 패킷 스냅숏이라 build-steps 와 같은 어긋남이 있고,
#           같은 이유로 그대로 둔다 — 테이블이 곧 전이라는 읽기가 성립한다.
# 체인 선택: mangle·nat·filter 셋을 다 가진 체인은 INPUT 과 OUTPUT 뿐이라 OUTPUT 을 골랐다.
#           본문 표(테이블×체인)가 그 제약을 이미 적어 두었다.
# 주소: 본문 frontmatter allow 에 이미 있는 값만 쓴다 (10.96.192.224 · 10.244.1.66).
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 862
d = D(W, H, "ONE CHAIN · MANGLE → NAT → FILTER",
      "한 체인 안에서 값이 어떻게 바뀌는가",
      "노드의 프로세스가 ClusterIP 로 보낸 패킷이 OUTPUT 체인을 지나는 동안입니다. "
      "왼쪽은 그 테이블을 지난 직후의 패킷이고, 오른쪽은 그 자리에서 평가되는 테이블과 규칙입니다.",
      lead="값을 바꾸는 둘이 먼저, 그 값으로 판정하는 하나가 나중")

SX, SW, SH = 56, 408, 104
CY = [186, 348, 510, 672]
LX = 520
AVAIL = W - LX - 44

d.t(SX, 128, "결과 — 그 직후의 패킷", 11, SOFT, KR, "start", 600)
d.t(LX, 128, "전이 — 그 자리의 테이블과 규칙", 11, SOFT, KR, "start", 600)

# 필드는 둘로 나눠 적고, 그 칸에서 *바뀐 쪽만* 상자 색으로 집는다.
# 두 줄을 나란히 두고 눈으로 diff 하게 하면 이 그림의 요지가 독자 몫으로 넘어간다.
STATES = [
    ("프로세스가 만든 패킷", "dst 10.96.192.224:80", "mark 0x0", None, None),
    ("mangle 을 지난 뒤", "dst 10.96.192.224:80", "mark 0x1", INFO, "mark"),
    ("nat 을 지난 뒤", "dst 10.244.1.66:80", "mark 0x1", INFO, "dst"),
    ("filter 가 판정", "-d 10.244.1.66", "-> ACCEPT", ACC, "both"),
]
MX = SX + 24 + 212
for (name, dst, mark, c, changed), cy in zip(STATES, CY):
    if c is None:
        d.box(SX, cy - SH // 2, SW, SH, PAPER2, RULE, 1.1, 8); tc = INK
    else:
        d.o.append(f'<rect x="{SX}" y="{cy-SH//2}" width="{SW}" height="{SH}" rx="8" '
                   f'fill="{c}12" stroke="{c}" stroke-width="{1.4 if c is ACC else 1.1}"/>'); tc = c
    d.t(SX + 24, cy - 18, ddx.fit(name, 13, SW - 48, name), 13, tc, KR, "start", 600)
    dc = c if changed in ("dst", "both") else MUTED
    mc = c if changed in ("mark", "both") else MUTED
    d.t(SX + 24, cy + 16, ddx.fit(dst, 11, 200, dst), 11, dc, MONO, "start",
        600 if dc is not MUTED else 400)
    d.t(MX, cy + 16, ddx.fit(mark, 11, SW - 236 - 24, mark), 11, mc, MONO, "start",
        600 if mc is not MUTED else 400)

for i in (0, 1, 2):
    d.path(f"M {SX+SW//2} {CY[i]+SH//2} L {SX+SW//2} {CY[i+1]-SH//2-8}", MUTED, 1.5, m="ar")

# 전이 셋 — 테이블 이름 · 규칙 전문 · 그 자리가 하는 일
TRANS = [
    ("mangle  OUTPUT", "-j MARK --set-mark 0x1", "표식만 붙는다 — 주소는 그대로다", INFO, 267),
    ("nat  OUTPUT", "-j DNAT --to-destination 10.244.1.66:80", "목적지가 갈린다 — 여기가 값이 바뀌는 자리다", INFO, 429),
    ("filter  OUTPUT", "-d 10.244.1.66 -j ACCEPT", "바뀐 목적지를 보고 판정한다", ACC, 591),
]
for title, rule, why, c, y in TRANS:
    d.t(LX, y - 24, title, 11, c, MONO, "start", 600)
    d.t(LX, y, ddx.fit(rule, 11, AVAIL, rule), 11, INK, MONO, "start")
    d.t(LX, y + 24, ddx.fit(why, 12, AVAIL, why), 12, MUTED, KR, "start")
    d.path(f"M {SX+SW+10} {y-4} L {LX-10} {y-4}", c if c is ACC else RULE,
           1.2 if c is ACC else 1.0, dash="4 4")

d.t(36, 752, "순서가 뒤집혔다면 filter 는 10.96.192.224 를 보고 판정합니다 — Pod IP 로 쓴 규칙은 발화하지 않습니다.",
    12, ACC, KR, "start", 600)
d.t(36, 776, "앞에 Raw 가 한 칸 더 있습니다. 연결 추적을 켤지 정할 뿐 위 값들은 건드리지 않아 뺐습니다.", 12, MUTED, KR, "start")
d.t(36, 798, "mangle 규칙은 순서를 보이려고 든 예이며 kube-proxy 가 넣는 것은 아닙니다.", 12, MUTED, KR, "start")
d.legend(820, [("값이 바뀐 자리", INFO), ("바뀐 값으로 판정", ACC)])
d.save("02-02.table-order-value-change.svg")
print("ok table-order-value-change")
