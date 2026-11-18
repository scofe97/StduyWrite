# 03-02.isolation-spectrum — 모드마다 패킷이 호스트 NIC 까지 가는 길과 물리망에 드러나는 주소
# 본문 요구: §1 이 "모드 선택은 격리를 얼마나 내주고 무엇을 얻느냐의 거래"라고 세운다. 그 거래가
#           실제로 드러나는 자리는 물리망이 누구의 주소를 보느냐다 — none 은 아무것도, bridge 는
#           호스트 IP 만, macvlan 은 컨테이너 MAC 과 IP, ipvlan 은 호스트 MAC 과 컨테이너 IP,
#           host 는 호스트 그 자체.
# 타입 스펙: type-data-flow.md — 행이 모드, 열이 패킷이 지나는 자리(컨테이너 → 호스트 → 물리망).
#           행마다 같은 세 자리를 지나므로 같은 x 에 같은 역할이 온다.
# 근거: docker/docs network drivers(none·bridge·host·macvlan·ipvlan), 커널 ipvlan.rst.
# 이력: 2026-11-18 재제작. 옛 판은 None · 가운데 다섯 · Host 를 세 상자로 나열해 본문 표를 되풀이했고
#       원서 시점을 맞대는 문구가 라벨에 있었다. 한 호스트 안 다섯 모드의 길로 다시 그렸다.
#       user-defined bridge 는 bridge 행과 길이 같고 overlay 는 §4 도식이 맡아 뺐다.
# 좌표: 행 stride 72(상자 56 + 틈 16), 열 중심 316 · 568 · 836. 전부 4의 배수.
import ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 584
ROW_Y0, STRIDE, BH = 184, 72, 56
CX = [316, 568, 836]
BW = [212, 212, 256]
HDR = ["컨테이너가 갖는 것", "호스트에서 거치는 것", "물리망이 보는 주소"]

ROWS = [
    ("none", ("lo 만 있음", "밖으로 나갈 인터페이스 없음"), None,
     ("아무것도 안 보임", "연결이 없음"), False),
    ("bridge", ("eth0 · 사설 IP", "예: 172.17.0.2"), ("veth → docker0", "나갈 때 masquerade"),
     ("호스트 IP 만", "컨테이너 주소는 가려짐"), False),
    ("macvlan", ("eth0 · 자기 MAC", "물리망 대역의 IP"), ("부모 NIC", "MAC 으로 갈라 전달"),
     ("컨테이너 MAC 과 IP", "장비 한 대처럼 보임"), False),
    ("ipvlan", ("eth0 · 부모 MAC", "IP 만 자기 것"), ("부모 NIC", "IP 로 갈라 전달"),
     ("호스트 MAC + 컨테이너 IP", "MAC 은 하나로 유지"), False),
    ("host", ("자기 netns 없음", "호스트 스택을 같이 씀"), ("호스트 NIC 그대로", "포트 공간도 공유"),
     ("호스트 IP 와 포트", "격리가 남지 않음"), True),
]

d = D(W, H, "DOCKER NETWORK MODES · WHAT THE WIRE SEES",
      "모드마다 물리망에 드러나는 주소가 다르다",
      "한 호스트 안의 다섯 모드에서 컨테이너가 갖는 인터페이스, 호스트에서 거치는 장치, 물리망이 보는 주소를 "
      "행마다 견준 흐름. 아래로 갈수록 컨테이너가 물리망에 더 드러나고 host 에서 격리가 사라진다.",
      lead="아래 행으로 갈수록 컨테이너가 물리망에 더 드러납니다 · host 에서 격리가 사라집니다")


def cell(cx, cy, w, top, sub, c=None, focal=False):
    x, y = cx - w // 2, cy - BH // 2
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{BH}" rx="6" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
        tc = ACC
    else:
        d.box(x, y, w, BH, PAPER2, c or RULE, 1.1, 6)
        tc = c or INK
    d.t(cx, cy - 4, ddx.fit(top, 13, w - 16, top), 13, tc, KR, "middle", 600)
    d.t(cx, cy + 16, ddx.fit(sub, 11, w - 14, sub), 11, MUTED, KR)


for cx, name in zip(CX, HDR):
    d.t(cx, 128, name, 12, SOFT, KR, "middle", 600)

# 왼쪽 눈금 — 아래로 갈수록 더 드러난다
AX = 40
d.path(f"M {AX} {ROW_Y0 - BH // 2} L {AX} {ROW_Y0 + 4 * STRIDE + BH // 2 - 10}", SOFT, 1.2, m="soft")
d.t(AX + 12, 128, "더 드러남 ↓", 11, SOFT, KR, "start")

for i, (mode, a, b, c, focal) in enumerate(ROWS):
    cy = ROW_Y0 + i * STRIDE
    d.t(AX + 20, cy + 5, mode, 14, ACC if focal else INFO, MONO, "start", 600)
    cell(CX[0], cy, BW[0], a[0], a[1], INFO)
    if b is None:
        # none — 길이 끊겨 있다
        d.path(f"M {CX[0] + BW[0] // 2 + 8} {cy} L {CX[2] - BW[2] // 2 - 10} {cy}", SOFT, 1.2, dash="3 6")
        d.t(CX[1], cy - 10, "길이 없음", 11, SOFT, KR)
    else:
        cell(CX[1], cy, BW[1], b[0], b[1])
        d.path(f"M {CX[0] + BW[0] // 2 + 8} {cy} L {CX[1] - BW[1] // 2 - 10} {cy}", MUTED, 1.4, m="ar")
        d.path(f"M {CX[1] + BW[1] // 2 + 8} {cy} L {CX[2] - BW[2] // 2 - 10} {cy}",
               ACC if focal else MUTED, 1.4, m="acc" if focal else "ar")
    cell(CX[2], cy, BW[2], c[0], c[1], None if not focal else ACC, focal=focal)

# overlay 와 user-defined bridge 가 빠진 이유는 본문 §1 의 표가 맡는다
d.legend(ROW_Y0 + 4 * STRIDE + BH // 2 + 28, [("컨테이너가 갖는 인터페이스", INFO), ("격리를 내주는 끝", ACC)])
d.save("03-02.isolation-spectrum.svg")
print("ok isolation-spectrum")
