# a0-03 §6 토큰 하나가 인증서가 되기까지.
# 값 근거(본문 a0-03 §6, 원문 부록 C.2.6):
#   - 경로: /var/run/secrets/kubernetes.io/serviceaccount/ (토큰 페이로드 sub: system:serviceaccount:istioinaction:default, 본문 §6 JSON 과 같은 글자).
#   - 개인 키: 파일럿 에이전트가 시작할 때 만든다(Istio 보안 문서 Identity provisioning). 토큰은 파드 볼륨에 마운트된 파일이지 API 호출이 아니다.
#   - 다섯 걸음: 1. SA 토큰 할당 → 2. token + CSR (SAN URI = spiffe://cluster.local/ns/istioinaction/sa/default) 전송 →
#     3. Istio CA 가 TokenReview API 검증 → 4. 서명된 X.509 인증서 응답 → 5. 파일럿 에이전트가 Envoy SDS 로 전달.
# 타입 스펙: type-sequence — 참여자 사이 시간 순 주고받기가 논점이다. 레인 + 메시지, 상태는 칩으로.
#           축약: Seq 서브클래스로 한글 폰트와 크기를 분기하고, 규격과 다른 걸음(CA 의 TokenReview)에 accent 를 건다.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, INFO, PAPER2, RULE, KR, MONO

W, H = 1000, 676


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


class KrSeq(Seq):
    def lanes(s, names, y0=104, lane_w=216):
        s.LX = {}
        n = len(names)
        span = (s.w - 48 - 24) - lane_w
        for i, (nm, sub) in enumerate(names):
            x = 24 + lane_w / 2 + (span * i / (n - 1) if n > 1 else 0)
            s.LX[nm] = x
            s.box(x - lane_w / 2, y0, lane_w, 50, PAPER2, RULE, 1.0)
            s.t(x, y0 + 21, nm, 14, INK, kr(nm), "middle", 600)
            s.t(x, y0 + 41, sub, 13, MUTED, kr(sub))
        s.lane_top = y0 + 50
        return s.LX

    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]
        d_dir = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * d_dir} {y} L {x2 - 12 * d_dir} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 9, label, 13, c, kr(label), "middle", 600)
        if sub:
            s.t(mx, y + 18, sub, 13, MUTED, kr(sub))

    def selfmsg(s, a, label, y, c=MUTED, sub=None):
        x = s.LX[a]
        s.path(f"M {x + 10} {y - 10} L {x + 58} {y - 10} L {x + 58} {y + 10} L {x + 13} {y + 10}", c, 1.4, m="ar")
        s.t(x + 68, y - 4, label, 13, c, kr(label), "start", 600)
        if sub:
            s.t(x + 68, y + 16, sub, 13, MUTED, kr(sub), "start")

    def state(s, a, txt, y, c):
        x = s.LX[a]
        w = sum(13 if "가" <= ch <= "힣" else 8 for ch in txt) + 22
        s.o.append(f'<rect x="{x - w / 2}" y="{y - 12}" width="{w}" height="24" rx="4" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
        s.t(x, y + 5, txt, 13, c, kr(txt))


d = KrSeq(W, H, "ISTIO IN ACTION · A0-03 §6",
          "쿠버네티스가 준 토큰이 SPIFFE 신원이 된다",
          "파드에 마운트된 서비스 어카운트 토큰에서 시작해 에이전트가 SPIFFE ID 를 만들고 CSR 에 담는다. "
          "CA 가 토큰을 검증한 뒤 서명하고, 에이전트가 SDS 로 인증서를 프록시에 넣는다.",
          "색이 붙은 걸음이 규격과 다른 자리입니다 — 원래는 에이전트의 몫입니다")

d.lanes([("쿠버네티스", "API 서버"),
         ("파일럿 에이전트", "Workload Endpoint"),
         ("Istio CA", "Workload API"),
         ("Envoy 프록시", "service proxy")], y0=104, lane_w=216)
d.rails(540)

d.msg("쿠버네티스", "파일럿 에이전트", "1. 토큰 파일 마운트", 200, MUTED, "ar", sub="sub: system:serviceaccount:istioinaction:default")
d.selfmsg("파일럿 에이전트", "개인 키 · CSR 조립", 262, MUTED, sub="SAN URI 확장 생성")
d.msg("파일럿 에이전트", "Istio CA", "2. token + CSR", 328, MUTED, "ar", sub="SAN URI: .../sa/default")
d.msg("Istio CA", "쿠버네티스", "3. TokenReview API", 392, ACC, "acc", sub="규격상 에이전트 몫이었다")
d.msg("Istio CA", "파일럿 에이전트", "4. X.509 SVID", 456, MUTED, "ar", sub="검증 성공 뒤 서명 응답")
d.msg("파일럿 에이전트", "Envoy 프록시", "5. Envoy SDS", 518, MUTED, "ar", sub="인증서와 개인 키 전달")

d.state("Envoy 프록시", "mTLS 가능", 568, INFO)

d.t(24, 604, "토큰의 페이로드는 고칠 수 없다 — 고치면 서명 검증에 실패한다", 13, SOFT, KR, "start")
d.legend(624, [("규격에서 옮겨 간 걸음", ACC), ("부트스트랩이 끝난 상태", INFO)])
d.save("a0-03.bootstrap-steps.svg")
print("ok bootstrap-steps")
