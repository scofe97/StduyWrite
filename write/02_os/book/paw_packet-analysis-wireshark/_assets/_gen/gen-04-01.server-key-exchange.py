# 04-01 §4 「Server Key Exchange — 올 때와 안 올 때」 — 같은 자리에 이 메시지가 끼거나 안 낀다.
# 본문 요구: "서버는 Server Certificate 메시지가 클라이언트가 pre-master secret 를 교환하기에 충분한
#            데이터를 담고 있지 않을 때만 이 메시지를 보냅니다."
#            목록 둘(오는 방식·오면 안 되는 방식)만으로는 '충분한 데이터'가 무엇인지가 안 선다.
#            같은 구간을 두 번 그려 무엇이 더 오고 왜 더 오는지를 보인다.
# 타입 스펙: type-sequence — 주체 둘 사이의 시간순 메시지. 두 경우를 구분선으로 나눠 쌓고,
#           headline(acc)은 한쪽에만 끼는 메시지 하나다.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, OK, BAD, WARN, INFO, PAPER, PAPER2, RULE, KR, MONO

def _kr(t): return KR if any("가" <= c <= "힣" for c in str(t)) else MONO

class SeqKR(Seq):
    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]; dd = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dd} {y} L {x2 - 12 * dd} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 9, label, 13, c, _kr(label), "middle", 600)
        if sub: s.t(mx, y + 16, sub, 12, MUTED, KR)

W, H = 960, 720
d = SeqKR(W, H, "PACKET ANALYSIS WITH WIRESHARK · 04-01 §4",
          "ServerKeyExchange 가 끼는 자리와 안 끼는 자리",
          "같은 구간을 두 경우로 그렸다. 정적 RSA 는 인증서 안의 공개키만으로 클라이언트가 비밀을 만들 수 "
          "있어 이 메시지가 오지 않는다. 임시 방식은 회차마다 새 공개값을 만들어 보내야 해서 이 메시지가 "
          "필요하고, 그 값이 진짜 서버의 것임을 인증서의 키로 서명해 붙인다.",
          "TLS 1.2: 정적 RSA 와 인증된 DHE·ECDHE 를 비교합니다")

d.lanes([("클라이언트", "CLIENT"), ("서버", "SERVER")], y0=104, lane_w=280)
d.rails(600)
for top in (170, 396):
    d.o.append(f'<rect x="{d.LX["클라이언트"] - 8}" y="{top}" width="16" height="40" fill="{PAPER}"/>')

# ── A · 정적 RSA — 안 온다 ────────────────────────────────────
d.t(24, 184, "A · 정적 RSA — 생략", 13, SOFT, KR, "start", 600)
d.t(24, 202, "RSA key exchange", 12, MUTED, MONO, "start")
# B 와 같은 자리에서 비교되도록, 빈 자리는 Certificate 와 ServerHelloDone 사이에 둔다
d.msg("서버", "클라이언트", "Certificate", 238, INFO, "info", sub="비밀 암호화에 쓰는 RSA 공개키")
d.t((d.LX["클라이언트"] + d.LX["서버"]) / 2, 286, "ServerKeyExchange 자리 — 비어 있음", 11, SOFT, KR)
d.msg("서버", "클라이언트", "ServerHelloDone", 322, MUTED, "ar")
d.msg("클라이언트", "서버", "ClientKeyExchange", 358, OK, "ok", sub="서버 공개키로 감싼 비밀")

d.line(24, 386, W - 48, 386, RULE, 0.8, "4 6")

# ── B · 임시 방식 — 온다 ──────────────────────────────────────
d.t(24, 410, "B · 인증된 임시 키 교환 — 전송", 13, SOFT, KR, "start", 600)
d.t(24, 428, "DHE_DSS · DHE_RSA · ECDHE_RSA · ECDHE_ECDSA", 12, MUTED, MONO, "start")
d.msg("서버", "클라이언트", "Certificate", 466, INFO, "info", sub="서명 검증용 공개키만 들어 있음")
d.msg("서버", "클라이언트", "ServerKeyExchange", 522, ACC, "acc",
      sub="이번 회차의 새 공개값 + 그 값에 대한 서명")
d.msg("서버", "클라이언트", "ServerHelloDone", 570, MUTED, "ar")
d.msg("클라이언트", "서버", "ClientKeyExchange", 614, OK, "ok", sub="클라이언트의 새 공개값")

d.t(24, 660, "범위 밖: 정적 DH 는 인증서의 DH 공개값 사용 · 익명 DH 는 인증서·서명 없음", 12, MUTED, KR, "start")

d.legend(H - 40, [("추가 공개값과 서명", ACC), ("서버 인증서", INFO), ("클라이언트 키 교환", OK)])
d.save("04-01.server-key-exchange.svg")
