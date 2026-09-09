# 02-01 §4 — 애플리케이션과 애플리케이션 층 프로토콜을 갈라 놓는다.
# 본문이 웹의 조각을 넷으로 세어 두었다: HTML, 브라우저, 웹 서버, 그리고 애플리케이션 층 프로토콜.
# Netflix 도 같은 방식으로 셋다. 그래서 두 상자를 같은 문법으로 그리고, 프로토콜 칸에만 강조를 줬다.
# 아래 칸의 넷은 본문이 "프로토콜이 정의하는 것"으로 센 종류·문법·의미·규칙 그대로다.
# 타입 스펙: type-nested — 포함으로 드러나는 계층. 바깥은 애플리케이션, 안은 그 조각.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, PAPER2, RULE, KR, MONO

W, H = 1000, 648
d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 02-01 §4",
      "프로토콜은 애플리케이션의 한 조각입니다",
      "웹과 Netflix 를 각각 네 조각으로 나누고, 그중 프로토콜 한 칸이 정의하는 것을 아래에 폈다.",
      "HTTP 를 안다고 웹을 아는 것이 아닙니다")

def app_box(x, title, items, focal_idx, focal_col):
    d.box(x, 112, 468, 192, "none", RULE, 1.0)
    d.t(x + 20, 138, title, 14, INK, KR, "start", 600)
    cx = []
    for i, (name, sub) in enumerate(items):
        bx = x + 20 + (i % 2) * 218
        by = 156 + (i // 2) * 60
        cx.append(bx + 105)
        if i == focal_idx:
            d.tone(bx, by, 210, 48, focal_col, 6, "12", 1.4)
            d.t(bx + 105, by + 22, name, 12, focal_col, KR, "middle", 600)
        else:
            d.box(bx, by, 210, 48, PAPER2, RULE, 0.9)
            d.t(bx + 105, by + 22, name, 12, INK, KR)
        d.t(bx + 105, by + 39, sub, 11, MUTED, KR)
    return cx[focal_idx]

hx = app_box(24, "웹 애플리케이션",
             [("HTML", "문서 형식 표준"), ("브라우저", "클라이언트"),
              ("웹 서버", "요청을 받는 쪽"), ("HTTP", "애플리케이션 층 프로토콜")], 3, ACC)
nx = app_box(508, "Netflix",
             [("비디오 서버", "저장하고 전송합니다"), ("과금·관리 서버", "클라이언트 기능을 관리합니다"),
              ("클라이언트 앱", "재생하는 쪽"), ("DASH", "애플리케이션 층 프로토콜")], 3, INFO)

d.path(f"M {hx} 306 L {hx} 348", ACC, 1.4, m="acc")
d.path(f"M {nx} 306 L {nx} 348", INFO, 1.3, m="info")

d.box(24, 350, 952, 156, "none", RULE, 1.0)
d.t(44, 376, "그 한 조각이 정의하는 넷", 14, INK, KR, "start", 600)
FOUR = [("메시지의 종류", "요청과 응답 같은 것"), ("메시지의 문법", "어떤 필드가 있고 어떻게 나누나"),
        ("필드의 의미", "그 안의 정보가 무엇을 뜻하나"), ("언제 어떻게", "보내고 응답하는 규칙")]
for i, (name, sub) in enumerate(FOUR):
    bx = 44 + i * 228
    d.box(bx, 394, 212, 60, PAPER2, RULE, 0.9)
    d.t(bx + 106, 418, name, 12, INK, KR)
    d.t(bx + 106, 438, sub, 11, MUTED, KR)
d.t(44, 484, "일부는 RFC 로 공개돼 누구나 따를 수 있고, Zoom 처럼 독점인 것도 많습니다.", 11, MUTED, KR, "start")

d.line(24, 530, 976, 530, RULE, 0.8)
d.t(24, 554, "DASH 는 서버와 클라이언트가 주고받는 메시지의 형식과 순서를 정할 뿐입니다. Netflix 는 그보다 큽니다.",
    11, MUTED, KR, "start")

d.legend(H - 44, [("이 절이 짚는 조각", ACC), ("같은 자리의 다른 예", INFO), ("나머지 조각", MUTED)])
d.save("02-01.protocol-is-a-piece.svg")
print("ok protocol-is-a-piece")
