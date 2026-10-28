# 03-01 §3~4 — 같은 이력서 한 건을 관계형(테이블 넷, user_id 참조)과 문서(JSON 한 개, 트리)로 나란히 그린다.
# 옛 도식의 라벨 중 본문에 없는 것은 뺐다. 필드는 본문 예(user_id·first_name·last_name)만 쓴다.
# 타입 스펙: type-er
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO

W = 880
PY, PH = 100, 252
LEG = PY + PH + 32
H = LEG + 56

d = D(W, H, "03-01 · RELATIONAL VS DOCUMENT", "같은 이력서의 두 표현",
      "관계형은 users 와 하위 테이블 셋으로 나누고 user_id 로 잇고, 문서 모델은 직위·학력·연락처를 JSON 한 개에 트리로 담는다.",
      "이력서 한 건의 저장 형태")

d.box(16, PY, 416, PH, PAPER, RULE, 0.9)
d.box(448, PY, 416, PH, PAPER, ACC, 1.4)
d.t(32, 124, "관계형 — 테이블 넷", 14, INK, KR, "start", 600)
d.t(464, 124, "문서 — JSON 한 개", 14, INK, KR, "start", 600)

# 관계형: users 위, 하위 테이블 셋이 user_id 로 users 를 가리킨다
d.box(32, 144, 384, 56, PAPER2, INFO, 1.2)
d.t(224, 166, "users", 14, INK, MONO, "middle", 600)
d.t(224, 186, "user_id · first_name · last_name", 12, MUTED, MONO)
for i, name in enumerate(["positions", "education", "contact_info"]):
    x = 32 + 136 * i
    d.box(x, 256, 112, 48, PAPER2, INFO, 1.2)
    d.t(x + 56, 286, name, 12, INK, MONO)
    d.arrow([(x + 56, 252), (x + 56, 204)], MUTED, "ar", 1.4)
    d.chip(x + 56, 228, "user_id", MUTED, 11)
d.t(224, 336, "테이블마다 user_id 로 조회", 12, WARN, KR)

# 문서: 한 문서 안에 하위 항목이 중첩
d.box(464, 144, 384, 160, PAPER2, ACC, 1.4)
d.t(656, 164, "프로필 문서 · user_id 251", 12, MUTED, KR)
for i, (name, br) in enumerate([("positions", "[ ]"), ("education", "[ ]"), ("contact_info", "{ }")]):
    y = 176 + 44 * i
    d.box(480, y, 352, 32, PAPER, RULE, 1.0)
    d.t(496, y + 21, name, 12, INK, MONO, "start")
    d.t(816, y + 21, br, 12, MUTED, MONO, "end")
d.t(656, 336, "관련 정보가 한 곳에 · locality", 12, OK, KR)

d.legend(LEG, [("문서 모델", ACC), ("테이블·엔티티", INFO), ("조회 비용", WARN), ("locality 이점", OK)])
d.save("03-01.relational-vs-document.svg")
