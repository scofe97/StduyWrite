# 06-02 학습 목표 뒤 전체 지도 — 질의 여섯 종류가 기본 Corefile 의 어느 줄에서 어떻게 끝나는가.
# 본문 근거: 이 노트 §1(kubernetes 플러그인이 메모리에서 즉석 생성) · §2(cache 이득) · §3(Endpoints · noendpoints NXDOMAIN)
#            · §4(역방향 CIDR · fallthrough · forward) · §5(최장 일치로 corp.example.com:53 블록, 10.0.0.10).
# 타입 스펙: type-dp-security-matrix — 질의(행) × 받는 줄·결과(열) 격자가 논지다.
#           2026-10-03 절 제목을 이은 노드 사슬에서 실제 이름이 든 격자로 다시 그렸다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 640
d = D(W, H, "LEARNING COREDNS · 06-02",
      "질의 하나가 기본 Corefile 의 어느 줄에서 끝나는가",
      "클러스터 안 이름, 헤드리스, 서비스 IP 와 외부 IP 의 PTR, 외부 이름, 사내 이름을 기본 Corefile 에 차례로 물었을 때 "
      "처음 받는 줄과 결과를 적었다. 이 편의 절은 이 여섯 줄을 하나씩 설명한다.",
      "주황 행이 나머지를 설명하는 사실입니다")


def fam(txt):
    return KR if any("가" <= c <= "힣" for c in txt) else MONO


COLS = [(20, 300, "질의"), (330, 170, "받는 줄"), (510, 260, "결과"), (780, 80, "절")]
rows = [
    (("orders.default.svc.cluster.local", "A · 서비스"), ("kubernetes", "Services 메모리"), ("즉석에서 만든 응답", "cache 30 의 이득은 작음"), "§1 · §2"),
    (("web-0.nginx.default.svc.cluster.local", "A · 헤드리스"), ("kubernetes", "Endpoints watch"), ("파드 IP 여럿", "noendpoints 면 NXDOMAIN"), "§3"),
    (("10.7.240.10 의 PTR", "서비스 CIDR 안"), ("kubernetes", "역방향 존"), ("서비스 이름", ""), "§4"),
    (("8.8.8.8 의 PTR", "클러스터와 무관"), ("forward", "fallthrough 로 넘어옴"), ("상류의 PTR 응답", "fallthrough 없으면 NXDOMAIN"), "§4"),
    (("www.example.org", "A · 외부 이름"), ("forward", "/etc/resolv.conf"), ("상류 응답", "cache 30 이 실제로 일함"), "§2 · §4"),
    (("host.corp.example.com", "A · 사내 이름"), ("corp.example.com:53", "최장 일치 블록"), ("10.0.0.10 의 응답", ""), "§5"),
]
FOCAL = 0
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
        size = 12 if (k == 0 and fam(main) == MONO) else 13 if fam(main) == MONO else 14
        col = ACC if (i == FOCAL and k == 0) else INK
        if sub:
            d.t(x + 12, y + 24, main, size, col, fam(main), "start", 600)
            d.t(x + 12, y + 44, sub, 12, MUTED, fam(sub) if not sub.startswith("/") else MONO, "start")
        else:
            d.t(x + 12, y + 34, main, size, col, fam(main), "start", 600)

d.t(20, 544, "1~3절 · 플러그인이 메모리에서 답하는 방식 · 4절 · 열두 줄이 질의를 나누는 자리", 13, MUTED, KR, "start")
d.t(20, 568, "5절 · 서버 블록을 하나 더 · 6절 · 지금은 없는 federation", 13, MUTED, KR, "start")

d.legend(592, [("레코드를 쌓아 두지 않는다", ACC)])
d.save("06-02.chapter-overview.svg")
