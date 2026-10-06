# 타입 스펙: type-state
# 04-03 CLOSE_WAIT 상태 함정과 소켓 누수 메커니즘
# 사실 출처: NPG Ch.4 Listing 4-27, TII Ch.13 §13.5
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, OK, WARN, BAD, INFO, ACC, KR, MONO

W, H = 880, 460
d = D(W, H, "LISTING 4-27 CLOSE_WAIT TRAP",
      "CLOSE_WAIT 전이와 누수 함정",
      "상대 FIN 수신 후 Close 호출 누락에 따른 CLOSE_WAIT 상태 고착",
      "Close() 누락 시 CLOSE_WAIT 탈출 불가")

y_mid = 260

# 1. 시작 (Filled dot)
d.o.append(f'<circle cx="50" cy="{y_mid}" r="6" fill="{INK}"/>')
d.arrow([(58, y_mid), (96, y_mid)], MUTED, "ar", 1.4)

# 2. ESTABLISHED
d.box(96, y_mid - 24, 136, 48, fill=PAPER2, stroke=RULE, r=8)
d.t(164, y_mid - 4, "ESTABLISHED", 12, INK, MONO, "middle", 600)
d.t(164, y_mid + 14, "정상 연결 유지", 11, MUTED, KR, "middle")

# ESTABLISHED -> CLOSE_WAIT
d.arrow([(232, y_mid), (360, y_mid)], OK, "ok", 1.4)
d.t(296, y_mid - 12, "상대 FIN 수신", 11, OK, KR, "middle")
d.t(296, y_mid + 20, "커널 ACK 송신", 11, OK, KR, "middle")

# 3. CLOSE_WAIT (함정 상태)
d.tone(360, y_mid - 24, 144, 48, BAD, r=8, op="20", sw=1.4)
d.t(432, y_mid - 4, "CLOSE_WAIT", 12, BAD, MONO, "middle", 600)
d.t(432, y_mid + 14, "수동 종료 대기", 11, BAD, KR, "middle")

# 누수 함정 자기 루프 (Close 누락)
d.arrow([(410, y_mid - 24), (410, 166), (456, 166), (456, y_mid - 26)], BAD, "bad", 1.4)
d.t(433, 154, "Close() 누락", 11, BAD, KR, "middle", 600)
d.t(466, 186, "소켓 누수 고착", 11, BAD, KR, "start")

# 4. CLOSE_WAIT -> LAST_ACK (정상 탈출)
d.arrow([(504, y_mid), (620, y_mid)], OK, "ok", 1.4)
d.t(562, y_mid - 12, "Close() 호출", 11, OK, KR, "middle", 600)
d.t(562, y_mid + 20, "로컬 FIN 송신", 11, OK, KR, "middle")

# 5. LAST_ACK
d.box(620, y_mid - 24, 130, 48, fill=PAPER2, stroke=RULE, r=8)
d.t(685, y_mid - 4, "LAST_ACK", 12, INK, MONO, "middle", 600)
d.t(685, y_mid + 14, "최종 ACK 대기", 11, MUTED, KR, "middle")

# LAST_ACK -> CLOSED
d.arrow([(750, y_mid), (814, y_mid)], MUTED, "ar", 1.4)
d.t(782, y_mid - 12, "상대 ACK", 11, MUTED, KR, "middle")

# 6. 종료 (Ringed dot)
d.o.append(f'<circle cx="824" cy="{y_mid}" r="9" fill="none" stroke="{SOFT}" stroke-width="1.5"/>')
d.o.append(f'<circle cx="824" cy="{y_mid}" r="5" fill="{SOFT}"/>')
d.t(824, y_mid + 24, "CLOSED", 10, SOFT, MONO, "middle")

d.legend(H - 46, [("정상 전이", OK), ("누수 함정 (고착)", BAD), ("종료 상태", SOFT)])

out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "04-03.close-wait-trap.svg"))
d.save(out_path)
print(f"Generated: {out_path}")
