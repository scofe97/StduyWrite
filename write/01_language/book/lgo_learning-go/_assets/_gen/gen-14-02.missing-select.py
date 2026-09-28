# 14-02.missing-select — select 보호 없이 ch <- 로 보내는 고루틴은, main 이 취소를 보고 떠난 뒤에 보내면 영원히 멈춘다
# 본문 요구(14-02 §2 「select 보호를 뺀 판은 드물게 멈출 수 있습니다」): cancel_error_http 는 첫 판의 select { case ch <- …: case <-ctx.Done(): } 를
#           ch <- … 로 바꿨다. 응답을 받은 고루틴이 쓰려는 순간 main 이 이미 루프를 떠났다면 받는 쪽이 없다. 노트는 status 쪽 100ms 뒤 취소,
#           delay 쪽 200ms 뒤 쓰기로 순서를 강제해 deadlock 을 재현했다.
# 타입 스펙: type-sequence — 레인 3개(main · status 고루틴 · delay 고루틴), 시간은 위→아래, 메시지는 수평 화살표. 14-02.cancel-sequence 와 같은 방식.
#           stride: 행 간격 56. focal 은 받는 쪽 없이 멈춘 쓰기 칩 하나. 100ms·200ms 는 재현을 위해 강제한 시점이다.
# 사실 출처: go1.25.1 재현(2026-09-28) — in main: cancelled with error bad status · fatal error: all goroutines are asleep - deadlock!
#           로컬 HTTP 서버 + http.DefaultClient 로는 deadlock 없이 5초 timeout 까지 멈춤(exit 124), DisableKeepAlives 면 deadlock!.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, BAD, INFO, PAPER2, KR, MONO

W, H = 984, 584
LANE_W = 232
LX = {"main": 152, "st": 492, "dl": 832}
Y0, STRIDE = 104, 56


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


d = D(W, H, "SEQUENCE · 14-02 §2",
      "select 보호가 없으면 떠난 main 에게 보내다 멈춥니다",
      "select 보호를 뺀 cancel_error_http 의 모양에서 순서를 강제한 재현. 100ms 에 status 고루틴이 원인을 넘겨 취소하면 main 은 Done 을 보고 루프를 떠나 wg.Wait 에 들어간다. "
      "200ms 에 응답을 받은 delay 고루틴이 ch 에 쓰려 하지만 읽는 쪽이 없어 멈추고, 모든 고루틴이 잠들어 런타임이 deadlock 으로 끝낸다. "
      "기본 클라이언트의 keep-alive 연결이 남아 있으면 그 고루틴이 네트워크를 기다리므로 deadlock 없이 wg.Wait 에서 계속 멈춘다.",
      lead="100ms·200ms 는 강제한 시점입니다. keep-alive 연결이 남으면 deadlock 없이 멈춥니다.")

for key, title, sub in [("main", "main", "for-select → wg.Wait"), ("st", "status 고루틴", "100ms 에 실패"), ("dl", "delay 고루틴", "200ms 에 응답")]:
    x = LX[key]
    d.box(x - LANE_W // 2, Y0, LANE_W, 48)
    d.t(x, Y0 + 20, title, 14, INK, kr(title), "middle", 600)
    d.t(x, Y0 + 38, sub, 11, MUTED, kr(sub), "middle")
    d.line(x, Y0 + 56, x, 508, RULE, 1.0, "3 6")


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
chip("st", y, "cancelFunc(bad status)", INFO)
y += STRIDE
msg("st", "main", "Done 채널 닫힘", y, BAD, "bad")
y += STRIDE
chip("main", y, "break loop → wg.Wait()", INFO, w=224)
y += STRIDE
chip("dl", y, "ch <- \"success …\"", ACC, focal=True)
y += STRIDE
d.t(LX["dl"] - 16, y, "읽는 쪽이 없어 멈춤", 12, ACC, KR, "end", 600)
y += STRIDE
chip("main", y, "deadlock! 또는 무한 대기", BAD, w=224)

d.legend(528, [("취소", INFO), ("받는 쪽 없는 쓰기", ACC), ("결과", BAD)])
d.save("14-02.missing-select.svg")
print("ok 14-02 missing-select")
