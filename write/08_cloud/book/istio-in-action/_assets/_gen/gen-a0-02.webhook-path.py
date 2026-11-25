# a0-02 §3 파드 하나가 만들어지는 동안.
# 값 근거(본문 §3 · 부록 B.1.2):
#   - kubectl -> API 서버 -> MutatingWebhookConfiguration(istio-sidecar-injector) -> istiod -> etcd 저장.
#   - 네임스페이스 라벨 istio-injection=enabled 가 맞을 때만 웹훅이 끼어든다.
#   - 반환 patch 는 istio-proxy + istio-init 을 추가한다(책 출력 기준 이미지는 proxyv2:1.13.0).
# 타입 스펙: type-sequence — 참여자 사이 시간 순 주고받기. Seq 서브클래스로 한글/영문 폰트 분리.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, INK, INFO, PAPER, PAPER2, RULE, KR, MONO

def fam(t):
    return KR if any("가" <= c <= "힣" for c in str(t)) else MONO

class KSeq(Seq):
    def lanes(s, names, y0=104, lane_w=204):
        s.LX = {}; n = len(names)
        span = (s.w - 48) - lane_w
        for i, (nm, sub) in enumerate(names):
            x = 24 + lane_w / 2 + (span * i / (n - 1) if n > 1 else 0)
            s.LX[nm] = x
            s.box(x - lane_w / 2, y0, lane_w, 48, PAPER2, RULE, 1.0)
            s.t(x, y0 + 20, nm, 13, INK, fam(nm), "middle", 600)
            s.t(x, y0 + 40, sub, 12, MUTED, fam(sub))
        s.lane_top = y0 + 48
        return s.LX
    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]; d = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * d} {y} L {x2 - 12 * d} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        lw = len(label) * (13.5 if fam(label) == KR else 8.2) + 12
        s.o.append(f'<rect x="{mx - lw / 2}" y="{y - 24}" width="{lw}" height="18" fill="{PAPER}"/>')
        s.t(mx, y - 9, label, 13, c, fam(label), "middle", 600)
        if sub:
            w = len(sub) * (12.5 if fam(sub) == KR else 7.4) + 12
            s.o.append(f'<rect x="{mx - w / 2}" y="{y + 6}" width="{w}" height="17" fill="{PAPER}"/>')
            s.t(mx, y + 18, sub, 12, MUTED, fam(sub))
    def selfmsg(s, a, label, y, c=MUTED, sub=None):
        x = s.LX[a]
        s.path(f"M {x + 10} {y - 10} L {x + 56} {y - 10} L {x + 56} {y + 10} L {x + 13} {y + 10}", c, 1.4, m="ar")
        s.t(x + 66, y - 4, label, 13, c, fam(label), "start", 600)
        if sub: s.t(x + 66, y + 15, sub, 12, MUTED, fam(sub), "start")
    def state(s, a, txt, y, c):
        x = s.LX[a]
        w = len(txt) * 12 + 24
        s.o.append(f'<rect x="{x - w / 2}" y="{y - 12}" width="{w}" height="24" rx="4" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
        s.t(x, y + 5, txt, 12, c, fam(txt), "middle", 600)

W, H = 960, 540
d = KSeq(W, H, "ISTIO IN ACTION · A0-02 §3",
         "부품은 데이터스토어에 저장되기 전에 끼워진다",
         "kubectl 이 올린 파드 정의가 API 서버에 닿으면, 서버는 MutatingWebhookConfiguration 을 보고 "
         "그 이벤트를 istiod 로 보낸다. 고쳐진 정의가 돌아온 뒤에야 데이터스토어에 저장된다.",
         lead="네임스페이스에 istio-injection=enabled 라벨이 없으면 가운데 웹훅 왕복이 일어나지 않습니다.")

d.lanes([("kubectl", "명세 적용"),
         ("API 서버", "저장 전 관문"),
         ("istiod", "sidecar injector"),
         ("데이터스토어", "etcd")], y0=104, lane_w=204)
d.rails(452)

d.msg("kubectl", "API 서버", "create Pod", 192, MUTED, "ar", sub="부품 없는 정의")
d.selfmsg("API 서버", "웹훅 설정 확인", 248, MUTED, sub="istio-sidecar-injector")
d.msg("API 서버", "istiod", "admission review", 316, ACC, "acc", sub="라벨이 맞을 때만 호출")
d.msg("istiod", "API 서버", "patch 반환", 374, ACC, "acc", sub="istio-proxy + istio-init")
d.msg("API 서버", "데이터스토어", "저장 완료", 432, MUTED, "ar", sub="이미 고쳐진 파드 정의")

d.state("API 서버", "저장 전", 286, INFO)

d.legend(480, [("주입이 일어나는 왕복", ACC), ("저장 전 표지", INFO)])
d.save("a0-02.webhook-path.svg")
print("ok webhook-path")
