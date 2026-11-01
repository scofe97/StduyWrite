# 타입 스펙: type-timeline — 2014년 eBPF·K8s 부터 Cilium 첫 커밋, 클라우드 채택, CNCF 인큐베이팅·졸업, Cisco 인수, 최신 v1.20 까지.
# 사실 출처: 원서 1장 p.1 (K8s 2014 오픈소스) · p.2 (2014 eBPF) · Origins and Evolution p.3 (December 2015 first commit,
#   multiple container schedulers) · Industry Adoption p.4 (GKE Dataplane V2·EKS Anywhere·Azure CNI powered by Cilium) ·
#   Becoming a CNCF Graduated Project p.5 (2023, only project in the Cloud Native Networking category) ·
#   본문 §1 L71 (2014 커널 병합) · §2 L83-93 (2015.12, 2021.10 인큐베이팅, 2023.10.11 졸업, 2024.04.12 Cisco 인수, 최신 v1.20).
# 클라우드 채택 점은 연도가 본문·원서에 없어 날짜 대신 이름 칩을 달고, 본문 순서(L87 채택 → L91 "이러한 신뢰를 발판으로" 인큐베이팅)대로 둔다.
#   원서 p.5 는 채택을 2023 졸업과 잇는다 — 보고서 「본문·원서 불일치」.
# v1.20 은 본문이 연도를 말하지 않아 "현행" 칩으로 두고, netkit(§5)은 v1.20 과 묶지 않는다 (2026-11-01 검증).
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 480
d = D(W, H, "CILIUM UP AND RUNNING · 01-01 §2", "Cilium 발전 타임라인",
      "2014년 eBPF 와 2015년 첫 커밋부터 클라우드 3사 채택, CNCF 인큐베이팅·졸업, Cisco 인수, 최신 v1.20 까지",
      "2015년 첫 커밋에서 CNCF 졸업 프로젝트까지")

Y_BASE = 248

# 기준선 (Baseline)
d.line(40, Y_BASE, 880, Y_BASE, RULE, sw=1.2)

# 연도 틱 및 이벤트
# (x, date_str, is_above, title, sub, color, focal)
events = [
    (68, "2014", True, "eBPF 커널 병합", "K8s 오픈소스 공개", SOFT, False),
    (175, "2015.12", False, "Cilium 첫 커밋", "eBPF 네트워킹 비전", SOFT, False),
    (290, "초기 발전", True, "K8s CNI 집중", "다중 스케줄러에서 통합", INFO, False),
    (410, "클라우드 채택", False, "클라우드 3사 기본 채택", "GKE · EKS-A · Azure", WARN, False),
    (530, "2021.10", True, "CNCF 인큐베이팅", "재단 프로젝트 선정", INFO, False),
    (655, "2023.10", False, "CNCF 졸업", "네트워킹 범주 유일", ACC, True),
    (755, "2024.04", True, "Cisco 인수 완료", "창립 멤버 기업 Isovalent", OK, False),
    (850, "현행", False, "Cilium v1.20", "공식 릴리스 최신", OK, False),
]

for x, date_str, is_above, title, sub, color, focal in events:
    r = 6 if focal else 4
    fill_col = color if focal else PAPER
    stroke_col = color
    d.o.append(f'<circle cx="{x}" cy="{Y_BASE}" r="{r}" fill="{fill_col}" stroke="{stroke_col}" stroke-width="1.4"/>')

    # 날짜 칩 (기준선 바로 옆, 한글 포함 시 KR 글꼴 및 하한 11px 준수)
    date_y = Y_BASE - 14 if is_above else Y_BASE + 22
    font_date = KR if any('가' <= ch <= '힣' for ch in date_str) else MONO
    d.t(x, date_y, date_str, 11, color if focal else MUTED, font_date, "middle", 600)

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
    ("생태계 확장·CNCF", INFO),
    ("하이퍼스케일러 채택", WARN),
    ("CNCF 졸업", ACC),
    ("Cisco 인수·최신 릴리스", OK),
])

d.save("01-01.cilium-evolution.svg")
