# 타입 스펙: type-sequence — 클라이언트 ARP 질의 → 리스 쥔 노드 ARP 응답 → HTTP 트래픽 → 장애 → 리스 이전 → 새 노드 Gratuitous ARP
# 사실 출처: 추출본 cil10.txt 줄 119-148, 238-245, 263-270, 296-338, 421-477 / docs.cilium.io v1.20 network/l2-announcements/
import sys
sys.path.insert(0, ".")
from dd import D, Seq, ACC, OK, WARN, INFO, BAD, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO


def _kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO


class SeqKR(Seq):
    def lanes(s, names, xs, y0=104, lane_w=196):
        s.LX = {}
        for (nm, sub), x in zip(names, xs):
            s.LX[nm] = x
            s.box(x - lane_w / 2, y0, lane_w, 44, PAPER2, RULE, 1.0)
            s.t(x, y0 + 20, nm, 12, INK, _kr(nm), "middle", 600)
            s.t(x, y0 + 37, sub, 11, MUTED, MONO)
        s.lane_top = y0 + 44

    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]
        dr = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dr} {y} L {x2 - 12 * dr} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 9, label, 12, c, _kr(label), "middle", 600)
        if sub:
            s.t(mx, y + 17, sub, 11, MUTED, _kr(sub))

    def state(s, a, txt, y, c):
        x = s.LX[a]
        w = len(txt) * 7.2 + 18
        s.o.append(f'<rect x="{x - w / 2}" y="{y - 10}" width="{w}" height="20" rx="4" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
        s.t(x, y + 4, txt, 11, c, _kr(txt))


W, H = 920, 580
d = SeqKR(W, H, "CILIUM UP AND RUNNING · 10-01", "L2 Announcements 동작과 장애 복구",
          "선출 노드가 ARP 에 응답하고 장애 시 새 리더가 Gratuitous ARP 로 잇습니다",
          "kind 클러스터 · 172.18.0.0/16 망")

C, W2, W1 = "client (netshoot)", "kind-worker2 (초기 리더)", "kind-worker (새 리더)"
d.lanes([(C, "172.18.0.5"), (W2, "ea:f5:fb:51:a1:17"), (W1, "대기 · 이전")],
        [150, 470, 770], lane_w=190)
d.rails(510)

# 1. 정상 흐름
d.msg(C, W2, "ARP Request", 176, INFO, "info", sub="who-has 172.18.255.200")
d.msg(W2, C, "ARP Reply", 218, OK, "ok", sub="172.18.255.200 is-at ea:f5:fb:51:a1:17")
d.msg(C, W2, "HTTP GET", 262, ACC, "acc", sub="TCP 80 포트 요청")
d.msg(W2, C, "HTTP 200 OK", 300, OK, "ok", dash="4 4", sub="It works! 응답")

# 2. 노드 장애 경계선
d.line(24, 332, 460 - 110, 332, RULE, 0.8, "4 6")
d.line(460 + 110, 332, W - 24, 332, RULE, 0.8, "4 6")
d.chip(460, 332, "docker stop kind-worker2", BAD, size=11)

# 3. 타임아웃과 이전
d.msg(C, W2, "curl 타임아웃", 374, WARN, "warn", dash="3 3", sub="5001ms 패킷 블랙홀")
d.state(W1, "리스 획득 · 새 리더", 412, ACC)
d.msg(W1, C, "Gratuitous ARP", 448, OK, "ok", sub="새 MAC 브로드캐스트")
d.msg(C, W1, "HTTP GET 재개", 488, ACC, "acc", sub="HTTP 200 OK 복구")

d.legend(534, [("정상 통신", OK), ("ARP 질의", INFO), ("HTTP 트래픽", ACC), ("장애 발생", BAD), ("타임아웃", WARN)])
d.save("10-01.chapter-overview.svg")
