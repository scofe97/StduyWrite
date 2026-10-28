# 본문 요구: ### 함정·관찰: 이름이 같은 두 KeepAlive. 이름이 같은 두 설정이 다른 층의 다른 시계라는 것.
# 타입 스펙: type-gantt
# 사실 출처: go1.25.1 src/net/tcpsock.go:136-148, src/net/tcpsock.go:289-296, src/net/dial.go:171-190, src/net/http/transport.go:45-56, src/net/http/transport.go:224, src/net/http/transport.go:1134
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 960, 480

d = D(W, H,
      "KEEPALIVE TIMERS COMPARISON",
      "두 KeepAlive 시계: TCP 탐침과 HTTP 풀 타임아웃",
      "이름이 같은 두 KeepAlive는 동작 계층과 시계가 다르다. 풀에 있는 연결은 90s에 먼저 닫히고, 무응답 연결은 TCP 15s 재전송 9회 실패 후 165s에 소켓을 절단한다",
      "응답하는 상대에게 탐침은 30s 마다 가고, 풀의 빈 연결을 닫는 것은 90s 의 IdleConnTimeout 입니다")

TX = 240
TW = 660

# 상단 시간축 헤더 (Y = 96)
d.box(TX, 96, TW, 28, fill=PAPER2, stroke=RULE, sw=0.8, r=4)

ticks = [
    (0, "0s"),
    (15, "15s"),
    (30, "30s"),
    (45, "45s"),
    (60, "60s"),
    (75, "75s"),
    (90, "90s"),
    (105, "105s"),
    (120, "120s"),
    (135, "135s"),
    (150, "150s"),
    (165, "165s"),
]

for sec, label in ticks:
    x = TX + int(sec * 4)
    # 수직 기준선 (90s는 주황 강조선)
    c_line = ACC if sec == 90 else RULE
    w_line = 1.1 if sec == 90 else 0.6
    d_dash = "3 3" if sec == 90 else "2 4"
    d.line(x, 124, x, 396, c=c_line, sw=w_line, dash=d_dash)

    # 시간 라벨
    c_text = ACC if sec == 90 else (INK if sec in (0, 30, 90, 165) else SOFT)
    weight = 600 if sec in (0, 30, 90, 165) else 400
    anc = "start" if sec == 0 else ("end" if sec == 165 else "middle")
    tx_pos = x + 6 if sec == 0 else (x - 6 if sec == 165 else x)
    d.t(tx_pos, 114, label, 10, c_text, fam=MONO, anchor=anc, weight=weight)

# 위 줄: TCP keepalive (Dialer.KeepAlive) — L4 소켓 계층
Y1 = 134
d.box(24, Y1, 204, 134, fill=PAPER2, stroke=RULE, sw=0.8, r=6)
d.t(36, Y1 + 24, "TCP keepalive", 13, INK, fam=MONO, anchor="start", weight=600)
d.t(36, Y1 + 46, "Dialer.KeepAlive 30s", 11, INFO, fam=MONO, anchor="start")
d.t(36, Y1 + 68, "L4 커널 소켓 생존 탐침", 11, SOFT, fam=KR, anchor="start")
d.t(36, Y1 + 88, "KeepAliveConfig (15s · 9회)", 11, SOFT, fam=KR, anchor="start")
d.t(36, Y1 + 108, "최대 165s 후 커널 절단", 11, SOFT, fam=KR, anchor="start")

# 1) 정상 응답 경로: 0~30s 유휴 대기, 30s · 60s 탐침, 90s 에 풀이 닫음
Y_NORM = 158
d.box(TX, Y_NORM - 14, 114, 28, fill=f"{INFO}18", stroke=INFO, sw=1.1, r=4)
d.t(TX + 57, Y_NORM + 4, "30s 유휴 대기", 11, INFO, fam=KR, anchor="middle", weight=600)

d.line(TX + 120, Y_NORM, TX + 360, Y_NORM, INFO, 1.4)
for i, sec in enumerate((30, 60)):
    px = TX + int(sec * 4)
    d.o.append(f'<circle cx="{px}" cy="{Y_NORM}" r="4" fill="{INFO}" stroke="{PAPER}" stroke-width="1.2"/>')
    d.t(px, Y_NORM - 8, f"#{i+1}", 9, INFO, fam=MONO, anchor="middle", weight=600)

d.t(TX + 240, Y_NORM + 20, "정상 응답: 30s 마다 탐침, 90s 에 풀이 닫음", 11, INFO, fam=KR, anchor="middle")

# 2) 무응답 레인: 0s 부터 별도 레인, 30s #1 → 45~150s 15s 재전송 #2~#9 → 165s 절단
Y_FAIL = 230
d.t(TX, 198, "무응답 상대 · 풀 밖 연결 (예: 응답을 기다리는 중인 연결)", 11, WARN, fam=KR, anchor="start", weight=600)

d.box(TX, Y_FAIL - 14, 100, 28, fill=f"{SOFT}14", stroke=RULE, sw=0.8, r=4)
d.t(TX + 50, Y_FAIL + 4, "30s 유휴 대기", 11, SOFT, fam=KR, anchor="middle")

d.line(TX + 120, Y_FAIL, TX + 660, Y_FAIL, WARN, 1.2)

for i in range(9):
    sec = 30 + i * 15
    px = TX + int(sec * 4)
    c_dot = INFO if i == 0 else WARN
    d.o.append(f'<circle cx="{px}" cy="{Y_FAIL}" r="4" fill="{c_dot}" stroke="{PAPER}" stroke-width="1.2"/>')
    d.t(px, Y_FAIL - 8, f"#{i+1}", 9, c_dot, fam=MONO, anchor="middle", weight=600)

d.t(TX + 360, Y_FAIL + 18, "탐침 9회 (15s 간격)", 11, WARN, fam=KR, anchor="middle")

d.line(TX + 660, Y_FAIL - 12, TX + 660, Y_FAIL + 12, BAD, sw=2.0)
d.box(TX + 508, Y_FAIL + 7, 152, 24, fill=PAPER, stroke=BAD, sw=1.1, r=4)
d.t(TX + 584, Y_FAIL + 23, "30s + 15s×9 = 165s 절단", 11, BAD, fam=KR, anchor="middle", weight=600)

# 아래 줄: HTTP keep-alive (Transport 풀) — L7 HTTP 전송 계층
Y2 = 282
d.box(24, Y2, 204, 104, fill=PAPER2, stroke=RULE, sw=0.8, r=6)
d.t(36, Y2 + 24, "HTTP keep-alive", 13, ACC, fam=MONO, anchor="start", weight=600)
d.t(36, Y2 + 44, "IdleConnTimeout 90s", 11, ACC, fam=MONO, anchor="start")
d.t(36, Y2 + 64, "L7 Transport 유휴 풀", 11, SOFT, fam=KR, anchor="start")
d.t(36, Y2 + 82, "호스트당 빈 연결 2", 11, SOFT, fam=KR, anchor="start")

# 0~90s: 풀에 유휴 보관 막대 (x = TX to TX + 356)
d.box(TX, Y2 + 10, 356, 40, fill=f"{ACC}14", stroke=ACC, sw=1.4, r=4)
d.t(TX + 160, Y2 + 35, "커넥션 풀 유휴 보관 (최대 90s)", 11, ACC, fam=KR, anchor="middle", weight=600)

# 재사용 화살표 (45s 지점 = TX + 180)
d.arrow([(TX + 180, Y2 + 76), (TX + 180, Y2 + 52)], c=OK, m="ok", sw=1.3)
d.t(TX + 180, Y2 + 90, "새 요청 도착 시 재사용", 11, OK, fam=KR, anchor="middle")

# 90s focal: IdleConnTimeout 만료로 먼저 닫음 (x = TX + 360 to TX + 500)
d.box(TX + 360, Y2 + 6, 140, 48, fill=PAPER, stroke=ACC, sw=1.6, r=4)
d.t(TX + 430, Y2 + 26, "IdleConnTimeout", 12, ACC, fam=MONO, anchor="middle", weight=600)
d.t(TX + 430, Y2 + 44, "90s 닫음 (focal)", 11, ACC, fam=KR, anchor="middle", weight=600)

# 90~165s: 닫힌 연결 (x = TX + 504 to TX + 660)
d.o.append(f'<rect x="{TX + 504}" y="{Y2 + 10}" width="156" height="40" rx="4" fill="{PAPER2}88" stroke="{RULE}" stroke-width="0.8" stroke-dasharray="3 3"/>')
d.t(TX + 582, Y2 + 35, "연결 닫힘 (풀에서 제거)", 11, SOFT, fam=KR, anchor="middle")

# 범례
def custom_legend(y, items):
    d.line(12, y, d.w - 48, y, RULE, 0.8)
    d.t(12, y + 22, "LEGEND", 8, SOFT, MONO, "start")
    x = 80
    for lab, c in items:
        d.o.append(f'<rect x="{x}" y="{y+12}" width="14" height="12" rx="2" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
        d.t(x + 22, y + 22, lab, 11, MUTED, KR, "start")
        w = sum(12.0 if '가' <= ch <= '힣' else 7.0 for ch in lab)
        x += int(w + 38)

d.legend = custom_legend

d.legend(422, [
    ("HTTP 90s (focal)", ACC),
    ("TCP 30s 탐침", INFO),
    ("TCP 15s 재전송 (무응답)", WARN),
    ("TCP 165s 절단", BAD),
    ("재사용", OK),
])

out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "02-01.dt-keepalive-clocks.svg"))
d.save(out_path)
