# 45-01 ### 2 — 받는 쪽은 인증서에 든 서명을 미리 가진 CA 공개 키로 확인하고, 통과하면 인증서 속 공개 키를 사이트 이름에 묶어 믿으며 불일치하면 인증서를 거부한다.
# 본문 근거: 이 노트 ### 2 「인증서는 서명으로 공개 키를 이름에 묶는다」.
# 검증 근거: openssl 3.6.4 로 루트 인증서가 서명한 서버 인증서를 만들어 openssl verify 가 OK, 루트 없이 하면 error 20, DER 한 바이트를 바꾸면 error 7(서명 실패).
# 공식 근거: RFC 5280 §4.1.1.3(서명은 DER 로 인코딩한 tbsCertificate 에 대해 계산)과 §6(신뢰 앵커 선택은 정책의 문제). OSTEP 57장 §57.3.
# 타입 스펙: type-flowchart — 본 흐름 세 노드 + 선행 조건 한 노드 + 실패 분기 한 노드.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, OK, WARN, BAD, INFO, KR, MONO

W, H = 880, 392
d = D(W, H, "OSTEP · 45-01 §2",
      "인증서는 미리 가진 CA 공개 키로 서명을 확인해 사이트 키를 믿게 한다",
      "받는 쪽은 사이트에서 인증서를 받아 그 안의 서명을 미리 설치된 CA 공개 키로 확인한다. 서명이 맞으면 인증서에 든 공개 키를 사이트 이름에 묶어 믿고, 서명이 맞지 않으면 인증서를 거부한다. "
      "CA 공개 키는 소프트웨어와 함께 설치되어 있어야 하므로 이 확인은 미리 가진 키에서 출발한다.",
      "공개 키는 비밀이 아니므로 누구의 키인지를 서명으로 확인합니다")

BW, BH, PITCH, X0 = 200, 76, 280, 24
Y1, Y2 = 104, 240

# 본 흐름
main = [
    ("인증서 수신", "이름·공개 키·서명", SOFT),
    ("서명 확인", "CA 공개 키로 검증", INFO),
    ("사이트 공개 키 확보", "서명 일치 시 키가 묶임", OK),
]
for i, (title, sub, c) in enumerate(main):
    x = X0 + i * PITCH
    d.tone(x, Y1, BW, BH, c, 6, "14", 1.4 if c == OK else 1.1)
    d.t(x + BW / 2, Y1 + 32, title, 12.5, INK, KR, "middle", 600)
    d.t(x + BW / 2, Y1 + 56, sub, 12, MUTED, KR)
    if i < len(main) - 1:
        d.path(f"M {x + BW + 2} {Y1 + BH / 2} L {x + PITCH - 2} {Y1 + BH / 2}", MUTED, 1.4, m="ar")

# 미리 있어야 하는 것
x_ca = X0
d.tone(x_ca, Y2, BW, BH, ACC, 6, "14", 1.4)
d.t(x_ca + BW / 2, Y2 + 32, "미리 설치된 CA 공개 키", 12.5, INK, KR, "middle", 600)
d.t(x_ca + BW / 2, Y2 + 56, "소프트웨어에 포함", 12, MUTED, KR)
x_chk = X0 + PITCH + BW / 2 - 30
d.arrow([(x_ca + BW + 2, Y2 + BH / 2), (x_chk, Y2 + BH / 2), (x_chk, Y1 + BH + 3)], ACC, "acc", 1.4)

# 실패 분기
x_bad = X0 + 2 * PITCH
d.tone(x_bad, Y2, BW, BH, BAD, 6, "14", 1.1)
d.t(x_bad + BW / 2, Y2 + 32, "인증서 거부", 12.5, INK, KR, "middle", 600)
d.t(x_bad + BW / 2, Y2 + 56, "신뢰하지 않음", 12, MUTED, KR)
x_out = X0 + PITCH + BW / 2 + 30
d.arrow([(x_out, Y1 + BH + 3), (x_out, Y2 + BH / 2), (x_bad - 2, Y2 + BH / 2)], BAD, "bad", 1.4)
d.chip(x_out + 76, Y2 + BH / 2 - 14, "서명 불일치", BAD, 12)

d.legend(352, [("받는 쪽이 얻는 것", SOFT), ("확인하는 연산", INFO), ("믿게 되는 결과", OK), ("미리 있어야 하는 것", ACC), ("거부", BAD)])
d.save("45-01.certificate-chain.svg")
