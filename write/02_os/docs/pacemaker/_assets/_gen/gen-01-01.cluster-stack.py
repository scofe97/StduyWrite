# 타입 스펙: type-layers — 고가용성 클러스터 스택의 4계층 구조. 상위 리소스부터 하위 하드웨어 펜싱 장비까지 4개 층. focal 은 리소스 관리 총괄 계층인 Pacemaker.
# 사실 출처: ClusterLabs Pacemaker Explained 2.1 §1.2.1 Cluster Architecture, §1.2.2 Pacemaker Architecture, Corosync man votequorum(5)
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dd import D, ACC, OK, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 432
LX, LW, LH, Y0 = 84, 764, 64, 108
d = D(W, H, "02_OS / PACEMAKER · 01-01 §1", "고가용성 클러스터 스택의 계층 구조",
      "Corosync 의 통신·쿼럼 위에 Pacemaker 의 상태 제어와 리소스 에이전트가 동작한다.",
      lead="서비스와 리소스 에이전트부터 하드웨어 펜싱 장비까지 계층별 책임 분담")

layers = [
    ("L4", "리소스 및 에이전트", "ocf:heartbeat:IPaddr2 · systemd · OCF 스크립트", False),
    ("L3", "Pacemaker 리소스 관리자", "CIB · schedulerd · controld (DC) · execd · fenced", True),
    ("L2", "Corosync 멤버십 및 쿼럼", "Totem 프로토콜 · votequorum · two_node · wait_for_all", False),
    ("L1", "인프라 및 펜싱 장비", "서버 노드 · L2 스위치 · IPMI · iLO · PDU 전원 제어", False),
]

for i, (tag, name, sub, focal) in enumerate(layers):
    y = Y0 + i * LH
    if focal:
        d.tone(LX, y, LW, LH, ACC, r=0, op="14", sw=1.4)
    else:
        d.box(LX, y, LW, LH, PAPER2 if i % 2 == 0 else PAPER, RULE, 0.8, r=0)
    cy = y + LH / 2
    d.t(LX + 16, cy + 4, tag, 13, ACC if focal else SOFT, MONO, "start")
    d.t(LX + 68, cy + 6, name, 15, ACC if focal else INK, KR, "start", 600)
    sfam = KR if any("가" <= c <= "힣" for c in sub) else MONO
    d.t(LX + LW - 16, cy + 5, sub, 13, MUTED, sfam, "end")

# 왼쪽 여백: 서비스 → 인프라 방향
d.t(42, Y0 + 20, "서비스", 13, MUTED, KR)
d.arrow([(42, Y0 + 36), (42, Y0 + 4 * LH - 36)], MUTED, "ar", 1.4)
d.t(42, Y0 + 4 * LH - 16, "인프라", 13, MUTED, KR)

out_path = os.path.join(os.path.dirname(__file__), "..", "01-01.cluster-stack.svg")
d.save(out_path)
print("ok generated 01-01.cluster-stack.svg")
