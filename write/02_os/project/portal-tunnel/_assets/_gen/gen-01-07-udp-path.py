# 타입 스펙: type-data-flow — UDP 클라이언트 둘(A·B)의 패킷이 릴레이 공개 포트에서 flow ID로 변환되고 QUIC DATAGRAM 백홀을 거쳐 터널의 flow별 로컬 소켓과 최종 서비스로 왕복하는 데이터 흐름.
# 사실 출처: docs/src/routes/architecture/+page.md §1, docs/maintainer/architecture.md UDP resource ownership,
#   portal/transport/datagram_relay.go:29,132,197,268,291,
#   portal/transport/datagram_session.go:18,43,104,116,187,
#   types/transport.go:15,18,29,41,50, sdk/proxy.go:379,443,489.
import pathlib
import sys

_HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))

from dd import D, ACC, MUTED, SOFT, INK, OK, WARN, BAD, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 960, 560
d = D(W, H, "PORTAL-TUNNEL · UDP MULTIPLEXING DATA FLOW",
      "UDP 데이터그램 경로 — Flow ID 다중화와 QUIC 백홀",
      "클라이언트 패킷을 Flow ID로 사상해 QUIC DATAGRAM으로 전달하고 터널의 로컬 소켓으로 격리 중계합니다.",
      "단일 QUIC 백홀 안에서 Flow ID를 통해 클라이언트 소켓 문맥을 격리 보존합니다")

# 5개 처리 단계 열 정의
COLS = [
    ("1. UDP 클라이언트", 40, 140),
    ("2. Relay 공개 포트", 212, 172),
    ("3. QUIC 백홀", 416, 172),
    ("4. Tunnel 세션", 620, 160),
    ("5. 로컬 서비스", 812, 116)
]

for title, x, w in COLS:
    d.box(x, 104, w, 30, PAPER2, RULE, 1.0)
    d.t(x + w // 2, 123, title, 11, INK, KR, "middle", 600)

# 레인 1: 클라이언트 A (Flow 1)
Y_A = 164
H_A = 132

# 레인 2: 클라이언트 B (Flow 2)
Y_B = 328
H_B = 132

# 1열: 클라이언트 노드
d.box(40, Y_A, 140, H_A, PAPER2, RULE, 1.0)
d.t(110, Y_A + 28, "클라이언트 A", 12, INK, KR, "middle", 600)
d.t(110, Y_A + 52, "198.51.100.10:4120", 10, MUTED, MONO, "middle")
d.t(110, Y_A + 80, "DNS 질의 패킷", 11, INFO, KR, "middle")
d.t(110, Y_A + 104, "64바이트", 10, SOFT, MONO, "middle")

d.box(40, Y_B, 140, H_B, PAPER2, RULE, 1.0)
d.t(110, Y_B + 28, "클라이언트 B", 12, INK, KR, "middle", 600)
d.t(110, Y_B + 52, "203.0.113.25:5380", 10, MUTED, MONO, "middle")
d.t(110, Y_B + 80, "게임 상태 패킷", 11, WARN, KR, "middle")
d.t(110, Y_B + 104, "256바이트", 10, SOFT, MONO, "middle")

# 2열: RelayDatagram (Flow ID 부여)
d.box(212, Y_A, 172, H_A, PAPER2, INFO, 1.1)
d.t(298, Y_A + 28, "RelayDatagram", 12, INFO, MONO, "middle", 600)
d.t(298, Y_A + 52, "touchFlow → ID = 1", 11, OK, MONO, "middle")
d.t(298, Y_A + 76, "addrIndex 등록", 10, MUTED, KR, "middle")
d.t(298, Y_A + 104, "유휴 만료 5분", 10, SOFT, KR, "middle")

d.box(212, Y_B, 172, H_B, PAPER2, WARN, 1.1)
d.t(298, Y_B + 28, "RelayDatagram", 12, WARN, MONO, "middle", 600)
d.t(298, Y_B + 52, "touchFlow → ID = 2", 11, OK, MONO, "middle")
d.t(298, Y_B + 76, "addrIndex 등록", 10, MUTED, KR, "middle")
d.t(298, Y_B + 104, "신규 64/s (버스트 128)", 10, SOFT, KR, "middle")

# 3열: QUIC 백홀 프레임 (DatagramFrame)
d.box(416, Y_A, 172, H_A, PAPER2, RULE, 1.0)
d.t(502, Y_A + 26, "QUIC DATAGRAM", 11, ACC, MONO, "middle", 600)
d.t(502, Y_A + 50, "[flowID=1][payload]", 11, INK, MONO, "middle")
d.t(502, Y_A + 74, "ALPN portal-tunnel", 10, MUTED, MONO, "middle")
d.t(502, Y_A + 96, "최대 1238바이트", 10, OK, KR, "middle")
d.t(502, Y_A + 116, "HOL 차단 없음", 10, SOFT, KR, "middle")

d.box(416, Y_B, 172, H_B, PAPER2, RULE, 1.0)
d.t(502, Y_B + 26, "QUIC DATAGRAM", 11, ACC, MONO, "middle", 600)
d.t(502, Y_B + 50, "[flowID=2][payload]", 11, INK, MONO, "middle")
d.t(502, Y_B + 74, "ALPN portal-tunnel", 10, MUTED, MONO, "middle")
d.t(502, Y_B + 96, "최대 1238바이트", 10, OK, KR, "middle")
d.t(502, Y_B + 116, "손실 시 독립 폐기", 10, SOFT, KR, "middle")

# 4열: Tunnel (DatagramSession + udpFlowManager)
d.box(620, Y_A, 160, H_A, PAPER2, OK, 1.1)
d.t(700, Y_A + 26, "DatagramSession", 11, INK, MONO, "middle", 600)
d.t(700, Y_A + 48, "Accept() 디코딩", 10, MUTED, MONO, "middle")
d.t(700, Y_A + 72, "udpFlowManager", 11, OK, MONO, "middle", 600)
d.t(700, Y_A + 94, "소켓 키: (ID=1, T1)", 10, INK, KR, "middle")
d.t(700, Y_A + 114, "DialUDP 로컬 소켓", 10, SOFT, KR, "middle")

d.box(620, Y_B, 160, H_B, PAPER2, OK, 1.1)
d.t(700, Y_B + 26, "DatagramSession", 11, INK, MONO, "middle", 600)
d.t(700, Y_B + 48, "Accept() 디코딩", 10, MUTED, MONO, "middle")
d.t(700, Y_B + 72, "udpFlowManager", 11, OK, MONO, "middle", 600)
d.t(700, Y_B + 94, "소켓 키: (ID=2, T1)", 10, INK, KR, "middle")
d.t(700, Y_B + 114, "DialUDP 로컬 소켓", 10, SOFT, KR, "middle")

# 5열: 로컬 대상 서비스
d.box(812, Y_A, 116, H_A, PAPER2, RULE, 1.0)
d.t(870, Y_A + 36, "로컬 DNS", 12, INK, KR, "middle", 600)
d.t(870, Y_A + 64, ":5353", 11, MUTED, MONO, "middle")
d.t(870, Y_A + 94, "응답 패킷 생성", 10, OK, KR, "middle")

d.box(812, Y_B, 116, H_B, PAPER2, RULE, 1.0)
d.t(870, Y_B + 36, "게임 서버", 12, INK, KR, "middle", 600)
d.t(870, Y_B + 64, ":7777", 11, MUTED, MONO, "middle")
d.t(870, Y_B + 94, "상태 갱신 응답", 10, WARN, KR, "middle")

# 연결 화살표: 상행(순방향 요청) + 하행(역방향 응답)
for y_box, c in [(Y_A, INFO), (Y_B, WARN)]:
    y_fwd = y_box + 44
    y_rev = y_box + 88
    # 1 -> 2
    d.arrow([(180, y_fwd), (210, y_fwd)], c, "ar", 1.3)
    d.arrow([(210, y_rev), (180, y_rev)], OK, "ar", 1.2)
    # 2 -> 3
    d.arrow([(384, y_fwd), (414, y_fwd)], c, "ar", 1.3)
    d.arrow([(414, y_rev), (384, y_rev)], OK, "ar", 1.2)
    # 3 -> 4
    d.arrow([(588, y_fwd), (618, y_fwd)], c, "ar", 1.3)
    d.arrow([(618, y_rev), (588, y_rev)], OK, "ar", 1.2)
    # 4 -> 5
    d.arrow([(780, y_fwd), (810, y_fwd)], c, "ar", 1.3)
    d.arrow([(810, y_rev), (780, y_rev)], OK, "ar", 1.2)

d.legend(H - 44, [
    ("클라이언트 A 흐름", INFO),
    ("클라이언트 B 흐름", WARN),
    ("역방향 응답 흐름", OK),
    ("QUIC DATAGRAM 프레임", ACC)
])

out_path = _HERE.parent / "01-07-udp-path.svg"
d.save(str(out_path))
print(f"saved: {out_path}")
