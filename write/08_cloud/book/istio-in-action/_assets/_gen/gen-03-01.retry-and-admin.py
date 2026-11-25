# 03-01 §6 Admin API와 재시도 관측 — /status/500 요청 시 3회 재시도와 :15000/stats 카운터 확인.
# 값 근거: 03-01 본문 §6 — curl → Envoy(:15001) → httpbin(:8000), retry_on: 5xx, num_retries: 3,
#          Admin API(:15000/stats), upstream_rq_retry: 3, upstream_rq_retry_success: 0.
# 타입 스펙: type-sequence — 참여자 셋(curl · Envoy · httpbin) 사이의 시간순 요청·재시도·관측 흐름.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, OK, WARN, INFO, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 592


class SeqKR(Seq):
    def lanes(s, names, y0=104, lane_w=204):
        s.LX = {}
        n = len(names)
        span = (s.w - 48 - 24) - lane_w
        for i, (nm, sub) in enumerate(names):
            x = 24 + lane_w / 2 + (span * i / (n - 1) if n > 1 else 0)
            s.LX[nm] = x
            s.box(x - lane_w / 2, y0, lane_w, 48, PAPER2, RULE, 1.0)
            s.t(x, y0 + 21, nm, 13, INK, KR, "middle", 600)
            s.t(x, y0 + 39, sub, 11, MUTED, MONO)
        s.lane_top = y0 + 48
        return s.LX


d = SeqKR(W, H, "ISTIO IN ACTION · 03-01 §6",
          "재시도 실행과 Admin API 카운터 관측",
          "curl이 :15001로 /status/500을 호출하면 Envoy가 httpbin(:8000)에 3회 재시도하고, 이후 :15000/stats에서 upstream_rq_retry: 3을 확인합니다.",
          "프록시 포트(:15001)의 재시도 결과가 Admin API(:15000) 통계로 그대로 드러납니다")

LX = d.lanes([("curl 클라이언트", "curlimages/curl"), ("Envoy 프록시", ":15001 · :15000"), ("httpbin", "httpbin:8000")], y0=104, lane_w=204)
XC, XE, XH = LX["curl 클라이언트"], LX["Envoy 프록시"], LX["httpbin"]
d.rails(532)


def msg(a, b, label, y, c=MUTED, mk="ar", dash=None):
    x1, x2 = LX[a], LX[b]
    dr = 1 if x2 > x1 else -1
    d.path(f"M {x1 + 10 * dr} {y} L {x2 - 12 * dr} {y}", c, 1.4, m=mk, dash=dash)
    fam = KR if any("가" <= ch <= "힣" for ch in label) else MONO
    d.t((x1 + x2) / 2, y - 9, label, 12, c, fam, "middle", 600)


# 1. 초기 요청과 500 응답
msg("curl 클라이언트", "Envoy 프록시", "GET :15001/status/500", 192, INFO, "info")
msg("Envoy 프록시", "httpbin", "첫 요청 전달", 228, INFO, "info")
msg("httpbin", "Envoy 프록시", "HTTP 500", 264, WARN, "warn", "4 3")

# 2. retry_policy 루프 프레임
FX, FY, FW, FH = XE - 40, 286, (XH - XE) + 80, 116
d.o.append(f'<rect x="{FX}" y="{FY}" width="{FW}" height="{FH}" rx="4" fill="rgba(245,245,245,0.03)" stroke="rgba(245,245,245,0.22)" stroke-width="1"/>')
d.o.append(f'<rect x="{FX}" y="{FY}" width="56" height="16" rx="2" fill="{PAPER}" stroke="rgba(245,245,245,0.22)" stroke-width="1"/>')
d.t(FX + 28, FY + 12, "RETRY x3", 8, WARN, MONO)
d.t(XE + 28, FY + 14, "retry_on: 5xx · num_retries: 3", 11, MUTED, MONO, "start")

msg("Envoy 프록시", "httpbin", "재시도 요청 (num_retries)", 344, WARN, "warn")
msg("httpbin", "Envoy 프록시", "모두 HTTP 500", 384, WARN, "warn", "4 3")

# 3. 클라이언트로 반환 후 Admin API 관측
msg("Envoy 프록시", "curl 클라이언트", "HTTP 500 (재시도 모두 실패)", 432, MUTED, "ar", "4 3")
msg("curl 클라이언트", "Envoy 프록시", "GET :15000/stats | grep retry", 472, OK, "ok")

# 상태 칩 (Envoy 레일 위, 레인 중앙 기준)
sw = 380
d.o.append(f'<rect x="{XE - sw / 2}" y="496" width="{sw}" height="28" rx="5" fill="{ACC}22" stroke="{ACC}" stroke-width="1.2"/>')
d.t(XE, 514, "upstream_rq_retry: 3 · upstream_rq_retry_success: 0", 11, ACC, MONO, "middle", 600)

d.legend(548, [("요청 전달", INFO), ("500 응답 · 재시도", WARN), ("Admin API 조회", OK), ("재시도 카운터 증명", ACC)])
d.save("03-01.retry-and-admin.svg")
print("ok 03-01 retry-and-admin")
