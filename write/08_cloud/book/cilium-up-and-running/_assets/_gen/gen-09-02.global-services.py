# 타입 스펙: type-data-flow — 세 클러스터의 백엔드 Pod → eBPF 전역 서비스 맵 취합 → kind-green 에서 curl 호출 시 무작위 부하 분산 흐름.
# 사실 출처: Cilium Up and Running 9장 cil9.txt 줄 781-794(global-service.yaml), 816-840(curl nginx 8회 응답: blue-worker 4회, red-worker 3회, green-worker2 1회)
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 390
CW, GAP, X0 = 264, 38, 26
XS = [X0 + i * (CW + GAP) for i in range(3)]
Y_HDR, H_HDR = 96, 36
Y0, ROW_H = 150, 206

d = D(W, H, "CILIUM UP AND RUNNING · 09-02 §1", "전역 서비스 백엔드 취합과 요청 분산",
      "각 클러스터의 백엔드가 하나의 eBPF 엔드포인트 풀로 모여 무작위 분산된다",
      "각 클러스터의 백엔드가 하나의 eBPF 엔드포인트 풀로 모여 무작위 분산된다")

headers = [
    ("클러스터별 백엔드", "Pod IP & Node"),
    ("eBPF 전역 서비스 풀", "service.cilium.io/global"),
    ("curl 8회 호출 응답 분포", "예시 실습 결과 (kind-green)")
]

for x, (title, sub) in zip(XS, headers):
    d.box(x, Y_HDR, CW, H_HDR, PAPER2, SOFT, 1.0)
    d.t(x + CW / 2, Y_HDR + 18, title, 12, INK, KR, "middle", 600)
    sfam = KR if any("가" <= c <= "힣" for c in sub) else MONO
    d.t(x + CW / 2, Y_HDR + 31, sub, 11, MUTED, sfam)

# 1. 클러스터별 백엔드
d.box(XS[0], Y0, CW, ROW_H, PAPER2, RULE, 0.9)
d.box(XS[0] + 12, Y0 + 16, CW - 24, 50, PAPER, RULE, 0.8)
d.t(XS[0] + CW / 2, Y0 + 36, "kind-red · red-worker", 12, INK, MONO)
d.t(XS[0] + CW / 2, Y0 + 54, "Pod: nginx (port 8080)", 11, MUTED, MONO)

d.box(XS[0] + 12, Y0 + 76, CW - 24, 50, PAPER, RULE, 0.8)
d.t(XS[0] + CW / 2, Y0 + 96, "kind-green · green-worker2", 12, OK, MONO)
d.t(XS[0] + CW / 2, Y0 + 114, "Pod: nginx (port 8080)", 11, MUTED, MONO)

d.box(XS[0] + 12, Y0 + 136, CW - 24, 50, PAPER, RULE, 0.8)
d.t(XS[0] + CW / 2, Y0 + 156, "kind-blue · blue-worker", 12, INK, MONO)
d.t(XS[0] + CW / 2, Y0 + 174, "Pod: nginx (port 8080)", 11, MUTED, MONO)

# 화살표 0 -> 1
d.arrow([(XS[0] + CW + 4, Y0 + ROW_H / 2), (XS[1] - 6, Y0 + ROW_H / 2)], MUTED, "ar", 1.4)

# 2. eBPF 전역 서비스 풀 (focal)
d.tone(XS[1], Y0, CW, ROW_H, ACC, r=6, op="12", sw=1.3)
d.t(XS[1] + CW / 2, Y0 + 26, "ClusterIP : nginx", 12, ACC, MONO, "middle", 600)
d.t(XS[1] + CW / 2, Y0 + 44, "로컬 eBPF 서비스 맵", 11, MUTED, MONO)

d.box(XS[1] + 12, Y0 + 58, CW - 24, 134, PAPER, RULE, 0.8)
d.t(XS[1] + CW / 2, Y0 + 78, "통합 백엔드 엔드포인트 3개", 12, INK, KR)
d.line(XS[1] + 24, Y0 + 88, XS[1] + CW - 24, Y0 + 88, RULE, 0.6)
d.t(XS[1] + 28, Y0 + 108, "1. red-worker:8080", 11, INK, MONO, "start")
d.t(XS[1] + 28, Y0 + 132, "2. green-worker2:8080", 11, OK, MONO, "start")
d.t(XS[1] + 28, Y0 + 156, "3. blue-worker:8080", 11, INK, MONO, "start")
d.t(XS[1] + CW / 2, Y0 + 179, "요청마다 무작위로 선택", 11, MUTED, KR)

# 화살표 1 -> 2
d.arrow([(XS[1] + CW + 4, Y0 + ROW_H / 2), (XS[2] - 6, Y0 + ROW_H / 2)], MUTED, "ar", 1.4)

# 3. 실측 응답 분포
d.box(XS[2], Y0, CW, ROW_H, PAPER2, RULE, 0.9)
d.box(XS[2] + 12, Y0 + 16, CW - 24, 50, PAPER, RULE, 0.8)
d.t(XS[2] + CW / 2, Y0 + 36, "blue-worker 응답: 4회", 12, INK, KR)
d.t(XS[2] + CW / 2, Y0 + 54, "1·3·5·6회차 수신 (50%)", 11, MUTED, KR)

d.box(XS[2] + 12, Y0 + 76, CW - 24, 50, PAPER, RULE, 0.8)
d.t(XS[2] + CW / 2, Y0 + 96, "red-worker 응답: 3회", 12, INK, KR)
d.t(XS[2] + CW / 2, Y0 + 114, "2·4·8회차 수신 (37.5%)", 11, MUTED, KR)

d.box(XS[2] + 12, Y0 + 136, CW - 24, 50, PAPER, RULE, 0.8)
d.t(XS[2] + CW / 2, Y0 + 156, "green-worker2 응답: 1회", 12, OK, KR)
d.t(XS[2] + CW / 2, Y0 + 174, "7회차 수신 (12.5%)", 11, MUTED, KR)

d.save("09-02.global-services.svg")
