# 02-02 §5 — 브라우저가 캐시한 객체를 두고 오가는 상태. 전이 라벨은 원문 2.2.5 의 헤더·상태 코드 그대로다.
# 초점을 "신선"에 둔 것은 그 상태에 있을 때만 왕복이 0 이 되기 때문이다 — 이 절이 노리는 값이 그것이다.
# 타입 스펙: type-state — 유한 상태와 전이. 전이는 `사건 / 동작` 으로 적고, 자기 전이는 상태 위로 돈다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 568
SY = 250
BW, BH = 176, 52

d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 02-02 §5",
      "캐시한 객체는 언제 쓸 수 있나",
      "브라우저 캐시의 상태와 전이. 신선한 동안에는 서버에 묻지 않아 왕복이 0 이고, 만료가 의심되면 조건부 GET 으로 확인한다.",
      "304 는 응답은 오지만 객체는 오지 않는 자리입니다")

def state(cx, label, sub, c=MUTED, focal=False):
    x, y = cx - BW / 2, SY - BH / 2
    if focal:
        d.tone(x, y, BW, BH, c, 8, "14", 1.4)
    else:
        d.box(x, y, BW, BH, PAPER2, RULE, 1.0, 8)
    d.t(cx, SY - 4, label, 12, c if focal else INK, KR, "middle", 600)
    d.t(cx, SY + 16, sub, 12, SOFT, MONO)

S1, S2, S3 = 210, 512, 830

# 시작 표시
d.o.append(f'<circle cx="96" cy="{SY}" r="6" fill="{INK}"/>')
d.path(f"M 104 {SY} L {S1 - BW / 2 - 10} {SY}", MUTED, 1.3, m="ar")

state(S1, "캐시에 없음", "no cached copy")
state(S2, "신선", "fresh · 0 RTT", ACC, True)
state(S3, "만료 의심", "stale?")

# 전이
d.path(f"M {S1 + BW / 2 + 6} {SY} L {S2 - BW / 2 - 10} {SY}", MUTED, 1.3, m="ar")
d.t((S1 + S2) / 2, SY - 14, "GET / 200 OK", 12, MUTED, MONO)
d.t((S1 + S2) / 2, SY + 22, "max-age=N", 12, SOFT, MONO)

d.path(f"M {S2 + BW / 2 + 6} {SY} L {S3 - BW / 2 - 10} {SY}", MUTED, 1.3, m="ar")
d.t((S2 + S3) / 2, SY - 14, "max-age 만료", 12, MUTED, KR)

# 자기 전이 — 상태 위로
d.path(f"M {S2 - 44} {SY - BH / 2 - 2} L {S2 - 44} {SY - BH / 2 - 46} "
       f"L {S2 + 44} {SY - BH / 2 - 46} L {S2 + 44} {SY - BH / 2 - 10}", ACC, 1.4, m="acc")
d.t(S2 + 60, SY - BH / 2 - 42, "사용자 요청 / 캐시에서 바로 표시 — 서버에 묻지 않습니다", 12, ACC, KR, "start")

# 돌아오는 두 갈래
d.path(f"M {S3 - 40} {SY + BH / 2 + 2} L {S3 - 40} {SY + BH / 2 + 54} "
       f"L {S2 - 30} {SY + BH / 2 + 54} L {S2 - 30} {SY + BH / 2 + 10}", OK, 1.4, m="ok")
# 라벨은 가로 구간(+54) 위로 6px 띄운다 — 같은 y 에 두면 선이 글자를 관통한다.
d.t((S2 + S3) / 2 - 40, SY + BH / 2 + 40, "조건부 GET / 304 Not Modified — 본문이 오지 않습니다", 12, OK, KR)

d.path(f"M {S3 + 40} {SY + BH / 2 + 2} L {S3 + 40} {SY + BH / 2 + 118} "
       f"L {S2 + 30} {SY + BH / 2 + 118} L {S2 + 30} {SY + BH / 2 + 10}", INFO, 1.4, m="info")
d.t((S2 + S3) / 2 + 20, SY + BH / 2 + 104, "조건부 GET / 200 OK — 새 본문을 받습니다", 12, INFO, KR)

d.t(S1, SY + BH / 2 + 34, "Cache-Control: no-store 면", 12, SOFT, KR)
d.t(S1, SY + BH / 2 + 54, "이 상태를 벗어나지 않습니다", 12, SOFT, KR)

d.t(20, 444, "서버가 Cache-Control: max-age=N 을 주면 그 시간 동안 신선하고, 지나면 만료를 의심합니다.", 12, MUTED, KR, "start")
d.t(20, 466, "조건부 GET 은 왕복 한 번을 쓰지만 객체 본문의 전송 시간은 아낍니다. 객체가 클수록 그 차이가 커집니다.", 12, MUTED, KR, "start")

d.legend(H - 56, [("왕복이 0 인 자리", ACC), ("본문 없이 끝남", OK), ("본문을 다시 받음", INFO)])
d.save("02-02.cache-freshness.svg")
