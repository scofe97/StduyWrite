# 04-03.dns-query-counts — 같은 이름 web 의 질의 수는 클라이언트마다 2에서 5까지 갈린다
# 본문 요구: 「클라이언트마다 다른 질의 횟수」 — glibc·musl 의 getent hosts web 은 2번, curl 8.23.0(c-ares 1.34.9) 은 5번(A 1 + AAAA 4),
#           같은 curl 이 example.com 은 8번, example.com. 은 2번. CoreDNS v1.14.6 의 log 플러그인으로 센 값(2026-11-08).
# 타입 스펙: type-bar — 가로 막대. 길이가 질의 횟수에 비례하고 focal 은 홀수 5번인 curl 막대 하나.
import ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, PAPER2, KR, MONO

W, H = 1000, 568
d = D(W, H, "CLUSTER DNS · QUERIES PER CLIENT",
      "같은 이름 web 을 부르는데 질의 수는 2에서 5까지 갈린다",
      "glibc 2.41 과 musl 의 getent hosts web 은 질의가 2번이고, c-ares 1.34.9 를 쓰는 curl 8.23.0 은 5번이다(A 1, AAAA 4). "
      "같은 curl 이 example.com 은 8번, 끝점을 찍은 example.com. 은 2번이다. CoreDNS v1.14.6 로그 기준, 2026-11-08.",
      lead="web 은 A 레코드만 있어서 AAAA 질의가 어디서 멈추는지가 횟수를 가릅니다")

LX, BX, UNIT = 48, 372, 70            # 라벨 열 · 막대 시작 · 질의 1번의 길이
BH, Y0, STRIDE = 32, 164, 62
d.t(LX, 134, "클라이언트 · 부른 이름", 12, SOFT, KR, "start", 600)
d.t(BX, 134, "질의 횟수 (A + AAAA)", 12, SOFT, KR, "start", 600)

ROWS = [
    ("glibc 2.41", "getent hosts web", [("A 1", 1, INFO), ("AAAA 1", 1, INFO)], "2번", INFO),
    ("musl (Alpine)", "getent hosts web", [("A 1", 1, INFO), ("AAAA 1", 1, INFO)], "2번", INFO),
    ("curl 8.23.0 · c-ares 1.34.9", "web", [("A 1", 1, ACC), ("AAAA 4", 4, ACC)], "5번", ACC),
    ("curl 8.23.0", "example.com", [("시도 4번 × (A 1 + AAAA 1)", 8, WARN)], "8번", WARN),
    ("curl 8.23.0", "example.com.", [("A 1", 1, OK), ("AAAA 1", 1, OK)], "2번", OK),
]

for i, (cli, name, segs, total, c) in enumerate(ROWS):
    y = Y0 + i * STRIDE
    d.t(LX, y + 14, ddx.fit(cli, 13, BX - LX - 16, cli), 13, INK, KR, "start", 600)
    d.t(LX, y + 34, name, 12, MUTED, MONO, "start")
    x = BX
    for k, (lab, n, sc) in enumerate(segs):
        w = n * UNIT
        focal = sc == ACC
        d.tone(x, y, w - 3, BH, sc, 4, "26" if focal else "1A", 1.5 if focal else 1.0)
        d.t(x + (w - 3) // 2, y + 21, ddx.fit(lab, 12, w - 10, lab), 12, sc, KR, "middle", 600)
        x += w
    d.t(x + 10, y + 21, total, 14, c, KR, "start", 600)

d.t(BX, Y0 + 5 * STRIDE + 6, "CoreDNS v1.14.6 log 플러그인 · kind 노드 v1.37.0 · 2026-11-08", 12, SOFT, KR, "start")
d.legend(520, [("표준 리졸버의 web", INFO), ("c-ares 의 web", ACC), ("검색 경로를 다 돈 이름", WARN), ("끝점을 찍은 이름", OK)])
d.save("04-03.dns-query-counts.svg")
print("ok dns-query-counts")
