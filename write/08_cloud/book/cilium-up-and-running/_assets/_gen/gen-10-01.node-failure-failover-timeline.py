# 타입 스펙: type-timeline — 노드 장애 발생부터 리스 만료, 새 리더 선출, Gratuitous ARP 공지 및 트래픽 복구 타임라인
# 사실 출처: 추출본 cil10.txt 줄 420-480(docker stop·5001ms timeout·lease transfer·gratuitous ARP) / docs.cilium.io v1.20 network/l2-announcements/
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, BAD, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 480
d = D(W, H, "CILIUM UP AND RUNNING · 10-01 §4", "노드 장애와 페일오버 타임라인",
      "노드 정지 후 리스가 만료될 때까지 블랙홀이 발생하고 새 리더의 ARP 로 복구됩니다",
      "리스 만료 10~20초 · Gratuitous ARP · 이웃 테이블 갱신")

Y_BASE = 240
d.line(40, Y_BASE, 880, Y_BASE, RULE, sw=1.2)

events = [
    (100, "0초", True, "노드 장애 발생", "docker stop kind-worker2", BAD, True),
    (260, "리스 만료까지", False, "패킷 블랙홀", "curl 5001ms 타임아웃", WARN, False),
    (420, "10~20초", True, "리스 만료", "페일오버 10~20초", INFO, False),
    (580, "만료 직후", False, "새 리더 선출", "kind-worker 리스 획득", ACC, True),
    (720, "선출 직후", True, "Gratuitous ARP", "새 MAC 브로드캐스트", OK, False),
    (840, "복구", False, "트래픽 복구", "ARP 캐시 갱신 뒤", OK, True),
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
        bw, bh = max(120, sum(6.8 if ord(c) < 128 else 11.5 for c in sub) + 20), 44
        by = text_y - 14
        d.tone(x - bw / 2, by, bw, bh, color, r=4, op="18", sw=1.2)
        d.t(x, by + 18, title, 11, color, KR, "middle", 600)
        d.t(x, by + 34, sub, 11, INK, KR, "middle")
    else:
        d.t(x, text_y, title, 11, color if is_above else INK, KR, "middle", 600)
        d.t(x, text_y + 16, sub, 11, MUTED, KR, "middle")

d.legend(428, [
    ("장애 발생", BAD),
    ("블랙홀 구간", WARN),
    ("리스 만료", INFO),
    ("새 리더 선출", ACC),
    ("ARP 갱신 · 복구", OK),
])
d.save("10-01.node-failure-failover-timeline.svg")
