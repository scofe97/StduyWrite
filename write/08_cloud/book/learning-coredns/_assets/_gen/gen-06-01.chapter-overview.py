# 06-01 학습 목표 뒤 전체 지도 — 무엇을 선언하면 어떤 레코드가 나오는지를 원서 예의 실제 응답과 함께 놓는다.
# 본문 근거: 이 노트 §4~§8 의 원서 예(Example 6-1·6-4·6-5·6-7·6-9·6-10)와 DNS 명세 §2.3·§2.4.
# 타입 스펙: type-dp-security-matrix — 선언(행) × 생기는 레코드·실제 응답(열) 격자가 논지다.
#           2026-10-03 절 제목을 이은 노드 사슬에서 실제 값이 든 격자로 다시 그렸다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 640
d = D(W, H, "LEARNING COREDNS · 06-01",
      "무엇을 선언하면 어떤 레코드가 나오는가",
      "Service 종류, 포트 이름, 워크로드 종류가 레코드의 개수와 이름을 정한다. "
      "오른쪽 열은 원서 예제가 실제로 받은 응답이다.",
      "주황 행이 이 편 전체의 갈림길입니다")

COLS = [(20, 200, "선언"), (230, 250, "생기는 레코드"), (490, 270, "원서 예의 응답"), (770, 90, "절")]
rows = [
    (("ClusterIP Service", ""), ("A 하나 · PTR 하나", "이름 붙은 포트마다 SRV 하나"), ("hello-world.default.svc", "A 10.0.0.100"), "§4 · §5"),
    (("헤드리스 Service", "clusterIP: None"), ("Ready 엔드포인트마다 A", "Ready 0 이면 NXDOMAIN"), ("headless.default.svc", "A 10.5.88.4 외 셋"), "§4 · §5"),
    (("이름 붙은 포트", ""), ("헤드리스는 엔드포인트 × 포트", "이름 없는 포트는 SRV 없음"), ("_http._tcp.headless", "SRV 0 25 80 넷"), "§6"),
    (("Deployment + hostname", ""), ("대상 이름이 하나로 뭉침", ""), ("myhost.headless", "A 넷이 한 이름에"), "§7"),
    (("StatefulSet", ""), ("서수 이름 · 재생성에도 유지", ""), ("headless-0 … headless-3", "IP 만 바뀜"), "§7"),
    (("파드 A 레코드", "명세 이전 kube-dns"), ("현행 명세에서 빠짐", "CoreDNS pods 옵션으로만"), ("a-b-c-d.ns.pod", "존재 확인 없이 응답"), "§8"),
]
FOCAL = 1
Y0, PITCH, RH = 132, 64, 56

for x, w, head in COLS:
    d.t(x + 12, 118, head, 12, SOFT, KR, "start", 600)

for i, cells in enumerate(rows):
    y = Y0 + i * PITCH
    if i == FOCAL:
        d.tone(16, y - 2, 848, RH + 4, ACC, 8, "12", 1.4)
    for k, (x, w, _) in enumerate(COLS):
        if i != FOCAL:
            d.box(x, y, w, RH, PAPER2, RULE, 1.0, 6)
        cell = cells[k]
        if k == 3:
            d.t(x + w / 2, y + 34, cell, 13, ACC if i == FOCAL else MUTED, KR)
            continue
        main, sub = cell
        fam = MONO if (k == 2) else KR
        size = 13 if k == 2 else 14
        col = ACC if (i == FOCAL and k == 0) else INK
        if sub:
            d.t(x + 12, y + 24, main, size, col, fam, "start", 600)
            d.t(x + 12, y + 44, sub, 12, MUTED, KR, "start")
        else:
            d.t(x + 12, y + 34, main, size, col, fam, "start", 600)

d.t(20, 544, "1~3절 · 선언과 Service 가 왜 필요한가 · 조정 루프 · watch · 파드 IP 변동", 13, MUTED, KR, "start")
d.t(20, 568, "원서 예의 TTL 5초 · kubeadm 기본 Corefile 은 ttl 30", 13, MUTED, KR, "start")

d.legend(592, [("이 편의 갈림길", ACC)])
d.save("06-01.chapter-overview.svg")
