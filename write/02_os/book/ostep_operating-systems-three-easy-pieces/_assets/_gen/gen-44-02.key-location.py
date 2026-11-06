# 44-02 ### 3 — 저장 데이터 암호화에서 키는 부팅 때 입력한 passphrase 에서 만들어져 메모리에만 있고, 응용과 운영체제는 평문을 보며, 저장 장치에는 암호문만 놓인다.
# 본문 근거: 이 노트 ### 3 「저장 데이터 암호화는 장치를 떼어 갈 때만 지켜 준다」.
# 검증 근거: openssl 3.6.4 로 passphrase 에서 PBKDF2 키를 만들어 암호화한 파일은 맞는 passphrase 로만 복호되고 틀리면 bad decrypt. 암호문 파일은 Salted__ 머리말 뒤가 무작위 바이트.
# 공식 근거: NIST SP 800-38E(저장 장치 데이터 기밀성을 위한 XTS-AES), Linux 커널 문서 dm-crypt(aes-xts-plain64).
# 타입 스펙: type-swimlane — 두 레인(데이터가 흐르는 길·키가 생기는 길).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, OK, WARN, BAD, INFO, KR, MONO

W, H = 880, 432
d = D(W, H, "OSTEP · 44-02 §3",
      "소프트웨어 디스크 암호화에서 키는 메모리에만 있다",
      "위 레인은 응용이 쓴 평문이 운영체제의 메모리를 지나 암호화 계층에서 암호문이 되어 저장 장치에 놓이는 길이다. "
      "아래 레인은 부팅할 때 사용자가 passphrase 를 입력하면 키가 만들어져 메모리에 놓이고 암호화 계층이 그 키를 쓰는 길이다. 평문 키는 저장 장치에 쓰이지 않는다.",
      "장치를 떼어 가도 평문 키가 장치 안에 없어 암호문만 가져간다")

BW, BH, PITCH, X0 = 160, 76, 208, 24
LANE_X, LANE_W, LANE_H = 12, 856, 132
A_Y, B_Y = 96, 244


def lane(y, name):
    d.o.append(f'<rect x="{LANE_X}" y="{y}" width="{LANE_W}" height="{LANE_H}" rx="8" fill="{SOFT}0A" stroke="{SOFT}" stroke-width="0.9"/>')
    d.t(LANE_X + 12, y + 20, name, 12, MUTED, KR, "start", 600)


def lane_steps(y, items):
    by = y + 40
    for i, (title, sub, c) in enumerate(items):
        x = X0 + i * PITCH
        d.tone(x, by, BW, BH, c, 6, "14", 1.4 if c == ACC else 1.1)
        d.t(x + BW / 2, by + 32, title, 12.5, INK, KR, "middle", 600)
        d.t(x + BW / 2, by + 56, sub, 12, MUTED, KR)
        if i < len(items) - 1:
            d.path(f"M {x + BW + 2} {by + BH / 2} L {x + PITCH - 2} {by + BH / 2}", MUTED, 1.4, m="ar")


lane(A_Y, "데이터가 흐르는 길")
lane_steps(A_Y, [
    ("응용", "평문을 씀", SOFT),
    ("운영체제 메모리", "평문 버퍼", SOFT),
    ("암호화 계층", "드라이버", INFO),
    ("저장 장치", "암호문만 놓임", ACC),
])
d.chip(750, A_Y + 16, "평문은 메모리까지만", SOFT, 12)

lane(B_Y, "키가 생기는 길")
lane_steps(B_Y, [
    ("부팅", "passphrase 요청", SOFT),
    ("키 만들기", "passphrase 에서 도출", INFO),
    ("메모리", "재부팅 때까지 보관", OK),
    ("암호화 계층", "메모리의 키를 사용", INFO),
])
d.chip(750, B_Y + 16, "평문 키는 장치에 쓰지 않음", OK, 12)

d.legend(392, [("평문이 있는 곳", SOFT), ("암호화가 일어나는 곳", INFO), ("암호문만 있는 곳", ACC), ("키가 머무는 곳", OK)])
d.save("44-02.key-location.svg")
