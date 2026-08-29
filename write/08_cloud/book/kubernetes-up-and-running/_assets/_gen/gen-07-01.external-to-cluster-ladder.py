# 07-01 §바깥과 잇기 — 두 방향
# 본문이 형태를 두 번 못 박는다. "방향이 둘이고 난이도가 다릅니다" 와
# "밖에서 안으로 잇는 네 사다리를 순서대로". 두 방향을 같은 크기 두 칸으로 그리면
# 난이도 차가 지워지므로, 한쪽은 상자 둘로 끝내고 다른 쪽만 4 단 사다리로 세운다.
# 사다리는 읽는 순서 = 시도 순서라야 하므로 1 번을 위에 두고 방향을 오른쪽 위에 적는다.
# 3·4 번에 본문이 붙이는 단서("오직 최후의 수단")를 두 단 사이 경계선으로 세운다 — 초점 한 곳.
# 타입 스펙: type-layers.md — 오른쪽 사다리가 같은 x·같은 폭 전폭 상자 4 단이고, 칸마다
#           왼쪽 인덱스(01~04) · 가운데 이름 · 오른쪽 주석이라는 정본의 행 해부를 그대로 쓴다.
#           방향 표시("아래로 갈수록 어려워진다 ↓")도 정본이 요구하는 direction indicator 다.
#           어긋나는 지점: 왼쪽 열(안→밖)은 층이 아니라 상자 둘 + 경고 하나다. 그리고 여기서
#           계층은 추상 수준이 아니라 *시도 순서* 다 — memory hierarchy 가 속도로 층을 나누는 것과 같다.
#           pyramid 는 기각 — 폭이 정직해야 하는데 네 사다리에 비례할 수치가 없다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, MUTED, SOFT, INK, PAPER2, PAPER, RULE, KR, MONO
import ddx

W, H = 1240, 572
d = D(W, H, "KUBERNETES UP AND RUNNING · 07-01",
      "나가는 길은 하나, 들어오는 길은 사다리",
      "클러스터 바깥과 잇는 두 방향은 난이도가 다르다. 안에서 밖으로는 정리된 답이 하나 있고, "
      "밖에서 안으로는 가능한 것부터 차례로 시도한다.",
      "3·4 번은 책이 최후의 수단으로만 여기라고 못 박는다")

LX, LW = 12, 388            # 안 → 밖
RX, RW = 430, 798           # 밖 → 안 사다리
Y0, RH, GAP = 150, 68, 44
tops = [Y0, Y0 + RH, Y0 + RH * 2 + GAP, Y0 + RH * 3 + GAP]
BOT = tops[3] + RH          # 두 열의 공통 밑변

d.t(LX, 124, "안 → 밖", 13, INK, KR, "start", 600)
d.t(LX + 84, 124, "정해진 답이 하나", 10, OK, KR, "start")
d.t(RX, 124, "밖 → 안", 13, INK, KR, "start", 600)
d.t(RX + RW, 124, "아래로 갈수록 어려워진다  ↓", 10, SOFT, KR, "end")

# ── 안 → 밖: 상자 둘이면 끝나고, 남는 것은 운영 부담 하나다
def lbox(y0, y1, title, subs, tone=None):
    if tone:
        d.o.append(f'<rect x="{LX}" y="{y0}" width="{LW}" height="{y1-y0}" rx="6" '
                   f'fill="{tone}12" stroke="{tone}" stroke-width="1.2"/>')
    else:
        d.box(LX, y0, LW, y1 - y0, PAPER2, RULE, 1.0, 6)
    cx, cy = LX + LW / 2, (y0 + y1) / 2
    ty = cy - 2 - 11 * (len(subs) - 1)
    d.t(cx, ty, ddx.fit(title, 13, LW - 40, title), 13, tone or INK, KR, "middle", 600)
    for i, s in enumerate(subs):
        d.t(cx, ty + 21 + i * 20, ddx.fit(s, 11, LW - 40, s), 11, tone or MUTED, KR)

lbox(Y0, Y0 + RH, "selector 없는 Service", ["spec.selector 를 빼고 나머지는 그대로"])
d.path(f"M {LX+LW/2} {Y0+RH} L {LX+LW/2} {Y0+RH+26}", MUTED, 1.5, m="ar")
lbox(Y0 + RH + 26, Y0 + RH * 2 + 26, "Endpoints 를 직접 넣는다", ["이름은 Service 이름과 같게"])
lbox(BOT - 116, BOT, "IP 가 바뀌면 따라서 갱신한다",
     ["자동으로 따라가지 않는다", "이 방식에 계속 남는 운영 부담이다"], tone=WARN)

# ── 밖 → 안: 네 사다리. 3·4 번은 바탕을 낮춰 "여기부터 다르다" 를 색 하나 더 쓰지 않고 보인다
RUNGS = [("01", "내부 로드밸런서", "클라우드가 지원하면 가장 쉽다 · 고정 IP 를 전통 DNS 로 알린다"),
         ("02", "NodePort 와 그 앞의 분산", "물리 로드밸런서 또는 DNS 기반 분산"),
         ("03", "직접 배선", "외부에서 kube-proxy 를 통째로 돌린다 · 온프레미스만"),
         ("04", "외부 도구", "Consul 같은 오픈소스로 안팎 연결을 관리한다")]
for i, (ix, name, note) in enumerate(RUNGS):
    y = tops[i]; last = i >= 2
    d.box(RX, y, RW, RH, PAPER if last else PAPER2, RULE, 1.0, 0)
    cy = y + RH / 2
    d.t(RX + 16, cy + 4, ix, 9, SOFT, MONO, "start")
    d.t(RX + 60, cy + 5, name, 15, MUTED if last else INK, KR, "start", 600)
    d.t(RX + RW - 18, cy + 4, ddx.fit(note, 10, RW - 340, note), 10, SOFT, KR, "end")
d.box(RX, Y0, RW, RH * 2, "none", MUTED, 1.0, 0)
d.box(RX, tops[2], RW, RH * 2, "none", SOFT, 1.0, 0)

BD = Y0 + RH * 2 + GAP / 2
d.t(RX + RW / 2, BD - 2,
    "여기부터는 최후의 수단 — 네트워킹과 쿠버네티스 양쪽에 상당한 지식을 요구한다", 11, ACC, KR)
d.line(RX, BD + 12, RX + RW, BD + 12, ACC, 1.4, "6 5")

d.t(LX, BOT + 34,
    "밖에서 안으로는 정해진 답이 하나 있는 게 아니라, 되는 것부터 차례로 시도하는 구조다. "
    "위 둘로 끝나면 그 아래는 볼 일이 없다.", 11, MUTED, KR, "start")

LY = BOT + 58
d.legend(LY, [("여기부터 최후의 수단", ACC), ("정해진 답이 있다", OK), ("남는 운영 부담", WARN)])
d.save("07-01.external-to-cluster-ladder.svg")
print("h 필요:", LY + 48, " 실제:", H)
