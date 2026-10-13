# 타입 스펙: type-sequence — 첫 앱에서 IdP 로 리디렉션되어 로그인하고, 인가 코드는 브라우저를 거쳐 오지만 토큰 교환은 앱과 IdP 가 직접 하는 OpenID Connect 인가 코드 흐름.
# 사실 출처: OpenID Connect Core 1.0 §3.1.2.1 예시 요청(response_type=code · scope=openid profile email · client_id=s6BhdRkqt3 · state=af0ifjsldkj · redirect_uri), §3.1.2.5 예시 응답(302 Location …/cb?code=SplxlOBeZQQYbYS6WxSbIA&state=af0ifjsldkj),
#   §3.1.3.1 토큰 요청(grant_type=authorization_code&code=SplxlOBeZQQYbYS6WxSbIA), §3.1.3.3 응답(access_token · id_token), §3.1.3.7 ID 토큰 검증(iss · aud · exp 등). IdP 세션 재사용은 SAML 2.0 Profiles §4.1.3.4 "reuse an existing authenticated session".
#   /inbox 는 이 노트가 만든 예시 경로. 추출본 v1.txt 355~405행(SSO 1~7단계).
# Layout conventions: 레인 3·폭 200, 메시지 y=196·252·336·460·536·596·672·764(부제가 붙는 메시지는 뒤 간격 72), 상태 칩 y=400·716. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, Seq, ACC, OK, WARN, INFO, BAD, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO


def _kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO


class SeqKR(Seq):
    def lanes(s, names, y0=104, lane_w=210):
        s.LX = {}
        n = len(names)
        span = (s.w - 48 - 24) - lane_w
        for i, (nm, sub) in enumerate(names):
            x = 24 + lane_w / 2 + (span * i / (n - 1) if n > 1 else 0)
            s.LX[nm] = x
            s.box(x - lane_w / 2, y0, lane_w, 44, PAPER2, RULE, 1.0)
            s.t(x, y0 + 20, nm, 13, INK, _kr(nm), "middle", 600)
            s.t(x, y0 + 37, sub, 12, MUTED, _kr(sub))
        s.lane_top = y0 + 44
        return s.LX

    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, subs=(), lx=None):
        x1, x2 = s.LX[a], s.LX[b]
        d_ = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * d_} {y} L {x2 - 12 * d_} {y}", c, 1.5, m=mk, dash=dash)
        mx = lx if lx is not None else (x1 + x2) / 2
        s.t(mx, y - 9, label, 12, c, _kr(label), "middle", 600)
        for i, sb in enumerate(subs):
            s.t(mx, y + 17 + 16 * i, sb, 12, MUTED, _kr(sb))

    def state(s, a, txt, y, c, dx=0):
        x = s.LX[a] + dx
        w = len(txt) * (12 if any("가" <= ch <= "힣" for ch in txt) else 7.8) + 20
        s.o.append(f'<rect x="{x - w / 2}" y="{y - 10}" width="{w}" height="20" rx="4" fill="{PAPER}"/>')
        s.o.append(f'<rect x="{x - w / 2}" y="{y - 10}" width="{w}" height="20" rx="4" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
        s.t(x, y + 4, txt, 12, c, _kr(txt))


W, H = 880, 864
d = SeqKR(W, H, "BYTEBYTEGO · 03-02 §4",
          "첫 로그인에서 코드는 브라우저를, 토큰은 뒷길을 지난다",
          "앱이 IdP 로 리디렉션하고 IdP 가 로그인과 세션을 만든 뒤 코드를 돌려주면 앱이 토큰으로 바꿉니다",
          "OpenID Connect 인가 코드 흐름 · 앱 A 가 처음 열린 경우")
AP, BR, IP = "앱 A", "브라우저", "IdP"
d.lanes([(AP, "client_id s6BhdRkqt3"), (BR, "사용자"), (IP, "인증 서버")], 100, 200)
d.rails(H - 80)

d.msg(BR, AP, "GET /inbox", 196)
d.msg(AP, BR, "302 → IdP /authorize", 252, MUTED, "ar", "5 4", ["client_id=s6BhdRkqt3", "state=af0ifjsldkj"])
d.msg(BR, IP, "GET /authorize", 336, MUTED, "ar", None, ["response_type=code · scope=openid"], lx=580)
d.state(IP, "로그인 → IdP 세션", 400, INFO)
d.msg(IP, BR, "302 → /cb?code=SplxlOBe…", 460, MUTED, "ar", "5 4", ["state=af0ifjsldkj"], lx=580)
d.msg(BR, AP, "GET /cb?code=SplxlOBe…", 536)
d.msg(AP, IP, "POST /token", 596, ACC, "acc", None, ["grant_type=authorization_code"], lx=590)
d.msg(IP, AP, "id_token · access_token", 672, OK, "ok", "5 4", lx=590)
d.state(AP, "iss · aud · exp 검증", 716, OK, dx=96)
d.msg(AP, BR, "200 /inbox", 764, OK, "ok", "5 4")

d.legend(H - 56, [("뒷길 토큰 교환", ACC), ("성공", OK), ("IdP 세션", INFO)])
d.save("03-02.sso-first-sequence.svg")
