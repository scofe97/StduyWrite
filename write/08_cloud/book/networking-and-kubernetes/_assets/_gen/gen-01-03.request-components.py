# 01-03.request-components — 접히는 왕복 경로
# 본문: "눈여겨볼 것은 가운데가 접힌다는 점이다. localhost 요청이라 패킷이 물리 케이블로
#        나가지 않고 lo0 에서 되돌아온다. 같은 커널이 송신에서 붙이고 수신에서 벗긴다."
# 타입 스펙: type-flowchart.md 관례 — 되돌아오는 흐름은 직교 라우팅으로 접고,
#           접히는 지점 하나에만 focal 을 건다
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 620
d = D(W, H, "curl localhost:8080 · COMPONENT PATH",
      "요청 하나가 지나는 실제 구성 요소 — lo0 에서 접혀 되돌아온다",
      "계층 이름 대신 실제로 존재하는 구성 요소로 같은 여정을 놓으면 가운데가 접힌다",
      lead="계층 이름 대신 실제 구성 요소로 놓으면 — 가운데가 접힌다")

BW, BH = 160, 84
TOP_CX, BOT_CX = [132, 332, 532], [532, 332, 132]
CY_T, CY_B, FOLD = 204, 444, (808, 324)

def comp(cx, cy, label, sub, tag, c=None, focal=False, w=BW):
    x, y = cx - w // 2, cy - BH // 2
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{BH}" rx="6" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
        lc, sc, tc = ACC, ACC, ACC
    else:
        d.box(x, y, w, BH, PAPER2, c or RULE, 1.1, 6)
        lc, sc, tc = INK, MUTED, (c or SOFT)
    d.t(cx, cy - 12, ddx.fit(label, 12, w - 20, label), 12, lc, KR, "middle", 600)
    d.t(cx, cy + 8,  ddx.fit(sub, 11, w - 20, sub), 11, sc, KR)
    d.t(cx, cy + 30, tag, 9, tc, MONO)

ddx.band(d, 104, 544, "같은 커널이 송신 경로에서 헤더를 붙이고 수신 경로에서 그것을 벗긴다")

for cx, (l, s, t) in zip(TOP_CX, [("cURL 프로세스", "사용자 공간", "REQUEST START"),
                                  ("클라이언트 소켓", "임시 포트", "LOGICAL ENDPOINT"),
                                  ("커널 송신", "헤더 붙이기", "ENCAPSULATE")]):
    comp(cx, CY_T, l, s, t, INFO if t == "ENCAPSULATE" else None)
for cx, (l, s, t) in zip(BOT_CX, [("커널 수신", "헤더 벗기기", "DECAPSULATE"),
                                  ("서버 소켓", "8080", "LISTEN"),
                                  ("Go 서버", "0.0.0.0:8080", "RESPONSE")]):
    comp(cx, CY_B, l, s, t, INFO if t == "DECAPSULATE" else (OK if t == "RESPONSE" else None))
comp(FOLD[0], FOLD[1], "lo0", "논리 인터페이스", "LOOPBACK", focal=True, w=140)

E = BW // 2
for a, b in zip(TOP_CX, TOP_CX[1:]):                       # 위: 왼→오
    d.path(f"M {a+E+8} {CY_T} L {b-E-10} {CY_T}", MUTED, 1.5, m="ar")
for a, b in zip(BOT_CX, BOT_CX[1:]):                       # 아래: 오→왼
    d.path(f"M {a-E-8} {CY_B} L {b+E+10} {CY_B}", MUTED, 1.5, m="ar")
# 접히는 자리 — 오른쪽으로 나갔다가 그대로 되돌아온다
d.path(f"M {TOP_CX[2]+E+8} {CY_T} L {FOLD[0]} {CY_T} L {FOLD[0]} {FOLD[1]-BH//2-10}", ACC, 1.6, m="acc")
d.path(f"M {FOLD[0]} {FOLD[1]+BH//2+8} L {FOLD[0]} {CY_B} L {BOT_CX[0]+E+10} {CY_B}", ACC, 1.6, m="acc")
d.t(FOLD[0] - 16, 250, "물리 케이블로 나가지 않는다", 11, ACC, KR, "end")

d.t(24 + 12, 514, "tcpdump -i lo0 이 잡은 자리가 바로 이 접히는 지점이다 — 나가는 프레임과 "
                  "돌아오는 프레임이 같은 인터페이스에서 관측된다", 12, MUTED, KR, "start")
d.legend(564, [("캡슐화·역캡슐화", INFO), ("응답 생성", OK), ("되돌아오는 자리", ACC)])
d.save("01-03.request-components.svg")
print("ok request-components")
