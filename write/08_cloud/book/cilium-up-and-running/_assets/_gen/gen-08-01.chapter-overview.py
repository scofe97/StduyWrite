# 타입 스펙: type-dp-security-matrix — 행 = 기본 분산 · Service Traffic Distribution · LRP 세 정책, 열 = 트래픽 도달 범위 · 전달 백엔드 위치 · 절감 비용 비교 행렬. 배정된 비교(comparison) 타입이 설치 목록에 없어 비교 행렬 문법을 가진 이 타입으로 선언했다.
# 사실 출처: Cilium Up and Running 8장 cil8.txt 줄 46-56(STD·LRP 개요), 줄 164-169(zone-a: kind-worker·kind-worker2, zone-b: kind-worker3·kind-worker4), 줄 238-245(STD 동일 존 유지), 줄 403-406·482-484(LRP 동일 노드 echo-server-pvkgf 10.0.2.27 전달) / docs.cilium.io v1.20 local-redirect-policy 및 kubeproxy-free
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 424
LP, COMP_W, GAP, ROLE_W, ROLE_GAP = 16, 210, 12, 214, 12
HDR_Y, HDR_H = 96, 52
ROW_Y0, ROW_H, STRIDE = 168, 52, 60
RX = [LP + COMP_W + GAP + j * (ROLE_W + ROLE_GAP) for j in range(3)]

d = D(W, H, "CILIUM UP AND RUNNING · 08-01", "서비스 트래픽 제어 정책 비교",
      "기본 분산 · 존 인지 분산 · 노드 로컬 리다이렉트의 트래픽 도달 범위 비교",
      "각 정책별 트래픽 도달 범위와 백엔드 선택 기준 및 절감 비용")

d.box(LP, HDR_Y, COMP_W, HDR_H, PAPER2, RULE, 0.9)
d.t(LP + COMP_W / 2, HDR_Y + 24, "트래픽 제어 정책", 13, INK, KR, "middle", 600)
d.t(LP + COMP_W / 2, HDR_Y + 42, "routing policy", 11, MUTED, MONO)

cols = [("트래픽 도달 범위", "routing scope"), ("선택 백엔드 위치", "selected backend"), ("네트워크 비용 절감", "cost reduction")]
for j, (nm, code) in enumerate(cols):
    d.box(RX[j], HDR_Y, ROLE_W, HDR_H, PAPER2, SOFT, 1.0)
    d.t(RX[j] + ROLE_W / 2, HDR_Y + 24, nm, 13, INK, KR, "middle", 600)
    d.t(RX[j] + ROLE_W / 2, HDR_H + HDR_Y - 10, code, 11, MUTED, MONO)

rows = [
    ("기본 무작위 분산", "Cluster-wide Random", [
        ("클러스터 전체 백엔드", "무작위 8개 Pod 분산", None),
        ("zone-a · zone-b 전역", "원격 워커 노드 다수 경유", None),
        ("교차 존 · 노드 홉 발생", "지연 증가 및 이그레스 과금", None)]),
    ("존 인지 트래픽 분배", "PreferSameZone", [
        ("동일 가용 영역 우선", "로컬 존 부재 시 타 존 폴백", OK),
        ("zone-a 워커 2대 한정", "kind-worker · kind-worker2", None),
        ("존 간 이그레스 비용 절감", "교차 존 네트워크 지연 단축", OK)]),
    ("노드 로컬 리다이렉트", "Local Redirect Policy", [
        ("동일 노드 백엔드 강제", "소켓 또는 tc eBPF 리다이렉트", OK),
        ("클라이언트 실행 노드 단독", "kind-worker2 로컬 Pod 1대", "focal"),
        ("노드 간 네트워크 홉 제거", "단일 노드 내부 완결 처리", OK)]),
]

for i, (name, hint, cells) in enumerate(rows):
    y = ROW_Y0 + i * STRIDE
    d.box(LP, y, COMP_W, ROW_H, PAPER2, RULE, 0.9, r=4)
    d.t(LP + 14, y + 23, name, 12, INK, KR, "start", 600)
    d.t(LP + 14, y + 41, hint, 11, MUTED, MONO, "start")
    for j, (val, sub, tone) in enumerate(cells):
        x = RX[j]
        if tone == "focal":
            d.tone(x, y, ROLE_W, ROW_H, ACC, r=4, op="14", sw=1.4)
        elif tone == OK:
            d.tone(x, y, ROLE_W, ROW_H, OK, r=4, op="10", sw=0.9)
        else:
            d.box(x, y, ROLE_W, ROW_H, PAPER2, RULE, 0.7, r=4)
        col = ACC if tone == "focal" else (OK if tone == OK else INK)
        fam = KR if any("가" <= c <= "힣" for c in val) else MONO
        d.t(x + ROLE_W / 2, y + 22, val, 12, col, fam, "middle", 600)
        sfam = KR if any("가" <= c <= "힣" for c in sub) else MONO
        d.t(x + ROLE_W / 2, y + 41, sub, 12, MUTED, sfam)

d.save("08-01.chapter-overview.svg")
