# 08-01 §7 — 크래시 복구가 어디서 꺼지는가. 그리고 공식 문서 한 문장이 소스와 어긋난다는 것.
# 원문 근거(원서): "debug instructs CoreDNS not to recover from a crash so that you can retrieve
#            the stack trace" / Example 8-26 은 두 서버 블록 모두에 errors 와 debug 를 함께 적는다.
# 공식 문서: "Note that the errors plugin (if loaded) will also set a `recover`, negating this
#            setting." (coredns.io/plugins/debug/) — 그런데 소스에는 그 코드가 없다.
# 소스 실측: plugin/errors/errors.go 에 recover 도 panic 도 없다(ServeDNS 는 NextOrFailure 의
#            err 를 정규식에 물려 기록만 한다). 복구는 core/dnsserver/server.go 한 곳뿐이고
#            `if !s.debug { defer func() { ... recover() ... } }` 로 감싸여 있으며,
#            구조체 필드 주석이 `debug bool // disable recover()` 다.
# 타입 스펙: type-flowchart — 크래시가 났을 때의 갈림이 논지다. 문서가 있다고 적은 갈림이
#           실제로는 없다는 것을 보이려면 그 자리를 그려 두고 지워야 한다.
#           마름모는 마커 없는 path 라 dd-lint 의 diagonal 검사 대상이 아니다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, BAD, OK, KR, MONO

W, H = 880, 598
d = D(W, H, "LEARNING COREDNS · 08-01 §7",
      "복구가 꺼지는 자리는 한 곳뿐이다",
      "panic 복구는 서버 본체 한 곳에만 있고 debug 가 그 자리를 끈다. 공식 문서는 errors 가 "
      "복구를 다시 건다고 적지만 소스에는 그 코드가 없다.",
      "주황이 문서에만 있고 코드에는 없는 갈림입니다")

SP = 280
HW, HH = 136, 36


def diamond(cx, cy, l1, l2, c=MUTED):
    d.path(f"M {cx} {cy - HH} L {cx + HW} {cy} L {cx} {cy + HH} L {cx - HW} {cy} Z", c, 1.2)
    d.t(cx, cy - 3, l1, 12, INK, MONO)
    d.t(cx, cy + 16, l2, 12, INK, KR)


d.box(SP - 90, 96, 180, 40, PAPER2, RULE, 1.0, 20)
d.t(SP, 121, "panic 발생", 13, INK, KR, "middle", 600)
d.arrow([(SP, 136), (SP, 190)], MUTED, "ar", 1.4)

diamond(SP, 230, "s.debug", "가 서 있는가")
d.arrow([(SP + HW, 230), (596, 230)], MUTED, "ar", 1.4)
d.t(504, 220, "아니오", 11, MUTED, KR)
d.arrow([(SP, 266), (SP, 316)], OK, "ok", 1.5)
d.t(SP + 12, 296, "예", 11, OK, KR, "start")

d.box(598, 202, 244, 60, PAPER2, RULE, 1.0)
d.t(720, 228, "서버가 복구한다", 13, INK, KR, "middle", 600)
d.t(720, 248, "SERVFAIL 을 돌려주고 산다", 11, MUTED, KR)

d.tone(SP - 122, 318, 244, 60, OK, 6, "12", 1.4)
d.t(SP, 344, "복구하지 않는다", 13, OK, KR, "middle", 600)
d.t(SP, 364, "스택 트레이스를 얻는다", 11, OK, KR)

# 문서에만 있는 갈림 — 점선으로 그려 두고 없다고 표시한다
# 문서에만 있는 갈림 — 사선으로 지우면 라벨이 안 읽히므로 점선과 문구로만 표시한다.
d.path("M 402 348 L 596 348", ACC, 1.4, m="acc", dash="5 4")
d.t(499, 338, "문서만", 11, ACC, KR)
d.tone(598, 318, 244, 60, ACC, 6, "0E", 1.3)
d.t(720, 342, "errors 가 recover 를 건다", 11, ACC, MONO, "middle", 600)
d.t(720, 362, "코드에는 이 갈림이 없다", 11, ACC, KR)

d.box(20, 402, 840, 106, PAPER, RULE, 0.8)
d.t(36, 426, "소스에서 확인한 것", 12, INK, KR, "start", 600)
d.t(36, 450, "plugin/errors/errors.go 에 recover 도 panic 도 없다", 11, MUTED, MONO, "start")
d.t(36, 472, "core/dnsserver/server.go 의 복구 한 곳이 if !s.debug 로 감싸여 있다", 11, MUTED, MONO, "start")
d.t(36, 494, "구조체 필드 주석이 debug bool // disable recover() 다", 11, MUTED, MONO, "start")

d.legend(536, [("문서에만 있고 코드에 없는 갈림", ACC), ("스택 트레이스를 얻는 길", OK)])
d.save("08-01.debug-recover.svg")
