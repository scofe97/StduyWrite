# 타입 스펙: type-sequence — 같은 브라우저가 둘째 앱을 열면 IdP 가 세션 쿠키를 보고 비밀번호 입력 없이 곧바로 코드를 돌려주는 왕복.
# 사실 출처: IdP 세션 재사용은 SAML 2.0 Profiles §4.1.3.4(https://docs.oasis-open.org/security/saml/v2.0/saml-profiles-2.0-os.pdf) "This may require a new act of authentication, or it may reuse an existing authenticated session" 와 §4.1.3.4 의 ForceAuthn=true 는 새 인증을 강제.
#   OpenID Connect Core 1.0 §3.1.2.5 응답 형식(302 …/cb?code=…&state=…). 앱 B 의 client_id k2Pq9Tz · code Zx81q0Lm… · state bB7c3d 와 /feed 는 이 노트가 만든 예시 값(스펙 값 아님). 추출본 v1.txt 388~404행(YouTube 단계 8~14).
# Layout conventions: 레인 3·폭 200, 메시지 y=196·252·336·460·532(부제가 붙는 메시지는 뒤 간격 72), 상태 칩 y=400, 생략 표시 점선 y=580. 모든 좌표 4의 배수.
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


W, H = 880, 668
d = SeqKR(W, H, "BYTEBYTEGO · 03-02 §5",
          "둘째 앱은 IdP 세션 덕분에 비밀번호를 묻지 않는다",
          "브라우저가 IdP 로 가면 세션 쿠키가 따라가서 로그인 화면 없이 코드가 돌아옵니다",
          "앱 B 가 열린 경우 · 같은 브라우저")
AP, BR, IP = "앱 B", "브라우저", "IdP"
d.lanes([(AP, "client_id k2Pq9Tz"), (BR, "같은 사용자"), (IP, "인증 서버")], 100, 200)
d.rails(H - 80)

d.msg(BR, AP, "GET /feed", 196)
d.msg(AP, BR, "302 → IdP /authorize", 252, MUTED, "ar", "5 4", ["client_id=k2Pq9Tz", "state=bB7c3d"])
d.msg(BR, IP, "GET /authorize + 세션 쿠키", 336, ACC, "acc", None, ["response_type=code · scope=openid"], lx=580)
d.state(IP, "세션 있음 → 입력 없음", 400, OK)
d.msg(IP, BR, "302 → /cb?code=Zx81q0Lm…", 460, MUTED, "ar", "5 4", ["state=bB7c3d"], lx=580)
d.msg(BR, AP, "GET /cb?code=Zx81q0Lm…", 536)
d.line(40, 580, W - 64, 580, RULE, 0.8, "4 4")
d.t(276, 572, "이하 코드 교환은 첫 로그인과 같음", 12, MUTED, KR, "middle")

d.legend(H - 56, [("세션 쿠키로 통과", ACC), ("로그인 입력 없음", OK)])
d.save("03-02.sso-second-sequence.svg")
