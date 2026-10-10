# 타입 스펙: type-dp-security-matrix — Cluster Mesh mTLS 인증서 4종의 Secret 이름·CN/SAN·통신 주체와 상대·용도 비교 행렬.
# 사실 출처: Cilium Up and Running 9장 cil9.txt 줄 1214-1251(Table 9-2 및 server cert SAN 목록) / docs.cilium.io v1.20 clustermesh setup TLS
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

def _kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO

W, H = 920, 440
LP, GAP = 16, 12
CW = [240, 180, 200, 240]
RX = [LP, LP + CW[0] + GAP, LP + CW[0] + CW[1] + 2 * GAP, LP + CW[0] + CW[1] + CW[2] + 3 * GAP]
HDR_Y, HDR_H = 96, 38
ROW_Y0, ROW_H, STRIDE = 146, 54, 64

d = D(W, H, "CILIUM UP AND RUNNING · 09-02 §4", "Cluster Mesh 내부 통신 mTLS 인증서 4종",
      "API 서버와 etcd 간 상호 인증을 위해 용도별로 분리된 인증서",
      "API 서버와 etcd 간 상호 인증을 위해 용도별로 분리된 인증서")

headers = [
    ("인증서 Secret", "secret name"),
    ("Common Name / SAN", "identity"),
    ("접속 주체 → 상대", "client to target"),
    ("용도", "purpose")
]

for x, w, (nm, code) in zip(RX, CW, headers):
    d.box(x, HDR_Y, w, HDR_H, PAPER2, SOFT, 1.0)
    d.t(x + w / 2, HDR_Y + 20, nm, 12, INK, KR, "middle", 600)
    d.t(x + w / 2, HDR_Y + 34, code, 10, MUTED, MONO)

rows = [
    ("clustermesh-apiserver-admin-cert", "클라이언트",
     "admin-${cluster.name}", "Common Name",
     "API Server → 자체 etcd", "사이드카 관리",
     "자체 etcd 관리", False),
    ("clustermesh-apiserver-remote-cert", "클라이언트",
     "remote-${cluster.name}", "CN · authMode: cluster",
     "API Server → 원격 etcd", "원격 동기화",
     "원격 etcd 상태 동기화", True),
    ("clustermesh-apiserver-local-cert", "클라이언트",
     "local-${cluster.name}", "Common Name",
     "Cilium 에이전트 → 로컬 etcd", "상태 조회",
     "로컬 에이전트 상태 읽기", False),
    ("clustermesh-apiserver-server-cert", "서버 TLS",
     "CN/SAN 다섯 항목", "도메인 3 · IP 2",
     "etcd 인스턴스 (서버)", "클라이언트 3종 수신",
     "서버 신원 증명 및 암호화", False),
]

for i, (sec, cat, cn, cnextra, flow, flowsub, purpose, focal) in enumerate(rows):
    y = ROW_Y0 + i * STRIDE
    # 열 1: Secret 이름
    if focal:
        d.tone(RX[0], y, CW[0], ROW_H, ACC, r=4, op="12", sw=1.3)
        d.t(RX[0] + CW[0] / 2, y + 23, sec, 11, ACC, MONO, "middle", 600)
        d.t(RX[0] + CW[0] / 2, y + 42, cat, 11, MUTED, KR)
    else:
        d.box(RX[0], y, CW[0], ROW_H, PAPER2, RULE, 0.9, r=4)
        d.t(RX[0] + CW[0] / 2, y + 23, sec, 11, INK, MONO, "middle", 600)
        d.t(RX[0] + CW[0] / 2, y + 42, cat, 11, MUTED, KR)

    # 열 2: CN / SAN
    d.box(RX[1], y, CW[1], ROW_H, PAPER2, RULE, 0.8, r=4)
    d.t(RX[1] + CW[1] / 2, y + 23, cn, 11, INK, _kr(cn), "middle", 600)
    d.t(RX[1] + CW[1] / 2, y + 42, cnextra, 11 if _kr(cnextra) == KR else 10, MUTED, _kr(cnextra))

    # 열 3: 통신 주체 -> 상대
    d.box(RX[2], y, CW[2], ROW_H, PAPER2, RULE, 0.8, r=4)
    d.t(RX[2] + CW[2] / 2, y + 23, flow, 11, INK, KR, "middle", 600)
    d.t(RX[2] + CW[2] / 2, y + 42, flowsub, 11, MUTED, KR)

    # 열 4: 용도
    d.box(RX[3], y, CW[3], ROW_H, PAPER2, RULE, 0.8, r=4)
    d.t(RX[3] + CW[3] / 2, y + 33, purpose, 12, OK if not focal else ACC, KR, "middle", 600)

d.save("09-02.tls-certificates.svg")
