# 45-02 §6 — 클라이언트는 HSTS 호스트로 알려진 도메인의 http 주소를 https 로 바꾸고, 보안 전송에서 오류를 만나면 연결을 끊는다. 클라이언트가 아직 모르는 HSTS 호스트에는 서버가 영구 리다이렉트를 돌려주라고 권고한다.
# 본문 근거: 이 노트 §6 「HTTPS 인증서와 HSTS」의 소절 「HSTS 는 http 로의 물러남을 막는다」.
# 검증 근거: 2026-11-08 RFC 6797 — §8.3 "The UA MUST replace the URI scheme with "https"", §8.4 "the UA MUST terminate the connection ... if there are any errors, whether "warning" or "fatal" or any other error level, with the underlying secure transport",
#            §7.2 "If an HSTS Host receives an HTTP request message over a non-secure transport, it SHOULD send an HTTP response message containing a status code indicating a permanent redirect".
# 타입 스펙: type-flowchart — 판단 분기. 타원은 시작, 마름모는 판단(출구 둘, 모든 출구에 라벨), 사각형은 결과. 코랄은 가장 중요한 판단 하나에만 쓴다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INK, MUTED, SOFT, RULE, PAPER2, OK, BAD, WARN, KR, MONO

W, H = 1000, 592
d = D(W, H, "OSTEP · 45-02 §6",
      "HSTS 호스트의 http 주소는 https 로 바뀌고 오류는 연결을 끊는다",
      "클라이언트가 http 주소를 열 때 알려진 HSTS 호스트의 도메인이면 스킴을 https 로 바꾼다. 보안 전송을 세우다 경고든 치명적이든 어떤 오류를 만나도 연결을 끊고, 오류가 없으면 https 로 통신한다. "
      "클라이언트가 아직 모르는 HSTS 호스트에 http 로 요청하면 보안이 걸리지 않으므로 HSTS 호스트인 서버가 평문 요청에 https 주소로 가는 영구 리다이렉트를 돌려주라고 권고한다.",
      "알려진 HSTS 호스트에는 클라이언트가 https 만 쓰고, HSTS 호스트인 서버는 평문 요청에 리다이렉트를 권고받는다")


def oval(cx, cy, w, h, text):
    d.o.append(f'<rect x="{cx - w / 2}" y="{cy - h / 2}" width="{w}" height="{h}" rx="20" fill="{PAPER2}" stroke="{SOFT}" stroke-width="1.1"/>')
    d.t(cx, cy + 5, text, 13, INK, KR, "middle", 600)


def step(x, y, w, h, title, sub, c=None):
    if c:
        d.tone(x, y, w, h, c, 6, "14", 1.4)
    else:
        d.box(x, y, w, h)
    d.t(x + w / 2, y + 28, title, 14, c or INK, KR if any("가" <= ch <= "힣" for ch in title) else MONO, "middle", 600)
    d.t(x + w / 2, y + 52, sub, 12, MUTED, KR)


def diamond(cx, cy, hw, hh, text, c):
    pts = f"{cx},{cy - hh} {cx + hw},{cy} {cx},{cy + hh} {cx - hw},{cy}"
    d.o.append(f'<polygon points="{pts}" fill="{c}14" stroke="{c}" stroke-width="1.4"/>')
    d.t(cx, cy + 5, text, 14, c if c != SOFT else INK, KR, "middle", 600)


# 시작과 첫 판단
oval(240, 124, 232, 40, "http:// 주소를 열려 함")
d.arrow([(240, 144), (240, 180)], MUTED, "ar", 1.4)
diamond(240, 232, 132, 52, "알려진 HSTS 호스트인가?", ACC)

# 예: https 로 바꾸고 보안 전송을 세운다
d.arrow([(374, 232), (436, 232)], MUTED, "ar", 1.4)
d.t(405, 222, "예", 12, MUTED, KR, "middle", 600)
step(440, 196, 200, 72, "https 로 바꿈", "URI 스킴을 교체")
d.arrow([(540, 268), (540, 324)], MUTED, "ar", 1.4)
d.t(552, 302, "보안 전송을 세움", 12, MUTED, KR, "start", 600)
diamond(540, 376, 100, 52, "오류가 있는가?", SOFT)

# 오류: 끊음, 오류 없음: 통신
d.arrow([(642, 376), (700, 376)], MUTED, "ar", 1.4)
d.t(671, 366, "예", 12, MUTED, KR, "middle", 600)
step(704, 340, 240, 72, "연결을 끊음", "경고든 치명이든 모든 오류", BAD)
d.arrow([(540, 430), (540, 476)], MUTED, "ar", 1.4)
d.t(552, 458, "아니오", 12, MUTED, KR, "start", 600)
step(440, 480, 200, 72, "https 로 통신", "보호된 연결을 씀", OK)

# 아니오: 평문 요청과 리다이렉트
d.arrow([(240, 286), (240, 332)], MUTED, "ar", 1.4)
d.t(252, 314, "아니오", 12, MUTED, KR, "start", 600)
step(120, 336, 240, 72, "http 로 요청", "보안이 걸리지 않은 채 통신", WARN)
d.arrow([(240, 410), (240, 456)], MUTED, "ar", 1.4)
d.t(252, 438, "HSTS 호스트인 서버가 응답", 12, MUTED, KR, "start", 600)
step(120, 460, 240, 72, "영구 리다이렉트", "https 주소로 보내라고 권고")

d.save("45-02.hsts-flow.svg")
