# 타입 스펙: type-state — TCP 혼잡 제어의 세 상태(느린 시작 · 혼잡 회피 · 빠른 회복)와 사건별 전이.
# 사실 출처: ch16.txt 480~650행 — ssthresh 분기(cwnd < ssthresh vs cwnd ≥ ssthresh), 중복 ACK 3개(빠른 재전송/회복), RTO 만료, 새 ACK 복귀.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, INFO, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 500
d = D(W, H, "TCP/IP ILLUSTRATED VOL.1 · 16-01 §4",
      "TCP 혼잡 제어의 세 상태와 전이 조건",
      "연결 수립과 RTO 만료 뒤에는 느린 시작에서 cwnd 를 지수적으로 키운다. cwnd 가 ssthresh 에 도달하면 혼잡 회피로 전이해 선형 증가한다. 3개 중복 ACK 로 손실을 감지하면 빠른 회복에 진입하고 새 ACK 로 혼잡 회피로 복귀한다.",
      "임계값 도달과 손실 피드백이 세 상태 사이의 전이를 결정합니다")

# 세 상태 박스 좌표 (박스 폭 축소 및 간격 100px 확보)
X_SS, Y_SS, W_SS, H_SS = 44, 150, 206, 150
X_CA, Y_CA, W_CA, H_CA = 356, 150, 218, 150
X_FR, Y_FR, W_FR, H_FR = 670, 150, 206, 150

# 시작 진입 화살표 (연결 수립)
d.arrow([(X_SS + W_SS // 2, 96), (X_SS + W_SS // 2, Y_SS - 4)], OK, "ok", 1.4)
d.t(X_SS + W_SS // 2, 88, "연결 시작 (cwnd = IW)", 11, OK, KR, "middle", 600)

# 1. 느린 시작 박스
d.box(X_SS, Y_SS, W_SS, H_SS, PAPER2, OK, 1.2, 8)
d.t(X_SS + W_SS // 2, Y_SS + 26, "느린 시작", 14, OK, KR, "middle", 600)
d.chip(X_SS + W_SS // 2, Y_SS + 54, "cwnd < ssthresh", OK, 11)
d.t(X_SS + W_SS // 2, Y_SS + 86, "ACK 마다 +SMSS", 11, INK, KR, "middle")
d.t(X_SS + W_SS // 2, Y_SS + 108, "매 왕복 2배 지수 증가", 11, MUTED, KR, "middle")
d.t(X_SS + W_SS // 2, Y_SS + 130, "미확인 대역폭 탐색", 11, SOFT, KR, "middle")

# 2. 혼잡 회피 박스 (초점)
d.o.append(f'<rect x="{X_CA}" y="{Y_CA}" width="{W_CA}" height="{H_CA}" rx="8" fill="{ACC}12" stroke="{ACC}" stroke-width="1.6"/>')
d.t(X_CA + W_CA // 2, Y_CA + 26, "혼잡 회피", 14, ACC, KR, "middle", 600)
d.chip(X_CA + W_CA // 2, Y_CA + 54, "cwnd ≥ ssthresh", ACC, 11)
d.t(X_CA + W_CA // 2, Y_CA + 86, "왕복당 +1 SMSS", 11, INK, KR, "middle")
d.t(X_CA + W_CA // 2, Y_CA + 108, "cwnd += SMSS²/cwnd", 11, ACC, MONO, "middle")
d.t(X_CA + W_CA // 2, Y_CA + 130, "보수적 선형 탐색 (AIMD)", 11, SOFT, KR, "middle")

# 3. 빠른 회복 박스
d.box(X_FR, Y_FR, W_FR, H_FR, PAPER2, WARN, 1.2, 8)
d.t(X_FR + W_FR // 2, Y_FR + 26, "빠른 회복", 14, WARN, KR, "middle", 600)
d.chip(X_FR + W_FR // 2, Y_FR + 54, "손실 패킷 재전송", WARN, 11)
d.t(X_FR + W_FR // 2, Y_FR + 86, "중복 ACK 마다 부풀리기", 11, INK, KR, "middle")
d.t(X_FR + W_FR // 2, Y_FR + 108, "ssthresh = 비행/2", 11, WARN, KR, "middle")
d.t(X_FR + W_FR // 2, Y_FR + 130, "파이프 보존하며 복구", 11, SOFT, KR, "middle")

# 전이 화살표 1: 느린 시작 → 혼잡 회피
d.arrow([(X_SS + W_SS, Y_SS + 50), (X_CA - 4, Y_CA + 50)], ACC, "acc", 1.4)
d.t((X_SS + W_SS + X_CA) // 2, Y_SS + 38, "cwnd ≥ ssthresh", 11, ACC, MONO, "middle", 600)

# 전이 화살표 1b: 느린 시작 → 빠른 회복 (느린 시작 중 3개 중복 ACK 발생 시 상단 경로)
d.path(f"M {X_SS + W_SS - 24} {Y_SS - 2} "
       f"L {X_SS + W_SS - 24} 114 "
       f"L {X_FR + 24} 114 "
       f"L {X_FR + 24} {Y_FR - 4}",
       WARN, 1.3, m="warn")
d.t((X_SS + W_SS - 24 + X_FR + 24) // 2, 106, "중복 ACK 3개 (빠른 재전송)", 11, WARN, KR, "middle", 600)

# 전이 화살표 2: 혼잡 회피 → 빠른 회복 (순방향, 상단 y=190)
d.arrow([(X_CA + W_CA, Y_CA + 40), (X_FR - 4, Y_FR + 40)], WARN, "warn", 1.4)
d.t((X_CA + W_CA + X_FR) // 2, Y_CA + 28, "중복 ACK 3개", 11, WARN, KR, "middle", 600)

# 전이 화살표 3: 빠른 회복 → 혼잡 회피 (복구 완료 역방향, 하단 y=250)
d.arrow([(X_FR, Y_FR + 100), (X_CA + W_CA + 4, Y_CA + 100)], OK, "ok", 1.4)
d.t((X_CA + W_CA + X_FR) // 2, Y_FR + 122, "새 ACK (복구)", 11, OK, KR, "middle", 600)

# 전이 화살표 4: 하단 RTO 타임아웃 (혼잡 회피 → 느린 시작)
d.path(f"M {X_CA + W_CA // 2} {Y_CA + H_CA + 2} "
       f"L {X_CA + W_CA // 2} {Y_CA + H_CA + 34} "
       f"L {X_SS + W_SS // 2 + 25} {Y_CA + H_CA + 34} "
       f"L {X_SS + W_SS // 2 + 25} {Y_SS + H_SS + 6}",
       BAD, 1.4, m="bad", dash="4 4")
d.t((X_SS + W_SS // 2 + X_CA + W_CA // 2) // 2, Y_CA + H_CA + 26, "RTO 만료 (cwnd = 1)", 11, BAD, KR, "middle", 600)

# 전이 화살표 5: 빠른 회복 → 느린 시작 (RTO 만료)
d.path(f"M {X_FR + W_FR // 2} {Y_FR + H_FR + 2} "
       f"L {X_FR + W_FR // 2} {Y_CA + H_CA + 60} "
       f"L {X_SS + W_SS // 2 - 25} {Y_CA + H_CA + 60} "
       f"L {X_SS + W_SS // 2 - 25} {Y_SS + H_SS + 6}",
       BAD, 1.4, m="bad", dash="4 4")
d.t(W // 2, Y_CA + H_CA + 78, "회복 중 RTO 만료 (파이프 동결, cwnd = 1)", 11, BAD, KR, "middle")

d.legend(H - 48, [
    ("정상 전이", ACC),
    ("중복 ACK 복구", WARN),
    ("새 ACK 완료", OK),
    ("RTO 재시작", BAD),
])

d.save("16-01.congestion-state-machine.svg")
