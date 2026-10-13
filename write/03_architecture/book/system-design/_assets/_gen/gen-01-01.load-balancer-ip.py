# 타입 스펙: type-architecture — 공인 IP 하나(로드밸런서)와 사설 IP 둘(웹 서버)을 존으로 가르고, 같은 구성을 정상 · 한 대 정지 두 컷으로 쌓아 요청이 옮겨 가는 것을 보인다.
# 사실 출처: 추출본 v2.txt 144~164행(로드밸런서 · 공인 IP · 사설 IP · server 1 이 꺼지면 server 2 로), PDF 10쪽 로드밸런서 그림(mywebsite.com · 88.88.88.1 · 10.0.0.1 · 10.0.0.2),
#   RFC 1918 §3(10.0.0.0 ~ 10.255.255.255 는 사설 주소). 요청 4건은 균등 분배를 보이려는 예시 값이다.
# Layout conventions: 노드 높이 52~56, 컷 높이 220(y0=96·320), 존 폭 328, 서버 노드 폭 296, 모든 좌표 4의 배수. 대각선 대신 직각 꺾임으로 이은다.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, ACC, OK, BAD, MUTED, INK, PAPER, PAPER2, RULE, SOFT, INFO, KR, MONO

W, H = 960, 596
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 01-01 §3",
      "공인 IP 하나 뒤에 사설 IP 둘",
      "mywebsite.com 은 88.88.88.1 하나로 풀리고, 로드밸런서가 사설 IP 10.0.0.1 · 10.0.0.2 의 웹 서버로 요청을 나눈다. Server1 이 멈추면 요청이 모두 10.0.0.2 로 간다.",
      "클라이언트는 공인 IP 만 알고 웹 서버의 사설 IP 는 모릅니다")


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def cut(y0, tag, down):
    d.t(24, y0 + 8, tag, 13, MUTED, KR, "start", 600)
    # 클라이언트
    d.box(36, y0 + 72, 168, 56, PAPER2, RULE, 1.0, 6)
    d.t(120, y0 + 96, "클라이언트", 13, INK, KR, "middle", 600)
    d.t(120, y0 + 116, "브라우저 · 앱", 13, MUTED, KR, "middle")
    # 클라이언트 → 로드밸런서
    d.arrow([(206, y0 + 100), (366, y0 + 100)], MUTED, "ar", 1.5)
    d.chip(286, y0 + 72, "88.88.88.1", INFO, 13)
    d.t(286, y0 + 124, "공인 IP", 13, MUTED, KR, "middle")
    # 로드밸런서
    d.box(372, y0 + 72, 156, 56, PAPER2, RULE, 1.0, 6)
    d.t(450, y0 + 106, "로드밸런서", 13, INK, KR, "middle", 600)
    # 사설 존
    d.box(596, y0 + 16, 328, 172, PAPER, RULE, 0.9, 8)
    d.t(608, y0 + 36, "PRIVATE IP", 9, SOFT, MONO, "start")
    ys = (y0 + 70, y0 + 138)
    subs = (("10.0.0.1 · 정지", BAD), ("10.0.0.2 · 요청 4건", OK)) if down else \
           (("10.0.0.1 · 요청 2건", OK), ("10.0.0.2 · 요청 2건", OK))
    names = ("Server1", "Server2")
    for k in range(2):
        y = ys[k] - 26
        sub, c = subs[k]
        d.tone(612, y, 296, 52, c, 6, "12", 1.2)
        d.t(760, y + 22, names[k], 13, c, MONO, "middle", 600)
        d.t(760, y + 42, sub, 13, MUTED, kr(sub), "middle")
        if down and k == 0:
            c_arrow, mk, sw, dash = BAD, None, 1.5, "4 4"
        elif down and k == 1:
            c_arrow, mk, sw, dash = ACC, "acc", 2.2, None
        else:
            c_arrow, mk, sw, dash = MUTED, "ar", 1.5, None
        if mk is None:
            d.path(f"M 530 {y0 + 100} L 564 {y0 + 100} L 564 {ys[k]} L 600 {ys[k]}", c_arrow, sw, None, dash)
            d.t(606, ys[k] + 6, "×", 18, BAD, MONO, "middle", 600)
        else:
            d.arrow([(530, y0 + 100), (564, y0 + 100), (564, ys[k]), (610, ys[k])], c_arrow, mk, sw, dash)


cut(96, "정상", False)
d.line(24, 308, W - 48, 308, RULE, 0.8)
cut(320, "Server1 정지", True)
d.legend(H - 56, [("정상 서버", OK), ("정지", BAD), ("몰린 요청", ACC), ("공인 IP", INFO)])
d.save("01-01.load-balancer-ip.svg")
print("ok load-balancer-ip")
