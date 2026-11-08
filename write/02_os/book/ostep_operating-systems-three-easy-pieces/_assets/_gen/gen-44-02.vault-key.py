# 44-02 §3 — 비밀번호 보관함의 키는 passphrase 를 맞게 입력하면 RAM 에 올라오고 로그아웃·종료 때 잊히는 두 상태를 오간다.
# 본문 근거: 이 노트 §3 「저장 데이터 암호화가 지키는 범위」의 소절 「비밀번호 보관함의 타협」.
# 검증 근거: 2026-11-08 OpenSSL 3.6.4. 맞는 passphrase 는 보관함 내용을 풀고, 틀린 passphrase 는 `bad decrypt` 를 낸다(정답 5).
#            키는 파일로 저장하지 않고 RAM 에만 둔다.
# 타입 스펙: type-state — 주체 하나(보관함 키)의 상태 전이. 상태 둘, 전이마다 `사건 / 동작` 라벨. 시작은 채운 점.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INK, MUTED, SOFT, RULE, PAPER2, WARN, BAD, KR, MONO

W, H = 880, 332
SW, SH, SY = 200, 80, 184          # 상태 크기, 상태 상단 y
XL, XR = 96, 584                   # 상태 왼쪽 x
d = D(W, H, "OSTEP · 44-02 §3",
      "보관함 키는 RAM 에서만 살았다가 잊힌다",
      "상태는 둘이다. 잠김은 RAM 에 키가 없는 상태이고 열림은 RAM 에 키가 있어 복호할 수 있는 상태다. "
      "passphrase 가 맞으면 잠김에서 열림으로 가고, 틀리면 bad decrypt 가 나와 잠김에 머문다. "
      "열림에서는 복호 요청마다 평문을 돌려주고, 로그아웃이나 종료나 보관함 응용 종료 때 키를 폐기해 잠김으로 돌아간다.",
      "키는 디스크에 쓰지 않는다 — 열림 상태가 길수록 편하지만 자리를 비운 단말이 위험하다")


def state(x, title, sub, c=None):
    if c:
        d.tone(x, SY, SW, SH, c, 8, "14", 1.5)
    else:
        d.box(x, SY, SW, SH, PAPER2, RULE, 1.2, 8)
    d.t(x + SW / 2, SY + 34, title, 14, c or INK, KR, "middle", 600)
    d.t(x + SW / 2, SY + 58, sub, 12, MUTED)


def loop(cx, label, c=MUTED, m="ar"):
    top = SY
    d.path(f"M {cx - 36} {top} C {cx - 36} {top - 52}, {cx + 36} {top - 52}, {cx + 36} {top - 2}", c, 1.4, m=m)
    d.t(cx, top - 62, label, 12, c, KR if any("가" <= ch <= "힣" for ch in label) else MONO, "middle", 600)


state(XL, "잠김", "RAM 에 키가 없음")
state(XR, "열림", "RAM 에 키가 있음", ACC)

# 시작
d.o.append(f'<circle cx="48" cy="{SY + SH / 2}" r="6" fill="{INK}"/>')
d.arrow([(56, SY + SH / 2), (XL - 4, SY + SH / 2)], MUTED, "ar", 1.4)

# 잠김 ↔ 열림
yf, yb = SY + 28, SY + SH - 28
d.arrow([(XL + SW + 2, yf), (XR - 4, yf)], ACC, "acc", 1.5)
d.t((XL + SW + XR) / 2, yf - 10, "passphrase 일치 / 키를 RAM 에 둠", 12, ACC, KR, "middle", 600)
d.arrow([(XR - 2, yb), (XL + SW + 4, yb)], MUTED, "ar", 1.4)
d.t((XL + SW + XR) / 2, yb + 22, "로그아웃 · 종료 · 보관함 종료 / 키 폐기", 12, MUTED, KR, "middle", 600)

# 자기 전이
loop(XL + SW / 2, "passphrase 불일치 / bad decrypt", MUTED)
loop(XR + SW / 2, "복호 요청 / 평문 반환", ACC, "acc")

# 열림의 약점
d.chip(XR + SW / 2, SY + SH + 36, "자리를 비운 단말은 누구나 사용", WARN, 12, 8)
d.save("44-02.vault-key.svg")
