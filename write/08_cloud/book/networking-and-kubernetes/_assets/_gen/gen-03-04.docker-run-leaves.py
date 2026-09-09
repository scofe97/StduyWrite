# 03-04.docker-run-leaves — docker run 한 줄이 어디에 무엇을 남기는가
# 본문 요구: §2 는 "자동으로 됐다고 해서 없어진 것은 아니다 — 정상일 때 그 셋이 호스트
#           어디에 어떤 모양으로 남는지를 먼저 봐 둬야 한다"로 절을 연다. 남은 것이
#           어느 네임스페이스에 속하는지가 요점이라 소속을 보이는 형태가 필요하다.
# 타입 스펙: type-nested.md 의 경계 링 — 링 하나가 네트워크 네임스페이스 하나이고,
#           그 안에 든 것이 그 스택에 속한 것이다. veth 쌍만 두 링을 가로지른다.
# 좌표: Layout conventions 타입이라 공식이 없다. 링 둘을 같은 y 에 두고 폭만 다르게,
#       안쪽 항목은 stride 44 하나로 쌓는다. 전부 4의 배수.
import ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 580
RING_Y, RING_H = 116, 312
HOST = (24, 560)          # x, w
CTR = (632, 344)
ITEM_H, STRIDE = 40, 48

d = D(W, H, "DOCKER RUN · WHAT IT LEAVES BEHIND",
      "docker run 한 줄이 남긴 것 — 어느 스택에 무엇이 있나",
      "컨테이너 하나를 띄운 뒤 호스트에 남는 배선과 컨테이너 안에 생긴 것을 네임스페이스별로 나눈 그림. "
      "veth 쌍만 두 네임스페이스를 가로지르고, 나머지는 각자 한쪽에만 존재한다.",
      lead="링 하나가 네트워크 네임스페이스 하나입니다 · 포트 매핑과 NAT 은 호스트 쪽에만 있습니다")


def ring(x, w, label, sub, c):
    d.o.append(f'<rect x="{x}" y="{RING_Y}" width="{w}" height="{RING_H}" rx="10" '
               f'fill="{c}06" stroke="{c}" stroke-width="1.2" stroke-dasharray="7 6"/>')
    d.t(x + 16, RING_Y - 14, label, 12, c, KR, "start", 600)
    d.t(x + 16 + 8 * len(label) + 96, RING_Y - 14, sub, 11, SOFT, MONO, "start")


def item(x, w, i, name, sub, c=None):
    y = RING_Y + 40 + i * STRIDE
    d.box(x + 16, y, w - 32, ITEM_H, PAPER2, c or RULE, 1.1, 6)
    d.t(x + 32, y + 17, ddx.fit(name, 12, w - 152, name), 12, c or INK,
        MONO if all(ord(ch) < 128 for ch in name) else KR, "start", 600)
    d.t(x + w - 32, y + 17, ddx.fit(sub, 11, w - 240, sub), 11, MUTED, KR, "end")
    return y


ring(HOST[0], HOST[1], "호스트 네트워크 네임스페이스", "netns 4026532281", INFO)
ring(CTR[0], CTR[1], "컨테이너 네임스페이스", "netns 4026532947", OK)

item(*HOST, 0, "docker0", "브리지 · 172.17.0.1/16", INFO)
YV = item(*HOST, 1, "vethe6c0259@if2", "veth 반쪽 · master docker0", ACC)
item(*HOST, 2, "172.17.0.0/16 dev docker0", "라우팅 항목", INFO)
item(*HOST, 3, "MASQUERADE  out !docker0", "나갈 때만 출발지 위장", WARN)
# -p 를 붙인 컨테이너가 있어야 생기는 둘 — 이 시점(§2 busybox)에는 아직 없다
item(*HOST, 4, "DNAT · docker-proxy", "포트 매핑을 붙이면 여기 생긴다 — §4", SOFT)

YE = item(*CTR, 1, "eth0@if4", "172.17.0.2/16", ACC)
item(*CTR, 2, "default via 172.17.0.1", "기본 경로", OK)
item(*CTR, 3, "lo", "자기 안에서만", OK)

# veth 쌍만 두 링을 가로지른다 — 같은 y 로 맞춰 한 줄로 잇는다
d.path(f"M {HOST[0]+HOST[1]-16} {YV+ITEM_H//2} L {CTR[0]+16} {YE+ITEM_H//2}", ACC, 1.6, m="acc")
d.t((HOST[0] + HOST[1] + CTR[0]) // 2, YV + ITEM_H // 2 - 12, "한 쌍", 11, ACC, KR)

d.t(24, RING_Y + RING_H + 40,
    "포트 매핑과 NAT 은 전부 왼쪽 링 안에 생깁니다. 그래서 컨테이너끼리 주고받는 트래픽은 그것들을 지나지 않습니다.",
    12, MUTED, KR, "start")
d.legend(RING_Y + RING_H + 68,
         [("두 스택을 잇는 것", ACC), ("호스트 쪽 배선", INFO), ("호스트 쪽 변환", WARN), ("컨테이너 쪽", OK)])
d.save("03-04.docker-run-leaves.svg")
print("ok docker-run-leaves")
