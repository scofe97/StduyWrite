# 01-03.vxlan-encapsulation — 캡슐화 (01-01 encapsulation 참고)
# 본문: "L2 프레임을 L4 UDP 패킷에 캡슐화해 IP 네트워크를 가로질러 L2 인접성을 만든다"
#        "VLAN 이 가두는 기술이라면 VXLAN 은 잇는 기술이다"
# 타입 스펙: type-architecture.md — 상자에 든 것은 단계마다의 프레임 모습이다. 컴포넌트는 밴드 머리(노드 A · 라우터 · 노드 B)에 있다.
#           38개 메뉴에 이 형태(주체 레인 없는 값·단계 사슬)를 담을 타입이 없다 —
#           layout 문법만 architecture 를 따르고 그 사실을 여기 적어 둔다.
#           2026-08-29 정정: type-data-flow 로 적었으나 그 정본은 역할 레인 1~4 × 단계 열 ×
#           타입 있는 페이로드 칩이 입력 계약인 데이터 플랫폼 전용 타입이다. 이 그림에 레인은 없다.
#           type-architecture 의 Best for 에 "data-flow diagrams" 가 그대로 들어 있다.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 552
d = D(W, H, "VXLAN · WRAP -> CROSS -> UNWRAP",
      "VXLAN — 경계를 못 넘는 프레임을 넘게 하는 법",
      "L2 프레임을 UDP 페이로드로 감싸면 라우터에게는 평범한 IP 트래픽으로 보인다",
      lead="L2 프레임을 UDP 페이로드로 감싸면 라우터에게는 평범한 IP 트래픽으로 보인다")

PAD, SLOT = 36, 232
CX = [PAD + j * SLOT + SLOT // 2 for j in range(4)]          # 152 384 616 848
CY = 288
FW, FH, SW_, SH = 132, 48, 160, 124                          # 프레임 / 봉투
FH_, SH_ = FW // 2, SW_ // 2
HALF = [FH_, SH_, SH_, FH_]                                  # 단계별 바깥 반폭

ddx.band(d, 104, 484, "껍데기가 붙었다 벗겨진다 — 속의 프레임은 한 번도 손대지 않는다")
for cx, t in zip(CX, ["(1) 노드 A 안에서", "(2) 감싼다", "(3) IP 망을 건넌다", "(4) 노드 B 안에서"]):
    d.t(cx, 168, t, 12, SOFT, KR, "middle", 600)

def frame(cx, cy, c=INFO):
    d.o.append(f'<rect x="{cx-FH_}" y="{cy-FH//2}" width="{FW}" height="{FH}" rx="5" '
               f'fill="{c}14" stroke="{c}" stroke-width="1.2"/>')
    d.t(cx, cy - 2, "L2 프레임", 12, c, KR, "middle", 600)
    d.t(cx, cy + 15, "Pod -> Pod", 9, MUTED, MONO)

def shell(cx, cy, label, focal=False):
    c, sw = (ACC, 1.4) if focal else (INFO, 1.2)
    d.o.append(f'<rect x="{cx-SH_}" y="{cy-SH//2}" width="{SW_}" height="{SH}" rx="7" '
               f'fill="{c}0A" stroke="{c}" stroke-width="{sw}"/>')
    d.t(cx, cy - SH // 2 + 22, ddx.fit(label, 11, SW_ - 16, label), 11, c, KR, "middle", 600)

frame(CX[0], CY)
shell(CX[1], CY, "IP · UDP · VXLAN 봉투", focal=True); frame(CX[1], CY + 16)
shell(CX[2], CY, "겉만 읽힌다");                        frame(CX[2], CY + 16, SOFT)
frame(CX[3], CY)

for cx, note, c in zip(CX, ["경계를 못 넘는다", "봉투가 붙는다", "라우터에겐 평범한 IP", "그대로 나온다"],
                       [MUTED, ACC, MUTED, OK]):
    d.t(cx, CY + SH // 2 + 26, note, 11, c, KR)

for j, lab in enumerate(["넣는다", "봉함된 채", "꺼낸다"]):
    a, b = CX[j] + HALF[j], CX[j + 1] - HALF[j + 1]          # 코리도어 양 끝
    d.path(f"M {a+10} {CY} L {b-12} {CY}", MUTED, 1.5, m="ar")
    d.t((a + b) // 2, CY - 20, ddx.fit(lab, 11, b - a - 8, f"corridor{j+1}"), 11, MUTED, KR)

d.t(36, 448, "VLAN 이 가두는 기술이라면 VXLAN 은 잇는 기술이다 — 떨어진 노드의 Pod 들이 "
             "같은 L2 에 있는 것처럼 통신하는 바닥이 이 봉함이다", 12, MUTED, KR, "start")
d.legend(504, [("겉봉 · 라우터가 읽는 부분", INFO), ("감싸는 순간", ACC)])
d.save("01-03.vxlan-encapsulation.svg")
print("ok vxlan-encapsulation")
