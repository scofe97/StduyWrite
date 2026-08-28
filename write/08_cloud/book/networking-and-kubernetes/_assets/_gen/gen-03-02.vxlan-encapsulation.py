# 03-02.vxlan-encapsulation — MAC-in-UDP, 껍질을 씌우고 벗긴다
# 본문 요구: 네 단계 — 원본 프레임 / 캡슐화(VNI 24비트) / L3 언더레이 / 역캡슐화
# 타입 스펙: type-architecture.md — 상자에 든 것은 단계마다의 프레임 모습이고, 컴포넌트는 단계 머리(호스트1 컨테이너 · 송신 VTEP · L3 언더레이 · 호스트2 VTEP)에 있다.
#           38개 메뉴에 이 형태(주체 레인 없는 값·단계 사슬)를 담을 타입이 없다 —
#           layout 문법만 architecture 를 따르고 그 사실을 여기 적어 둔다.
#           2026-08-29 정정: type-data-flow 로 적었으나 그 정본은 역할 레인 1~4 × 단계 열 ×
#           타입 있는 페이로드 칩이 입력 계약인 데이터 플랫폼 전용 타입이다. 이 그림에 레인은 없다.
#           type-architecture 의 Best for 에 "data-flow diagrams" 가 그대로 들어 있다.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 564
d = D(W, H, "VXLAN · MAC-in-UDP",
      "MAC-in-UDP — 껍질을 씌워 보내고 반대편에서 벗긴다",
      "물리망은 바깥 헤더만 보고 내용물은 모른다. VNI 24비트가 어느 논리 네트워크인지를 가른다.",
      lead="물리망은 바깥 헤더만 보고 내용물은 모른다 · VNI 가 논리 네트워크를 가른다")

PAD, SLOT = 36, 232
CX = [PAD + j * SLOT + SLOT // 2 for j in range(4)]
CY, FW, FH, SW_, SH = 300, 132, 48, 160, 124
FH_, SH_ = FW // 2, SW_ // 2
HALF = [FH_, SH_, SH_, FH_]

ddx.band(d, 104, 500, "껍질이 있는 동안에는 평범한 UDP 트래픽으로 보인다")
for cx, t in zip(CX, ["① 호스트1 컨테이너", "② 송신 VTEP", "③ L3 언더레이", "④ 호스트2 VTEP"]):
    d.t(cx, 180, t, 12, SOFT, KR, "middle", 600)

def frame(cx, cy, c=INFO):
    d.o.append(f'<rect x="{cx-FH_}" y="{cy-FH//2}" width="{FW}" height="{FH}" rx="5" '
               f'fill="{c}14" stroke="{c}" stroke-width="1.2"/>')
    d.t(cx, cy - 2, "원본 프레임", 12, c, KR, "middle", 600)
    d.t(cx, cy + 15, "Ethernet·IP·TCP", 9, MUTED, MONO)

def shell(cx, cy, label, focal=False):
    c, sw = (ACC, 1.4) if focal else (INFO, 1.2)
    d.o.append(f'<rect x="{cx-SH_}" y="{cy-SH//2}" width="{SW_}" height="{SH}" rx="7" '
               f'fill="{c}0A" stroke="{c}" stroke-width="{sw}"/>')
    d.t(cx, cy - SH // 2 + 22, ddx.fit(label, 11, SW_ - 16, label), 11, c, KR, "middle", 600)

frame(CX[0], CY)
shell(CX[1], CY, "VNI 24비트 · UDP", focal=True); frame(CX[1], CY + 16)
shell(CX[2], CY, "바깥 헤더만 읽힘");             frame(CX[2], CY + 16, SOFT)
frame(CX[3], CY)
for cx, note, c in zip(CX, ["브리지로 나감", "MAC-in-UDP", "내용물은 모름", "목적지 컨테이너"],
                       [MUTED, ACC, MUTED, OK]):
    d.t(cx, CY + SH // 2 + 26, note, 11, c, KR)
for j, lab in enumerate(["브리지로", "UDP 로", "반대편"]):
    a, b = CX[j] + HALF[j], CX[j + 1] - HALF[j + 1]
    d.path(f"M {a+10} {CY} L {b-12} {CY}", MUTED, 1.5, m="ar")
    d.t((a + b) // 2, CY - 20, ddx.fit(lab, 11, b - a - 8, f"corridor{j+1}"), 11, MUTED, KR)

d.t(36, 464, "VTEP 가 감싸고 벗기는 사이에 물리망은 노드 사이의 평범한 트래픽만 본다 — "
             "그래서 L3 를 가로질러 L2 인접성이 만들어진다", 12, MUTED, KR, "start")
d.legend(516, [("겉봉 · 물리망이 읽는 부분", INFO), ("감싸는 순간", ACC), ("도착", OK)])
d.save("03-02.vxlan-encapsulation.svg")
print("ok 03-02.vxlan-encapsulation")
