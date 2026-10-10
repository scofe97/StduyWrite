# 타입 스펙: type-sequence — WireGuard 공개키 생성, CiliumNode 주석 등록, 피어 노드 공개키 발견 및 피어 설정 절차.
# 사실 출처: Cilium Up and Running 14장 cil14.txt 줄 227-238(Encryption and Authentication), 297-324(CiliumNode wg-pub-key 주석) / docs.cilium.io v1.20 security/network/encryption-wireguard/
import sys
sys.path.insert(0, ".")
from dd import D, Seq, ACC, OK, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

def _kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO

class SeqKR(Seq):
    def lanes(s, names, y0=104, lane_w=200):
        s.LX = {}; n = len(names)
        span = (s.w - 48 - 24) - lane_w
        for i, (nm, sub) in enumerate(names):
            x = 24 + lane_w / 2 + (span * i / (n - 1) if n > 1 else 0)
            s.LX[nm] = x
            s.box(x - lane_w / 2, y0, lane_w, 44, PAPER2, RULE, 1.0)
            s.t(x, y0 + 20, nm, 12, INK, _kr(nm), "middle", 600)
            s.t(x, y0 + 37, sub, 11, MUTED, _kr(sub))
        s.lane_top = y0 + 44
        return s.LX
    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]; d_ = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * d_} {y} L {x2 - 12 * d_} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 9, label, 12 if _kr(label) == KR else 11, c, _kr(label), "middle", 600)
        if sub: s.t(mx, y + 17, sub, 12 if _kr(sub) == KR else 11, MUTED, _kr(sub))
    def selfmsg(s, a, label, y, c=MUTED, sub=None):
        x = s.LX[a]
        s.path(f"M {x + 10} {y - 10} L {x + 52} {y - 10} L {x + 52} {y + 10} L {x + 13} {y + 10}", c, 1.4, m="ar")
        s.t(x + 62, y - 4, label, 11, c, _kr(label), "start")
        if sub: s.t(x + 62, y + 13, sub, 11, MUTED, _kr(sub), "start")
    def selfmsg_left(s, a, label, y, c=MUTED, sub=None):
        x = s.LX[a]
        s.path(f"M {x - 10} {y - 10} L {x - 52} {y - 10} L {x - 52} {y + 10} L {x - 13} {y + 10}", c, 1.4, m="ar")
        s.t(x - 62, y - 4, label, 11, c, _kr(label), "end")
        if sub: s.t(x - 62, y + 13, sub, 11, MUTED, _kr(sub), "end")

W, H = 920, 520
d = SeqKR(W, H, "CILIUM UP AND RUNNING · 14-01 §4", "WireGuard 노드 인증과 피어 등록",
          "Kubernetes API 를 거쳐 공개키를 교환하고 WireGuard 피어를 맺는다",
          "Kubernetes API 를 거쳐 공개키를 교환하고 WireGuard 피어를 맺는다")

L = d.lanes([("노드 A 에이전트", "cilium-agent"), ("Kubernetes API", "kube-apiserver"),
             ("노드 B 에이전트", "cilium-agent")], y0=100, lane_w=190)
d.rails(432)

# 1. 노드 A 키쌍 생성
d.selfmsg("노드 A 에이전트", "WireGuard 키쌍 생성", 170, INFO, sub="cilium_wg0 장치")

# 2. 노드 A -> API 주석 등록
d.msg("노드 A 에이전트", "Kubernetes API", "CiliumNode 주석 등록", 218, INFO, "info", sub="network.cilium.io/wg-pub-key")

# 3. API -> 노드 B 주석 전파
d.msg("Kubernetes API", "노드 B 에이전트", "노드 A 공개키 수신", 264, INFO, "info", sub="Watch CiliumNode")

# 4. 노드 B 피어 설정 (왼쪽 방향으로 꺾어 잘림 방지)
d.selfmsg_left("노드 B 에이전트", "피어 등록 (노드 A)", 310, OK, sub="AllowedIPs: 노드 A IP (+ 그 노드 엔드포인트 IP)")

# 5. 구분선
d.line(24, 350, W / 2 - 70, 350, RULE, 0.8, "4 6")
d.line(W / 2 + 70, 350, W - 48, 350, RULE, 0.8, "4 6")
d.chip(W / 2, 350, "키 교환 완료 후 암호화", SOFT, size=11)

# 6. 상호 암호화 터널 통신
d.msg("노드 A 에이전트", "노드 B 에이전트", "UDP 51871 암호화 전송", 394, ACC, "acc", sub="서명 검증 통과 트래픽만 수락")

LEG_Y = 466
d.legend(LEG_Y, [("Kubernetes API 제어면", INFO), ("WireGuard 피어 설정", OK), ("암호화 데이터패스", ACC)])
d.save("14-01.encryption-auth.svg")
