# 타입 스펙: type-data-flow — 빠른 링크에서 병목을 거쳐 ACK 귀환까지 패킷과 ACK 간격의 보존 흐름.
# 사실 출처: ch16.txt 230~290행 — 패킷 보존 원리(Jacobson 1988), 병목 링크 직렬화(L/C), 간격 벌어짐, ACK 시계(self-clocking).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 500
d = D(W, H, "TCP/IP ILLUSTRATED VOL.1 · 16-01 §2",
      "병목 링크와 ACK 시계 — 자체 클러킹의 패킷 보존 원리",
      "송신자가 빠른 링크로 내보낸 밀착 패킷이 병목 링크에서 직렬화 지연을 겪으며 시간 축에서 벌어진다. 수신자가 그 간격대로 ACK 를 회신하면 송신자는 별도 타이머 없이도 병목 처리율에 맞춰 새 패킷을 주입한다.",
      "도착한 ACK 가 망을 빠져나간 패킷 하나를 증명하고 새 패킷을 엽니다")

Y_DATA = 120
H_DATA = 140

# 송신자 버스트 (빠른 링크)
d.box(24, Y_DATA, 240, H_DATA, PAPER2, RULE, 1.0, 8)
d.t(144, Y_DATA + 24, "송신자 버스트 (빠른 링크)", 13, INK, KR, "middle", 600)
d.t(144, Y_DATA + 44, "고속 링크 (예: 1Gbps) · 밀착 전송", 11, SOFT, KR, "middle")

# 패킷 세 개 (밀착)
for i, name in enumerate(["P1", "P2", "P3"]):
    px = 44 + i * 56
    d.box(px, Y_DATA + 64, 46, 32, PAPER, ACC, 1.2, 4)
    d.t(px + 23, Y_DATA + 84, name, 12, ACC, MONO, "middle", 600)
d.t(144, Y_DATA + 120, "좁은 패킷 간격 (Δt1)", 11, ACC, KR, "middle")

# 송신자 → 병목 화살표
d.arrow([(268, Y_DATA + 80), (328, Y_DATA + 80)], MUTED, "ar", 1.4)

# 병목 라우터
d.box(332, Y_DATA, 256, H_DATA, PAPER2, WARN, 1.2, 8)
d.t(460, Y_DATA + 24, "병목 라우터 (느린 링크)", 13, WARN, KR, "middle", 600)
d.t(460, Y_DATA + 44, "병목 링크 (예: 10Mbps) · 직렬화 L/C", 11, SOFT, KR, "middle")

# 병목 통과 패킷들 (벌어진 간격)
d.box(352, Y_DATA + 64, 44, 32, PAPER, WARN, 1.2, 4)
d.t(374, Y_DATA + 84, "P1", 12, WARN, MONO, "middle", 600)
d.box(438, Y_DATA + 64, 44, 32, PAPER, WARN, 1.2, 4)
d.t(460, Y_DATA + 84, "P2", 12, WARN, MONO, "middle", 600)
d.box(524, Y_DATA + 64, 44, 32, PAPER, WARN, 1.2, 4)
d.t(546, Y_DATA + 84, "P3", 12, WARN, MONO, "middle", 600)
d.t(460, Y_DATA + 120, "벌어진 간격 (Δt2 = L/C)", 11, WARN, KR, "middle")

# 병목 → 수신자 화살표
d.arrow([(592, Y_DATA + 80), (652, Y_DATA + 80)], MUTED, "ar", 1.4)

# 수신자
d.box(656, Y_DATA, 240, H_DATA, PAPER2, OK, 1.2, 8)
d.t(776, Y_DATA + 24, "수신자 도착 및 ACK 회신", 13, OK, KR, "middle", 600)
d.t(776, Y_DATA + 44, "도착 간격 = Δt2 그대로 ACK 생성", 11, SOFT, KR, "middle")

# 수신자 ACK 블록들
for i, name in enumerate(["A1", "A2", "A3"]):
    ax = 676 + i * 68
    d.box(ax, Y_DATA + 64, 44, 32, PAPER, OK, 1.2, 4)
    d.t(ax + 22, Y_DATA + 84, name, 12, OK, MONO, "middle", 600)
d.t(776, Y_DATA + 120, "ACK 간격 = Δt2 보존", 11, OK, KR, "middle")

# 중간 전이: 수신자에서 하단 ACK 귀환로로 연결
d.arrow([(776, Y_DATA + H_DATA + 4), (776, 300), (716, 300)], OK, "ok", 1.4)

# 하단: ACK 귀환 및 송신자 클러킹
Y_ACK = 290

# 귀환 중인 ACK 스트림
d.box(296, Y_ACK - 16, 416, 96, PAPER2, RULE, 1.0, 8)
d.t(504, Y_ACK + 6, "귀환 경로 (ACK 스트림)", 12, SOFT, KR, "middle", 600)
for i, name in enumerate(["A3", "A2", "A1"]):
    ax = 340 + i * 110
    d.box(ax, Y_ACK + 18, 48, 28, PAPER, OK, 1.2, 4)
    d.t(ax + 24, Y_ACK + 36, name, 11, OK, MONO, "middle", 600)
d.arrow([(336, Y_ACK + 32), (268, Y_ACK + 32)], OK, "ok", 1.4)
d.t(504, Y_ACK + 68, "동일 간격 유지 (Δt2)", 11, MUTED, KR, "middle")

# 송신자의 새 패킷 전송 (자체 클러킹 결론)
d.box(24, Y_ACK - 16, 240, 120, PAPER2, ACC, 1.4, 8)
d.t(144, Y_ACK + 10, "송신자 자체 클러킹", 14, ACC, KR, "middle", 600)
d.t(144, Y_ACK + 32, "ACK 1개 도착 = 패킷 1개 방출", 11, INK, KR, "middle")

# 새 패킷 P4·P5·P6 주입 (A1~A3 각각에 대응)
for i, name in enumerate(["새 P4", "새 P5", "새 P6"]):
    px = 57 + i * 62
    d.box(px, Y_ACK + 48, 50, 28, PAPER, ACC, 1.2, 4)
    d.t(px + 25, Y_ACK + 66, name, 11, ACC, KR, "middle", 600)

d.t(144, Y_ACK + 92, "병목 속도로 자동 동기화", 11, ACC, KR, "middle", 600)

d.legend(H - 48, [
    ("데이터 패킷", ACC),
    ("병목 지연", WARN),
    ("수신자 ACK", OK),
    ("자체 클러킹", ACC),
])

d.save("16-01.ack-clock.svg")
