# 타입 스펙: type-data-flow — 클러스터별 같은 이름 서비스 선언 → eBPF 전역 백엔드 풀 취합 → affinity 에 따른 백엔드 선택 → 정책의 클러스터 라벨 판정 흐름.
# 사실 출처: Cilium Up and Running 9장 cil9.txt 줄 726-731(global annotation), 853-857(affinity), 1057-1080(policy cluster label), 1214-1235(TLS) / docs.cilium.io v1.20
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

def _kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO

W, H = 920, 420
CW, GAP, X0 = 200, 26, 22
XS = [X0 + i * (CW + GAP) for i in range(4)]
Y_HDR, H_HDR = 96, 36
Y0, ROW_H = 152, 230

d = D(W, H, "CILIUM UP AND RUNNING · 09-02", "전역 서비스와 전역 정책의 처리 흐름",
      "주석으로 묶인 백엔드 목록 취합부터 affinity 선택과 클러스터 라벨 정책 판정까지",
      "주석으로 묶인 백엔드 목록 취합부터 affinity 선택과 클러스터 라벨 정책 판정까지")

headers = [
    ("1. 서비스 선언", "service.cilium.io/global"),
    ("2. 엔드포인트 취합", "로컬 eBPF 서비스 맵"),
    ("3. 친화도 선택", "service.cilium.io/affinity"),
    ("4. 보안 정책 판정", "io.cilium.k8s.policy.cluster"),
]

for x, (title, sub) in zip(XS, headers):
    d.box(x, Y_HDR, CW, H_HDR, PAPER2, SOFT, 1.0)
    d.t(x + CW / 2, Y_HDR + 18, title, 12, INK, KR, "middle", 600)
    d.t(x + CW / 2, Y_HDR + 31, sub, 11 if _kr(sub) == KR else 10, MUTED, _kr(sub))

# 1. 서비스 선언 카드
d.box(XS[0], Y0, CW, ROW_H, PAPER2, RULE, 0.9)
d.t(XS[0] + CW / 2, Y0 + 26, "각 클러스터 서비스", 12, INK, KR, "middle", 600)
d.box(XS[0] + 12, Y0 + 44, CW - 24, 46, PAPER, RULE, 0.8)
d.t(XS[0] + CW / 2, Y0 + 64, "kind-red · nginx", 12, INK, MONO)
d.t(XS[0] + CW / 2, Y0 + 81, "ClusterIP (각자 다름)", 11, MUTED, MONO)

d.box(XS[0] + 12, Y0 + 102, CW - 24, 46, PAPER, RULE, 0.8)
d.t(XS[0] + CW / 2, Y0 + 122, "kind-green · nginx", 12, INK, MONO)
d.t(XS[0] + CW / 2, Y0 + 139, "ClusterIP (각자 다름)", 11, MUTED, MONO)

d.box(XS[0] + 12, Y0 + 160, CW - 24, 46, PAPER, RULE, 0.8)
d.t(XS[0] + CW / 2, Y0 + 180, "kind-blue · nginx", 12, INK, MONO)
d.t(XS[0] + CW / 2, Y0 + 197, "ClusterIP (각자 다름)", 11, MUTED, MONO)

# 화살표 1 -> 2
d.arrow([(XS[0] + CW + 4, Y0 + ROW_H / 2), (XS[1] - 6, Y0 + ROW_H / 2)], MUTED, "ar", 1.4)

# 2. 엔드포인트 취합 카드
d.box(XS[1], Y0, CW, ROW_H, PAPER2, RULE, 0.9)
d.t(XS[1] + CW / 2, Y0 + 26, "전역 엔드포인트 풀", 12, INK, KR, "middle", 600)

d.box(XS[1] + 12, Y0 + 44, CW - 24, 38, PAPER, RULE, 0.8)
d.t(XS[1] + CW / 2, Y0 + 68, "red-worker:8080", 12, INFO, MONO)

d.box(XS[1] + 12, Y0 + 94, CW - 24, 38, PAPER, RULE, 0.8)
d.t(XS[1] + CW / 2, Y0 + 118, "green-worker2:8080", 12, OK, MONO)

d.box(XS[1] + 12, Y0 + 144, CW - 24, 38, PAPER, RULE, 0.8)
d.t(XS[1] + CW / 2, Y0 + 168, "blue-worker:8080", 12, INFO, MONO)

d.t(XS[1] + CW / 2, Y0 + 208, "독립 IP · 엔드포인트 공유", 11, MUTED, KR)

# 화살표 2 -> 3
d.arrow([(XS[1] + CW + 4, Y0 + ROW_H / 2), (XS[2] - 6, Y0 + ROW_H / 2)], MUTED, "ar", 1.4)

# 3. 친화도 선택 카드 (focal)
d.tone(XS[2], Y0, CW, ROW_H, ACC, r=6, op="12", sw=1.3)
d.t(XS[2] + CW / 2, Y0 + 26, "affinity 판정", 12, ACC, KR, "middle", 600)

d.box(XS[2] + 12, Y0 + 46, CW - 24, 68, PAPER, RULE, 0.8)
d.t(XS[2] + CW / 2, Y0 + 68, "affinity=local", 12, OK, MONO)
d.t(XS[2] + CW / 2, Y0 + 88, "green-worker 선택", 12, INK, KR)
d.t(XS[2] + CW / 2, Y0 + 104, "로컬 엔드포인트 우선", 11, MUTED, KR)

d.box(XS[2] + 12, Y0 + 126, CW - 24, 68, PAPER, RULE, 0.8)
d.t(XS[2] + CW / 2, Y0 + 148, "로컬 백엔드 중단 시", 12, ACC, KR)
d.t(XS[2] + CW / 2, Y0 + 168, "원격 풀 자동 폴백", 12, INK, KR)
d.t(XS[2] + CW / 2, Y0 + 184, "blue·red-worker2 전달", 11, MUTED, KR)

# 화살표 3 -> 4
d.arrow([(XS[2] + CW + 4, Y0 + ROW_H / 2), (XS[3] - 6, Y0 + ROW_H / 2)], MUTED, "ar", 1.4)

# 4. 보안 정책 판정 카드
d.box(XS[3], Y0, CW, ROW_H, PAPER2, RULE, 0.9)
d.t(XS[3] + CW / 2, Y0 + 26, "네트워크 정책 검사", 12, INK, KR, "middle", 600)

d.box(XS[3] + 12, Y0 + 46, CW - 24, 68, PAPER, RULE, 0.8)
d.t(XS[3] + CW / 2, Y0 + 68, "출발지 신원 일치", 12, OK, KR)
d.t(XS[3] + CW / 2, Y0 + 88, "cluster: red 라벨 확인", 11, MUTED, MONO)
d.t(XS[3] + CW / 2, Y0 + 104, "트래픽 통과", 12, OK, KR)

d.box(XS[3] + 12, Y0 + 126, CW - 24, 68, PAPER, RULE, 0.8)
d.t(XS[3] + CW / 2, Y0 + 148, "신원 미일치 또는 외부", 12, SOFT, KR)
d.t(XS[3] + CW / 2, Y0 + 168, "nginx 인그레스 정책 불일치", 11, MUTED, KR)
d.t(XS[3] + CW / 2, Y0 + 184, "드롭 (타임아웃)", 12, SOFT, KR)

d.save("09-02.chapter-overview.svg")
