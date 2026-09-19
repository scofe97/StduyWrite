# 04-01 §4 「상호 인증일 때만 오는 셋」 — 기본 흐름의 어느 자리에 셋이 끼는가.
# 본문 요구: 서버가 CertificateRequest(13)를 보내고, 클라이언트가 Certificate(11)와
#            CertificateVerify(15)로 답한다. 인증서가 없으면 빈 목록을 보내고 서버 정책을 따른다.
#            목록만 보면 셋이 연달아 오는 것처럼 읽히는데, 실제로는 기본 흐름 사이사이에 끼어든다.
# 타입 스펙: type-sequence — 주체 둘 사이의 시간순 메시지. 기본 흐름은 흐린 색으로 두고
#           상호 인증에서만 오는 셋을 강조해, 끼어드는 자리가 서로 떨어져 있음을 보인다.
#           headline(acc)은 이 구성을 여는 메시지 하나(CertificateRequest)다.
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

W, H = 960, 748
d = SeqKR(W, H, "PACKET ANALYSIS WITH WIRESHARK · 04-01 §4",
          "상호 인증의 셋은 연달아 오지 않는다",
          "상호 인증에서만 오는 메시지 셋은 기본 흐름 사이사이에 끼어든다. 서버가 ServerHelloDone 앞에서 "
          "요구하고, 클라이언트는 ClientKeyExchange 앞뒤로 인증서와 그 인증서의 개인키를 가졌다는 서명을 "
          "나눠 보낸다. 인증서가 없으면 빈 Certificate를 보내고, 서버가 인증을 필수로 요구하는지에 따라 계속하거나 중단한다.",
          "TLS 1.2 서명용 클라이언트 인증서의 예입니다. 인증서가 없을 때의 처리는 서버 정책에 따릅니다")

d.lanes([("클라이언트", "CLIENT"), ("서버", "SERVER")], y0=104, lane_w=280)
d.rails(596)
MX = (d.LX["클라이언트"] + d.LX["서버"]) / 2

d.msg("서버", "클라이언트", "Certificate", 190, SOFT, "soft", sub="기본 흐름 — 서버 인증서")
d.msg("서버", "클라이언트", "CertificateRequest", 244, ACC, "acc",
      sub="상호 인증을 여는 메시지 · 13")
d.msg("서버", "클라이언트", "ServerHelloDone", 296, SOFT, "soft", sub="기본 흐름 — 서버 차례 끝")

d.msg("클라이언트", "서버", "Certificate", 350, ACC, "acc", sub="클라이언트 인증서 · 11")
d.msg("클라이언트", "서버", "ClientKeyExchange", 404, SOFT, "soft", sub="기본 흐름 — 언제나 옴")
d.msg("클라이언트", "서버", "CertificateVerify", 458, ACC, "acc",
      sub="핸드셰이크 기록에 대한 개인키 서명 · 15")
d.msg("클라이언트", "서버", "ChangeCipherSpec · Finished", 512, SOFT, "soft")

# 응하지 못했을 때
d.line(24, 552, W - 48, 552, RULE, 0.8, "4 6")
d.t(24, 580, "인증 정보가 없거나 검증에 실패한 경우", 13, SOFT, KR, "start", 600)
BW_, GAP = 288, 24
for i, (cond, res) in enumerate((("낼 인증서가 없음 → 빈 Certificate", "서버 정책에 따라 계속·중단"),
                                 ("클라이언트 인증서 검증 실패", "서버에서 fatal Alert · 중단"),
                                 ("서명이 안 맞음", "개인키 소유가 증명 안 됨"))):
    x = 24 + i * (BW_ + GAP)
    d.box(x, 600, BW_, 62, PAPER2, RULE, 1.0, 8)
    d.t(x + BW_ / 2, 624, cond, 12, INK, KR, "middle", 600)
    d.t(x + BW_ / 2, 644, res, 11, BAD, KR)

d.legend(H - 48, [("클라이언트 인증 메시지", ACC), ("기본 흐름", SOFT), ("예외 처리", BAD)])
d.save("04-01.mutual-auth-messages.svg")
