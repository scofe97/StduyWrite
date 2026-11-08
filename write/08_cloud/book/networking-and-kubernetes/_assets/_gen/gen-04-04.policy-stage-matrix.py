# 04-04.policy-stage-matrix — 정책 단계마다 같은 요청이 받은 응답 코드
# 본문 요구: `## 선택되는 순간의 잠금` 의 확인된 것 — 정책 전 둘 다 200, 2단계(선택만)에서 demo→db·cart→db 는 000 인데 cart→web 은 200,
#           demo-db 의 DNS 는 bad address, 3단계(demo 허용)에서 demo 200·cart 000, port 8080 이면 둘 다 000, ports 생략이면 demo 200·cart 000.
#           잠근 것은 그 정책이 아니라 "선택되었다는 사실" — lockdown 을 지워도 결과는 그대로.
# 타입 스펙: type-heatmap — 행(요청) × 열(정책 단계) 교차표의 값을 칸 색으로. 어느 칸이 튀는지가 논지.
#           200 은 OK, 000 은 BAD, DNS 실패는 WARN, 재지 않은 칸은 점선. coral focal 은 2단계 cart→web 200 한 칸.
import ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER2, KR, MONO

W, H = 1000, 580
LX = 24
CX0, CW, CG = 236, 140, 8
RY0, RH, RS = 178, 64, 76

COLS = [
    ("정책 전", "선택된 Pod 없음"),
    ("2단계", "선택만 · 규칙 0줄"),
    ("3단계", "demo 허용 · 80"),
    ("변형 1", "허용 포트 8080"),
    ("변형 2", "ports 생략"),
]
ROWS = [
    ("demo → demo-db:80", [("200", ""), ("000", "3.00s 타임아웃"), ("200", ""), ("000", "3.00s 타임아웃"), ("200", "")]),
    ("cart → demo-db:80", [("200", ""), ("000", "3.00s 타임아웃"), ("000", "3.00s 타임아웃"), ("000", "3.00s 타임아웃"), ("000", "3.00s 타임아웃")]),
    ("cart → web.default", [None, ("200", "정책에 이름이 없음"), None, None, None]),
    ("demo-db → DNS", [None, ("FAIL", "bad address"), None, None, None]),
]
FOCAL = (2, 1)

d = D(W, H, "HEATMAP · 04-04 POLICY STAGES",
      "같은 cart 가 목적지에 따라 막히고 열립니다",
      "NetworkPolicy 단계별 응답 코드 격자. 정책 전에는 demo 와 cart 모두 demo-db 에 200 을 받는다. "
      "2단계에서 demo-db 만 선택하면 demo 와 cart 모두 demo-db 에 000 을 받지만 cart 는 web 에 200 을 받는다. "
      "3단계에서 demo 를 허용하면 demo 는 200, cart 는 000 이다. 포트를 8080 으로 바꾸면 둘 다 000 이고 ports 를 생략하면 demo 200, cart 000 이다.",
      lead="칸 안은 curl 응답 코드이고 000 은 응답이 없는 타임아웃입니다")

for j, (h1, h2) in enumerate(COLS):
    cx = CX0 + j * (CW + CG) + CW / 2
    d.t(cx, 122, h1, 14, INK, KR, "middle", 600)
    d.t(cx, 144, ddx.fit(h2, 12, CW - 4, h2), 12, MUTED, KR, "middle")
d.line(LX, 156, CX0 + 5 * (CW + CG) - CG, 156, RULE, 0.8)

for i, (label, cells) in enumerate(ROWS):
    y = RY0 + i * RS
    d.t(LX, y + RH / 2 + 4, ddx.fit(label, 13, CX0 - LX - 16, label), 13, INK, MONO, "start", 600)
    for j, cell in enumerate(cells):
        x = CX0 + j * (CW + CG)
        if cell is None:
            d.o.append(f'<rect x="{x}" y="{y}" width="{CW}" height="{RH}" rx="6" fill="none" '
                       f'stroke="{SOFT}" stroke-width="0.9" stroke-dasharray="4 4"/>')
            d.t(x + CW / 2, y + RH / 2 + 5, "—", 14, SOFT, MONO, "middle")
            continue
        code, sub = cell
        if (i, j) == FOCAL:
            c, op, sw = ACC, "1F", 1.6
        elif code == "200":
            c, op, sw = OK, "14", 1.1
        elif code == "000":
            c, op, sw = BAD, "14", 1.1
        else:
            c, op, sw = WARN, "14", 1.1
        d.tone(x, y, CW, RH, c, 6, op, sw)
        if sub:
            d.t(x + CW / 2, y + 28, code, 18, c, MONO, "middle", 600)
            d.t(x + CW / 2, y + 50, ddx.fit(sub, 12, CW - 12, sub), 12, MUTED, KR, "middle")
        else:
            d.t(x + CW / 2, y + RH / 2 + 6, code, 18, c, MONO, "middle", 600)

d.t(LX, 500, "demo-db-lockdown 삭제 → 3단계 결과 그대로 · 잠근 것은 선택되었다는 사실", 12, MUTED, KR, "start")
d.legend(524, [("응답 200", OK), ("응답 없음 000", BAD), ("이름 풀기 실패", WARN), ("같은 cart 인데 열린 칸", ACC)])
d.save("04-04.policy-stage-matrix.svg")
print("ok policy-stage-matrix")
