# 03-01 슬라이딩 윈도와 수신 버퍼 갱신 과정
# 사실 출처: NPG Ch.3 Fig 3-3 (p.5-6), 버퍼 3,072 B · 패킷 1,024 B x 3 · Read 2,048 B
# 타입 스펙: type-data-flow — 서버, 수신 버퍼 슬롯, Go 앱 사이의 패킷 블록 이동과 창 크기 광고
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, OK, WARN, BAD, INFO, ACC, KR, MONO

W, H = 840, 460
d = D(W, H, "NPG CH.3 — SLIDING WINDOW",
      "수신 버퍼와 슬라이딩 윈도 흐름",
      "패킷 블록 적재와 Go 앱 소비에 따른 수신 창 크기 광고",
      "패킷 수신과 앱 소비에 따른 수신 창 크기 광고")

# Columns header
y_top = 100
d.t(70, y_top, "단계", 12, SOFT, KR, "middle", 600)
d.t(210, y_top, "송신 서버", 12, INFO, KR, "middle", 600)
d.t(450, y_top, "수신 버퍼 (3 슬롯)", 12, OK, KR, "middle", 600)
d.t(730, y_top, "Go 앱", 12, ACC, KR, "middle", 600)
d.line(20, y_top + 12, W - 20, y_top + 12, RULE, 1.0)

def draw_buffer(y, filled_count, retained_count=0):
    slot_w, slot_h = 56, 26
    start_x = 450 - (slot_w * 3 + 12) / 2
    for i in range(3):
        sx = start_x + i * (slot_w + 6)
        is_filled = i < filled_count
        is_retained = (i < retained_count)
        if is_retained:
            # 남아 있던 블록 1개: 점선 테두리와 차분한 MUTED 톤
            d.o.append(f'<rect x="{sx}" y="{y}" width="{slot_w}" height="{slot_h}" rx="4" fill="{MUTED}20" stroke="{MUTED}" stroke-width="1.2" stroke-dasharray="3 2"/>')
            d.t(sx + slot_w / 2, y + 17, "1,024B", 11, SOFT, MONO, "middle", 600)
        elif is_filled:
            # 새로 온 블록: 선명한 실선 WARN 톤
            fill = f"{WARN}32"
            stroke = WARN
            d.box(sx, y, slot_w, slot_h, fill=fill, stroke=stroke, sw=1.5, r=4)
            d.t(sx + slot_w / 2, y + 17, "1,024B", 11, INK, MONO, "middle", 600)
        else:
            d.box(sx, y, slot_w, slot_h, fill=PAPER, stroke=RULE, sw=1.2, r=4)
            d.t(sx + slot_w / 2, y + 17, "빈 슬롯", 11, SOFT, KR, "middle")

# Step 1: Initial ACK advertising Win=3072B
y1 = 135
d.t(70, y1 + 18, "1. 초기", 12, INK, KR, "middle", 600)
d.box(165, y1, 90, 36, fill=PAPER2, stroke=INFO, r=6)
d.t(210, y1 + 23, "송신 대기", 11, INFO, KR, "middle")
draw_buffer(y1 + 5, 0)
d.arrow([(345, y1 + 28), (265, y1 + 28)], c=INFO, m="info")
d.t(305, y1 + 18, "Win=3,072B", 11, INFO, MONO, "middle", 600)
d.box(685, y1, 90, 36, fill=PAPER2, stroke=RULE, r=6)
d.t(730, y1 + 23, "Read 대기", 11, SOFT, KR, "middle")

# Step 2: Server sends 3 packets -> Buffer filled
y2 = 210
d.t(70, y2 + 18, "2. 전송", 12, INK, KR, "middle", 600)
d.box(165, y2, 90, 36, fill=PAPER2, stroke=INFO, r=6)
d.t(210, y2 + 23, "3개 송신", 11, INFO, KR, "middle")
d.arrow([(265, y2 + 18), (350, y2 + 18)], c=WARN, m="warn")
d.t(307, y2 + 10, "1,024B x 3", 11, WARN, MONO, "middle", 600)
draw_buffer(y2 + 5, 3)
d.box(685, y2, 90, 36, fill=PAPER2, stroke=RULE, r=6)
d.t(730, y2 + 23, "적재 대기", 11, MUTED, KR, "middle")

# Step 3: Go App reads 2,048B -> Buffer frees 2 slots -> ACK Win=2048B
y3 = 285
d.t(70, y3 + 18, "3. 소비", 12, INK, KR, "middle", 600)
d.box(165, y3, 90, 36, fill=PAPER2, stroke=INFO, r=6)
d.t(210, y3 + 23, "ACK 대기", 11, INFO, KR, "middle")
draw_buffer(y3 + 5, 1)
d.arrow([(550, y3 + 18), (675, y3 + 18)], c=OK, m="ok")
d.t(612, y3 + 10, "Read(2,048B)", 11, OK, MONO, "middle", 600)
d.box(685, y3, 90, 36, fill=f"{OK}15", stroke=OK, r=6)
d.t(730, y3 + 23, "2,048B 소비", 11, OK, KR, "middle", 600)
d.arrow([(345, y3 + 28), (265, y3 + 28)], c=INFO, m="info")
d.t(305, y3 + 18, "Win=2,048B", 11, INFO, MONO, "middle", 600)

# Step 4: Server sends 2 packets -> Buffer filled again (retained 1 block + new 2 blocks)
y4 = 360
d.t(70, y4 + 18, "4. 전송", 12, INK, KR, "middle", 600)
d.box(165, y4, 90, 36, fill=PAPER2, stroke=INFO, r=6)
d.t(210, y4 + 23, "2개 송신", 11, INFO, KR, "middle")
d.arrow([(265, y4 + 18), (350, y4 + 18)], c=WARN, m="warn")
d.t(307, y4 + 10, "1,024B x 2", 11, WARN, MONO, "middle", 600)
draw_buffer(y4 + 5, 3, retained_count=1)
d.box(685, y4, 90, 36, fill=PAPER2, stroke=RULE, r=6)
d.t(730, y4 + 23, "후속 대기", 11, SOFT, KR, "middle")

# Legend
d.legend(415, [("창 광고", INFO), ("패킷 흐름", WARN), ("앱 소비", OK), ("기존 잔여", MUTED)])

out = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "03-01.receive-window.svg"))
d.save(out)
print(f"saved: {out}")
