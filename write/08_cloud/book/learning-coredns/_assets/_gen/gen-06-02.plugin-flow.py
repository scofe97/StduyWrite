# 06-02 §1 — kubernetes 플러그인은 watch 로 받아 두고 질의가 올 때 레코드를 만든다.
# 원문 근거: "The CoreDNS kubernetes plug-in works very much like a controller, except that it never
#            writes data back to the API server. It creates a watch on the Services and Endpoints
#            resources, and caches that data." / "The response records are not generated and stored
#            somewhere; they are built on the fly based on the incoming request." /
#            "CoreDNS never needs to query the API server in direct response to a DNS query."
# 타입 스펙: type-architecture — 구성요소와 연결이 논지이고, 없는 연결 하나가 결론이다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, BAD, KR, MONO

W, H = 880, 604
d = D(W, H, "LEARNING COREDNS · 06-02 §1",
      "watch 로 받아 두고 질의가 올 때 만든다",
      "플러그인은 컨트롤러처럼 watch 를 걸지만 API 서버로 되쓰지 않는다. 응답 레코드는 어디에도 저장되지 "
      "않고 요청이 올 때마다 인메모리 자원에서 만들어진다.",
      "붉은 점선이 컨트롤러에는 있고 여기에는 없는 경로입니다")

d.box(20, 132, 200, 96, PAPER2, RULE, 1.0)
d.t(120, 170, "API 서버", 15, INFO, KR, "middle", 600)
d.t(120, 194, "Services · Endpoints", 12, MUTED, MONO)
d.t(120, 214, "etcd 가 뒤를 받친다", 12, MUTED, KR)

ZX, ZY, ZW, ZH = 296, 108, 388, 232
d.o.append(f'<rect x="{ZX}" y="{ZY}" width="{ZW}" height="{ZH}" rx="8" fill="{PAPER}" '
           f'stroke="{RULE}" stroke-width="1.0" stroke-dasharray="4 4"/>')
ZL = "COREDNS PROCESS"
d.o.append(f'<rect x="{ZX + 14}" y="{ZY - 8}" width="{len(ZL) * 6 + 16}" height="16" fill="{PAPER}"/>')
d.t(ZX + 22, ZY + 4, ZL, 9, SOFT, MONO, "start", 600)

d.box(ZX + 28, 140, 332, 76, PAPER2, RULE, 1.0)
d.t(ZX + 194, 172, "인메모리 자원 캐시", 15, INK, KR, "middle", 600)
d.t(ZX + 194, 196, "쿠버네티스 객체 그대로", 12, MUTED, KR)

d.tone(ZX + 28, 240, 332, 76, ACC, 6, "12", 1.4)
d.t(ZX + 194, 272, "레코드를 즉석에서 만든다", 15, ACC, KR, "middle", 600)
d.t(ZX + 194, 296, "저장하지 않는다", 12, ACC, KR)

d.box(720, 132, 140, 96, PAPER2, RULE, 1.0)
d.t(790, 170, "파드 안", 15, INK, KR, "middle", 600)
d.t(790, 192, "클라이언트", 15, INK, KR, "middle", 600)
d.t(790, 214, "resolver", 12, MUTED, MONO)

d.arrow([(224, 164), (ZX + 24, 164)], INFO, "info", 1.4)
d.t(258, 152, "watch", 12, INFO, MONO)
d.path(f"M {ZX + 24} 200 L 224 200", BAD, 1.2, m="bad", dash="5 4")
d.t(258, 222, "되쓰기 없음", 12, BAD, KR)

d.path(f"M {ZX + 194} 216 L {ZX + 194} 236", MUTED, 1.4, m="ar")

d.path(f"M 790 232 L 790 278 L {ZX + 364} 278", MUTED, 1.4, m="ar")
d.t(700, 266, "질의", 12, MUTED, KR)
d.path(f"M {ZX + 364} 300 L 800 300 L 800 236", ACC, 1.4, m="acc")
d.t(714, 322, "응답", 12, ACC, KR)

d.t(20, 396, "쿠버네티스 자원이 이미 메모리에 있어 레코드를 만드는 일이 아주 빠르다", 13, MUTED, KR, "start")
d.t(20, 420, "그래서 DNS 질의에 답하려고 API 서버를 부를 일이 전혀 없다", 13, MUTED, KR, "start")
d.t(20, 444, "이 사실이 2절의 \"캐시가 아낄 것이 없다\" 로 곧장 이어진다", 13, MUTED, KR, "start")

d.legend(480, [("저장되지 않는 자리", ACC), ("클러스터 상태를 읽는 경로", INFO), ("컨트롤러에는 있고 여기엔 없는 경로", BAD)])
d.save("06-02.plugin-flow.svg")
