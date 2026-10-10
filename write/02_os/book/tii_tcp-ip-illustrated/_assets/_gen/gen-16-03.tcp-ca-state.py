# 타입 스펙: type-state — Linux TCP의 다섯 가지 혼잡 제어 상태(TCP_CA_Open/Disorder/CWR/Recovery/Loss)와 전이 조건.
# 사실 출처: ch16.txt 1468, 1657, 1676, 1799, 1813, 1852, 1892, 1943행 및 include/uapi/linux/tcp.h enum tcp_ca_state.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, INFO, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 920, 500
d = D(W, H, "TCP/IP ILLUSTRATED VOL.1 · 16-03",
      "Linux 송신자의 다섯 가지 혼잡 상태 전이",
      "Open·Disorder·CWR·Recovery·Loss 사이를 오가며 창을 줄이고 타임아웃 오류 시 되돌립니다.",
      "실험의 11개 사건이 각 전이 경로를 그대로 밟습니다")

NW, NH = 160, 60
NODES = {
    "Open": (380, 120, "Open (0)", "정상 혼잡 회피", OK),
    "Disorder": (680, 120, "Disorder (1)", "순서 어긋남 감지", INFO),
    "Recovery": (680, 310, "Recovery (3)", "빠른 재전송 복구", BAD),
    "CWR": (80, 215, "CWR (2)", "창 축소 진행", WARN),
    "Loss": (380, 320, "Loss (4)", "RTO 만료 재시작", BAD),
}

for name, (x, y, title, desc, color) in NODES.items():
    d.box(x, y, NW, NH, PAPER2, color, 1.2, 8)
    d.t(x + NW // 2, y + 26, title, 13, color, MONO, "middle", 600)
    d.t(x + NW // 2, y + 46, desc, 11, MUTED, KR, "middle")

# 1. Open -> Disorder
d.arrow([(540, 135), (676, 135)], INFO, "info", 1.3)
d.t(610, 125, "중복 ACK [4,8]", 11, INFO, KR, "middle")

# 2. Disorder -> Open
d.arrow([(676, 160), (544, 160)], OK, "ok", 1.3)
d.t(548, 190, "누적 ACK 수신", 11, MUTED, KR, "start")

# 3. Disorder -> Recovery
d.arrow([(760, 180), (760, 306)], BAD, "bad", 1.3)
d.t(768, 245, "중복 ACK 누적 [4,8]", 11, BAD, KR, "start")

# 4. Open -> Recovery (사건 2: 단일 중복 ACK + SACK으로 직행, 직교 맨해튼 경로)
d.arrow([(540, 170), (640, 170), (640, 325), (676, 325)], BAD, "bad", 1.3)
d.t(648, 250, "SACK 즉시", 11, BAD, KR, "start")
d.t(648, 264, "판정 [2]", 11, BAD, KR, "start")

# 5. Recovery -> Open (상단 우회 맨해튼 라우팅)
d.arrow([(840, 340), (872, 340), (872, 75), (460, 75), (460, 116)], OK, "ok", 1.3)
d.t(610, 65, "회복 지점 도달 [2,4,8]", 11, OK, KR, "middle")

# 6. Open -> CWR
d.arrow([(380, 140), (160, 140), (160, 211)], WARN, "warn", 1.3)
d.t(270, 130, "로컬 큐 포화 [1,3,5,6,9]", 11, WARN, KR, "middle")

# 7. CWR -> Open
d.arrow([(240, 230), (270, 230), (270, 165), (376, 165)], OK, "ok", 1.3)
d.t(215, 192, "cwnd<=ssthresh", 11, OK, KR, "middle")
d.t(215, 206, "[1,3,5]", 11, OK, KR, "middle")

# 8. CWR -> Loss (CWR 진행 중 RTO 만료)
d.arrow([(160, 275), (160, 350), (376, 350)], BAD, "bad", 1.3)
d.t(265, 365, "CWR 중 RTO 만료 [7,10]", 11, BAD, KR, "middle")

# 9. Open -> Loss (실제 손실 타임아웃)
d.arrow([(400, 180), (400, 316)], BAD, "bad", 1.3)
d.t(392, 248, "RTO 만료 [11]", 11, BAD, KR, "end")

# 10. Loss -> Open (헛 RTO 되돌리기)
d.arrow([(450, 320), (450, 184)], OK, "ok", 1.3, dash="4 4")
d.t(458, 235, "헛 RTO 취소", 11, OK, KR, "start")
d.t(458, 249, "[7,10]", 11, OK, KR, "start")

# 11. Loss -> Open (느린 시작 완료)
d.arrow([(535, 320), (535, 184)], OK, "ok", 1.3)
d.t(543, 270, "느린 시작 완료", 11, OK, KR, "start")
d.t(543, 284, "[11]", 11, OK, KR, "start")

# 범례
d.legend(H - 44, [
    ("정상 (Open)", OK),
    ("어긋남 (Disorder)", INFO),
    ("로컬 제동 (CWR)", WARN),
    ("복구 (Recovery)", BAD),
])

d.save("16-03.tcp-ca-state.svg")
