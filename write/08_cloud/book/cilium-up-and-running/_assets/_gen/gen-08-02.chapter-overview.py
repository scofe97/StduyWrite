# 타입 스펙: type-dp-security-matrix — 행 = DSR·Maglev·netkit 세 기능, 열 = 줄이는 비용·켜는 옵션·전제 조건 비교 행렬. 배정된 비교/행렬 타입이 설치 목록에 없어 비교 행렬 문법을 가진 이 타입으로 선언했다.
# 사실 출처: Cilium Up and Running 8장 cil8.txt 줄 827-843(DSR 옵션·KPR·native), 줄 1082-1095(Maglev 옵션·KPR), 줄 1286-1308(netkit 커널 6.7·L3) / docs.cilium.io v1.20 kubeproxy-free(DSR·Maglev) 및 tuning(netkit 커널 6.8·datapathMode)
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 424
LP, COMP_W, GAP, ROLE_W, ROLE_GAP = 12, 180, 12, 224, 14
HDR_Y, HDR_H = 96, 52
ROW_Y0, ROW_H, STRIDE = 168, 52, 60
RX = [LP + COMP_W + GAP + j * (ROLE_W + ROLE_GAP) for j in range(3)]

d = D(W, H, "CILIUM UP AND RUNNING · 08-02", "DSR · Maglev · netkit 의 비용 절감과 조건",
      "응답 경로 우회·일관 해시 백엔드 선택·Pod veth 네임스페이스 전환 비용을 줄인다",
      "각 기능이 줄이는 병목과 활성화 옵션 및 커널·모드 전제 조건")

d.box(LP, HDR_Y, COMP_W, HDR_H, PAPER2, RULE, 0.9)
d.t(LP + COMP_W / 2, HDR_Y + 24, "최적화 기능", 13, INK, KR, "middle", 600)
d.t(LP + COMP_W / 2, HDR_Y + 42, "feature", 11, MUTED, MONO)

cols = [("줄이는 비용", "cost reduced"), ("켜는 옵션", "helm option"), ("전제 조건", "prerequisites")]
for j, (nm, code) in enumerate(cols):
    d.box(RX[j], HDR_Y, ROLE_W, HDR_H, PAPER2, SOFT, 1.0)
    d.t(RX[j] + ROLE_W / 2, HDR_Y + 24, nm, 13, INK, KR, "middle", 600)
    d.t(RX[j] + ROLE_W / 2, HDR_H + HDR_Y - 10, code, 11, MUTED, MONO)

rows = [
    ("DSR", "Direct Server Return", [
        ("역방향 경유 홉 제거", "출발지 클라이언트 IP 보존", OK),
        ("loadBalancer.mode: dsr", "kubeProxyReplacement: true", None),
        ("KPR 필수 · opt 는 native 전용", "Geneve 는 dsrDispatch=geneve", "focal")]),
    ("Maglev", "Consistent Hashing", [
        ("경로 분기 시 TCP 리셋 방지", "노드 간 상태 동기화 없음", OK),
        ("loadBalancer.algorithm: maglev", "기본 tableSize 16381", None),
        ("KPR 필수 · 5-튜플 유지", "소수 룩업 테이블 크기", None)]),
    ("netkit", "BPF Network Device", [
        ("네임스페이스 전환 비용 감소", "per-CPU 백로그 큐 비용 감소", OK),
        ("bpf.datapathMode: netkit", "기본 L3 모드 (L2 지원)", None),
        ("커널 6.8+ · eBPF Host-Routing", "기존 Pod 인플레이스 불가", "focal")]),
]

for i, (name, hint, cells) in enumerate(rows):
    y = ROW_Y0 + i * STRIDE
    d.box(LP, y, COMP_W, ROW_H, PAPER2, RULE, 0.9, r=4)
    d.t(LP + 14, y + 23, name, 13, INK, KR, "start", 600)
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

LEG_Y = ROW_Y0 + 2 * STRIDE + ROW_H + 24
d.legend(LEG_Y, [("비용 절감 효과", OK), ("주요 전제 조건 제약", ACC)])
d.save("08-02.chapter-overview.svg")
