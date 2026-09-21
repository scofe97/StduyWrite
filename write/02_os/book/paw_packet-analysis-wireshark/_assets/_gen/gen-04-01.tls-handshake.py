# 04-01 §2 — TLS 1.2 최초 전체 핸드셰이크의 개념적 메시지 순서.
# 타입 스펙: type-sequence — 주체 둘 사이의 시간순 메시지. 조건부·선택 메시지는 점선,
#           headline(accent)은 ChangeCipherSpec+Finished 두 줄뿐이다(스펙 coral 상한 2).
#           프리미티브의 Seq.msg 가 한글 라벨을 MONO 로 하드코딩하므로 계약대로 서브클래스로 감싼다.
#           2026-09-20 보강: 메시지마다 화살표를 따로 그리면 각각 따로 도착하는 것으로 읽힌다.
#           근거: 랩 캡처 a1-handshake.pcap 프레임 7 — 레코드 넷(2·11·12·14)이 한 세그먼트.
#           2026-09-20 개편: 그 보강이 왼쪽 괄호('덩어리')로 들어가면서 기존 '단계' 맨텍스트와
#           묶음 체계가 둘로 겹쳤다. 경계가 어긋나 '단계 4'(y=616) 가 '덩어리 3'(500~664) 안에
#           들어갔고, 괄호 라벨의 accent 가 범례의 '암호화가 시작되는 지점'과 충돌했다.
#           둘을 플라이트 하나로 합친다. 플라이트는 보내는 쪽이 바뀌는 단위(RFC 5246 §7.3)라
#           한 띠에 방향이 하나뿐이고, 그래서 묶음과 송수신 방향이 같이 읽힌다.
#           표시는 색이 아니라 네 겹이다 — 배경 띠 · 띠 사이 여백 · 띠 제목 · 보내는 쪽 세로 막대.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, OK, INFO, WARN, PAPER, PAPER2, RULE, KR, MONO

def _kr(t): return KR if any("가" <= c <= "힣" for c in str(t)) else MONO

class SeqKR(Seq):
    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]; dd = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dd} {y} L {x2 - 12 * dd} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 9, label, 13, c, _kr(label), "middle", 600)
        if sub: s.t(mx, y + 16, sub, 13, MUTED, KR)   # +15 면 13px 몸통 윗변이 화살표 선에 닿는다

W, H = 960, 1016
STRIDE = 48          # 반복 요소는 stride 하나. 전 메시지 공통
BAND_X, BAND_W = 12, W - 60

d = SeqKR(W, H, "PACKET ANALYSIS WITH WIRESHARK · 04-01",
          "TLS 1.2 최초 전체 핸드셰이크의 메시지 순서",
          "인증서 기반 최초 전체 핸드셰이크의 개념도. 네 띠는 보내는 쪽이 바뀌는 단위로 끊은 단계이고, "
          "점선은 조건부 메시지다. 각 방향의 ChangeCipherSpec 자체는 평문이고 다음 Finished부터 "
          "암호화된다. 세션 재개와 재협상은 제외한다.",
          "단계가 바뀔 때마다 보내는 쪽이 바뀝니다. 점선은 조건부이고, 각 방향에서 CCS 는 평문이며 Finished 부터 암호화됩니다")

d.lanes([("클라이언트", "CLIENT"), ("서버", "SERVER")], y0=104, lane_w=300)

# (띠 위쪽 y, 높이, 번호, 이름, 방향, 클라이언트가 보내는가)
# 높이 = 제목행 48 + 메시지 (n-1)*48 + 아래 여백 28
BANDS = [(176,  76, "1", "클라이언트 제안",         "클라이언트 → 서버", True),
         (264, 268, "2", "서버 선택과 인증",         "서버 → 클라이언트", False),
         (544, 220, "3", "클라이언트 키 재료와 전환", "클라이언트 → 서버", True),
         (776,  76, "4", "서버 전환과 검증",         "서버 → 클라이언트", False)]

for y0, h, *_ in BANDS:
    d.box(BAND_X, y0, BAND_W, h, "#F5F5F303", RULE, 1.0, 8)

d.rails(824)   # 라이프라인을 띠 위에 얹고, 띠 제목은 그 뒤에 그려 라이프라인이 끊기지 않게 한다

for y0, h, no, name, way, from_client in BANDS:
    # 보내는 쪽 변에 붙는 세로 막대 — 좌·우로 번갈아 붙어 왕복 두 번이 색 없이 읽힌다
    bx = BAND_X if from_client else BAND_X + BAND_W - 4
    d.box(bx, y0 + 8, 4, h - 16, SOFT, SOFT, 0.8, 2)
    d.t(24, y0 + 22, f"단계 {no} · {name}", 13, INK, KR, "start", 600)
    d.t(W - 60, y0 + 22, way, 13, MUTED, KR, "end")

d.msg("클라이언트", "서버", "Client Hello", 224, INFO, "info",
      sub="type==1 · 버전 · 랜덤 · cipher suite 목록 · 확장")

d.msg("서버", "클라이언트", "Server Hello", 312, INFO, "info",
      sub="type==2 · cipher suite 하나 선택")
d.msg("서버", "클라이언트", "Certificate", 360, MUTED, "ar", sub="type==11 · X.509 체인")
d.msg("서버", "클라이언트", "Server Key Exchange", 408, WARN, "warn", dash="4,3",
      sub="type==12 · 인증된 DHE·ECDHE 의 임시 공개값")
d.msg("서버", "클라이언트", "Certificate Request", 456, WARN, "warn", dash="4,3",
      sub="type==13 · 상호 인증일 때만")
d.msg("서버", "클라이언트", "Server Hello Done", 504, MUTED, "ar", sub="type==14")

d.msg("클라이언트", "서버", "Certificate", 592, WARN, "warn", dash="4,3",
      sub="type==11 · 요청에 대한 응답 · 없으면 빈 목록")
d.msg("클라이언트", "서버", "Client Key Exchange", 640, MUTED, "ar",
      sub="type==16 · RSA: 암호화된 비밀 / (EC)DHE: 공개값")
d.msg("클라이언트", "서버", "Certificate Verify", 688, WARN, "warn", dash="4,3",
      sub="type==15 · 서명용 클라이언트 인증서를 보낸 경우")
d.msg("클라이언트", "서버", "ChangeCipherSpec + Finished", 736, ACC, "acc",
      sub="CCS(20): 평문 → Finished(22): 암호화")

d.msg("서버", "클라이언트", "ChangeCipherSpec + Finished", 824, ACC, "acc",
      sub="CCS(20): 평문 → Finished(22): 암호화")

d.t(24, 880, "한 단계 = 응답을 기다리지 않고 잇달아 보내는 묶음 · 왕복 두 번", 13, SOFT, KR, "start", 600)
d.t(24, 904, "공통 필터: type 는 tls.handshake.type · content_type 은 tls.record.content_type", 13, MUTED, KR, "start")
d.t(24, 928, "Finished 의 handshake.type 은 복호화한 뒤 확인 가능", 13, MUTED, KR, "start")

d.legend(H - 60, [("암호화가 시작되는 지점", ACC), ("조건이 맞을 때만", WARN),
                  ("Hello 교환", INFO), ("이 단계를 보내는 쪽", SOFT)])
d.save("04-01.tls-handshake.svg")
