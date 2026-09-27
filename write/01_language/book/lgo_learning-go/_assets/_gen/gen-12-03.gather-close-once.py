# 12-03.gather-close-once — processAndGather: 처리 고루틴 num 개가 out 에 쓰고, 감시 고루틴이 Wait 뒤에 out 을 한 번만 닫는다
# 본문 요구(12-03 §5 「채널을 한 번만 닫습니다」): in 채널을 처리 고루틴 num 개가 나눠 읽어 out 에 쓰고, 각자 defer wg.Done() 한다.
#           감시 고루틴은 wg.Wait() 로 모두 끝나기를 기다린 뒤 close(out) 을 한 번만 부르고, 함수는 out 을 for-range 로 모아 돌려준다.
# 타입 스펙: type-architecture — 왼쪽 in 채널 → 가운데 처리 고루틴 셋(1 · 2 · num) → out 채널 → result. 감시 고루틴은 out 아래.
#           직교 화살표만 쓴다. focal 은 감시 고루틴의 close 화살표 하나. 노드 폭 in 150 · 처리 190 · out 170 · result 136.
# 사실 출처: Learning Go 2판 12장 「Use WaitGroups」, 원서 예제 저장소 ch12 sample_code/waitgroup_close_once 를 go1.25.1 로 실행 —
#           값 20개를 섞인 순서로 모두 모음(2026-09-28).
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, KR, MONO

W, H = 960, 560


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


d = D(W, H, "ARCHITECTURE · 12-03 §5",
      "처리 고루틴 num 개가 out 에 쓰고, 감시 고루틴이 Wait 뒤에 한 번만 닫습니다",
      "processAndGather 의 구조. 처리 고루틴 num 개가 in 채널을 나눠 읽고 processor 결과를 버퍼 크기 num 인 out 채널에 쓴다. "
      "각 처리 고루틴은 끝날 때 defer wg.Done() 으로 수를 줄인다. 감시 고루틴은 wg.Wait() 로 모두 끝나기를 기다린 뒤 close(out) 을 한 번만 부른다. "
      "함수는 out 을 for-range 로 읽다가 닫히고 비면 모은 result 를 돌려준다.",
      lead="실선은 값의 흐름, 점선은 WaitGroup 수 줄이기, 주황은 채널을 닫는 한 번입니다.")


def node(x, y, w, h, title, sub, c=None):
    if c:
        d.tone(x, y, w, h, c, 6, "14", 1.1)
    else:
        d.box(x, y, w, h)
    d.t(x + w / 2, y + h / 2 - 3, title, 13, c or INK, kr(title), "middle", 600)
    d.t(x + w / 2, y + h / 2 + 16, sub, 11, MUTED, kr(sub), "middle")


IN = (24, 220, 150, 64)
WK = [(264, 124, 190, 56), (264, 224, 190, 56), (264, 324, 190, 56)]
OUT = (552, 220, 170, 64)
RES = (800, 220, 136, 64)
MON = (552, 404, 170, 64)

# 값의 흐름 — in → 처리 고루틴(분기), 처리 고루틴 → out(합류)
ix = IN[0] + IN[2]
d.line(ix, 252, 219, 252, SOFT, 1.3)
d.line(219, 152, 219, 352, SOFT, 1.3)
for (x, y, w, h) in WK:
    d.arrow([(219, y + h / 2), (x - 3, y + h / 2)], SOFT, "soft", 1.3)
    d.line(x + w, y + h / 2, 503, y + h / 2, SOFT, 1.3)
d.line(503, 152, 503, 352, SOFT, 1.3)
d.arrow([(503, 252), (OUT[0] - 3, 252)], SOFT, "soft", 1.3)
d.arrow([(OUT[0] + OUT[2], 252), (RES[0] - 3, 252)], SOFT, "soft", 1.3)
d.t(761, 244, "for-range", 11, MUTED, MONO, "middle", 600)

# WaitGroup — 처리 고루틴 → 감시 고루틴(점선)
wx = WK[2][0] + WK[2][2] / 2
d.path(f"M {wx} {WK[2][1] + WK[2][3]} L {wx} 436 L {MON[0] - 3} 436", MUTED, 1.2, m="ar", dash="5 4")
d.t(wx + 10, 420, "defer wg.Done() × num", 11, MUTED, MONO, "start", 600)

# 감시 고루틴 → out 을 닫음(focal)
mx = MON[0] + MON[2] / 2
d.arrow([(mx, MON[1] - 2), (mx, OUT[1] + OUT[3] + 4)], ACC, "acc", 1.6)
d.t(mx + 10, 350, "close(out) 한 번", 12, ACC, KR, "start", 600)

node(*IN, "in", "<-chan T")
for i, (x, y, w, h) in enumerate(WK):
    node(x, y, w, h, "처리 고루틴 " + ("1", "2", "num")[i], "for v := range in", INFO)
node(*OUT, "out", "chan R · 버퍼 num")
node(*RES, "result", "[]R 반환", OK)
node(*MON, "감시 고루틴", "wg.Wait()", ACC)

d.legend(496, [("처리 고루틴", INFO), ("채널을 닫는 한 번", ACC), ("돌려주는 값", OK)])
d.save("12-03.gather-close-once.svg")
print("ok 12-03 gather")
