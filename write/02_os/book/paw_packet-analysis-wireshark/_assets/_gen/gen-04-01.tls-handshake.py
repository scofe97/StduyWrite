# 04-01 학습 목표 뒤 전체 지도 — 원문 two-way-handshake.pcap(상호 인증)의 메시지 순서.
# 원문이 "네 단계"라 적은 구획을 왼쪽에 표시하고, 조건부 메시지는 점선으로 구분한다.
# 타입 스펙: type-sequence — 주체 둘 사이의 시간순 메시지. 조건부·선택 메시지는 점선,
#           headline(accent)은 암호화가 시작되는 ChangeCipherSpec·Finished 두 줄.
#           프리미티브의 Seq.msg 가 한글 라벨을 MONO 로 하드코딩하므로 계약대로 서브클래스로 감싼다.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, OK, INFO, WARN, PAPER, PAPER2, RULE, KR, MONO

def _kr(t): return KR if any("가" <= c <= "힣" for c in str(t)) else MONO

class SeqKR(Seq):
    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]; dd = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dd} {y} L {x2 - 12 * dd} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 9, label, 11, c, _kr(label), "middle", 600)
        if sub: s.t(mx, y + 15, sub, 11, MUTED, KR)

W, H = 960, 800
d = SeqKR(W, H, "PACKET ANALYSIS WITH WIRESHARK · 04-01",
          "TLS 핸드셰이크의 메시지 순서",
          "원문 two-way-handshake.pcap 의 상호 인증 흐름. 실선은 언제나 오가는 메시지이고 점선은 조건이 맞을 때만 오간다. 마지막 두 쌍이 오간 뒤부터 기록이 암호화된다.",
          "점선 넷은 조건부입니다 — 키 교환 방식과 상호 인증 여부가 그 조건입니다")

d.lanes([("클라이언트", "ssl.handshake.type"), ("서버", "ssl.record.content_type")],
        y0=104, lane_w=300)
d.rails(704)

PH = [(184, "1"), (256, "2"), (472, "3"), (616, "4")]
for y, n in PH:
    d.t(20, y, f"단계 {n}", 11, SOFT, KR, "start", 600)

d.msg("클라이언트", "서버", "Client Hello", 208, INFO, "info",
      sub="type==1 · 버전 · 랜덤 · cipher suite 목록 · 확장")
d.msg("서버", "클라이언트", "Server Hello", 272, INFO, "info",
      sub="type==2 · cipher suite 하나를 고릅니다")
d.msg("서버", "클라이언트", "Certificate", 320, MUTED, "ar", sub="type==11 · X.509 체인")
d.msg("서버", "클라이언트", "Server Key Exchange", 368, WARN, "warn", dash="4,3",
      sub="type==12 · DHE·DH_anon 계열일 때만")
d.msg("서버", "클라이언트", "Certificate Request", 416, WARN, "warn", dash="4,3",
      sub="type==13 · 상호 인증일 때만")
d.msg("서버", "클라이언트", "Server Hello Done", 460, MUTED, "ar", sub="type==14")

d.msg("클라이언트", "서버", "Certificate", 512, WARN, "warn", dash="4,3",
      sub="type==11 · 상호 인증일 때만")
d.msg("클라이언트", "서버", "Client Key Exchange", 560, MUTED, "ar",
      sub="type==16 · pre_master_secret 를 넘깁니다")
d.msg("클라이언트", "서버", "Certificate Verify", 604, WARN, "warn", dash="4,3",
      sub="type==15 · 상호 인증일 때만")

d.msg("클라이언트", "서버", "ChangeCipherSpec + Finished", 660, ACC, "acc",
      sub="content_type==20 · 22 · 여기부터 암호화")
d.msg("서버", "클라이언트", "ChangeCipherSpec + Finished", 704, ACC, "acc",
      sub="양쪽이 보내면 핸드셰이크가 끝납니다")

d.legend(H - 60, [("암호화가 시작되는 지점", ACC), ("조건이 맞을 때만", WARN), ("Hello 교환", INFO)])
d.save("04-01.tls-handshake.svg")
