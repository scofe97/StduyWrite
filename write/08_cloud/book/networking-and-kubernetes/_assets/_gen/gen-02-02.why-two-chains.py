# 02-02.why-two-chains — 확률은 한 줄에서 한 번만 굴러간다
# 본문 요구: 학습자 질문 "KUBE-SVC 와 SEP 의 차이가 뭔가". 본문 표는 둘이 무엇을 하는지만 적고
#           왜 둘이어야 하는지를 안 적었다. 합친 설계를 세워 놓고 어디서 어긋나는지를 보인다.
# 타입 스펙: type-flowchart.md — 같은 입력이 두 설계를 지나며 갈리는 짝 추적.
#           selection 의 "규칙 두 갈래가 통과·실패로 갈리고 어디서 갈렸는지가 논지다".
#           coral 은 실제 설계(정상 경로)에만. 확률 판정은 마름모, 단계는 사각, 시작·끝은 타원.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 696
d = D(W, H, "kube-proxy · WHY TWO CHAINS",
      "확률은 한 줄에서 한 번만 굴러간다",
      "합친 설계는 같은 확률을 두 번 굴려 표시한 백엔드와 보낸 백엔드가 어긋난다.",
      lead="뽑은 뒤 할 일이 두 줄이라 점프가 필요하다 — 그 갈 곳이 엔드포인트 체인이다")

COLW, CX = 464, (256, 744)
HDR = [("합쳤다면", "확률 줄 두 개 · 각자 따로 굴린다", BAD),
       ("실제 설계", "확률 줄 하나 · 뽑은 뒤 점프한다", ACC)]
HY, HH = 100, 44
for i, (lab, sub, col) in enumerate(HDR):
    x = 24 + i * (COLW + 24)
    d.box(x, HY, COLW, HH, PAPER2, RULE, 1.0)
    d.t(x + 16, HY + 27, ddx.fit(lab, 13, 140, f"hdr {lab}"), 13, col, KR, "start", 600)
    d.t(x + COLW - 16, HY + 27, ddx.fit(sub, 11, 290, f"sub {sub}"), 11, MUTED, KR, "end")

NW = 300
def oval(cx, cy, txt, col=INK, h=44):
    d.o.append(f'<rect x="{cx-NW/2}" y="{cy-h/2}" width="{NW}" height="{h}" rx="20" '
               f'fill="{PAPER2}" stroke="{col}" stroke-width="1.1"/>')
    d.t(cx, cy + 5, ddx.fit(txt, 12, NW - 28, f"oval {txt}"), 12, col, KR)

def step(cx, cy, txt, sub=None, col=RULE, tc=INK, h=52):
    d.box(cx - NW / 2, cy - h / 2, NW, h, PAPER2, col, 1.1, 6)
    if sub:
        d.t(cx, cy - 3, ddx.fit(txt, 12, NW - 28, f"step {txt}"), 12, tc, KR)
        d.t(cx, cy + 16, ddx.fit(sub, 11, NW - 28, f"sub {sub}"), 11, MUTED, MONO)
    else:
        d.t(cx, cy + 5, ddx.fit(txt, 12, NW - 28, f"step {txt}"), 12, tc, KR)

def diamond(cx, cy, txt, hw=112, hh=34):
    d.o.append(f'<path d="M {cx} {cy-hh} L {cx+hw} {cy} L {cx} {cy+hh} L {cx-hw} {cy} z" '
               f'fill="{WARN}12" stroke="{WARN}" stroke-width="1.3"/>')
    d.t(cx, cy + 4, ddx.fit(txt, 11, hw * 1.4, f"dia {txt}"), 11, WARN, KR)

def down(cx, y1, y2, label=None, c=SOFT):
    d.path(f"M {cx} {y1} L {cx} {y2}", c, 1.4, m="soft" if c == SOFT else "acc")
    if label:
        d.t(cx + 12, (y1 + y2) / 2 + 4, label, 11, c, MONO, "start")

# 왼쪽 — 합쳤다면
L = CX[0]
oval(L, 186, "ClusterIP 로 패킷이 온다")
down(L, 208, 234)
diamond(L, 262, "확률 0.33 굴림 · 1회차")
down(L, 296, 314, "A")
step(L, 338, "KUBE-MARK-MASQ", "-s 10.244.1.35 기준으로 표시")
down(L, 364, 386)
diamond(L, 414, "확률 0.33 굴림 · 2회차")
down(L, 448, 466, "B")
step(L, 490, "DNAT", "--to-destination 10.244.2.4:80")
down(L, 516, 542)
oval(L, 566, "A 를 표시하고 B 로 보낸다", BAD)

# 오른쪽 — 실제
R = CX[1]
oval(R, 186, "ClusterIP 로 패킷이 온다")
down(R, 208, 234)
diamond(R, 262, "확률 0.33 굴림 · 한 번뿐")
down(R, 296, 314, "A", ACC)
step(R, 338, "KUBE-SEP-A 로 점프", "-j KUBE-SEP-BN57OJOGDZOVVFD3", ACC, ACC)
down(R, 364, 390, None, ACC)
d.tone(R - NW / 2, 390, NW, 80, ACC, 6, "0E", 1.3)
d.t(R, 412, "그 체인 안 두 줄 — 조건이 없다", 11, ACC, KR)
d.t(R, 434, "KUBE-MARK-MASQ", 11, INK, MONO)
d.t(R, 454, "DNAT --to 10.244.1.35:80", 11, INK, MONO)
down(R, 470, 542, None, ACC)
oval(R, 566, "둘 다 A 에 걸린다", ACC)

d.t(24, 606, "확률을 두 줄에 각각 적으면 statistic 매치가 줄마다 따로 굴러간다. 앞줄이 A 를 뽑아도 뒷줄은 B 를 뽑을 수 있다.",
    12, MUTED, KR, "start")
d.t(24, 626, "한 번의 판정을 여러 동작으로 잇는 방법은 점프뿐이고, 그래서 엔드포인트 체인이 따로 존재한다.",
    12, MUTED, KR, "start")
d.legend(646, [("확률을 굴리는 자리", WARN), ("한 번 뽑아 그대로 잇는 길", ACC), ("어긋난 결과", BAD)])
d.save("02-02.why-two-chains.svg")
print("ok why-two-chains")
