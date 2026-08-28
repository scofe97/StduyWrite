# 02-02.conntrack-return-path — 왕복을 그려야 "역방향"이 무엇의 역인지 보인다
# 본문 요구: "응답은 같은 길을 거꾸로 오지만 규칙을 다시 평가하지 않습니다."
#            + "역방향 기대 튜플은 DNAT 결과를 뒤집은 것"
#            + "KUBE-SVC 체인의 확률 규칙은 이 과정에서 한 번도 평가되지 않습니다."
# 타입 스펙: type-sequence.md — 참여자 셋의 레인과 시간축 왕복. 규칙을 보는 구간과
#           안 보는 구간이 시간축에서 갈리는 것이 이 도식의 주장이라, 조회 한 자리에만 focal.
# 2026-08-28 재작성: 앞 판(type-process)은 응답 쪽 네 칸만 담아 요청 경로가 그림에 없었다.
#           "역방향"에 대응하는 원방향이 화면에 없으니 그 말이 가리키는 것이 안 보였다
#           (학습자 피드백). 왕복 여섯 걸음으로 바꾸고 conntrack 항목을 아래 띠로 뺀다.
# 좌표: Layout conventions 타입이라 공식이 없다 — 메시지 stride 64, 전부 4의 배수.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 808
d = D(W, H, "CONNTRACK · ONE ENTRY, TWO DIRECTIONS",
      "규칙을 보는 것은 첫 패킷뿐 — 응답은 conntrack 항목 하나를 따라 되돌아온다",
      "위에서 아래로 시간이 흐른다. 1~3 이 요청, 4~6 이 응답이다. "
      "확률 규칙을 평가하는 것은 2 한 번뿐이고, 5 는 규칙 대신 아래 띠의 항목을 읽는다.",
      lead="아래로 갈수록 시간 · 1~3 요청 · 4~6 응답 · 규칙을 보는 것은 2 한 번뿐")

LX = {"cli": 160, "node": 500, "be": 840}
LANE_W, LANE_Y = 280, 108
RAIL_TOP, RAIL_BOT = LANE_Y + 44 + 8, 560
Y0, STRIDE = 208, 64


def lane(key, name, sub):
    x = LX[key]
    d.box(x - LANE_W // 2, LANE_Y, LANE_W, 44, PAPER2, RULE, 1.0)
    d.t(x, LANE_Y + 20, name, 12, INK, KR, "middle", 600)
    d.t(x, LANE_Y + 37, sub, 11, MUTED, MONO)


def step(n, y, c=MUTED):
    # x=92 는 대괄호 라벨(요청·응답)이 서는 42~64 를 비켜 둔 자리다 — 44 에 두면 겹친다
    d.chip(92, y, str(n), c)


def msg(a, b, label, y, sub, c=MUTED, mk="ar"):
    x1, x2 = LX[a], LX[b]
    sign = 1 if x2 > x1 else -1
    d.path(f"M {x1 + 12 * sign} {y} L {x2 - 14 * sign} {y}", c, 1.6, m=mk)
    mx = (x1 + x2) // 2
    d.t(mx, y - 10, label, 12, c, MONO, "middle", 600)
    d.t(mx, y + 18, sub, 11, MUTED, KR)


def selfmsg(key, label, y, sub, c=MUTED):
    x = LX[key]
    d.path(f"M {x + 12} {y - 14} L {x + 64} {y - 14} L {x + 64} {y + 14} L {x + 14} {y + 14}", c, 1.5, m="ar")
    d.t(x + 76, y - 8, label, 12, c, MONO, "start", 600)
    d.t(x + 76, y + 12, sub, 11, MUTED, KR, "start")


lane("cli", "클라이언트 Pod", "10.244.1.11:43346")
lane("node", "노드 커널", "nat + conntrack")
lane("be", "백엔드 Pod", "10.244.1.66:8080")
for x in LX.values():
    d.line(x, RAIL_TOP, x, RAIL_BOT, RULE, 1.0, "3 6")

# ── 요청 — 규칙을 보는 구간 ────────────────────────────────────────────────
ddx.bracket(d, 20, Y0 - 24, Y0 + STRIDE * 2 + 24, "요청", INFO)
step(1, Y0, INFO)
msg("cli", "node", "dst 10.96.192.224:8080", Y0, "Service 주소로 보낸 첫 패킷", INFO, mk="info")
step(2, Y0 + STRIDE, INFO)
selfmsg("node", "KUBE-SVC 확률 → -j DNAT", Y0 + STRIDE, "이때 conntrack 항목이 만들어진다", INFO)
step(3, Y0 + STRIDE * 2, INFO)
msg("node", "be", "dst 10.244.1.66:8080", Y0 + STRIDE * 2, "바뀐 목적지로 도착한다", INFO, mk="info")

# ── 응답 — 규칙을 한 줄도 안 보는 구간 ─────────────────────────────────────
ddx.bracket(d, 20, Y0 + STRIDE * 3 - 24, Y0 + STRIDE * 5 + 24, "응답", ACC)
step(4, Y0 + STRIDE * 3)
msg("be", "node", "src 10.244.1.66:8080", Y0 + STRIDE * 3, "Pod 가 자기 주소로 응답한다")
step(5, Y0 + STRIDE * 4, ACC)
selfmsg("node", "conntrack 조회 → 역-DNAT", Y0 + STRIDE * 4,
        "규칙은 한 줄도 안 본다 — 항목이 목적지를 되돌린다", ACC)
step(6, Y0 + STRIDE * 5, ACC)
msg("node", "cli", "src 10.96.192.224:8080", Y0 + STRIDE * 5,
    "보낸 주소에서 온 것으로 보여야 소켓이 받는다", ACC, mk="acc")

# ── conntrack 항목 하나 ────────────────────────────────────────────────────
ddx.band(d, 592, 720, "conntrack 항목 하나 — 2 에서 만들어져 5 에서 읽힌다 (kind 실측)")
for i, (title, tup, note, c) in enumerate(
        (("원방향 튜플", "src=10.244.1.11:43346  dst=10.96.192.224:8080",
          "클라이언트가 보낸 그대로", MUTED),
         ("역방향 기대 튜플", "src=10.244.1.66:8080  dst=10.244.1.11:43346",
          "DNAT 결과를 뒤집어 미리 적어 둔 것", ACC))):
    x = 44 + i * 464
    d.box(x, 632, 448, 72, PAPER2, c, 1.1, 6)
    d.t(x + 20, 656, title, 12, c, KR, "start", 600)
    d.t(x + 20, 676, ddx.fit(tup, 11, 408, tup), 11, MUTED, MONO, "start")
    d.t(x + 20, 694, note, 10, SOFT, KR, "start")

d.t(36, 748, "응답이 역방향 기대 튜플과 맞으면 커널이 출발지를 되돌린다 — 확률 규칙은 연결 수명 동안 다시 평가되지 않는다",
     12, MUTED, KR, "start")
d.legend(764, [("요청 — 규칙을 보는 구간", INFO), ("응답 — 항목만 따라가는 구간", ACC)])
d.save("02-02.conntrack-return-path.svg")
print("ok conntrack-return-path")
