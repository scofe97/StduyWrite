# 타입 스펙: type-timeline — 1993년 BPF 논문부터 2020년 LSM BPF 도입까지 eBPF 의 진화 연표
# 사실 출처: 원문 ebpf1.txt 30-159(1993 McCanne/Jacobson·1997 tcpdump·2012 3.5·2014 3.15/3.18·2015 kprobe·2016 Cilium·2017 Katran 프로덕션·2018 BTF·2020 LSM BPF)
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 480
d = D(W, H, "LEARNING EBPF · 01-01 §1", "패킷 필터에서 범용 커널 플랫폼으로의 진화",
      "네트워크 패킷 거르기에서 시스템 추적·보안 통제 플랫폼으로 확장된 역사",
      "1993 BSD 패킷 필터 · 2014 eBPF 도입 · 2020 LSM BPF 보안 확장")

Y_BASE = 240
d.line(40, Y_BASE, 880, Y_BASE, RULE, sw=1.2)

events = [
    (70, "1993년", True, "BPF 논문 발표", "BSD 패킷 필터", INFO, False),
    (168, "1997년", False, "Linux 도입", "tcpdump 캡처", MUTED, False),
    (266, "2012년", True, "seccomp-bpf 3.5", "시스템 콜 필터링", WARN, False),
    (364, "2014년", False, "eBPF 3.15·3.18", "64비트·bpf()·맵", ACC, True),
    (462, "2015년", True, "eBPF kprobe 부착", "Linux 4.1", OK, False),
    (560, "2016년", False, "Cilium 프로젝트", "컨테이너 eBPF 망", OK, False),
    (658, "2017년", True, "Katran 프로덕션", "Meta L4 로드밸런서", INFO, False),
    (756, "2018년", False, "BTF·독립 서브시스템", "프로그램 이식성", OK, False),
    (854, "2020년", True, "LSM BPF 도입", "Linux 5.7 보안 제어", ACC, False),
]

for x, time_str, is_above, title, sub, color, focal in events:
    r = 6 if focal else 4
    fill_col = color if focal else PAPER
    d.o.append(f'<circle cx="{x}" cy="{Y_BASE}" r="{r}" fill="{fill_col}" stroke="{color}" stroke-width="1.4"/>')

    date_y = Y_BASE - 14 if is_above else Y_BASE + 22
    d.t(x, date_y, time_str, 11, color if focal else MUTED, MONO, "middle", 600)

    if is_above:
        text_y = Y_BASE - 56
        d.line(x, Y_BASE - 22, x, text_y + 18, RULE, sw=0.8, dash="2 2")
    else:
        text_y = Y_BASE + 56
        d.line(x, Y_BASE + 28, x, text_y - 14, RULE, sw=0.8, dash="2 2")

    if focal:
        bw, bh = 138, 44
        by = text_y - 14
        d.tone(x - bw / 2, by, bw, bh, color, r=4, op="18", sw=1.2)
        d.t(x, by + 18, title, 12, color, KR, "middle", 600)
        d.t(x, by + 34, sub, 12, INK, KR, "middle")
    else:
        d.t(x, text_y, title, 12, color if is_above else INK, KR, "middle", 600)
        d.t(x, text_y + 18, sub, 12, MUTED, KR, "middle")

d.legend(440, [
    ("초기 패킷 필터링", INFO),
    ("시스템 콜 제어", WARN),
    ("eBPF 확장 전환점", ACC),
    ("추적 및 네트워킹", OK),
])
d.save("01-01.bpf-timeline.svg")
