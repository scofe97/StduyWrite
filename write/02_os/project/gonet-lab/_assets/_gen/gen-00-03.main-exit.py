# 00-03.main-exit — main 이 돌아가면 다른 goroutine 도 함께 끝난다
# 본문 요구(00-03 §1): "main 이 돌아가면 프로그램이 끝나고 다른 goroutine 이 끝나기를 기다리지 않는다" — Sleep 이
#           있을 때와 없을 때 두 막대의 끝이 어디에 묶이는지가 논지다.
# 타입 스펙: type-gantt — 막대 길이가 곧 실행 구간. 위 두 줄은 Sleep 있음, 아래 두 줄은 Sleep 없음.
# 사실 출처: Go 명세 Program execution, 본문 §1 예제 (로컬 go1.25.1 로 실행해 A·B 출력 확인).
from dd import D, INK, MUTED, SOFT, RULE, OK, WARN, BAD, INFO, KR, MONO

W, H = 960, 470
TX0, P, BH, LX = 220, 200, 24, 24
d = D(W, H, "GANTT · 00-03 MAIN EXIT", "main 이 돌아가면 프로그램이 끝납니다",
      "§1 예제의 두 goroutine 실행 구간을 시간 막대로 그린 도식. Sleep 이 있으면 main 이 goroutine B 의 출력 뒤까지 "
      "살아 있어 B 가 끝까지 돈다. Sleep 이 없으면 main 이 먼저 돌아가 프로그램이 끝나고, 아직 출력 전인 B 도 함께 잘린다.",
      lead="위 두 줄은 Sleep 이 있을 때, 아래 두 줄은 Sleep 이 없을 때입니다.")
ticks = [(0, "시작"), (1, "go 문"), (2, "B 가 출력할 때"), (3, "Sleep 끝")]
for k, lab in ticks:
    x = TX0 + k * P
    d.t(x, 116, lab, 12, SOFT, KR, "start" if k == 0 else "middle")
    d.line(x, 128, x, 392, RULE, 0.8, "3 5")
d.line(TX0, 128, TX0 + 3 * P, 128, RULE, 0.8)

def row(y, name, sub, s, e, c, text, dash=False):
    d.t(LX, y + 20, name, 13, INK, KR if any("가" <= ch <= "힣" for ch in name) else MONO, "start", 600)
    d.t(LX, y + 38, sub, 12, MUTED, KR, "start")
    x, w = TX0 + s * P, (e - s) * P
    d.tone(x, y + 10, w, BH, c, 4, "12", 1.0)
    d.t(x + 12, y + 27, text, 12, c, KR if any("가" <= ch <= "힣" for ch in text) else MONO, "start")

row(144, "main", "Sleep 있음", 0, 3, INFO, "A 출력 · Sleep")
row(196, "goroutine B", "Sleep 있음", 1, 2, OK, "B 출력까지 끝남")
d.line(LX, 256, W - 40, 256, RULE, 0.8)
row(272, "main", "Sleep 없음", 0, 1.5, INFO, "A 출력 · return")
row(324, "goroutine B", "Sleep 없음", 1, 1.5, WARN, "잘림")
d.line(TX0 + 1.5 * P, 336, TX0 + 2 * P, 336, WARN, 1.2, "5 4")
d.t(TX0 + 2 * P + 8, 340, "출력하지 못함", 12, WARN, KR, "start")
d.line(TX0 + 1.5 * P, 264, TX0 + 1.5 * P, 384, BAD, 1.6)
d.t(TX0 + 1.5 * P + 8, 380, "프로그램 종료", 12, BAD, KR, "start", 600)
d.legend(412, [("main", INFO), ("끝까지 돈 goroutine", OK), ("잘린 goroutine", WARN), ("프로그램 종료", BAD)])
d.save("00-03.main-exit.svg")
print("ok main-exit")
