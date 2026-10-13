# 타입 스펙: type-bar — 같은 눈금(1비트 = 6px)에 UUIDv4 와 UUIDv7 의 128비트 필드를 가로 막대로 쌓고, 64비트 한도선을 세로로 건다.
# 사실 출처: RFC 9562 §5.4(UUIDv4: random_a 48 · ver 4 · random_b 12 · var 2 · random_c 62, 무작위 122비트), §5.7(UUIDv7: unix_ts_ms 48 · ver 4 · rand_a 12 · var 2 · rand_b 62), §4.1(var = 10).
#   예시 UUID 09c93e62-50b4-468d-bf8a-c07e1040bfb2 는 추출본 v2.txt 1971행. 세 번째 묶음 첫 글자 4 = 버전, 네 번째 묶음 첫 글자 b = 1011 → 앞 두 비트 10.
# Layout conventions: 막대 x0=112 · 1비트 6px(128비트 = 768px) · 막대 높이 56 · 줄 y=156·264. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, WARN, MUTED, INK, SOFT, PAPER2, RULE, BAD, KR, MONO

W, H = 960, 460
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 07-01 §3",
      "UUID 는 두 버전 모두 128비트라 64비트 한도를 두 배 넘는다",
      "UUIDv7 은 앞 48비트가 밀리초 시각이라 시간순이지만 폭은 UUIDv4 와 같다.",
      "1비트 = 6px · 점선은 64비트")

X0, U, BH = 112, 6, 56
ROWS = (
    ("UUIDv4", 156, (("random", 48, INFO), ("ver", 4, WARN), ("random", 12, INFO), ("var", 2, WARN), ("random", 62, INFO))),
    ("UUIDv7", 264, (("unix_ts_ms", 48, ACC), ("ver", 4, WARN), ("rand_a", 12, INFO), ("var", 2, WARN), ("rand_b", 62, INFO))),
)
for name, y, segs in ROWS:
    d.t(24, y + 34, name, 14, INK, KR, "start", 600)
    x = X0
    for lab, n, c in segs:
        w = n * U
        d.tone(x, y, w, BH, c, 3, "14" if c == ACC else "12", 1.4 if c == ACC else 1.0)
        if n >= 12:
            d.t(x + w / 2, y + 26, lab, 12, c, MONO, "middle", 600)
            d.t(x + w / 2, y + 46, str(n), 12, MUTED, MONO)
        else:
            if lab == "var":
                d.t(x + w + 8, y - 8, f"{lab} {n}비트", 12, c, MONO, "start", 600)
            else:
                d.t(x + w / 2, y - 8, f"{lab} {n}비트", 12, c, MONO, "middle", 600)
        x += w
LX = X0 + 64 * U
d.line(LX, 112, LX, 332, BAD, 1.4, "4 4")
d.t(LX, 104, "64비트", 13, BAD, KR, "middle", 600)
d.chip(X0 + 148, 372, "09c93e62-50b4-468d-bf8a-c07e1040bfb2", MUTED, 11)
d.chip(X0 + 408, 372, "468d → 버전 4", WARN, 12)
d.chip(X0 + 564, 372, "bf8a → 변종 10", WARN, 12)
d.legend(H - 56, [("무작위", INFO), ("버전 · 변종", WARN), ("시각", ACC)])
d.save("07-01.uuid-bits.svg")
