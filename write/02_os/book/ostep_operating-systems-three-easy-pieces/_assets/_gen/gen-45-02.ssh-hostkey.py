# 45-02 §7 — SSH 호스트 키는 known_hosts 에 없는 미등록에서 BatchMode=yes 로는 확인할 수 없어 실패하고, accept-new 는 확인 없이 등록하며, 등록된 뒤에는 서버의 키가 바뀌면 차단된다.
# 본문 근거: 이 노트 §7 「SSH 호스트 키」의 소절 「첫 접속과 known_hosts」.
# 검증 근거: 2026-11-08 OpenSSH_10.3p1 로컬 sshd(127.0.0.1:2222)로 실측(정답 6) — BatchMode=yes 첫 접속은 `Host key verification failed.`,
#            StrictHostKeyChecking=accept-new 첫 접속은 `Permanently added`, 서버의 호스트 키를 바꾼 뒤 접속은 `REMOTE HOST IDENTIFICATION HAS CHANGED` 와 `Host key verification failed`.
# 타입 스펙: type-state — 주체 하나(known_hosts 의 한 호스트)의 상태 전이. 상태 셋, 전이마다 `사건 / 동작` 라벨. 시작은 채운 점.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INK, MUTED, SOFT, RULE, PAPER2, OK, BAD, WARN, KR, MONO

W, H = 880, 464
SW, SH, SY = 200, 80, 184          # 상태 크기, 첫 줄 상태 상단 y
XL, XR = 96, 584                   # 상태 왼쪽 x
SY2 = 336                          # 둘째 줄 상태 상단 y
d = D(W, H, "OSTEP · 45-02 §7",
      "accept-new 는 첫 키를 확인 없이 등록하고 등록된 뒤 바뀐 키는 막는다",
      "상태는 셋이다. 미등록은 known_hosts 에 호스트 키가 없는 상태이고 등록됨은 키가 저장된 상태이며 차단은 저장된 키와 서버의 키가 달라 연결이 막힌 상태다. "
      "미등록에서 BatchMode=yes 로 접속하면 확인할 수 없어 Host key verification failed 로 끝나 미등록에 머문다. accept-new 로 접속하면 Permanently added 가 나오고 등록됨이 된다. "
      "등록된 호스트의 키가 바뀌면 REMOTE HOST IDENTIFICATION HAS CHANGED 경고와 함께 차단된다.",
      "처음 한 번의 확인이 약한 고리이고, 저장된 뒤의 변경은 크게 경고한다")


def state(x, y, title, sub, c=None):
    if c:
        d.tone(x, y, SW, SH, c, 8, "14", 1.5)
    else:
        d.box(x, y, SW, SH, PAPER2, RULE, 1.2, 8)
    d.t(x + SW / 2, y + 34, title, 14, c or INK, KR, "middle", 600)
    d.t(x + SW / 2, y + 58, sub, 12, MUTED, KR)


def loop(cx, label, c=MUTED, m="ar"):
    top = SY
    d.path(f"M {cx - 36} {top} C {cx - 36} {top - 52}, {cx + 36} {top - 52}, {cx + 36} {top - 2}", c, 1.4, m=m)
    d.t(cx, top - 62, label, 12, c, KR if any("가" <= ch <= "힣" for ch in label) else MONO, "middle", 600)


state(XL, SY, "미등록", "known_hosts 에 키 없음")
state(XR, SY, "등록됨", "known_hosts 에 키 저장", OK)
state(XR, SY2, "차단", "저장된 키와 서버 키가 다름", BAD)

# 시작
d.o.append(f'<circle cx="48" cy="{SY + SH / 2}" r="6" fill="{INK}"/>')
d.arrow([(56, SY + SH / 2), (XL - 4, SY + SH / 2)], MUTED, "ar", 1.4)

# 미등록 → 등록됨
yf = SY + SH / 2
d.arrow([(XL + SW + 2, yf), (XR - 4, yf)], ACC, "acc", 1.5)
d.t((XL + SW + XR) / 2, yf - 10, "accept-new / Permanently added", 12, ACC, MONO, "middle", 600)

# 미등록 자기 전이
loop(XL + SW / 2, "BatchMode=yes / Host key verification failed.", MUTED)

# 등록됨 → 차단
xm = XR + SW / 2
d.arrow([(xm, SY + SH + 2), (xm, SY2 - 4)], BAD, "bad", 1.5)
d.t(xm - 14, SY + SH + 36, "서버의 호스트 키가 바뀜 /", 12, BAD, KR, "end", 600)
d.t(xm - 14, SY + SH + 56, "REMOTE HOST IDENTIFICATION HAS CHANGED", 12, BAD, MONO, "end", 600)

d.save("45-02.ssh-hostkey.svg")
