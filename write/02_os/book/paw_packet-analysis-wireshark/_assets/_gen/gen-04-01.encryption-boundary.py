# 04-01 §5 — 어디까지 평문이고 어디부터 암호화인가.
# 본문 요구: "암호화가 시작되는 지점은 ChangeCipherSpec 뒤의 Finished 부터" 와
#            "TLS 가 가리는 층과 못 가리는 층"을 한 장에서 읽힌다. SNI는 앞서 보낸 ClientHello에서 확인한다.
# 경계는 방향마다 따로 선다 — 보낸 쪽이 자기 ChangeCipherSpec 을 보낸 뒤부터 그 쪽 메시지가 암호화된다.
# 그래서 가로선 하나로 나누지 않고 레인별로 경계 표지를 둔다.
# 타입 스펙: type-sequence — 주체 둘 사이의 시간순 메시지. 메시지 색이 평문인지 암호문인지를 나르고,
#           headline(acc)은 방향별 경계 표지다. 아래 띠는 그 경계와 무관하게 남는 것이다.
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

W, H = 960, 874
d = SeqKR(W, H, "PACKET ANALYSIS WITH WIRESHARK · 04-01 §5",
          "TLS 1.2: 방향마다 Finished 부터 암호화",
          "정적 RSA, 서버 인증만 사용하는 최초 전체 핸드셰이크의 예다. 버전·cipher suite·서버 인증서는 평문으로 읽힌다. 보낸 쪽이 자기 ChangeCipherSpec 을 "
          "보낸 뒤부터 그 방향의 메시지가 암호화되므로 경계는 방향마다 따로 선다. 그 뒤에도 IP 헤더와 TCP 헤더, "
          "이전 ClientHello 에 실렸던 SNI는 캡처에서 확인할 수 있다.",
          "정적 RSA · 서버 인증만 사용하는 최초 전체 핸드셰이크의 예입니다")

d.lanes([("클라이언트", "CLIENT"), ("서버", "SERVER")], y0=104, lane_w=280)
d.rails(642)
LC, LS = d.LX["클라이언트"], d.LX["서버"]

# ── 평문 구간 ─────────────────────────────────────────────────
d.msg("클라이언트", "서버", "ClientHello", 196, INFO, "info", sub="버전·cipher suite 목록·SNI")
d.msg("서버", "클라이언트", "ServerHello", 240, INFO, "info", sub="고른 버전과 cipher suite 하나")
d.msg("서버", "클라이언트", "Certificate", 284, INFO, "info", sub="서버 인증서 체인")
d.msg("서버", "클라이언트", "ServerHelloDone", 336, INFO, "info")
d.msg("클라이언트", "서버", "ClientKeyExchange", 380, INFO, "info")

# ── 클라이언트 쪽 경계 ─────────────────────────────────────────
d.msg("클라이언트", "서버", "ChangeCipherSpec", 424, ACC, "acc", sub="CCS 자체는 평문 · 다음 레코드부터 보호")
d.line(LC - 34, 448, LC + 34, 448, ACC, 1.6)
d.t(LC - 42, 452, "클라이언트 경계", 11, ACC, KR, "end", 600)
d.msg("클라이언트", "서버", "Finished", 482, OK, "ok", sub="encrypted handshake message")

# ── 서버 쪽 경계 ──────────────────────────────────────────────
d.msg("서버", "클라이언트", "ChangeCipherSpec", 526, ACC, "acc")
d.line(LS - 34, 550, LS + 34, 550, ACC, 1.6)
d.t(LS + 42, 554, "서버 경계", 11, ACC, KR, "start", 600)
d.msg("서버", "클라이언트", "Finished", 584, OK, "ok")

d.msg("클라이언트", "서버", "Application Data", 634, OK, "ok", sub="안이 안 보이는 레코드만 남음")

# ── 경계와 무관하게 남는 것 ────────────────────────────────────
BY = 686
d.line(24, BY - 16, W - 48, BY - 16, RULE, 0.8, "4 6")
d.t(24, BY + 8, "복호화 없이 캡처에서 확인 가능한 정보", 13, SOFT, KR, "start", 600)
BW_, GAP = 280, 24
for i, (title, sub) in enumerate((("출발지·목적지 IP", "IP 헤더 · 층이 다름"),
                                  ("출발지·목적지 포트", "TCP 헤더 · 층이 다름"),
                                  ("도메인 이름", "앞서 보낸 ClientHello 의 SNI"))):
    x = 24 + i * (BW_ + GAP)
    d.box(x, BY + 22, BW_, 62, PAPER2, RULE, 1.0, 8)
    d.t(x + BW_ / 2, BY + 46, title, 12, INK, KR, "middle", 600)
    d.t(x + BW_ / 2, BY + 66, sub, 11, MUTED, KR)

d.legend(H - 48, [("평문 — 화면에서 읽힘", INFO), ("암호화 — 안이 안 보임", OK), ("방향별 경계", ACC)])
d.save("04-01.encryption-boundary.svg")
