# 타입 스펙: type-sequence
# 14-01.request-context — HTTP 요청 도착부터 미들웨어의 context 감싸기, 핸들러 전달 및 업무 로직 호출 순서
# 본문 요구(14-01 §1 「HTTP 서버는 요청에 붙은 context 를 씁니다」): 요청 도착 → r.Context() 로 꺼냄 → 값을 더한 새 context
#           → r.WithContext(ctx) 로 바꾼 요청 → 다음 핸들러. 이름은 그 절 코드(84·99·121행 블록)의 것만 쓴다.
# 타입 스펙: type-sequence — 레인 4개(Client · Middleware · handler · logic), 시간은 위→아래, 메시지는 수평 화살표.
#           focal 은 req.WithContext(ctx) 로 새 요청을 만드는 칩 하나.
# 사실 출처: Learning Go 2판 14장 「The Context」 net/http context patterns, go1.25.1 / go1.27.1 로컬 대조.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, BAD, INFO, PAPER2, KR, MONO

W, H = 984, 640
LANE_W = 196
LX = {"client": 120, "mw": 360, "handler": 620, "logic": 860}
Y0, STRIDE = 104, 46


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


d = D(W, H, "SEQUENCE · 14-01 §1",
      "요청의 context 를 꺼내 감싸고 새 요청으로 넘깁니다",
      "요청 도착 시 미들웨어가 req.Context() 로 context 를 꺼내고 값을 더한 새 context 로 감싼다. "
      "req.WithContext(ctx) 로 새 요청을 만들어 handler.ServeHTTP 에 넘기면, "
      "핸들러는 context 를 꺼내 logic(ctx, data) 의 첫 매개변수로 전달한다.",
      lead="위에서 아래로 시간이 흐릅니다. Request 는 불변이므로 WithContext 로 새 요청을 만듭니다.")

lanes = [
    ("client", "Client", "http.Request"),
    ("mw", "Middleware", "http.HandlerFunc"),
    ("handler", "handler", "http.HandlerFunc"),
    ("logic", "logic", "logic(ctx, data)"),
]

for key, title, sub in lanes:
    x = LX[key]
    d.box(x - LANE_W // 2, Y0, LANE_W, 48)
    d.t(x, Y0 + 20, title, 14, INK, kr(title), "middle", 600)
    d.t(x, Y0 + 38, sub, 11, MUTED, MONO, "middle")
    d.line(x, Y0 + 56, x, 560, RULE, 1.0, "3 6")


def msg(a, b, label, y, c=MUTED, mk="soft", dash=None):
    x1, x2 = LX[a], LX[b]
    dr = 1 if x2 > x1 else -1
    d.arrow([(x1, y), (x2, y)], c, mk, 1.5, dash=dash)
    d.t((x1 + x2) / 2, y - 9, label, 11, c if c != MUTED else INK, kr(label), "middle", 600)


def chip(key, y, txt, c, w=200, focal=False):
    x = LX[key]
    d.o.append(f'<rect x="{x - w // 2}" y="{y - 13}" width="{w}" height="26" rx="4" fill="#0D1117"/>')
    d.tone(x - w // 2, y - 13, w, 26, c, 4, "22" if focal else "14", 1.4 if focal else 1.0)
    d.t(x, y + 4, txt, 11, c, MONO, "middle", 600)


y = Y0 + 72
msg("client", "mw", "req (HTTP 요청)", y, INFO, "info")
y += STRIDE
chip("mw", y, "ctx := req.Context()", SOFT, w=188)
y += STRIDE
chip("mw", y, "ctx (새 context 로 감싸기)", INFO, w=188)
y += STRIDE
chip("mw", y, "req = req.WithContext(ctx)", ACC, w=192, focal=True)
y += STRIDE
msg("mw", "handler", "handler.ServeHTTP(rw, req)", y, OK, "ok")
y += STRIDE
chip("handler", y, "ctx := req.Context()", SOFT, w=188)
y += STRIDE
msg("handler", "logic", "logic(ctx, data)", y, INFO, "info")
y += STRIDE
msg("logic", "handler", "result", y, OK, "ok", dash="4 4")
y += STRIDE
msg("handler", "client", "rw.Write([]byte(result))", y, OK, "ok", dash="4 4")

d.legend(584, [("요청 및 호출", INFO), ("새 요청 생성 (핵심)", ACC), ("정상 응답", OK)])
out_path = str(pathlib.Path(__file__).resolve().parent.parent / "14-01.request-context.svg")
d.save(out_path)
print("ok 14-01 request-context")
