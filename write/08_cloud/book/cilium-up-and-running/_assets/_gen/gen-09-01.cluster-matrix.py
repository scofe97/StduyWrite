# 타입 스펙: type-dp-security-matrix — 행 = red·green·blue 세 클러스터, 열 = cluster.name·cluster.id·PodCIDR·Node IP 비교 행렬. 배정된 비교 타입 이름이 스펙 목록에 없어 비교 행렬 문법의 이 타입으로 선언했다.
# 사실 출처: Cilium Up and Running 9장 cil9.txt 줄 390-399(Table 9-1 세 클러스터 설정 표), 줄 438-441(노드 IP) / docs.cilium.io v1.20 clustermesh/setup
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W = 920
LP, LBL_W, GAP = 16, 140, 12
COL_WS = [130, 180, 180, 220]
COL_XS = []
cur_x = LP + LBL_W + GAP
for w in COL_WS:
    COL_XS.append(cur_x)
    cur_x += w + GAP

HDR_Y, HDR_H = 104, 48
ROW_Y0, ROW_H, STRIDE = 164, 52, 62

cols = [
    ("고유 ID", "cluster.id"),
    ("Pod IPv4 대역", "PodCIDR (비중복)"),
    ("노드 주소", "InternalIP"),
    ("TLS 내부 도메인", "mesh.cilium.io"),
]

rows = [
    ("red", INFO, [
        ("1", "고유 식별자"),
        ("10.1.0.0/16", "격리 대역"),
        ("10.89.0.14", "컨트롤 플레인"),
        ("red.mesh.cilium.io", "TLS SNI"),
    ]),
    ("green", ACC, [
        ("2", "고유 식별자"),
        ("10.2.0.0/16", "격리 대역"),
        ("10.89.0.16", "컨트롤 플레인"),
        ("green.mesh.cilium.io", "TLS SNI"),
    ]),
    ("blue", OK, [
        ("3", "고유 식별자"),
        ("10.3.0.0/16", "격리 대역"),
        ("10.89.0.20", "컨트롤 플레인"),
        ("blue.mesh.cilium.io", "TLS SNI"),
    ]),
]

LEG_Y = ROW_Y0 + len(rows) * STRIDE + 12
H = LEG_Y + 56

d = D(W, H, "CILIUM UP AND RUNNING · 09-01 §3", "세 테스트 클러스터의 식별자와 네트워크 설정",
      "클러스터마다 이름·ID·Pod 대역이 겹치지 않아야 라우팅과 신원 충돌을 막을 수 있다",
      "예시 실습의 클러스터 설정과 노드 IP 기준")

# 헤더 행
d.box(LP, HDR_Y, LBL_W, HDR_H, PAPER2, RULE, 0.9, 6)
d.t(LP + LBL_W / 2, HDR_Y + 22, "클러스터", 12, INK, KR, "middle", 600)
d.t(LP + LBL_W / 2, HDR_Y + 38, "cluster.name", 11, MUTED, MONO)

for j, (t1, t2) in enumerate(cols):
    cx = COL_XS[j]
    cw = COL_WS[j]
    d.box(cx, HDR_Y, cw, HDR_H, PAPER2, RULE, 0.9, 6)
    d.t(cx + cw / 2, HDR_Y + 22, t1, 12, INK, KR, "middle", 600)
    d.t(cx + cw / 2, HDR_Y + 38, t2, 11, MUTED, MONO)

# 데이터 행
for i, (name, col, cells) in enumerate(rows):
    y = ROW_Y0 + i * STRIDE
    # 행 머리 (클러스터 이름)
    d.tone(LP, y, LBL_W, ROW_H, col, r=6, op="14", sw=1.1)
    d.t(LP + LBL_W / 2, y + 24, name, 13, col, MONO, "middle", 600)
    d.t(LP + LBL_W / 2, y + 42, f"kind-{name}", 11, MUTED, MONO)

    for j, (v1, v2) in enumerate(cells):
        cx = COL_XS[j]
        cw = COL_WS[j]
        d.box(cx, y, cw, ROW_H, PAPER2, RULE, 0.7, 4)
        d.t(cx + cw / 2, y + 24, v1, 12, INK, MONO, "middle", 600)
        d.t(cx + cw / 2, y + 42, v2, 11, MUTED, KR)

d.legend(LEG_Y, [
    ("red 클러스터", INFO),
    ("green 클러스터", ACC),
    ("blue 클러스터", OK),
])
d.save("09-01.cluster-matrix.svg")
