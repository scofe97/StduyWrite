# 04-01 「시스템 콜을 받는 쪽은 같아도 처리하는 쪽이 바뀐다」 — 일반 컨테이너는 호스트 커널이 받아 처리하고, gVisor systrap 은 호스트 커널이 받아 SIGSYS 로 Sentry 에 넘기며, KVM 은 Sentry 가 받는다.
# 본문 근거: 이 노트 「6. gVisor 에서 시스템 콜이 가는 곳」.
# 값 근거: 개념 도식이라 값은 없다.
# 공식 근거: gVisor 플랫폼 문서 — 플랫폼은 시스템 콜 가로채기·문맥 교환·메모리 매핑을 맡는다. systrap 은 seccomp 로 SIGSYS 를 보내 가로채고, KVM 은 Sentry 가 게스트 운영체제 겸 VMM 으로 일한다. 소개 문서 — Sentry 는 앱의 시스템 콜을 호스트로 그대로 넘기지 않고, 필요한 일만 호스트 시스템 콜로 바꿔 부른다.
# 타입 스펙: type-process — 행마다 같은 노드 열(앱 · 받는 곳 · 처리 · 호스트 요청)이 같은 자리에 반복된다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INK, MUTED, SOFT, RULE, PAPER2, INFO, OK, KR, MONO

W, H = 920, 508
d = D(W, H, "OSTEP · 04-01 §6",
      "같은 시스템 콜이라도 처리하는 곳이 다르다",
      "일반 컨테이너에서는 앱의 시스템 콜을 호스트 커널이 받아 그대로 처리한다. "
      "gVisor 의 systrap 플랫폼에서는 호스트 커널이 시스템 콜을 실행하지 않고 seccomp 필터가 SIGSYS 를 보내 Sentry 가 처리하게 하고, KVM 플랫폼에서는 Sentry 가 게스트 운영체제 자리에서 받는다. "
      "두 경우 모두 Sentry 가 필요한 일만 호스트 커널에 시스템 콜로 요청한다.")


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def node(x, y, w, h, name, c=None, sub=None):
    if c:
        d.tone(x, y, w, h, c)
    else:
        d.box(x, y, w, h, PAPER2, RULE, 1.0, 6)
    d.t(x + w / 2, y + (22 if sub else h / 2 + 5), name, 13, INK, kr(name), "middle", 600)
    if sub:
        d.t(x + w / 2, y + 42, sub, 12, MUTED, kr(sub))


# 열 머리글: 모든 행이 같은 노드 열(앱 · 받는 곳 · 처리 · 호스트 요청)을 쓴다
for x, label in ((24, "환경"), (196, "앱"), (346, "받는 곳"), (666, "처리"), (796, "호스트 요청")):
    d.t(x, 122, label, 12, SOFT, KR, "start", 600)

rows = [
    (150, "일반 컨테이너", "호스트 커널을 공유", "host kernel", None, "그대로", "host kernel", "없음", None, MUTED),
    (260, "gVisor · systrap", "기본 플랫폼", "host kernel", "실행하지 않음", "seccomp 필터 → SIGSYS", "Sentry", "host kernel", "필요한 일만", ACC),
    (370, "gVisor · KVM", "가상화 필요", "Sentry", "게스트 OS 자리", "그대로", "Sentry", "host kernel", "필요한 일만", INFO),
]
for y, env, envsub, recv, recvsub, how, proc, host, hop, c in rows:
    mk = "ar" if c == MUTED else ("acc" if c == ACC else "info")
    d.t(24, y + 26, env, 13, INK, kr(env), "start", 600)
    d.t(24, y + 46, envsub, 12, MUTED, KR, "start")
    node(196, y + 4, 80, 52, "앱")
    d.arrow([(276, y + 30), (346, y + 30)], c, mk, 1.6)
    d.t(311, y + 21, "syscall", 12, c if c != MUTED else INK, MONO, "middle", 600)
    node(346, y + 4, 150, 52, recv, None, recvsub)
    d.arrow([(496, y + 30), (666, y + 30)], c, mk, 1.6)
    d.t(581, y + 21, how, 12, c if c != MUTED else INK, kr(how), "middle", 600)
    node(666, y + 4, 110, 52, proc, None if c == MUTED else c)
    if hop:
        d.arrow([(776, y + 30), (796, y + 30)], MUTED, "ar", 1.2, "3 3")
        node(796, y + 4, 100, 52, host)
        d.t(846, y + 76, hop, 12, MUTED, KR, "middle")
    else:
        node(796, y + 4, 100, 52, host)
    if y < 370:
        d.line(24, y + 96, W - 48, y + 96, RULE, 0.8, "4 4")

d.legend(H - 40, [("호스트로 직접", MUTED), ("systrap 경로", ACC), ("KVM 경로", INFO)])
d.save("04-01.trap-destination.svg")
print("ok 04-01 trap-destination")
