# 타입 스펙: type-timeline — 2014년 커널 eBPF 병합부터 CNCF 졸업과 엔터프라이즈 채택까지.
# 사실 출처: Cilium Up and Running 1장 Origins and Evolution · Industry Adoption · CNCF 공식 발표 · Cisco 뉴스룸.
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 480
d = D(W, H, "CILIUM UP AND RUNNING · 01-01 §2", "Cilium 발전 타임라인 (2014–2026)",
      "초기 eBPF 기술 탄생부터 하이퍼스케일러 채택, CNCF 졸업 및 엔터프라이즈 표준 도약 과정",
      "2015년 첫 커밋에서 출발해 클라우드 네이티브 네트워킹의 졸업 표준이 되었습니다")

Y_BASE = 248

# 기준선 (Baseline)
d.line(40, Y_BASE, 880, Y_BASE, RULE, sw=1.2)

# 연도 틱 및 이벤트
# (x, date_str, is_above, title, sub, color, focal)
events = [
    (68, "2014", True, "eBPF 커널 병합", "K8s 오픈소스 공개", SOFT, False),
    (170, "2015.12", False, "Cilium 첫 커밋", "eBPF 네트워킹 비전", SOFT, False),
    (290, "2018", True, "Cilium 1.0 출시", "K8s 통합 집중", INFO, False),
    (410, "2020~22", False, "클라우드 3사 채택", "GKE · EKS-A · Azure", WARN, False),
    (530, "2021.10", True, "CNCF 인큐베이팅", "재단 프로젝트 선정", INFO, False),
    (655, "2023.10", False, "CNCF 졸업", "네트워킹 분야 유일", ACC, True),
    (755, "2024.04", True, "Cisco 인수 완료", "Isovalent 결합", OK, False),
    (850, "2026", False, "Cilium v1.20", "netkit · 엔터프라이즈", OK, False),
]

for x, date_str, is_above, title, sub, color, focal in events:
    r = 6 if focal else 4
    fill_col = color if focal else PAPER
    stroke_col = color
    d.o.append(f'<circle cx="{x}" cy="{Y_BASE}" r="{r}" fill="{fill_col}" stroke="{stroke_col}" stroke-width="1.4"/>')

    # 날짜 칩 (기준선 바로 옆)
    date_y = Y_BASE - 14 if is_above else Y_BASE + 22
    d.t(x, date_y, date_str, 10, color if focal else MUTED, MONO, "middle", 600)

    # 드롭 라인
    if is_above:
        text_y = Y_BASE - 58
        d.line(x, Y_BASE - 22, x, text_y + 18, RULE, sw=0.8, dash="2 2")
    else:
        text_y = Y_BASE + 58
        d.line(x, Y_BASE + 28, x, text_y - 14, RULE, sw=0.8, dash="2 2")

    if focal:
        bw, bh = 114, 44
        by = text_y - 14 if not is_above else text_y - 14
        d.tone(x - bw/2, by, bw, bh, ACC, r=4, op="18", sw=1.2)
        d.t(x, by + 18, title, 11, ACC, KR, "middle", 600)
        d.t(x, by + 34, sub, 11, INK, KR, "middle")
    else:
        d.t(x, text_y, title, 11, color if is_above else INK, KR, "middle", 600)
        d.t(x, text_y + 16, sub, 11, MUTED, KR, "middle")

# 범례
d.legend(428, [
    ("초기 태동", SOFT),
    ("주요 릴리스·CNCF", INFO),
    ("하이퍼스케일러 채택", WARN),
    ("CNCF 졸업 (유일)", ACC),
    ("엔터프라이즈 확장", OK),
])

d.save("01-01.cilium-evolution.svg")
