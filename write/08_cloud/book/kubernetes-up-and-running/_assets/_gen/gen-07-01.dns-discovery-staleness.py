# 07-01 §DNS 로는 왜 부족한가 — "잘못된 IP 에 닿는 경로"
# 본문이 "TTL 을 짧게 잡고 클라이언트가 얌전히 굴어도 … 자연스러운 지연이 남습니다" 라고
# 못 박는다. 그래서 클라이언트를 하나만 그리면 "설정을 잘못했다" 로 읽힌다 — 얌전한 쪽과
# 안 얌전한 쪽을 같은 시간축에 나란히 놓아야 "줄지만 0 이 되지 않는다" 가 보인다.
# 아래 고침 띠는 본문의 반전("캐싱을 막는 대신 캐싱해도 되는 대상을 만들었다") 을 받는다.
# 타입 스펙: type-gantt.md — 왼쪽 레인 이름 열 + 공용 시간축 위에 구간 막대, 사건마다 세로 눈금.
#           세 레인이 병렬 트랙이고 초점은 M1~M2 구간을 재는 대괄호다 — 정본의 milestone marker 관례.
#           어긋나는 지점: 막대가 작업이 아니라 *그때 믿고 있는 값* 이고, 아래 고침 띠는
#           architecture 어휘(노드 사슬)라 gantt 에 자리가 없다. timeline 은 기각 — 기준선 하나 위
#           사건 점이 아니라 병렬 레인의 구간 겹침이 요점이다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, BAD, MUTED, SOFT, INK, PAPER2, PAPER, RULE, KR, MONO
import ddx

W, H = 1240, 636
d = D(W, H, "KUBERNETES UP AND RUNNING · 07-01",
      "이름이 가리키는 값이 늦게 따라온다",
      "DNS 는 안정적인 이름 해석과 넓은 캐싱을 전제로 만들어졌다. 파드가 계속 바뀌는 클러스터에서는 "
      "그 전제가 깨져, 값이 바뀐 시점과 클라이언트가 알아채는 시점 사이가 벌어진다.",
      "재조회 여부와 무관하게 간격 자체는 남는다")

M0, M1, M2, XE = 250, 610, 900, 1215
LX = 12                      # 레인 이름 왼쪽 끝
ROW_H, GAP = 58, 20
RY = [140, 218, 296]         # 세 레인 상단

for x, lab, anc in ((M0, "이름을 조회한다", "start"),
                    (M1, "파드가 바뀐다", "middle"),
                    (M2, "TTL 만료 · 재조회", "middle")):
    d.t(x, 118, lab, 10, SOFT, KR, anc)
for x in (M1, M2):
    d.line(x, 128, x, RY[2] + ROW_H + 8, RULE, 1.0, "4 5")

def seg(y, x0, x1, txt, c=None, wrong=False):
    """구간 한 칸. wrong 이면 없는 IP 로 요청이 가는 구간이다."""
    if wrong:
        d.o.append(f'<rect x="{x0}" y="{y}" width="{x1-x0}" height="{ROW_H}" rx="6" '
                   f'fill="{BAD}12" stroke="{BAD}" stroke-width="1.3"/>')
    else:
        d.box(x0, y, x1 - x0, ROW_H, PAPER2, c or RULE, 1.0, 6)
    tc = BAD if wrong else (c or INK)
    d.t((x0 + x1) / 2, y + ROW_H / 2 + 5, txt, 13, tc, MONO)

def lane(i, l1, l2):
    y = RY[i]
    d.t(LX, y + 22, l1, 11, INK, KR, "start", 600)
    d.t(LX, y + 42, l2, 11, SOFT, KR, "start")

lane(0, "실제", "엔드포인트가 가리키는 파드")
seg(RY[0], M0, M1, "10.0.1.7")
seg(RY[0], M1, XE, "10.0.3.2")

lane(1, "재조회하지 않는", "클라이언트가 믿는 값")
seg(RY[1], M0, M1, "10.0.1.7")
seg(RY[1], M1, XE, "10.0.1.7", wrong=True)
d.t(XE - 16, RY[1] + 22, "끝까지 없는 주소로 보낸다", 10, BAD, KR, "end")

lane(2, "TTL 을 짧게 잡은", "얌전한 클라이언트")
seg(RY[2], M0, M1, "10.0.1.7")
seg(RY[2], M1, M2, "10.0.1.7", wrong=True)
seg(RY[2], M2, XE, "10.0.3.2")

# 초점 — 줄어들 뿐 사라지지 않는 간격
BY = RY[2] + ROW_H + 12
d.path(f"M {M1} {BY} L {M1} {BY+10} L {M2} {BY+10} L {M2} {BY}", ACC, 1.4)
d.t((M1 + M2) / 2, BY + 32,
    "짧게 잡아도 이 간격은 0 이 되지 않는다 — 값이 바뀐 시점과 알아채는 시점의 차이다", 11, ACC, KR)

# 고침 — 본문의 반전
DV = BY + 52
d.line(12, DV, W - 24, DV, RULE, 0.8)
d.t(12, DV + 24, "고침 — 쿠버네티스는 DNS 를 버리지 않았다", 13, INK, KR, "start", 600)

BT, BB = DV + 38, DV + 138
d.o.append(f'<rect x="12" y="{BT}" width="{W-36}" height="{BB-BT}" rx="8" '
           f'fill="{OK}0A" stroke="{OK}" stroke-width="1.0"/>')
CY = BT + 46
ddx.node(d, 368, CY, "alpaca-prod", "DNS 이름", w=170, h=56)
ddx.node(d, 607, CY, "10.96.0.31", "cluster IP · 고정", w=196, h=56, c=OK)
ddx.node(d, 859, CY, "파드 3 개", "IP 가 계속 바뀐다", w=196, h=56)
d.path(f"M 461 {CY} L 501 {CY}", MUTED, 1.5, m="ar")
d.path(f"M 713 {CY} L 753 {CY}", MUTED, 1.5, m="ar")
d.t(W / 2, BB - 16,
    "캐싱을 막는 대신, 캐싱해도 되는 대상을 만들었다 — 뒤가 바뀌어도 이름이 가리키는 값은 그대로다",
    11, OK, KR)

d.legend(BB + 26, [("없는 IP 로 요청이 가는 구간", BAD), ("고침", OK)])
d.save("07-01.dns-discovery-staleness.svg")
print("h 필요:", BB + 26 + 48, " 실제:", H)
