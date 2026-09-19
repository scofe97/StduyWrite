# 04-01 §6 — Alert 번호 구간이 원인의 층을 나눈다.
# 본문 요구: "10~30번대는 프로토콜 형식과 MAC, 40~51번은 핸드셰이크와 인증서,
#            60번대 이상은 정책과 버전입니다. 실패를 만나면 번호 구간만 봐도 어느 축을 볼지가 정해집니다."
#            23행짜리 표는 구간이라는 성질을 못 보여 준다. 수직 눈금 위에 구간을 얹어 그 성질을 세운다.
# 심각도는 구간과 다른 축이라 같은 칸에 섞지 않고, 각 항목 옆에 따로 표시한다.
# 타입 스펙: type-layers — 하나의 축(번호)을 구간으로 나눈 층. 세로 위치가 곧 번호 구간이고,
#           focal 은 실무에서 가장 자주 만나는 둘(40 · 48)이다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, BAD, WARN, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 960, 800
d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 04-01 §6",
      "Alert 번호가 원인의 층을 나눈다",
      "alert 번호는 임의의 식별자가 아니라 구간으로 묶여 있다. 낮은 쪽은 프로토콜 형식과 MAC, 가운데는 "
      "핸드셰이크와 인증서, 높은 쪽은 정책과 버전이다. 번호 구간만 봐도 어느 축을 볼지가 정해진다. "
      "심각도는 이 구간과 다른 축이라 항목마다 따로 표시했다.",
      "번호를 외우지 않아도 구간이 볼 곳을 정해 줍니다")

AX = 150                       # 눈금 축의 x
BX, BW = 210, 720              # 구간 상자
BANDS = [
    (168, 306, "10 ~ 30", "프로토콜 형식과 MAC", INFO,
     [("unexpected_message(10)", "fatal"), ("bad_record_mac(20)", "fatal"),
      ("record_overflow(22)", "fatal"), ("decompression_failure(30)", "fatal")]),
    (330, 494, "40 ~ 51", "핸드셰이크와 인증서", ACC,
     [("handshake_failure(40)", "fatal"), ("bad_certificate(42)", "fatal"),
      ("certificate_expired(45)", "warning"), ("unknown_ca(48)", "fatal"),
      ("decrypt_error(51)", "fatal")]),
    (518, 656, "60 이상", "정책과 버전", WARN,
     [("protocol_version(70)", "fatal"), ("insufficient_security(71)", "fatal"),
      ("internal_error(80)", "fatal"), ("no_renegotiation(100)", "warning")]),
]
FOCAL = {"handshake_failure(40)", "unknown_ca(48)"}

# 눈금 축
d.line(AX, 160, AX, 664, RULE, 1.2)
d.t(AX, 148, "번호", 11, SOFT, KR)

for y0, y1, rng, title, c in [(b[0], b[1], b[2], b[3], b[4]) for b in BANDS]:
    d.tone(BX, y0, BW, y1 - y0, c, 8, op="0E", sw=1.2)
    d.line(AX, y0 + 12, BX - 8, y0 + 12, c, 1.2)
    d.t(AX - 12, y0 + 16, rng, 11, c, MONO, "end", 600)
    d.t(BX + 16, y0 + 22, title, 13, c, KR, "start", 600)

for y0, y1, rng, title, c, items in BANDS:
    for i, (name, sev) in enumerate(items):
        y = y0 + 44 + i * 26
        focal = name in FOCAL
        d.t(BX + 26, y, name, 11, ACC if focal else INK, MONO, "start", 600 if focal else 400)
        sc = BAD if sev == "fatal" else WARN
        d.chip(BX + BW - 72, y - 4, sev, sc, 10, 6)
        if focal:
            d.t(BX + 300, y, "자주 만남", 11, ACC, KR, "start")

# 심각도가 다른 축이라는 것
d.t(24, 700, "심각도는 번호 구간과 다른 축 — 한 구간 안에 warning 과 fatal 이 섞임", 12, SOFT, KR, "start")
d.t(24, 722, "TLS 1.3 — 심각도가 alert 종류에 담겨 level 칸은 읽지 않아도 됨", 11, MUTED, KR, "start")

d.legend(H - 44, [("형식·MAC", INFO), ("핸드셰이크·인증서", ACC), ("정책·버전", WARN), ("연결이 끊김", BAD)])
d.save("04-01.alert-ranges.svg")
