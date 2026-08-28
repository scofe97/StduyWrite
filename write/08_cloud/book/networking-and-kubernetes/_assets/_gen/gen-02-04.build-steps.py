# 02-04.build-steps — 명령 하나가 배선을 어떻게 바꾸는가
# 본문 요구: §2 는 명령과 출력을 다 싣지만 '그 사이에 무엇이 바뀌었나'는 산문에만 있다.
#           특히 "veth 를 만들면 네 끝이 전부 기본 netns 에 생겼다가 둘만 옮겨진다"는
#           전이가 도식으로 없어, 완성된 배선만 보이면 그 중간이 사라진다.
# 타입 스펙: type-state.md — 명령이 전이(입력), 상태가 변화, 상태 안의 값이 결과다.
#           세로로 쌓아 전이 옆에 명령 전문을 실을 자리를 준다.
#           coral 은 한 상태 — 경계를 넘어 목록이 갈라지는 자리.
# 주의: RULE 은 rgba() 문자열이라 f"{RULE}12" 로 투명도를 붙이면 색이 깨진다. 무채색 상태는 PAPER2 로.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 740
d = D(W, H, "BUILD STEPS · INPUT → CHANGE → RESULT",
      "명령 하나가 목록을 어떻게 바꾸는가",
      "veth 쌍을 만들면 네 끝이 전부 기본 네임스페이스에 생기고, 옮기는 명령을 친 뒤에야 둘이 경계를 넘습니다. "
      "각 상태에 적힌 값은 그 직후 ip -br link 로 실제로 본 것입니다.",
      lead="veth 는 만들 때가 아니라 옮길 때 경계를 넘는다")

SX, SW, SH = 56, 448, 104
CY = [176, 368, 560]
LX = 560

d.t(SX, 118, "결과 — 그 직후 보이는 목록", 11, SOFT, KR, "start", 600)
d.t(LX, 118, "입력 — 내가 친 명령", 11, SOFT, KR, "start", 600)

STATES = [("네임스페이스 둘", "ns1 · ns2 — 둘 다 lo 뿐", None),
          ("장치 다섯, 전부 기본 netns", "veth1 veth1-br veth2 veth2-br br0", INFO),
          ("안쪽 끝 둘이 경계를 넘음", "기본 3 · ns1 1 · ns2 1", ACC)]
for (name, obs, c), cy in zip(STATES, CY):
    if c is None:
        d.box(SX, cy - SH // 2, SW, SH, PAPER2, RULE, 1.1, 8); tc = INK
    else:
        d.o.append(f'<rect x="{SX}" y="{cy-SH//2}" width="{SW}" height="{SH}" rx="8" '
                   f'fill="{c}12" stroke="{c}" stroke-width="{1.4 if c is ACC else 1.1}"/>'); tc = c
    d.t(SX + 24, cy - 18, ddx.fit(name, 13, SW - 48, name), 13, tc, KR, "start", 600)
    d.t(SX + 24, cy + 16, ddx.fit(obs, 11, SW - 48, obs), 11, MUTED, MONO, "start")

for i in (0, 1):
    d.path(f"M {SX+SW//2} {CY[i]+SH//2} L {SX+SW//2} {CY[i+1]-SH//2-8}", MUTED, 1.5, m="ar")

AVAIL = W - LX - 48
# 첫 상태에도 그것을 만든 명령이 붙어야 입력→결과 짝이 빠짐없이 선다
d.t(LX, 168, "ip netns add ns1", 10, INK, MONO, "start")
d.t(LX, 194, "빈 네임스페이스 둘을 만든다 — 아직 장치는 없다", 12, MUTED, KR, "start")
d.path(f"M {SX+SW+16} 176 L {LX-12} 176", RULE, 1.0, dash="4 4")

G1 = [("ip link add veth1 type veth peer name veth1-br", INK, 252),
      ("ip link add br0 type bridge", INK, 276)]
for cmd, c, y in G1:
    d.t(LX, y, ddx.fit(cmd, 10, AVAIL, cmd), 10, c, MONO, "start")
d.t(LX, 302, "관 하나에 두 끝 — 둘 다 기본 netns 에 생긴다", 12, MUTED, KR, "start")
d.path(f"M {SX+SW+16} 272 L {LX-12} 272", RULE, 1.0, dash="4 4")

d.t(LX, 452, ddx.fit("ip link set veth1 netns ns1", 10, AVAIL, "move"), 10, ACC, MONO, "start")
d.t(LX, 478, "안쪽 끝만 옮긴다 — 이때 경계를 넘는다", 12, ACC, KR, "start")
d.path(f"M {SX+SW+16} 464 L {LX-12} 464", ACC, 1.2, dash="4 4")

d.t(36, 660, "만드는 명령과 옮기는 명령이 갈려 있는 것이 요점입니다. veth 쌍은 만들 때 네 끝이 다 한자리에 "
             "생기고, 옮겨야 격리가 시작됩니다.", 12, MUTED, KR, "start")
d.t(36, 682, "브리지에 물리고 주소를 붙이는 것은 이 뒤 단계입니다.", 12, MUTED, KR, "start")
d.legend(698, [("만든 직후 — 전부 한자리", INFO), ("옮긴 뒤 — 목록이 갈라진다", ACC)])
d.save("02-04.build-steps.svg")
print("ok build-steps")
