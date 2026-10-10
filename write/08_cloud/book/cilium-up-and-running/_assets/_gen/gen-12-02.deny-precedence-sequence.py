# 타입 스펙: type-sequence — 클라이언트 Pod 의 트래픽에 allow 와 deny 규칙이 동시에 매칭될 때 eBPF 데이터패스가 deny 를 우선하여 패킷을 드롭하는 시퀀스.
# 사실 출처: Cilium Up and Running 12장 cil12.txt 줄 1065-1090(kube-api-deny.yaml, matchExpressions NotIn kube-system, toEntities kube-apiserver), 줄 1100-1125(순서 없음, deny 우선순위)
import sys
sys.path.insert(0, ".")
from dd import D, Seq, ACC, BAD, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO


def _kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO


class SeqKR(Seq):
    """한글 라벨을 한글 스택으로, 글자는 12px 로 내보내는 Seq."""
    def lanes(s, names, xs, y0=104, lane_w=200):
        s.LX = {}
        for (nm, sub), x in zip(names, xs):
            s.LX[nm] = x
            s.box(x - lane_w / 2, y0, lane_w, 44, PAPER2, RULE, 1.0)
            s.t(x, y0 + 20, nm, 12, INK, _kr(nm), "middle", 600)
            s.t(x, y0 + 37, sub, 11, MUTED, _kr(sub))
        s.lane_top = y0 + 44

    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]
        dr = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dr} {y} L {x2 - 12 * dr} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 9, label, 12, c, _kr(label), "middle", 600)
        if sub:
            s.t(mx, y + 18, sub, 11, MUTED, _kr(sub))

    def state(s, a, txt, y, c):
        x = s.LX[a]
        w = len(txt) * 7.4 + 24
        s.o.append(f'<rect x="{x - w / 2}" y="{y - 10}" width="{w}" height="20" rx="4" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
        s.t(x, y + 4, txt, 11, c, _kr(txt))


W, H = 920, 520
d = SeqKR(W, H, "CILIUM UP AND RUNNING · 12-02 §5", "allow 와 deny 규칙 충돌 시 우선순위 판정",
          "동일 트래픽에 allow 와 deny 가 함께 걸려도 deny 가 예외 없이 우선 승리한다",
          "동일 트래픽에 allow 와 deny 가 함께 걸려도 deny 가 예외 없이 우선 승리한다")

A = "클라이언트 Pod"
B = "노드 eBPF 데이터패스"
C = "kube-apiserver"

d.lanes([
    (A, "default 네임스페이스"),
    (B, "정책 맵 조회"),
    (C, "kube-apiserver 엔티티")
], [140, 460, 780])
d.rails(480)

d.msg(A, B, "요청 패킷 전송", 188, MUTED, "ar", sub="TCP SYN · kube-apiserver 대상")
d.state(B, "정책 맵 동시 매칭", 240, INFO)
d.state(B, "allow 허용 vs egressDeny 거부", 280, MUTED)
d.state(B, "deny 무조건 우선 판정", 330, ACC)
d.msg(B, A, "패킷 드롭 처리", 390, BAD, "bad", dash="5 4", sub="연결 차단")
d.msg(B, C, "패킷 도달 불가", 446, MUTED, dash="3 3", sub="API 서버로 전달되지 않음")

d.save("12-02.deny-precedence-sequence.svg")
