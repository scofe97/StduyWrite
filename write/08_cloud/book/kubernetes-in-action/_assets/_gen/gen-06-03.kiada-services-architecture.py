# 06-03 §4 — Kiada 스위트 서비스 구성
# 본문: "Kiada 스위트는 Node.js 앱 외에 Quote·Quiz 두 서비스를 갖게 됩니다."
#       "Quote 서비스의 첫 버전은 유닉스의 fortune 명령으로 만듭니다... nginx:alpine 이미지에 PostStart hook 으로"
# 타입 스펙: type-architecture.md — 프론트엔드(Web App) → 서비스(Quote·Quiz) → 데이터 저장소(Quote DB·Quiz DB)
#           계층과 REST 연결을 직각 둥근 엘보 화살표로 잇고, §4 실습 대상인 Quote service 만 focal 로 짚는다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, INFO, PAPER, PAPER2, KR, MONO
import ddx

W, H = 1000, 568
d = D(W, H, "KUBERNETES IN ACTION · 06-03",
      "Kiada 스위트 — Web App 이 Quote · Quiz 서비스 호출",
      "Kiada Web App(Node.js)이 REST 로 Quote 와 Quiz 두 서비스에 요청하고, 각 서비스는 자기 DB 를 둔다. "
      "§4 예제는 nginx:alpine 과 fortune 명령으로 Quote service 를 구성한다.",
      lead="Web App(Node.js) → REST → Quote · Quiz → 각 DB")

ddx.band(d, 104, 508, "세 계층 구성 — Web App · REST 서비스 · 데이터 저장소")

# Flat 3 tier zones (margin >= 16px above enclosed nodes)
ZONES = [
    (44,  148, 232, 296, "WEB TIER"),
    (344, 148, 284, 296, "SERVICE TIER"),
    (696, 148, 260, 296, "DATA TIER"),
]
for zx, zy, zw, zh, zlab in ZONES:
    d.o.append(f'<rect x="{zx}" y="{zy}" width="{zw}" height="{zh}" rx="8" '
               f'fill="{INK}05" stroke="{RULE}" stroke-width="0.9"/>')
    lw = len(zlab) * 7 + 16
    d.o.append(f'<rect x="{zx+12}" y="{zy+4}" width="{lw}" height="12" rx="2" fill="{PAPER}"/>')
    d.t(zx + 12 + lw / 2, zy + 13, zlab, 8, SOFT, MONO, "middle")

def comp(cx, cy, w, h, title, sub, tag, c, focal=False):
    x, y = cx - w // 2, cy - h // 2
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
        tc = ACC
    else:
        d.box(x, y, w, h, PAPER2, c, 1.1, 6)
        tc = c
    d.t(cx, cy - 16, ddx.fit(title, 14, w - 16, title), 14, tc,
        MONO if all(ord(ch) < 128 for ch in title) else KR, "middle", 600)
    d.t(cx, cy + 6, ddx.fit(sub, 11, w - 16, sub), 11, MUTED,
        MONO if all(ord(ch) < 128 for ch in sub) else KR)
    d.t(cx, cy + 26, ddx.fit(tag, 11, w - 16, tag), 11, SOFT, KR)

WEB = (160, 304, 196, 88)
QUOTE = (486, 236, 236, 88)
QUIZ = (486, 372, 236, 88)
QDB = (826, 236, 208, 88)
ZDB = (826, 372, 208, 88)

# Orthogonal rounded connectors drawn before boxes or cleanly between edges
# Web App (right x=258) fanned ports y=288, y=320 -> Quote (left x=368, y=236), Quiz (left x=368, y=372)
d.o.append(f'<path d="M 262 288 H 304 Q 312 288 312 280 V 244 Q 312 236 320 236 H 362" '
           f'fill="none" stroke="{INFO}" stroke-width="1.5" marker-end="url(#info)"/>')
d.chip(312, 260, "REST", INFO, 11)

d.o.append(f'<path d="M 262 320 H 304 Q 312 320 312 328 V 364 Q 312 372 320 372 H 362" '
           f'fill="none" stroke="{INFO}" stroke-width="1.5" marker-end="url(#info)"/>')
d.chip(312, 344, "REST", INFO, 11)

# Service -> DB horizontal connections
d.path(f"M {QUOTE[0]+QUOTE[2]//2+4} {QUOTE[1]} L {QDB[0]-QDB[2]//2-6} {QDB[1]}", OK, 1.5, m="ok")
d.path(f"M {QUIZ[0]+QUIZ[2]//2+4} {QUIZ[1]} L {ZDB[0]-ZDB[2]//2-6} {ZDB[1]}", OK, 1.5, m="ok")

comp(*WEB, "Kiada Web App", "Node.js", "웹 프론트엔드", INFO)
comp(*QUOTE, "Quote service", "nginx:alpine · fortune", "§4 PostStart 실습 대상", ACC, focal=True)
comp(*QUIZ, "Quiz service", "REST", "퀴즈 서비스", INFO)
comp(*QDB, "Quote DB", "인용문 데이터", "Quote 저장소", OK)
comp(*ZDB, "Quiz DB", "퀴즈 데이터", "Quiz 저장소", OK)

d.t(36, 480, "Quote v1 — 새 이미지 대신 nginx:alpine · PostStart hook 으로 fortune 생성",
     12, MUTED, KR, "start")
d.legend(520, [("웹 · 서비스", INFO), ("§4 실습 대상 (Quote)", ACC), ("데이터 저장소", OK)])
d.save("06-03-kiada-services-architecture.svg")
print("ok kiada-services-architecture")
