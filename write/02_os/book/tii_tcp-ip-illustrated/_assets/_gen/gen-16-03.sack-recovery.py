# 타입 스펙: type-sequence — 빠른 재전송과 SACK 복구 흐름 (사건 2).
# 사실 출처: ch16.txt 1099, 1132-1133, 1650~1768행 — 호스트 주소, 패킷 871~950 SACK 교환, seq 690201 빠른 재전송, 회복 지점 763000, 부분 ACK 7개, ACK 765801.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, OK, WARN, BAD, INFO, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 920, 540
s = Seq(W, H, "TCP/IP ILLUSTRATED VOL.1 · 16-03",
        "빠른 재전송과 SACK 복구 흐름 (사건 2)",
        "단일 중복 ACK의 SACK 블록으로 즉시 재전송하고 회복 지점을 넘을 때까지 복구를 유지합니다.",
        "수신 버퍼 블록을 근거로 구멍을 메우며 cwnd를 47에서 20으로 줄입니다")

s.lanes([("송신자 (Linux 2.6)", "adsl-63-203-72-138 · FACK"), ("수신자 (FreeBSD 5.4)", "128.32.37.219:6666 · SACK")], y0=100, lane_w=220)
s.rails(H - 60)

# 메시지 및 상태 흐름
# 1. 패킷 871 수신
s.msg("수신자 (FreeBSD 5.4)", "송신자 (Linux 2.6)", "ACK 690201 + SACK [698601,700001]", 170, WARN, "warn", sub="패킷 871 (t=21.209s) · 1개 블록 보고")

# 2. 송신자 Recovery 진입
s.selfmsg("송신자 (Linux 2.6)", "Recovery 진입 · 회복 지점 763000 설정", 205, BAD, "ssthresh=26 · cwnd=47 (FACK 6개 유실 추정)")

# 3. 빠른 재전송
s.msg("송신자 (Linux 2.6)", "수신자 (FreeBSD 5.4)", "빠른 재전송: seq 690201 (1400B)", 250, BAD, "bad", sub="누적 미수신 구간의 첫 패킷 재전송")

# 4. 수신자의 중복 ACK 및 SACK 확장
s.msg("수신자 (FreeBSD 5.4)", "송신자 (Linux 2.6)", "ACK 690201 + SACK [702801,763001] 외", 300, INFO, "info", sub="중복 ACK 44개 및 후속 SACK (패킷 871~950 구간)")

# 5. 송신자 복구 동작
s.selfmsg("송신자 (Linux 2.6)", "추가 7회 재전송 및 새 데이터 주입", 340, ACC, "ACK 2개당 cwnd 1 감소 (47 → 20 수축)")

# 6. 부분 ACK 7회
s.msg("수신자 (FreeBSD 5.4)", "송신자 (Linux 2.6)", "부분 ACK 7회 도착 (두 블록 5, 한 블록 2)", 385, MUTED, "ar", sub="회복 지점 이전 · Recovery 유지")

# 7. 최종 회복 ACK
s.msg("수신자 (FreeBSD 5.4)", "송신자 (Linux 2.6)", "누적 ACK 765801 수신 (t=23.301s)", 435, OK, "ok", sub="회복 지점 763000 초과 · 손실 복구 완료")

# 8. 정상 복귀
s.selfmsg("송신자 (Linux 2.6)", "느린 시작 거쳐 Open(혼잡 회피) 복귀", 470, OK, "t=23.659s cwnd 27 도달 · 정상 선형 증가 재개")

s.save("16-03.sack-recovery.svg")
