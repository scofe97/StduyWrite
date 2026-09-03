# 14-01 §4 전역 레이트 리미팅이 서는 자리 — 원문 그림 14.6 · 14.7.
# 본문(원문 14.3 · 14.3.1): 같은 서비스의 복제본 여럿이 같은 레이트 리밋 서비스를 불러 그 서비스에 대한
#       전역 레이트 리미팅을 얻는다. 전역 방식에서는 특정 워크로드의 모든 Envoy 프록시가 같은 서버를
#       부르고 그 서버가 백엔드 전역 키-값 저장소를 부른다. 이 구조로 복제본이 몇 개든 한도가 강제된다.
#       서버는 Envoy 커뮤니티의 것을 쓰며 백엔드 Redis 캐시와 이야기하고 카운터를 Redis 에 저장한다
#       (Memcache 도 가능). 요청의 속성 — 원격 주소 · 요청 헤더 · 목적지 등 — 을 Envoy 용어로
#       디스크립터라 부르고, 그것이 서버로 보내져 미리 정의된 집합과 대조되며 카운터가 올라간다.
#       카운트가 임계를 넘으면 그 요청이 제한된다.
# 복제본 셋은 예시다 — 원문 그림 14.6 은 개수를 못 박지 않고 "같은 서비스의 복제본 여럿" 이라 적는다.
# 타입 스펙: type-architecture — 구성요소와 그 사이의 연결이 논점이다. 노드 6 · 경로 5,
#           accent 는 여럿이 하나를 공유하는 자리에.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 676
d = D(W, H, "ISTIO IN ACTION · 14-01 §4",
      "복제본이 셋이어도 세는 곳은 하나여야 한다",
      "워크로드의 모든 Envoy 가 같은 레이트 리밋 서버를 부르고 그 서버가 공용 저장소를 본다. 색이 붙은 "
      "자리가 그 공유점이고, 그것 때문에 복제본 수와 무관하게 한도가 지켜진다.",
      "로컬 방식이었다면 한도가 복제본 수만큼 늘어납니다")

def node(x, y, w, h, tag, name, sub, focal=False, c=None):
    col = c or (ACC if focal else None)
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y, w, h, PAPER2, RULE, 1.0, 6)
    d.o.append(f'<rect x="{x + 12}" y="{y + 12}" width="40" height="14" rx="2" fill="{INK}14"/>')
    d.t(x + 32, y + 23, tag, 8, INK, MONO, "middle", 600)
    d.t(x + 62, y + 24, name, 13, ACC if focal else INK, KR, "start", 600)
    d.t(x + 62, y + 42, sub, 11, MUTED, MONO, "start")

REPY = [140, 236, 332]
for i, y in enumerate(REPY):
    node(40, y, 264, 68, "POD", f"catalog 복제본 {i + 1}", "app + istio-proxy")
    d.line(304, y + 34, 404, y + 34, INFO, 1.2)
d.line(404, REPY[0] + 34, 404, REPY[2] + 34, INFO, 1.2)
d.path("M 404 270 H 448", INFO, 1.3, m="info")

node(452, 236, 260, 68, "RLS", "레이트 리밋 서버", "Envoy 레이트 리밋 API 구현", focal=True)
node(740, 236, 220, 68, "KV", "Redis", "카운터를 저장한다 · Memcache 가능")
d.path("M 708 270 H 740", ACC, 1.5, m="acc")

d.t(424, 258, "디스크립터", 11, INFO, MONO, "middle", 600)
d.t(848, 220, "전역 카운터", 11, ACC, MONO, "middle", 600)

BY = 424
d.box(40, BY, 924, 116, PAPER2, RULE, 1.0, 6)
d.t(56, BY + 26, "디스크립터 — Envoy 용어로 요청의 속성 또는 속성 묶음", 11, ACC, KR, "start", 600)
d.t(56, BY + 50, "원격 주소 · 요청 헤더 · 목적지 · 그 밖의 일반적인 요청 속성", 11, INK, KR, "start")
d.line(56, BY + 66, 944, BY + 66, RULE, 0.9)
d.t(56, BY + 90, "서버가 하는 일 — 보내진 속성을 미리 정의된 집합과 대조하고 카운터를 올린다. 임계를 넘으면 그 요청을 제한한다", 11, SOFT, KR, "start")

d.t(24, 576, "Envoy 의 레이트 리미팅은 여럿이다 — 네트워크 필터로도, 로컬로도, 전역으로도 된다. 저자가 고르는 것은 전역", 11, SOFT, KR, "start")
d.t(24, 600, "같은 콜아웃 구조를 9 장의 외부 인가에서 이미 봤다 — 대신 요청 경로에 홉이 하나 는다", 11, MUTED, KR, "start")
d.legend(620, [("복제본이 공유하는 자리", ACC), ("프록시가 보내는 것", INFO)])
d.save("14-01.global-ratelimit.svg")
