# 타입 스펙: type-bar — 길이 = 헤더 바이트 수. 두 프로토콜의 헤더 예산 비교.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §4.3.1 Figure 4.17 · §4.3.4 Figure 4.26
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, BAD, KR, MONO

W, H = 960, 500
d = D(W, H, "HEADER BUDGET · IPV4 20B vs IPV6 40B",
      "주소는 네 배, 헤더는 두 배",
      "IPv4 20바이트와 IPv6 40바이트 헤더를 필드 묶음별 길이로 비교한 막대. IPv6 는 IPv4 제어 12바이트에서 6.5바이트(식별·플래그·오프셋·체크섬과 헤더 길이)를 버리고 흐름 레이블 2.5바이트를 더해 제어 8바이트가 되었고, 주소는 8바이트에서 32바이트로 늘렸다.",
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
bars(Y4, [("유지된 제어", 5.5, "keep"), ("IPv6 가 버림", 6.5, "drop"),
          ("출발지", 4, "addr"), ("목적지", 4, "addr")])

d.t(168, Y6 + 26, "IPv6", 15, INK, MONO, "end", 600)
d.t(168, Y6 + 45, "40 바이트", 11, MUTED, KR, "end")
bars(Y6, [("제어", 8, "keep"), ("출발지 주소", 16, "addr"), ("목적지 주소", 16, "addr")])

# 버린 6.5바이트가 무엇인지 (RFC 791 §3.1 · RFC 8200 §3 대조)
d.t(279, 236, "버린 6.5바이트 = 식별자 2 · 플래그와 오프셋 2 · 헤더 체크섬 2 · 헤더 길이(IHL) 0.5", 11, BAD, KR, "start")

# IPv6 주소 몫
AX0, AX1 = X0 + 8 * PX, X0 + 40 * PX
d.path(f"M {AX0} 272 L {AX0} 264 L {AX1} 264 L {AX1} 272", ACC, 1.2)
d.t((AX0 + AX1) / 2, 258, "주소 32바이트 = 헤더의 80%", 11, ACC, KR)

# 제어 셈: 12 − 6.5 + 2.5 = 8바이트 = 64비트 (버전 4 · 트래픽 클래스 8 · 흐름 레이블 20 · 적재량 길이 16 · 다음 헤더 8 · 홉 한도 8)
d.t(180, 402, "제어 셈 12 − 6.5 + 흐름 레이블 2.5 = 8바이트 · 고정 길이는 옵션을 다음 헤더로 뺀 덕", 11, MUTED, KR, "start")

d.legend(424, [("주소", ACC), ("IPv6 가 버린 필드", BAD), ("제어 필드 · IPv6 쪽은 흐름 레이블 포함", INK)])
d.t(920, 446, "LENGTH = HEADER BYTES · RFC 791 / RFC 8200", 8, SOFT, MONO, "end")

out = pathlib.Path(__file__).resolve().parent.parent / "04-04.header-v4-v6.svg"
d.save(out)
assert 12 - 6.5 + 20 / 8 == 8 and 4 + 8 + 20 + 16 + 8 + 8 == 64
print("IPv4", 5.5 + 6.5 + 4 + 4, "B · IPv6", 8 + 16 + 16, "B →", out)
