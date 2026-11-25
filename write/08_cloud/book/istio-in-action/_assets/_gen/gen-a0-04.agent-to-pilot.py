# a0-04 §3 질의가 에이전트를 거쳐 가는 길.
# 본문(부록 D.1.2): 15004 로 온 요청은 "forwarded securely to istiod as xDS events, which is a
#       good way to verify connectivity to the control plane from the agent". 응답의
#       genericXdsConfigs 안 configStatus 가 SYNCED 면 최신이다.
# 타입 스펙: type-sequence — 참여자 사이 시간 순 주고받기. 한글은 KR 스택, 응답은 점선 화살표.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, INFO, OK, KR, MONO

def fam_of(txt):
    return KR if any("가" <= ch <= "힣" for ch in str(txt)) else MONO

class KrSeq(Seq):
    def lanes(s, names, y0=104, lane_w=228):
        s.LX = {}
        n = len(names)
        span = (s.w - 48 - 24) - lane_w
        for i, (nm, sub) in enumerate(names):
            x = 24 + lane_w / 2 + (span * i / (n - 1) if n > 1 else 0)
            s.LX[nm] = x
            s.box(x - lane_w / 2, y0, lane_w, 48, "#161B22", "rgba(191,192,192,0.22)", 1.0)
            s.t(x, y0 + 21, nm, 13, INK, KR, "middle", 600)
            s.t(x, y0 + 39, sub, 11, MUTED, fam_of(sub))
        s.lane_top = y0 + 48
        return s.LX

    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]
        d = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * d} {y} L {x2 - 12 * d} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 10, label, 13, c, fam_of(label), "middle", 600)
        if sub:
            s.t(mx, y + 18, sub, 13, MUTED, fam_of(sub))

    def state(s, a, txt, y, c):
        x = s.LX[a]
        w = sum(13 if "가" <= ch <= "힣" else 7.5 for ch in txt) + 24
        s.o.append(f'<rect x="{x - w / 2}" y="{y - 12}" width="{w}" height="24" rx="4" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
        s.t(x, y + 5, txt, 13, c, fam_of(txt), "middle", 600)

W, H = 960, 504
d = KrSeq(W, H, "ISTIO IN ACTION · A0-04 §3",
          "15004 응답이 컨트롤 플레인 연결 확인이 된다",
          "15004 로 던진 질의는 xDS 이벤트로 istiod 에 안전하게 전달된다. 이 왕복은 동기화 상태를 "
          "묻는 동시에 에이전트와 컨트롤 플레인 사이 연결이 살아 있는지 확인한다.",
          lead="노출되는 정보는 Pilot 디버그 엔드포인트의 부분집합입니다")

d.lanes([("운영자 · 도구", "kubectl exec"),
         ("에이전트", "istio-agent · localhost:15004"),
         ("istiod", "debug endpoints")], y0=104, lane_w=228)
d.rails(388)

d.msg("운영자 · 도구", "에이전트", "curl /debug/syncz", 192, MUTED, "ar", sub="프록시 안에서 호출")
d.msg("에이전트", "istiod", "xDS 이벤트 전달", 256, ACC, "acc", sub="평문 HTTP 대신 xDS")
d.msg("istiod", "에이전트", "genericXdsConfigs", 320, MUTED, "ar", dash="5 3", sub="xDS API 별 configStatus")
d.msg("에이전트", "운영자 · 도구", "SYNCED", 372, OK, "ok", dash="5 3", sub="리스너 · 라우트 · 엔드포인트 · 클러스터")

d.state("에이전트", "연결 확인됨", 416, INFO)

d.legend(452, [("xDS 안전 전달 구간", ACC), ("왕복이 입증하는 연결", INFO), ("최신 동기화 응답", OK)])
d.save("a0-04.agent-to-pilot.svg")
print("ok a0-04.agent-to-pilot")
