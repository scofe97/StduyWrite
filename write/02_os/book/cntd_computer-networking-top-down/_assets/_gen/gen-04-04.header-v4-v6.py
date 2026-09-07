# 타입 스펙: type-bar — 길이 = 헤더 바이트 수. 두 프로토콜의 헤더 예산 비교.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §4.3.1 Figure 4.17 · §4.3.4 Figure 4.26
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, BAD, KR, MONO

W, H = 960, 500
d = D(W, H, "HEADER BUDGET · IPV4 20B vs IPV6 40B",
      "주소는 네 배, 헤더는 두 배",
      "IPv4 20바이트와 IPv6 40바이트 헤더를 필드 묶음별 길이로 비교한 막대. IPv6 는 제어 정보 6바이트를 버리고 주소를 8바이트에서 32바이트로 늘렸다.",
      "길이 = 바이트 수 · 같은 눈금으로 두 헤더를 나란히 놓았습니다")

X0, PX = 180, 18.0                    # 1바이트 = 18px, 40바이트 = 720px
BH = 60
Y4, Y6 = 150, 280

# 눈금
for b in (0, 10, 20, 30, 40):
    x = X0 + b * PX
    d.line(x, 138, x, 356, RULE, 0.8, "3 6")
    d.t(x, 376, f"{b} B", 10, SOFT, MONO)

def bars(y, segs):
    x = X0
    for name, nb, kind in segs:
        w = nb * PX
        c = {"keep": INK, "drop": BAD, "addr": ACC}[kind]
        op = {"keep": "12", "drop": "18", "addr": "1E"}[kind]
        sw = {"keep": 1.0, "drop": 1.4, "addr": 1.4}[kind]
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{BH}" rx="3" '
                   f'fill="{c}{op}" stroke="{c}" stroke-width="{sw}"/>')
        d.t(x + w / 2, y + 26, name, 11, c if kind != "keep" else INK, KR)
        d.t(x + w / 2, y + 45, f"{nb} B", 12, MUTED, MONO)
        x += w
    return x

d.t(168, Y4 + 26, "IPv4", 15, INK, MONO, "end", 600)
d.t(168, Y4 + 45, "20 바이트", 11, MUTED, KR, "end")
bars(Y4, [("유지된 제어", 6, "keep"), ("IPv6 가 버림", 6, "drop"),
          ("출발지", 4, "addr"), ("목적지", 4, "addr")])

d.t(168, Y6 + 26, "IPv6", 15, INK, MONO, "end", 600)
d.t(168, Y6 + 45, "40 바이트", 11, MUTED, KR, "end")
bars(Y6, [("제어", 8, "keep"), ("출발지 주소", 16, "addr"), ("목적지 주소", 16, "addr")])

# 버린 6바이트가 무엇인지
d.t(410, 236, "버린 6바이트 = 식별자 2 · 플래그와 오프셋 2 · 헤더 체크섬 2", 11, BAD, KR, "start")

# IPv6 주소 몫
AX0, AX1 = X0 + 8 * PX, X0 + 40 * PX
d.path(f"M {AX0} 272 L {AX0} 264 L {AX1} 264 L {AX1} 272", ACC, 1.2)
d.t((AX0 + AX1) / 2, 258, "주소 32바이트 = 헤더의 80%", 11, ACC, KR)

d.t(180, 402, "IPv4 의 제어 정보 12바이트 가운데 절반이 사라졌고, 그 자리를 주소가 채웠습니다. "
               "헤더가 고정 길이가 된 것도 여기서 나옵니다.", 11, MUTED, KR, "start")

d.legend(424, [("주소", ACC), ("IPv6 가 버린 필드", BAD), ("양쪽이 함께 가진 제어", INK)])
d.t(920, 446, "LENGTH = HEADER BYTES · RFC 791 / RFC 8200", 8, SOFT, MONO, "end")

out = pathlib.Path(__file__).resolve().parent.parent / "04-04.header-v4-v6.svg"
d.save(out)
print("IPv4", 6 + 6 + 4 + 4, "B · IPv6", 8 + 16 + 16, "B →", out)
