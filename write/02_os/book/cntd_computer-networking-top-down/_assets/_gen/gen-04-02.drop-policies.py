# 04-02 §4 — 넘치면 무엇을 버리나. 세 정책이 큐의 어느 시점에 개입하는지를 한 축 위에 편다.
# 왼쪽에서 오른쪽으로 큐가 차오르고, AQM 은 차기 전에 · 꼬리 버리기와 선 것 빼내기는 찬 뒤에 손을 댄다.
# 그 시점 차이가 곧 "송신자가 언제 알아채는가" 의 차이다.
# 타입 스펙: type-gantt — 시간축 위의 국면과 개입 구간. 막대의 시작 위치가 곧 개입 시점이다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, BAD, WARN, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 468
AX0, AX1 = 210, 936          # 큐 점유 축
AY = 152                     # 큐 막대
ABH = 44
ROW_Y0, ROW_H, BAR_H = 246, 58, 34
THRESH = 0.58                # AQM 이 반응하기 시작하는 지점 (장면용 값)

d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 04-02 §4",
      "언제 손대느냐가 세 정책을 가릅니다",
      "버퍼가 차오르는 축 위에 세 정책의 개입 시점을 놓았다. AQM 은 버퍼가 차기 전에 표시하거나 미리 버리고, "
      "꼬리 버리기와 이미 선 것 빼내기는 버퍼가 찬 뒤에만 반응하므로 지연이 이미 최대일 때 송신자가 알아챈다.",
      "AQM 은 차기 전에, 나머지 둘은 찬 뒤에 반응합니다")

def px(v):
    return AX0 + (AX1 - AX0) * v

# 큐 점유 막대
d.t(AX0 - 12, AY + 27, "출력 버퍼", 13, INK, KR, "end", 600)
d.box(AX0, AY, AX1 - AX0, ABH, PAPER2, RULE, 1.0, 6)
d.tone(AX0, AY, px(THRESH) - AX0, ABH, INFO, 6, "14", 1.0)
d.tone(px(THRESH), AY, px(1.0) - px(THRESH), ABH, WARN, 6, "14", 1.0)
d.t((AX0 + px(THRESH)) / 2, AY + 27, "여유 있음", 13, INFO, KR)
d.t((px(THRESH) + AX1) / 2, AY + 27, "차오름", 13, WARN, KR)

# 눈금 — 문턱과 가득
d.line(px(THRESH), AY - 14, px(THRESH), AY + ABH + 10, RULE, 0.9, "3 4")
d.t(px(THRESH), AY - 22, "AQM 문턱", 13, ACC, KR, "middle", 600)
d.line(AX1, AY - 14, AX1, AY + ABH + 10, RULE, 0.9, "3 4")
d.t(AX1, AY - 22, "가득 참", 13, BAD, KR, "middle", 600)
d.t(AX0, AY - 22, "버퍼 빔", 13, SOFT, KR, "middle")

# 세 정책 — 개입 시점에서 시작하는 막대
POL = [("AQM", "차기 전", THRESH, 1.0, ACC, "표시(ECN) 또는 조기 폐기", True),
       ("꼬리 버리기", "찬 뒤", 1.0, 1.0, BAD, "도착한 것을 버림", False),
       ("이미 선 것 빼내기", "찬 뒤", 1.0, 1.0, BAD, "줄 안에서 골라 뺌", False)]

for i, (name, when, s, e, c, what, focal) in enumerate(POL):
    y = ROW_Y0 + ROW_H * i
    d.t(AX0 - 12, y + 22, name, 13, INK, KR, "end", 600)
    d.t(AX0 - 12, y + 40, when, 13, SOFT, KR, "end")
    x0 = px(s)
    if s < e:
        d.tone(x0, y, px(e) - x0, BAR_H, c, 5, "14", 1.4 if focal else 1.1)
        d.t(x0 + 12, y + 22, what, 12, c, KR, "start", 600)
    else:
        d.tone(x0 - 8, y, 16, BAR_H, c, 3, "22", 1.2)
        d.t(x0 - 20, y + 22, what, 12, c, KR, "end", 600)
    # 개입 시점에서 큐 축으로 올리는 점선
    d.line(x0, AY + ABH + 10, x0, y - 6, c, 0.9, "3 4")

d.legend(H - 44, [("차기 전에 개입 — AQM", ACC), ("찬 뒤에만 개입", BAD), ("여유", INFO), ("차오름", WARN)])
d.save("04-02.drop-policies.svg")
