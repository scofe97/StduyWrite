# 2026-09-12 B(502) 문항 · 문제 소개 — 어떤 구조에서 일어난 일인가.
# 논지는 "요청이 어디를 거쳐 앱에 닿나"이지 종료 순서가 아니다.
# 두 갈래가 동시에 가는 인과는 원인 분석 절의 termination-race 가 맡는다.
# 타입 스펙: type-architecture — 구성요소와 연결. Pod 경계로 사이드카 범위를 보인다.
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dd import D, ACC, MUTED, SOFT, INK, BAD, PAPER2, RULE, KR, MONO

W, H = 808, 400
d = D(W, H, "TROUBLESHOOTING DRILL · 2026-09-12 B",
      "요청이 앱에 닿기까지",
      "바깥 요청은 Service 를 거쳐 Pod 에 들어오고, Pod 안에서 사이드카 프록시가 "
      "같은 네트워크 네임스페이스의 앱에게 넘긴다. 마지막 한 칸은 클러스터 라우팅을 거치지 않는다.",
      lead="502 를 내는 것은 마지막 한 칸입니다")

d.box(40, 128, 150, 68, PAPER2, RULE, 0.9, 6)
d.t(115, 156, "클라이언트", 13, INK, KR, "middle", 600)
d.t(115, 176, "바깥 요청", 11, SOFT, MONO)
d.arrow([(190, 162), (236, 162)], MUTED, "ar", 1.3)

d.box(236, 128, 150, 68, PAPER2, RULE, 0.9, 6)
d.t(311, 156, "Service", 13, INK, KR, "middle", 600)
d.t(311, 176, "EndpointSlice", 11, SOFT, MONO)
d.arrow([(386, 162), (432, 162)], MUTED, "ar", 1.3)

PX, PY, PW, PH = 432, 104, 336, 148
d.box(PX, PY, PW, PH, PAPER2, RULE, 1.0, 8)
d.t(PX + 14, PY + 22, "Pod — 컨테이너 둘", 12, SOFT, KR, "start", 600)

d.box(PX + 20, PY + 40, 138, 84, PAPER2, RULE, 0.9, 6)
d.t(PX + 89, PY + 68, "프록시", 13, INK, KR, "middle", 600)
d.t(PX + 89, PY + 88, "사이드카", 11, SOFT, KR)
d.t(PX + 89, PY + 108, "PID 1 따로", 11, SOFT, MONO)

d.tone(PX + 178, PY + 40, 138, 84, ACC, 6)
d.t(PX + 247, PY + 68, "앱", 13, ACC, KR, "middle", 600)
d.t(PX + 247, PY + 88, "java · 8080", 11, SOFT, MONO)
d.t(PX + 247, PY + 108, "PID 1 은 셸", 11, SOFT, MONO)

d.arrow([(PX + 158, PY + 82), (PX + 174, PY + 82)], ACC, "acc", 1.4)
d.t(PX + 166, PY + 138, "127.0.0.1:8080", 11, MUTED, MONO)

d.t(W // 2, 308, "이 마지막 한 칸은 같은 네트워크 네임스페이스라 클러스터 라우팅을 거치지 않습니다",
    13, MUTED, KR, "middle")
d.t(W // 2, 332, "그래서 connection refused 는 경로 문제가 아니라 도달했다는 증거입니다",
    12, BAD, KR, "middle")

d.save(os.path.join(os.path.dirname(__file__), "..", "2026-09-12.sidecar-topology.svg"))
print("ok")
