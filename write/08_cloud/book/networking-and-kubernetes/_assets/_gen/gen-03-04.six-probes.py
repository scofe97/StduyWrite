# 03-04.six-probes — 같은 컨테이너를 두 자리에서 셋씩 두드리면 결과가 갈린다
# 본문 요구: §4 는 "부르는 자리마다 서 있는 네트워크 스택이 다르기 때문"이라고 원인을
#           자리에 돌린다. 그러면 그림도 자리별로 묶여야 한다 — 주소별이 아니라.
# 타입 스펙: type-swimlane.md — 레인 = 두드리는 주체(그 주체가 선 네트워크 스택).
#           레인 안 칸이 그 자리에서 친 명령이고, 오른쪽 끝 결과가 레인마다 갈린다.
#           레인을 가로지르는 화살표가 없는 대신, 같은 열의 결과가 다르다는 것이 요점이다.
# 좌표: Layout conventions 타입이라 공식이 없다. 레인 높이 152, 칸 stride 296 하나로 고정.
import ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 600
LANE_X, LANE_W, LANE_H = 24, 952, 152
LANE_Y = [112, 288]
BW, BH, STRIDE = 264, 72, 296
CX = [216 + i * STRIDE for i in range(3)]

d = D(W, H, "SIX PROBES · SAME CONTAINER, TWO VANTAGE POINTS",
      "여섯 방향 — 어디서 부르느냐가 결과를 정한다",
      "포트 매핑된 컨테이너를 호스트 스택과 다른 컨테이너 스택에서 각각 세 번씩 두드린 결과. "
      "안에서는 컨테이너 포트만, 밖에서는 호스트 포트만 통한다는 규칙이 레인별로 드러난다.",
      lead="레인 = 두드린 자리(그 자리가 선 네트워크 스택) · exit 7 은 거부이고 도달했다는 증거입니다")


def lane(y, name, sub, c):
    d.box(LANE_X, y, LANE_W, LANE_H, PAPER2, RULE, 1.0, 8)
    d.o.append(f'<rect x="{LANE_X}" y="{y}" width="4" height="{LANE_H}" rx="2" fill="{c}"/>')
    d.t(LANE_X + 18, y + 26, name, 12, c, KR, "start", 600)
    d.t(LANE_X + 18, y + 46, sub, 11, SOFT, MONO, "start")


def cell(cx, y, addr, verdict, why, c, focal=False):
    cy = y + LANE_H // 2 + 14
    x = cx - BW // 2
    if focal:
        d.o.append(f'<rect x="{x}" y="{cy-BH//2}" width="{BW}" height="{BH}" rx="6" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
        tc = ACC
    else:
        d.box(x, cy - BH // 2, BW, BH, PAPER, c, 1.2, 6)
        tc = c
    d.t(x + 16, cy - 14, ddx.fit(addr, 12, BW - 110, addr), 12, INK, MONO, "start", 600)
    d.t(x + BW - 16, cy - 14, verdict, 12, tc, MONO, "end", 600)
    d.t(x + 16, cy + 10, ddx.fit(why, 11, BW - 32, why), 11, MUTED, KR, "start")


lane(LANE_Y[0], "호스트 스택에서", "ubuntu · 192.168.139.208", INFO)
cell(CX[0], LANE_Y[0], "172.17.0.4:8080", "200", "docker0 대역 경로가 있다", OK)
cell(CX[1], LANE_Y[0], "127.0.0.1:80", "200", "docker-proxy 가 듣고 있다", OK)
cell(CX[2], LANE_Y[0], "127.0.0.1:8080", "exit 7", "호스트에 8080 을 잡은 놈이 없다", BAD)

lane(LANE_Y[1], "다른 컨테이너 스택에서", "dnsutils · nsenter -n", OK)
cell(CX[0], LANE_Y[1], "172.17.0.4:8080", "200", "같은 브리지 · 직접 간다", OK)
cell(CX[1], LANE_Y[1], "172.17.0.4:80", "exit 7", "80 은 호스트 경계에만 있다", BAD)
cell(CX[2], LANE_Y[1], "localhost:8080", "exit 7", "자기 스택 안에는 아무도 없다", BAD, focal=True)

d.t(24, LANE_Y[1] + LANE_H + 40,
    "같은 열을 세로로 견주면 규칙이 보입니다. 가운데 열은 위아래가 정반대이고, 그 이유가 포트 매핑이 놓인 자리입니다.",
    12, MUTED, KR, "start")
d.t(24, LANE_Y[1] + LANE_H + 64,
    "오른쪽 아래 칸이 Pod 로 이어집니다. Pod 안 컨테이너들은 네임스페이스를 공유해 이 벽을 일부러 없앤 구조입니다.",
    12, ACC, KR, "start")
d.legend(LANE_Y[1] + LANE_H + 88, [("Pod 로 이어지는 자리", ACC), ("성공", OK), ("거부", BAD), ("호스트 스택", INFO)])
d.save("03-04.six-probes.svg")
print("ok six-probes")
