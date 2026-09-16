# 01-02.time-wait-2msl — 2MSL은 최악의 두 구간을 더한 값이다
# 본문 요구(01-02 §3 "2MSL이 왜 하필 두 배인가"): "두 구간이 각각 최대 1MSL입니다. 내가 보낸 마지막
#           ACK가 거의 다 가서 사라지기까지 1MSL, 그것을 못 받은 상대가 FIN을 재전송해 내게 닿기까지
#           다시 1MSL" — 구간 두 개가 이어 붙어 합이 되는 것이 논지다. 그리고 앞 문단의 대조
#           "기록이 이미 사라졌다면 … RST가 나가고, 상대는 오류로 끊긴 것으로 기록"이 아래 줄이다.
# 타입 스펙: type-gantt — 막대 길이가 곧 구간. 두 막대가 끝과 끝으로 이어지고, 그 둘을 덮는
#           TIME-WAIT 막대 하나가 focal 이다. 시간 축은 0 · 1MSL · 2MSL 세 눈금뿐이다.
# 사실 출처: 2026-09-09 손 SVG 원본과 본문 §3 두 문단. 원본은 두 레인 사이 비스듬한 선으로 유실과
#           재전송을 그렸는데, 구간의 합이 논지라 막대로 바꿨다.
# 이력: 2026-09-15 신설. 손 SVG 를 생성기로 옮기며 9px 한글 라벨과 하단 해설 문장을 없앴다.
import ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, WARN, BAD, KR, MONO

W, H = 1000, 460
TX0, MSL = 200, 360                 # 시간 축 시작 · 1MSL 폭 (2MSL = 720px, 끝 x=920)
RY0, RS, BH = 148, 56, 24           # 첫 줄 y · 줄 간격 · 막대 높이
LX = 24                             # 왼쪽 라벨 칸

d = D(W, H, "GANTT · 01-02 TIME-WAIT",
      "2MSL은 최악의 두 구간을 더한 값",
      "마지막 ACK 가 유실되는 최악의 경우를 시간 막대로 그린 도식. 유실까지 최대 1MSL, 상대의 FIN "
      "재전송이 돌아오기까지 다시 최대 1MSL 이라 TIME-WAIT 는 2MSL 을 기다린다. 기록을 미리 지우면 "
      "재전송 FIN 에 RST 가 나가는 갈래를 아래에 대조로 두었다.",
      lead="마지막 ACK가 유실되는 경우를 최악으로 잡고 두 구간을 더합니다.")

# 시간 눈금
for k, lab in enumerate(("0", "1 MSL", "2 MSL")):
    x = TX0 + k * MSL
    d.t(x, 124, lab, 12, SOFT, MONO, "start" if k == 0 else ("end" if k == 2 else "middle"))
    d.line(x, 132, x, 392, RULE, 0.8, "3 5")
d.line(TX0, 132, TX0 + 2 * MSL, 132, RULE, 0.8)

def row(i, name, sub, start, span, c, text, focal=False):
    y = RY0 + i * RS
    d.t(LX, y + 20, name, 13, INK, KR, "start", 600)
    d.t(LX, y + 38, sub, 11, MUTED, KR, "start")
    x, w = TX0 + start * MSL, span * MSL
    d.tone(x, y + 12, w, BH, c, 4, "14" if focal else "10", 1.4 if focal else 1.0)
    d.t(x + 12, y + 29, ddx.fit(text, 12, w - 20, text), 12, c, KR, "start", 600 if focal else 400)

row(0, "마지막 ACK", "먼저 닫은 쪽이 보냄", 0, 1, BAD, "유실까지 최대 1 MSL")
row(1, "FIN 재전송", "확인 못 받은 상대가 보냄", 1, 1, WARN, "돌아오기까지 최대 1 MSL")
row(2, "TIME-WAIT", "먼저 닫은 쪽의 기록", 0, 2, ACC, "2 MSL 유지 · 재전송 FIN 에 ACK 응답", focal=True)

# 대조 — 기록을 미리 지운 경우
d.line(LX, 324, W - 40, 324, RULE, 0.8)
y = RY0 + 3 * RS + 24
d.t(LX, y + 20, "기록 조기 삭제", 13, INK, KR, "start", 600)
d.t(LX, y + 38, "대조 · 잘못된 경우", 11, MUTED, KR, "start")
d.tone(TX0, y + 12, MSL // 2, BH, SOFT, 4, "10", 1.0)
d.t(TX0 + 12, y + 29, "기록 삭제", 12, SOFT, KR, "start")
d.line(TX0 + 2 * MSL, y + 8, TX0 + 2 * MSL, y + 40, BAD, 1.6)
d.t(TX0 + 2 * MSL - 12, y + 29, "재전송 FIN → RST · 오류 종료", 12, BAD, KR, "end", 600)

d.legend(420, [("유실 구간", BAD), ("재전송 구간", WARN), ("TIME-WAIT 대기", ACC), ("미리 지운 기록", SOFT)])
d.save("01-02.time-wait-2msl.svg")
print("ok time-wait-2msl")
