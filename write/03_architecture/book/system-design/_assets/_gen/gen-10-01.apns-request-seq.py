# 타입 스펙: type-sequence — 알림 서버가 APNs 에 POST 한 번을 보내고 응답과 기기 전달까지 이어지는 왕복. 요청 줄·인증 헤더·페이로드 키가 단계마다 실제 값으로 나온다.
# 사실 출처: 추출본 v2.txt 2723~2736행(제공자·기기 토큰·페이로드·APNs·iOS)과 PDF 153쪽 페이로드 그림(title Game Request, body Bob wants to play chess, badge 5),
#   Apple 문서 Sending notification requests to APNs 의 예시 요청(:path /3/device/00fc13ad…, apns-topic com.example.MyApp, apns-push-type alert, apns-priority 10, apns-id eabeae54-…)과 응답 :status 200,
#   Generating a remote notification 의 4096 바이트 한도, Establishing a token-based connection 의 ES256 JWT.
# Layout conventions: 레인 3개 폭 200, x = 160·500·840, 메시지 stride 56~64, 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, OK, WARN, INFO, RULE, KR, MONO


def _kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO


class SeqKR(Seq):
    def lanes(s, names, xs, y0=104, lane_w=200):
        s.LX = {}
        for (nm, sub), x in zip(names, xs):
            s.LX[nm] = x
            s.box(x - lane_w / 2, y0, lane_w, 44, "#161B22", RULE, 1.0)
            s.t(x, y0 + 20, nm, 13, INK, KR, "middle", 600)
            s.t(x, y0 + 37, sub, 13 if _kr(sub) == KR else 11, MUTED, _kr(sub))
        s.lane_top = y0 + 44
        return s.LX

    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None, dx=0):
        x1, x2 = s.LX[a], s.LX[b]
        dr = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dr} {y} L {x2 - 12 * dr} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2 + dx
        s.t(mx, y - 9, label, 13 if _kr(label) == KR else 12, c, _kr(label), "middle", 600)
        if sub:
            s.t(mx, y + 17, sub, 13 if _kr(sub) == KR else 12, MUTED, _kr(sub))


W, H = 1000, 504
d = SeqKR(W, H, "SYSTEM DESIGN INTERVIEW · 10-01 §2",
          "푸시 하나는 POST 한 번으로 APNs 에 닿는다",
          "알림 서버는 기기 토큰을 경로에, 인증 토큰과 주제를 헤더에, 알림 내용을 본문에 담아 보내고 APNs 가 기기로 전달한다.",
          "경로의 토큰이 기기를 고르고 본문의 aps 가 화면에 나온다")

d.lanes([("알림 서버", "제공자"), ("APNs", "api.push.apple.com"), ("iOS 기기", "앱 com.example.MyApp")],
        (160, 500, 840))
d.rails(456)

d.msg("알림 서버", "APNs", "POST /3/device/00fc13ad…", 220, MUTED)
mx = (d.LX["알림 서버"] + d.LX["APNs"]) / 2
d.t(mx, 244, "authorization: bearer ‹JWT ES256›", 12, MUTED, MONO)
d.t(mx, 264, "apns-topic: com.example.MyApp", 12, MUTED, MONO)
d.t(mx, 284, "apns-push-type: alert", 12, MUTED, MONO)
d.t(mx, 308, "본문 ≤ 4096 바이트", 13, ACC, KR, "middle", 600)
d.t(mx, 328, "aps.alert.title · aps.alert.body · aps.badge", 12, ACC, MONO)

d.msg("APNs", "알림 서버", "200", 380, OK, dash="5 4", sub="apns-id eabeae54-…")
d.msg("APNs", "iOS 기기", "알림 전달", 380, INFO, dash="5 4")

d.legend(H - 40, [("요청", MUTED), ("알림 내용", ACC), ("응답", OK), ("기기 전달", INFO)])
d.save("10-01.apns-request-seq.svg")
