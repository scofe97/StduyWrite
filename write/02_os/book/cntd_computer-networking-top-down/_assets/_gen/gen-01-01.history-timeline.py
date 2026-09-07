# 01-01 §5 — 지금의 모양이 정해진 결정들. 원문 1.7 의 연도와 인물을 그대로 옮긴다.
# 타입 스펙: type-timeline — 시간 축 위의 사건. 간격은 실제 연도 비율을 지키고,
#           focal 은 되돌릴 수 없게 방향을 정한 사건 하나(1983 flag day)다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, INFO, PAPER2, RULE, KR, MONO

W, H = 992, 500
AX0, AX1, AY = 56, 936, 268
Y0, Y1 = 1961, 1986

d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 01-01 §5",
      "패킷 교환에서 TCP/IP 전환까지",
      "원문 1.7 이 적는 사건들. 전화망이 지배하던 시절에 버스트 트래픽을 위해 다른 답을 낸 사람들이 있었고, 그 답이 25년 만에 표준이 됐다.",
      "칸 사이 간격은 실제 연도 비율입니다 — 1970년대에 몰려 있습니다")

def x(yr): return AX0 + (yr - Y0) / (Y1 - Y0) * (AX1 - AX0)

d.line(AX0, AY, AX1, AY, RULE, 1.2)

EV = [
    (1961, "Kleinrock", "큐잉 이론으로 패킷 교환이", "버스트 트래픽에 낫다는 것을 보임", "up", INFO),
    (1964, "Baran · Davies", "Rand 와 영국 NPL 이", "서로 모른 채 같은 답에 도달", "down", INFO),
    (1969, "첫 패킷 스위치", "노동절 UCLA 설치 · 연말 네 노드", "첫 원격 로그인이 시스템을 죽임", "up", MUTED),
    (1972, "NCP 와 이메일", "약 15노드 · Kahn 공개 시연", "Tomlinson 이 첫 이메일 작성", "down", MUTED),
    (1974, "internetting", "Cerf 와 Kahn 이", "네트워크를 잇는 원리를 세움", "up", MUTED),
    (1983, "flag day", "1월 1일 NCP 에서 TCP/IP 로", "모든 호스트가 그날 넘어옴", "down", ACC),
    (1986, "NSFNET", "백본 56 kbps 로 출발", "10년 안에 1.5 Mbps", "up", OK),
]

for yr, title, l1, l2, side, c in EV:
    cx = x(yr)
    up = side == "up"
    ty = AY - 116 if up else AY + 44
    d.line(cx, AY - (10 if up else 0), cx, ty + (72 if up else 0), c, 1.2, "3 5")
    d.o.append(f'<circle cx="{cx}" cy="{AY}" r="5" fill="{c}"/>')
    bw, bh = 176, 72
    bx = min(max(cx - bw / 2, 12), W - 12 - bw)
    if c == ACC: d.tone(bx, ty, bw, bh, ACC, 6)
    else: d.box(bx, ty, bw, bh, PAPER2, RULE, 1.0, 6)
    d.t(bx + bw / 2, ty + 21, title, 12, c, KR, "middle", 600)
    d.t(bx + bw / 2, ty + 40, l1, 11, MUTED, KR)
    d.t(bx + bw / 2, ty + 57, l2, 11, MUTED, KR)
    d.t(cx, AY + (22 if up else -14), str(yr), 11, INK, MONO, "middle", 600)

d.t(24, 404, "1970년대 말에 TCP·UDP·IP 세 프로토콜이 개념적으로 자리를 잡습니다 — UDP 는 TCP 의 축소판이 아니라 다른 요구에서 갈라져 나온 것입니다",
     11, MUTED, KR, "start")

d.legend(H - 60, [("되돌릴 수 없게 방향을 정한 날", ACC), ("발명 구간", INFO), ("확산 구간", OK)])
d.save("01-01.history-timeline.svg")
