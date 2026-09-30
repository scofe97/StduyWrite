# 02-02 세부 도식 둘 — 사용자 요청(2026-09-29) "도식은 더 적극적으로, 여러 장 그려도 됨".
# 타입 스펙: G 는 type-sequence, H 는 type-flowchart(시간축). 사실 출처: 02-02 본문, tc-netem(8), Linux tcp_recovery.c, 실험 5.
from dd import D, INK, MUTED, SOFT, ACC, OK, BAD, RULE, MONO, KR
from ddk import SeqKR

# G. 양방향 번호와 ACK 를 얹을 때·따로 보낼 때 (§1)
s = SeqKR(960, 520, "SEQUENCE · 02-02 ACK SEGMENTS", "서로의 바이트를 ACK 하는 양쪽",
          "TCP 는 양쪽이 각자 보내는 바이트에 번호를 따로 매긴다. 설명을 위해 클라이언트 번호는 1 부터, 서버 번호는 501 부터 센다. "
          "SEQ 는 내가 보내는 바이트의 번호이고 ACK 는 상대 바이트를 어디까지 받았는지다. 서버는 echo 데이터에 ACK 7 을 얹어 클라이언트의 1~6 을 "
          "받았다고 알리고, 클라이언트는 곧 보낼 데이터가 없으면 본문 0 바이트 세그먼트로 ACK 507 만 보내 서버의 501~506 을 받았다고 알린다. "
          "본문이 없으므로 번호를 쓰지 않아 뒤이은 msg2 도 SEQ 7 로 시작한다.",
          lead="SEQ = 내 바이트 번호, ACK = 상대 바이트를 어디까지 빈틈없이 받았나(누적 ACK). 빈자리가 없어 SACK 은 붙지 않습니다.")
s.LX = s.lanes([("클라이언트", "번호 1 부터"), ("서버", "번호 501 부터")], 104, 240)
s.rails(470)
s.msg("클라이언트", "서버", "SEQ 1 · ACK 501 · 본문 msg1 6B", 200, MUTED, sub="클라이언트 1~6 을 보냄")
s.msg("서버", "클라이언트", "SEQ 501 · ACK 7 · 본문 echo 6B", 276, OK, sub="서버 501~506 을 보내며 클라이언트 1~6 받음을 얹음")
s.msg("클라이언트", "서버", "SEQ 7 · ACK 507 · 본문 0B", 352, ACC, sub="ACK 만: 서버 501~506 받음 · 번호를 쓰지 않음")
s.msg("클라이언트", "서버", "SEQ 7 · ACK 507 · 본문 msg2 6B", 428, OK, sub="다음 데이터에 얹음 · 그래서 다시 SEQ 7")
s.save("02-02.ack-segments.svg")

# H. 실험 5 의 앞지르기 (§3)
d = D(960, 470, "FLOWCHART · 02-02 EXP5 OVERTAKE", "실험 5: 곧바로 나간 7 의 앞지르기",
      "1ms 간격으로 1 부터 7 을 보냈다. netem 은 75% 를 10ms 늦추고 25% 를 곧바로 보내므로, 이 예에서 7 만 곧바로 나가 7ms 에 "
      "도착하고 1~6 은 11~16ms 에 도착한다. 7 이 SACK 되면 RACK 의 첫 조건이 채워지고 창이 10ms 보다 훨씬 좁아 짧은 대기 뒤 "
      "늦었을 뿐인 1~6 을 잃었다고 판정해 불필요하게 재전송한다.",
      lead="위는 보낸 시각, 가운데는 도착 시각입니다. 1~6 은 사라지지 않았습니다.")
T0, PX = 200, 44


def x(ms):
    return T0 + ms * PX


for y, lab in ((150, "보냄"), (260, "도착")):
    d.t(24, y + 5, lab, 13, MUTED, KR, "start", 600)
    d.line(x(0), y, x(16), y, RULE, 0.8, "3 6")
for n in range(1, 8):
    c = OK if n == 7 else INK
    d.o.append(f'<rect x="{x(n)-15}" y="132" width="30" height="36" rx="5" fill="{c}14" stroke="{c}" stroke-width="1"/>')
    d.t(x(n), 155, str(n), 13, c, MONO, "middle", 600)
d.o.append(f'<rect x="{x(7)-15}" y="242" width="30" height="36" rx="5" fill="{OK}14" stroke="{OK}" stroke-width="1.4"/>')
d.t(x(7), 265, "7", 13, OK, MONO, "middle", 600)
for n in range(1, 7):
    d.o.append(f'<rect x="{x(n+10)-15}" y="242" width="30" height="36" rx="5" fill="{ACC}14" stroke="{ACC}" stroke-width="1"/>')
    d.t(x(n + 10), 265, str(n), 13, ACC, MONO, "middle", 600)
d.t(x(7), 300, "곧바로", 11, OK, KR, "middle")
d.t(x(13.5), 300, "10ms 늦음", 11, ACC, KR, "middle")
d.line(x(9), 280, x(9), 334, BAD, 1.2, "4 4")
d.tone(x(9) - 120, 334, 240, 40, BAD, 6, "10", 1.2)
d.t(x(9), 359, "RACK: 1~6 손실 판정", 12, BAD, KR, "middle", 600)
d.t(x(9) + 130, 359, "→ 불필요한 재전송", 12, BAD, KR, "start")
ya = 420
d.line(x(0), ya, x(16), ya, SOFT, 1.0)
for ms in range(0, 17, 2):
    d.line(x(ms), ya - 4, x(ms), ya + 4, SOFT, 1.0)
    d.t(x(ms), ya + 18, f"{ms}ms", 11, MUTED, MONO, "middle")
d.save("02-02.exp5-overtake.svg")
print("ok 02-02 details")

# I. 같은 손실을 문턱과 RACK 이 판정하는 시각표 (§3)
d = D(960, 560, "FLOWCHART · 02-02 RACK TIMELINE", "2 가 사라졌을 때 문턱과 RACK 의 시각표",
      "1 부터 5 를 1ms 간격으로 보냈고 2 가 사라졌다. RTT 는 10ms, 재정렬 창은 2.5ms 로 둔다. 12ms 에 3 의 SACK 이 오면 RACK 은 2 보다 나중에 "
      "보낸 것이 도착했음을 알고 2 의 마감을 보낸 시각 1ms 더하기 RTT 10ms 더하기 창 2.5ms 인 13.5ms 로 잡아 그때 재전송한다. "
      "문턱 방식은 3, 4, 5 의 도착으로 중복 ACK 를 세어 셋째인 14ms 에 재전송한다. 뒤에 3 만 오면 문턱은 멈추고 RTO 를 기다리지만 "
      "RACK 은 그대로 13.5ms 에 재전송한다.",
      lead="가로축은 보내는 쪽 시각입니다. RTT 10ms, 재정렬 창 2.5ms 로 가정했습니다.")
T0, PX = 206, 42


def x(ms):
    return T0 + ms * PX


def chip(y, ms, txt, c=None, dash=False, w=38):
    xx = x(ms) - w / 2
    if dash:
        d.o.append(f'<rect x="{xx}" y="{y}" width="{w}" height="28" rx="5" fill="none" stroke="{BAD}" stroke-width="1.2" stroke-dasharray="4 3"/>')
        d.t(x(ms), y + 19, txt, 12, BAD, MONO, "middle", 600)
    elif c:
        d.tone(xx, y, w, 28, c, 5, "14", 1.2)
        d.t(x(ms), y + 19, txt, 12, c, MONO if txt.isascii() else KR, "middle", 600)
    else:
        d.box(xx, y, w, 28, r=5)
        d.t(x(ms), y + 19, txt, 12, INK, MONO if txt.isascii() else KR, "middle", 600)


rows = [(120, "보냄"), (184, "받은 확인"), (262, "문턱 방식"), (340, "RACK"), (430, "3 만 왔다면")]
for y, lab in rows:
    d.t(24, y + 19, lab, 12, MUTED, KR, "start", 600)
    d.line(x(0), y + 14, x(16), y + 14, RULE, 0.8, "3 6")
for n in range(1, 6):
    chip(120, n - 1, str(n), dash=(n == 2))
d.t(x(1), 166, "사라짐", 11, BAD, KR, "middle")
chip(184, 10, "ACK 1")
for ms, n in ((12, 3), (13, 4), (14, 5)):
    chip(184, ms, f"S{n}", OK)
d.t(x(13), 230, "S = SACK", 11, MUTED, MONO, "middle")
# 문턱
chip(262, 12, "1")
chip(262, 13, "2")
chip(262, 14, "3", ACC)
d.t(x(14) + 26, 281, "→ 2 재전송", 12, ACC, KR, "start", 600)
d.t(x(12), 308, "중복 ACK 개수", 11, MUTED, KR, "middle")
# RACK
d.tone(x(1), 350, x(13.5) - x(1), 10, INK, 3, "10", 0.8)
d.t((x(1) + x(13.5)) / 2, 344, "2 의 마감: 보낸 1 + RTT 10 + 창 2.5", 11, MUTED, KR, "middle")
d.line(x(12), 364, x(12), 386, OK, 1.2, "4 3")
d.t(x(12) - 6, 400, "조건 1: 3 도착", 11, OK, KR, "end")
d.line(x(13.5), 336, x(13.5), 386, ACC, 1.6)
d.t(x(13.5) + 6, 400, "13.5 조건 2 → 2 재전송", 12, ACC, KR, "start", 600)
# 3 만 왔다면
chip(430, 12, "S3", OK)
d.t(x(12) - 26, 449, "문턱: 중복 1 에서 멈춤 → RTO 대기", 12, BAD, KR, "end")
d.line(x(13.5), 426, x(13.5), 466, ACC, 1.6)
d.t(x(13.5) + 6, 478, "RACK: 13.5 재전송 그대로", 12, ACC, KR, "start", 600)
ya = 506
d.line(x(0), ya, x(16), ya, SOFT, 1.0)
for ms in range(0, 17, 2):
    d.line(x(ms), ya - 4, x(ms), ya + 4, SOFT, 1.0)
    d.t(x(ms), ya + 18, f"{ms}ms", 11, MUTED, MONO, "middle")
d.save("02-02.rack-timeline.svg")
print("ok rack-timeline")
