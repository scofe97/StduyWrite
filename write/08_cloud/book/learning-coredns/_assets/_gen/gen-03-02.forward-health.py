# 03-02 §4 — forward 플러그인이 포워더의 건강을 판정하는 상태 전이.
# 원문 근거: "sending each forwarder a recursive query for the NS records for the root every half
#            second" / "As long as a forwarder responds, even with a negative response such as
#            NXDOMAIN or a DNS error such as SERVFAIL, CoreDNS counts it as healthy" /
#            "If a forwarder fails to respond or responds with an empty reply twice in a row, it's
#            marked unhealthy" / "If for whatever reason all of the forwarders appear unhealthy,
#            CoreDNS assumes that the health-checking mechanism itself has failed and will query a
#            randomly chosen forwarder" / max_fails 기본 2, health_check 기본 0.5초.
# 타입 스펙: type-state — 주체 하나(포워더)의 상태 전이와 가드와 재시도가 논지다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, OK, BAD, KR, MONO

W, H = 940, 520
d = D(W, H, "LEARNING COREDNS · 03-02 §4",
      "포워더의 건강은 응답 여부로만 판정한다",
      "CoreDNS 는 0.5초마다 각 포워더에 루트의 NS 레코드를 재귀 질의한다. "
      "응답만 오면 그 내용이 NXDOMAIN 이든 SERVFAIL 이든 건강한 것으로 세고, 연속 두 번 응답이 없어야 죽은 것으로 본다.",
      "전부 죽어 보이면 헬스 체크 쪽을 의심합니다")

def state(x, y, w, nm, sub, color=None):
    if color:
        d.tone(x, y, w, 64, color, 8, "12", 1.4)
    else:
        d.box(x, y, w, 64, PAPER2, RULE, 1.0, 8)
    d.t(x + w / 2, y + 28, nm, 14, color or INK, KR, "middle", 600)
    d.t(x + w / 2, y + 48, sub, 12, MUTED)

d.o.append(f'<circle cx="40" cy="180" r="6" fill="{INK}"/>')
d.path("M 48 180 L 108 180", MUTED, 1.4, m="ar")

state(116, 148, 216, "건강함", "질의를 받는다", OK)
state(412, 148, 216, "실패 1회", "연속 실패를 센다")
state(412, 300, 216, "죽음", "질의에서 제외", BAD)
state(700, 148, 216, "무작위 하나에 질의", "헬스 체크를 의심", ACC)

d.path("M 332 168 L 404 168", MUTED, 1.4, m="ar")
d.t(368, 156, "무응답", 12, MUTED, KR)

d.path("M 520 148 C 520 92 224 92 224 140", MUTED, 1.4, m="ar")
d.t(372, 100, "응답이 오면 — NXDOMAIN 이나 SERVFAIL 이어도", 12, MUTED, KR)
d.t(372, 120, "건강한 것으로 되돌린다", 12, SOFT, KR)

d.path("M 520 212 L 520 292", MUTED, 1.4, m="ar")
d.t(532, 258, "연속 두 번째 실패 · max_fails 기본 2", 12, MUTED, KR, "start")

d.path("M 412 332 C 356 332 356 212 224 212", MUTED, 1.4, m="ar", dash="5 4")
d.t(272, 268, "다시 응답하면 복귀", 12, MUTED, KR)

d.path("M 632 300 C 700 300 812 268 812 220", ACC, 1.6, m="acc")
d.t(736, 296, "모든 포워더가 죽음", 12, ACC, KR)

d.t(20, 404, "헬스 체크 주기는 health_check 로, 죽음 판정 횟수는 max_fails 로 바꾼다 — 0 이면 죽었다고 표시하지 않는다", 13, MUTED, KR, "start")
d.t(20, 426, "실패로 세는 것은 응답이 아예 없거나 빈 응답이 온 경우다 — 탐색 질의는 그 포워더의 전송 방식을 그대로 탄다", 13, MUTED, KR, "start")

d.legend(446, [("질의를 받을 수 있는 상태", OK), ("제외된 상태", BAD), ("판정 자체를 못 믿는 자리", ACC)])
d.save("03-02.forward-health.svg")
