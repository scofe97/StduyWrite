# 타입 스펙: type-sequence — 클라이언트가 여섯 줄 서명 문자열로 HMAC-SHA256 을 계산해 보내고, 서버가 같은 문자열로 다시 계산해 비교하는 왕복. 본문이 그대로면 200, {"item":9} 로 바뀌면 401 인 ALT 프레임 하나.
# 사실 출처: HMAC 구성은 RFC 2104(https://www.rfc-editor.org/rfc/rfc2104), 해시는 RFC 6151 §2 의 "new protocol designs should not employ HMAC-MD5" 와 HMAC-SHA256 권고에 따라 SHA-256. 401 은 RFC 9110 §15.5.2.
#   서명에 넣는 속성(App ID·URI·본문·메서드·타임스탬프·nonce)은 추출본 v1.txt 987~1000행과 쪽 36 그림의 hmac signature generation algorithm 상자. 값은 이 노트가 만든 시연 값을 python3 hmac.new(key, msg, sha256) 로 계산:
#   키 demo-api-key-8c41, 서명 문자열 "app-3f9a\nPOST\n/v1/orders\n{\"item\":7}\n1791849600\nb7f3a1" → 83f6b23283b33ad8…, 본문만 {"item":9} 로 바꾸면 b18dc40839e6d724…. 1791849600 = 2026-10-13 00:00:00 UTC. 재현 스크립트: scratchpad/sdi/demo-bbg0302.py.
# Layout conventions: 레인 2·폭 220, 서명 문자열 상자 폭 188(줄 stride 20), 호출 y=332, ALT 프레임 y=380~636(영역마다 자기 호출 1·반환 1 + 재계산 1), 영역 구분선 점선. 모든 좌표 4의 배수.
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

    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]
        d_ = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * d_} {y} L {x2 - 12 * d_} {y}", c, 1.5, m=mk, dash=dash)
        s.t((x1 + x2) / 2, y - 9, label, 12, c, _kr(label), "middle", 600)
        if sub:
            s.t((x1 + x2) / 2, y + 17, sub, 12, MUTED, _kr(sub))

    def selfmsg(s, a, label, y, c=MUTED, sub=None, left=False):
        x = s.LX[a]
        k = -1 if left else 1
        s.path(f"M {x + 10 * k} {y - 10} L {x + 58 * k} {y - 10} L {x + 58 * k} {y + 10} L {x + 13 * k} {y + 10}", c, 1.4, m="ar")
        anchor = "end" if left else "start"
        s.t(x + 68 * k, y - 4, label, 12, c, _kr(label), anchor, 600)
        if sub:
            s.t(x + 68 * k, y + 14, sub, 12, MUTED, _kr(sub), anchor)


W, H = 880, 712
d = SeqKR(W, H, "BYTEBYTEGO · 03-02 §3",
          "서명은 요청 속성을 키로 묶어 서버가 다시 계산한다",
          "본문이 한 글자 바뀌면 서버가 다시 계산한 값이 달라져 401 이 됩니다",
          "HMAC-SHA256 · API 키는 양쪽만 안다")
CL, SV = "클라이언트", "웹 서버"
d.lanes([(CL, "API 키 보유"), (SV, "같은 API 키 보유")], 100, 220)
d.rails(H - 80)

# 서명 문자열 상자 — 서명에 들어가는 여섯 줄
BX, BY, BW = 452, 152, 188
d.box(BX, BY, BW, 156, PAPER2, RULE, 0.9, 6)
d.t(BX + BW / 2, BY + 22, "서명 문자열", 12, MUTED, KR, "middle", 600)
for i, ln in enumerate(["app-3f9a", "POST", "/v1/orders", '{"item":7}', "1791849600", "b7f3a1"]):
    d.t(BX + 16, BY + 46 + i * 20, ln, 12, INK, MONO, "start")

d.selfmsg(CL, "HMAC-SHA256(키, 문자열)", 192, MUTED, "= 83f6b232…")
d.msg(CL, SV, "POST /v1/orders", 340, ACC, "acc", sub="X-Signature: 83f6b232…")

# ALT 프레임
FX, FY, FW, FH = 64, 380, 732, 256
d.o.append(f'<rect x="{FX}" y="{FY}" width="{FW}" height="{FH}" rx="4" fill="#F5F5F30a" stroke="rgba(245,245,243,0.22)" stroke-width="1"/>')
d.o.append(f'<rect x="{FX}" y="{FY}" width="40" height="16" rx="2" fill="{PAPER}" stroke="rgba(245,245,243,0.22)" stroke-width="1"/>')
d.t(FX + 20, FY + 12, "ALT", 8, MUTED, MONO, "middle")
d.t(156, FY + 36, "[본문이 그대로]", 12, MUTED, KR, "start")
d.selfmsg(SV, "재계산 = 83f6b232…", 424, OK, "보낸 서명과 같음", left=True)
d.msg(SV, CL, "200 OK", 480, OK, "ok", dash="5 4")
d.line(FX + 8, 508, FX + FW - 8, 508, RULE, 1.0, "4 3")
d.t(156, 532, '[본문이 {"item":9} 로 바뀜]', 12, MUTED, KR, "start")
d.selfmsg(SV, "재계산 = b18dc408…", 568, BAD, "보낸 서명과 다름", left=True)
d.msg(SV, CL, "401 Unauthorized", 612, BAD, "bad", dash="5 4")

d.legend(H - 56, [("서명 일치", OK), ("서명 불일치", BAD), ("서명 붙은 요청", ACC)])
d.save("03-02.hmac-sequence.svg")
