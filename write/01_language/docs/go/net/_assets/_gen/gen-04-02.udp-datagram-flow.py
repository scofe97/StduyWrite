# 사실 출처: go doc net.PacketConn, UDPConn, gonet-lab 02-01·02-03 (go1.25.1)
# 타입 스펙: type-data-flow
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 960, 520

d = D(W, H,
      "UDP DATAGRAM RECVFLOW & BUFFER TRUNCATION",
      "UDP 수신 버퍼와 데이터그램 경계 보존·잘림 메커니즘",
      "데이터그램 셋이 커널 수신 큐를 거쳐 ReadFrom 마다 하나씩 꺼내지며 버퍼보다 크면 초과분이 버려진다",
      "스트림과 달리 패킷 경계가 유지되므로 작은 버퍼로 읽을 때 남은 바이트는 다음 호출로 이어지지 않는다")

# ── 1. 수신 단계 3개 열 (도착 데이터그램 -> 커널 수신 큐 -> 애플리케이션 ReadFrom) ──
# 열 1: 도착 패킷 (X=36, W=200)
# 열 2: 커널 수신 소켓 큐 SO_RCVBUF (X=352, W=200)
# 열 3: ReadFrom 수신 버퍼 len(p)=128 (X=720, W=204)

C1_X, C2_X, C3_X = 36, 352, 720
CW = 200
C3W = 204

# 섹션 헤더
d.box(C1_X, 96, CW, 32, fill=PAPER2, stroke=RULE, sw=1.0)
d.t(C1_X + CW // 2, 117, "1. 네트워크 도착 패킷", 12, INK, fam=KR, anchor="middle", weight=600)

d.box(C2_X, 96, CW, 32, fill=PAPER2, stroke=RULE, sw=1.0)
d.t(C2_X + CW // 2, 117, "2. 커널 수신 큐", 12, INK, fam=KR, anchor="middle", weight=600)

d.box(C3_X, 96, C3W, 32, fill=PAPER2, stroke=RULE, sw=1.0)
d.t(C3_X + C3W // 2, 117, "3. ReadFrom 수신 버퍼", 12, INK, fam=KR, anchor="middle", weight=600)

# 행 1: D1 (100B) - 정상 수신
Y1 = 152
H1 = 80
# C1
d.box(C1_X, Y1, CW, H1, fill=PAPER2, stroke=OK, sw=1.0)
d.t(C1_X + 16, Y1 + 28, "데이터그램 #1", 12, OK, fam=KR, anchor="start", weight=600)
d.t(C1_X + 16, Y1 + 52, "크기: 100 바이트", 11, MUTED, fam=KR, anchor="start")

# C1 -> C2 화살표
d.arrow([(C1_X + CW, Y1 + H1 // 2), (C2_X, Y1 + H1 // 2)], MUTED, "ar", 1.2)

# C2
d.box(C2_X, Y1, CW, H1, fill=PAPER2, stroke=RULE, sw=0.9)
d.t(C2_X + 16, Y1 + 28, "큐 헤드 대기", 12, INK, fam=KR, anchor="start", weight=600)
d.t(C2_X + 16, Y1 + 52, "경계 보존 (100B 유지)", 11, MUTED, fam=KR, anchor="start")

# C2 -> C3 화살표
d.arrow([(C2_X + CW, Y1 + H1 // 2), (C3_X, Y1 + H1 // 2)], OK, "ar", 1.2)
d.chip((C2_X + CW + C3_X) // 2, Y1 + H1 // 2 - 14, "1차 ReadFrom", OK, 9)

# C3
d.box(C3_X, Y1, C3W, H1, fill=PAPER2, stroke=OK, sw=1.2)
d.t(C3_X + 16, Y1 + 28, "n = 100 복사 완료", 12, OK, fam=KR, anchor="start", weight=600)
d.t(C3_X + 16, Y1 + 52, "버퍼 여유 28B · 에러 없음", 11, MUTED, fam=KR, anchor="start")

# 행 2: D2 (200B) - 잘림 발생 (FOCAL POINT: ACC 테두리 및 경고)
Y2 = 252
H2 = 92
# C1
d.box(C1_X, Y2, CW, H2, fill=PAPER2, stroke=WARN, sw=1.0)
d.t(C1_X + 16, Y2 + 28, "데이터그램 #2", 12, WARN, fam=KR, anchor="start", weight=600)
d.t(C1_X + 16, Y2 + 52, "크기: 200 바이트", 11, MUTED, fam=KR, anchor="start")

# C1 -> C2 화살표
d.arrow([(C1_X + CW, Y2 + H2 // 2), (C2_X, Y2 + H2 // 2)], MUTED, "ar", 1.2)

# C2
d.box(C2_X, Y2, CW, H2, fill=PAPER2, stroke=RULE, sw=0.9)
d.t(C2_X + 16, Y2 + 28, "큐 중간 대기", 12, INK, fam=KR, anchor="start", weight=600)
d.t(C2_X + 16, Y2 + 52, "경계 보존 (200B 유지)", 11, MUTED, fam=KR, anchor="start")

# C2 -> C3 화살표
d.arrow([(C2_X + CW, Y2 + H2 // 2), (C3_X, Y2 + H2 // 2)], ACC, "ar", 1.4)
d.chip((C2_X + CW + C3_X) // 2, Y2 + H2 // 2 - 14, "2차 ReadFrom", ACC, 9)

# C3 (FOCAL)
d.box(C3_X, Y2, C3W, H2, fill=PAPER2, stroke=ACC, sw=1.4)
d.t(C3_X + 16, Y2 + 26, "n = 128 수신 (잘림 발생)", 12, ACC, fam=KR, anchor="start", weight=600)
d.t(C3_X + 16, Y2 + 48, "초과 72B 커널 즉시 폐기", 11, BAD, fam=KR, anchor="start", weight=600)
d.t(C3_X + 16, Y2 + 70, "에러 반환 없음 (err == nil)", 10, MUTED, fam=KR, anchor="start")

# 행 3: D3 (50B) - 다음 패킷 수신
Y3 = 364
H3 = 80
# C1
d.box(C1_X, Y3, CW, H3, fill=PAPER2, stroke=OK, sw=1.0)
d.t(C1_X + 16, Y3 + 28, "데이터그램 #3", 12, OK, fam=KR, anchor="start", weight=600)
d.t(C1_X + 16, Y3 + 52, "크기: 50 바이트", 11, MUTED, fam=KR, anchor="start")

# C1 -> C2 화살표
d.arrow([(C1_X + CW, Y3 + H3 // 2), (C2_X, Y3 + H3 // 2)], MUTED, "ar", 1.2)

# C2
d.box(C2_X, Y3, CW, H3, fill=PAPER2, stroke=RULE, sw=0.9)
d.t(C2_X + 16, Y3 + 28, "큐 테일 대기", 12, INK, fam=KR, anchor="start", weight=600)
d.t(C2_X + 16, Y3 + 52, "경계 보존 (50B 유지)", 11, MUTED, fam=KR, anchor="start")

# C2 -> C3 화살표
d.arrow([(C2_X + CW, Y3 + H3 // 2), (C3_X, Y3 + H3 // 2)], OK, "ar", 1.2)
d.chip((C2_X + CW + C3_X) // 2, Y3 + H3 // 2 - 14, "3차 ReadFrom", OK, 9)

# C3
d.box(C3_X, Y3, C3W, H3, fill=PAPER2, stroke=OK, sw=1.2)
d.t(C3_X + 16, Y3 + 28, "n = 50 복사 완료", 12, OK, fam=KR, anchor="start", weight=600)
d.t(C3_X + 16, Y3 + 52, "D2 잔여 72B 가 아닌 D3 수신", 11, MUTED, fam=KR, anchor="start")

# 범례
d.legend(474, [
    ("정상 수신", OK),
    ("버퍼 초과 (대용량)", WARN),
    ("잘림 발생 (focal)", ACC),
    ("데이터 유실", BAD)
])

out_name = "04-02.udp-datagram-flow.svg"
out_path = os.path.join(os.path.dirname(__file__), "..", out_name)
d.save(out_path if os.path.exists(os.path.dirname(out_path)) else out_name)
