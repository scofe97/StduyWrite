# 14-02.cancel-sequence — status 고루틴의 cancelFunc 가 Done 채널을 닫아 main 의 select 를 깨우고 delay 고루틴의 HTTP 요청도 끊는 순서
# 본문 요구(14-02 §1 「httpbin 예제」): status 고루틴이 500 을 받으면 cancelFunc 를 부른다. main 의 select 는 ctx.Done() case 로 루프를 빠져나오고,
#           delay 고루틴이 보낸 요청은 취소된 context 를 따라 context canceled 오류로 끝나 고루틴도 끝난다. main 은 wg.Wait 로 둘을 기다린다.
# 타입 스펙: type-sequence — 레인 3개(main · status 고루틴 · delay 고루틴), 시간은 위→아래, 메시지는 수평 화살표. 09-03.panic-recover 와 같은 방식.
#           stride: 행 간격 56. focal 은 cancelFunc 를 부르는 칩 하나.
# 사실 출처: Learning Go 2판 14장 「Cancellation」 cancel_http, go1.25.1 실행(2026-09-28) — bad status, exiting · in main: cancelled! ·
#           error in delay goroutine: Get "http://httpbin.org/delay/1": context canceled.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, BAD, INFO, PAPER2, KR, MONO

W, H = 984, 684
LANE_W = 232
LX = {"main": 152, "st": 492, "dl": 832}
Y0, STRIDE = 104, 56


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


d = D(W, H, "SEQUENCE · 14-02 §1",
      "status 고루틴의 취소가 delay 고루틴의 요청까지 끊습니다",
      "cancel_http 한 번을 시간순으로 그린 시퀀스. 두 고루틴이 성공 메시지를 채널로 보내다가 status 고루틴이 500 을 받고 cancelFunc 를 부른다. "
      "Done 채널이 닫혀 main 의 select 가 루프를 빠져나오고, delay 고루틴이 기다리던 HTTP 요청은 같은 context 를 따라 context canceled 로 끝나 고루틴도 끝난다.",
      lead="위에서 아래로 시간이 흐릅니다. 취소는 채널 하나가 닫히는 것으로 모두에게 전해집니다.")

for key, title, sub in [("main", "main", "for-select"), ("st", "status 고루틴", "/status/200,200,200,500"), ("dl", "delay 고루틴", "/delay/1")]:
    x = LX[key]
    d.box(x - LANE_W // 2, Y0, LANE_W, 48)
    d.t(x, Y0 + 20, title, 14, INK, kr(title), "middle", 600)
    d.t(x, Y0 + 38, sub, 11, MUTED, MONO, "middle")
    d.line(x, Y0 + 56, x, 608, RULE, 1.0, "3 6")


def msg(a, b, label, y, c=MUTED, mk="soft"):
    x1, x2 = LX[a], LX[b]
    dr = 1 if x2 > x1 else -1
    d.arrow([(x1 + 8 * dr, y), (x2 - 10 * dr, y)], c, mk, 1.5)
    d.t((x1 + x2) / 2, y - 10, label, 12, c if c != MUTED else INK, kr(label), "middle", 600)


def chip(key, y, txt, c, w=216, focal=False):
    x = LX[key]
    d.o.append(f'<rect x="{x - w // 2}" y="{y - 14}" width="{w}" height="28" rx="4" fill="#0D1117"/>')
    d.tone(x - w // 2, y - 14, w, 28, c, 4, "22" if focal else "14", 1.4 if focal else 1.0)
    d.t(x, y + 5, txt, 12, c, kr(txt), "middle", 600)


y = Y0 + 92
msg("st", "main", "success from status", y, OK, "ok")
y += STRIDE
msg("dl", "main", "success from delay", y, OK, "ok")
y += STRIDE
chip("st", y, "500 → cancelFunc()", ACC, focal=True)
y += STRIDE
msg("st", "main", "Done 채널 닫힘", y, BAD, "bad")
y += STRIDE
chip("main", y, "in main: cancelled! · break", INFO, w=224)
y += STRIDE
chip("dl", y, "Do → context canceled", BAD)
y += STRIDE
msg("dl", "main", "고루틴 끝 · wg.Done()", y, SOFT, "soft")
y += STRIDE
chip("main", y, "wg.Wait() 통과", OK)

d.legend(628, [("성공 메시지", OK), ("취소를 부름", ACC), ("취소가 전해짐", BAD)])
d.save("14-02.cancel-sequence.svg")
print("ok 14-02 cancel-sequence")
