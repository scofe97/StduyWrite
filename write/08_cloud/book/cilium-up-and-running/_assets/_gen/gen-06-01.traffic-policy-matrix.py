# 타입 스펙: type-dp-security-matrix — externalTrafficPolicy Cluster 와 Local 의 백엔드·출발지 IP·로컬 백엔드 부재 시 동작 비교. 배정된 비교 타입 이름이 스펙 목록에 없어 비교 행렬 문법의 이 타입으로 바꿨다
# 사실 출처: 추출본 cil6.txt 줄 773-808(service-A·Node-1·Node-2) / docs.cilium.io v1.20 kubeproxy-free(Client Source IP Preservation)
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W = 920
LP, LBL_W, GAP, COL_W = 12, 196, 12, 340
HDR_Y, HDR_H, ROW_Y0, STRIDE, ROW_H = 96, 40, 148, 52, 44
cols = ["Cluster (기본)", "Local"]
rows = [
    ("고르는 백엔드", "모든 Ready 백엔드", "들어온 노드의 로컬뿐"),
    ("출발지 IP", "들어온 노드 주소로 교체", "클라이언트 IP 보존"),
    ("Node-2 로 들어온 요청", "Node-1 백엔드로 전달", "로컬 백엔드 없음 · 버림"),
    ("추가 홉", "있을 수 있음", "없음"),
]
LEG_Y = ROW_Y0 + (len(rows) - 1) * STRIDE + ROW_H + 24
H = LEG_Y + 48
d = D(W, H, "CILIUM UP AND RUNNING · 06-01 §5", "externalTrafficPolicy 의 두 값",
      "service-A 백엔드는 Node-1 에만 있고 외부 트래픽이 두 노드로 들어옵니다",
      "행 = 항목 · 열 = 정책 값")

def cx(j): return LP + LBL_W + GAP + j * (COL_W + GAP)

d.box(LP, HDR_Y, LBL_W, HDR_H, PAPER2, RULE, 0.9, 6)
d.t(LP + LBL_W / 2, HDR_Y + 25, "항목", 12, INK, KR, "middle", 600)
for j, c in enumerate(cols):
    d.box(cx(j), HDR_Y, COL_W, HDR_H, PAPER2, RULE, 0.9, 6)
    d.t(cx(j) + COL_W / 2, HDR_Y + 25, c, 12, INK, KR if j == 0 and False else MONO, "middle", 600)

for i, (lab, a, b) in enumerate(rows):
    y = ROW_Y0 + i * STRIDE
    d.box(LP, y, LBL_W, ROW_H, PAPER2, RULE, 0.9, 4)
    d.t(LP + 12, y + 27, lab, 12, INK, KR, "start", 600)
    d.tone(cx(0), y, COL_W, ROW_H, INFO, r=4, op="12", sw=1.0)
    d.t(cx(0) + COL_W / 2, y + 27, a, 12, INFO, KR, "middle")
    if i == 2:
        d.tone(cx(1), y, COL_W, ROW_H, ACC, r=4, op="14", sw=1.4)
        d.t(cx(1) + COL_W / 2, y + 27, b, 12, ACC, KR, "middle", 600)
    else:
        d.tone(cx(1), y, COL_W, ROW_H, OK, r=4, op="12", sw=1.0)
        d.t(cx(1) + COL_W / 2, y + 27, b, 12, OK, KR, "middle")

d.legend(LEG_Y, [("Cluster", INFO), ("Local", OK), ("외부 트래픽을 버리는 경우", ACC)])
d.save("06-01.traffic-policy-matrix.svg")
