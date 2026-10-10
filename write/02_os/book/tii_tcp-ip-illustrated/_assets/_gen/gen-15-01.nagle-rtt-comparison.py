# 타입 스펙: type-sequence — RTT 190ms 조건에서 Nagle 해제와 적용 시 왕복 흐름 비교.
# 사실 출처: ch15.txt 300~374행 — Nagle 해제 시 19패킷·0.58s(요청 5·응답 7·ACK 7), Nagle 적용 시 11패킷·0.80s(190ms 주기 lockstep 0.0·0.19·0.38·0.57s).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, WARN, BAD, INFO, PAPER2, RULE, KR, MONO

W, H = 920, 620
d = D(W, H, "TCP/IP ILLUSTRATED VOL.1 · 15-01 §3",
      "RTT 190ms 환경에서 Nagle 알고리즘 해제와 적용 비교",
      "동일한 190ms RTT 네트워크에서 date 명령을 입력했을 때, Nagle 을 끄면 0.58초 동안 19개 패킷이 즉시 오간다. "
      "Nagle 을 켜면 ACK 가 올 때까지 작은 데이터를 묶어 전송하므로 패킷은 11개로 줄지만, 190ms 마다 멈춰 총 0.80초가 걸린다.",
      "패킷 수를 8개 줄이는 대가로 190ms 왕복 시간만큼 지연이 늘어납니다")

PW = 424
Y_LANE = 108
Y_BOT = 490

def panel_disabled(px, title):
    sx, rx = px + 68, px + PW - 68
    d.t(px + PW / 2, 98, title, 13, INK, KR, "middle", 600)
    for x, nm in ((sx, "클라이언트"), (rx, "서버")):
        d.box(x - 48, Y_LANE + 10, 96, 30, PAPER2, RULE, 1.0, 6)
        d.t(x, Y_LANE + 30, nm, 12, INK, KR, "middle", 600)
        d.line(x, Y_LANE + 44, x, Y_BOT, RULE, 0.8, "3 5")
    
    # Nagle 해제: 원문 19패킷(요청 5·응답 7·순수 ACK 7) 전체 표시 (수평선 축 정렬)
    pkts = [
        (1, "req 1", True, INFO, "info"),
        (2, "resp 1", False, WARN, "warn"),
        (3, "ack 1", True, MUTED, "ar"),
        (4, "req 2", True, INFO, "info"),
        (5, "resp 2", False, WARN, "warn"),
        (6, "ack 2", True, MUTED, "ar"),
        (7, "req 3", True, INFO, "info"),
        (8, "resp 3", False, WARN, "warn"),
        (9, "ack 3", True, MUTED, "ar"),
        (10, "req 4", True, INFO, "info"),
        (11, "resp 4", False, WARN, "warn"),
        (12, "ack 4", True, MUTED, "ar"),
        (13, "req 5", True, INFO, "info"),
        (14, "resp 5", False, WARN, "warn"),
        (15, "ack 5", True, MUTED, "ar"),
        (16, "resp 6", False, WARN, "warn"),
        (17, "ack 6", True, MUTED, "ar"),
        (18, "resp 7", False, WARN, "warn"),
        (19, "ack 7", True, MUTED, "ar"),
    ]
    y_start, dy = 160, 16.5
    for i, (num, lab, is_c2s, c, m) in enumerate(pkts):
        y = y_start + i * dy
        if is_c2s:
            d.arrow([(sx, y), (rx - 4, y)], c, m, 1.2)
            d.t(sx - 8, y + 4, f"{num}:{lab}", 9, c, MONO, "end")
        else:
            d.arrow([(rx, y), (sx + 4, y)], c, m, 1.2)
            d.t(rx + 8, y + 4, f"{num}:{lab}", 9, c, MONO, "start")
    
    cy = Y_BOT + 28
    d.chip(px + PW / 2, cy, "총 19패킷 · 소요 시간 0.58초", MUTED, 12)
    d.t(px + PW / 2, cy + 30, "요청 5 · 응답 7 · 순수 ACK 7", 11, SOFT, KR, "middle")

def panel_enabled(px, title):
    sx, rx = px + 68, px + PW - 68
    d.t(px + PW / 2, 98, title, 13, INK, KR, "middle", 600)
    for x, nm in ((sx, "클라이언트"), (rx, "서버")):
        d.box(x - 48, Y_LANE + 10, 96, 30, PAPER2, RULE, 1.0, 6)
        d.t(x, Y_LANE + 30, nm, 12, INK, KR, "middle", 600)
        d.line(x, Y_LANE + 44, x, Y_BOT, RULE, 0.8, "3 5")
    
    # Nagle 적용: 원문 11개 패킷, 190ms 주기 lockstep 4단계 (수평선 축 정렬, 한글 11px)
    rounds = [
        (160, "0.00s", [
            (1, "요청 1 (1B)", True, INFO, "info"),
            (2, "응답 1 (에코)", False, WARN, "warn"),
            (3, "ACK 1", True, MUTED, "ar"),
        ]),
        (245, "0.19s", [
            (4, "요청 2 (묶음)", True, INFO, "info"),
            (5, "응답 2 (에코)", False, WARN, "warn"),
            (6, "ACK 2", True, MUTED, "ar"),
        ]),
        (330, "0.38s", [
            (7, "요청 3", True, INFO, "info"),
            (8, "응답 3 (출력 64B)", False, WARN, "warn"),
            (9, "ACK 3", True, MUTED, "ar"),
        ]),
        (415, "0.57s", [
            (10, "응답 4 (프롬프트)", False, WARN, "warn"),
            (11, "ACK 4", True, MUTED, "ar"),
        ]),
    ]
    
    for y_base, t_sec, msgs in rounds:
        # 시간 라벨을 첫 화살표 높이에 정렬
        d.t(px + 12, y_base + 4, t_sec, 11, ACC, MONO, "start", 600)
        for j, (num, lab, is_c2s, c, m) in enumerate(msgs):
            my = y_base + j * 24
            if is_c2s:
                d.arrow([(sx, my), (rx - 4, my)], c, m, 1.3)
            else:
                d.arrow([(rx, my), (sx + 4, my)], c, m, 1.3)
            d.t((sx + rx) / 2, my - 5, f"{num}:{lab}", 11, c, KR, "middle", 600)
        
        # 190ms 대기 표시
        if y_base < 400:
            d.path(f"M {rx + 12} {y_base} H {rx + 20} V {y_base + 72} H {rx + 12}", SOFT, 1.0)
            d.t(rx + 26, y_base + 40, "190ms", 10, SOFT, MONO, "start")
    
    cy = Y_BOT + 28
    w = 260
    d.o.append(f'<rect x="{px + PW / 2 - w / 2}" y="{cy - 14}" width="{w}" height="28" rx="6" fill="{ACC}14" stroke="{ACC}" stroke-width="1.2"/>')
    d.t(px + PW / 2, cy + 5, "총 11패킷 · 소요 시간 0.80초 (8개 감소)", 12, ACC, KR, "middle", 600)
    d.t(px + PW / 2, cy + 30, "미확인 데이터 대기 중 버퍼링 묶음", 11, MUTED, KR, "middle")

panel_disabled(24, "Nagle 비활성화 (기본값)")
panel_enabled(472, "Nagle 활성화 (묶음 전송)")
d.line(W / 2, 80, W / 2, Y_BOT + 56, RULE, 0.8)

d.legend(H - 42, [
    ("요청 세그먼트", INFO),
    ("응답·에코 세그먼트", WARN),
    ("순수 ACK 세그먼트", MUTED),
    ("Nagle 묶음 지연", ACC)
])

d.save("15-01.nagle-rtt-comparison.svg")
