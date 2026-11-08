# 45-01 「1. 원격 기계의 인증」 — 사용자가 사이트에 자신을 증명할 때는 사용자마다 다른 비밀번호를, 사이트가 사용자에게 자신을 증명할 때는 모두에게 같은 공개 키 하나를 쓴다.
# 본문 근거: 이 노트 「사용자 → 사이트는 비밀번호, 사이트 → 사용자는 공개 키」 절.
# 값 근거: 비밀번호는 예시용 가짜 값이다. 공개 키 앞자리 MIIBIjANBg 는 RSA 2048 공개 키(SubjectPublicKeyInfo)를 base64 로 쓴 PEM 의 첫 줄이며 이 기기에서 만든 root.pub 로 확인했다(2026-11-08).
# 공식 근거: OSTEP 57장 §57.1~57.2 의 인증 방향(비밀번호는 많은 사용자 → 한 사이트, 공개 키는 한 쪽 → 많은 상대).
# 타입 스펙: type-architecture — 사용자 존과 사이트 존, 존 사이를 가로지르는 두 방향의 화살표.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, ACC, OK, INFO, KR, PAPER2, RULE

W, H = 880, 420
d = D(W, H, "OSTEP · 45-01 §1",
      "사용자는 비밀번호로, 사이트는 공개 키로 자신을 증명한다",
      "왼쪽 존은 사용자 수천 명이고 오른쪽 존은 웹 사이트 하나다. 사용자에서 사이트로 가는 화살표는 사용자마다 다른 ID 와 비밀번호를 싣고, 아는 쪽은 사용자와 사이트 둘뿐이다. "
      "사이트에서 사용자로 가는 화살표는 모두에게 같은 공개 키 하나를 싣고, 개인 키를 가진 쪽은 사이트뿐이다.")

# 존
d.box(12, 96, 276, 252, PAPER2, RULE, 0.9, 8)
d.t(24, 118, "사용자 수천 명", 12, SOFT, KR, "start", 600)
d.box(592, 96, 276, 252, PAPER2, RULE, 0.9, 8)
d.t(604, 118, "웹 사이트 하나", 12, SOFT, KR, "start", 600)

# 사용자 박스
users = [("user1", "hunter2"), ("user2", "swordfish"), ("user3", "letmein")]
for i, (name, pw) in enumerate(users):
    y = 132 + i * 68
    d.tone(28, y, 244, 56, INFO, 6, "14", 1.1)
    d.t(44, y + 24, name, 13, INK, KR, "start", 600)
    d.t(44, y + 44, "비밀번호 " + pw, 12, MUTED, KR, "start")

# 사이트 박스
d.tone(608, 172, 244, 100, OK, 6, "14", 1.4)
d.t(730, 200, "사이트 서버", 13, INK, KR, "middle", 600)
d.t(730, 224, "개인 키 · 공개 키 한 쌍", 12, MUTED, KR, "middle")
d.t(730, 248, "사용자별 솔트 · 해시 저장", 12, MUTED, KR, "middle")

# 사용자 → 사이트
d.arrow([(292, 196), (588, 196)], INFO, "info", 1.4)
d.t(440, 184, "ID + 비밀번호", 13, INFO, KR, "middle", 600)
d.chip(440, 220, "아는 쪽: 사용자와 사이트 둘", INFO, 12)

# 사이트 → 사용자
d.arrow([(588, 276), (292, 276)], ACC, "acc", 1.6)
d.t(440, 264, "공개 키  MIIBIjANBg…", 13, ACC, KR, "middle", 600)
d.chip(440, 300, "아는 쪽: 모두 · 개인 키는 사이트만", ACC, 12)

d.legend(380, [("사용자 쪽", INFO), ("사이트 쪽", OK), ("모두에게 같은 공개 키", ACC)])
d.save("45-01.proof-direction.svg")
