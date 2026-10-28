# 03-02 §2 — 로고 URL 을 사람마다 복제하는 비정규화와, 조직 엔티티 하나를 ID 로 참조하는 정규화를 비교한다.
# 옛 도식의 일반 원칙(읽기·쓰기 맞바꿈)은 뺐다. §2 본문 산문이 맡는다.
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO

W = 880
PY, PH = 100, 252
LEG = PY + PH + 32
H = LEG + 56

d = D(W, H, "03-02 · NORMALIZATION", "비정규화와 정규화의 로고 URL",
      "비정규화는 로고 URL 을 프로필마다 복제하고, 정규화는 조직 엔티티에 한 번 저장한 뒤 프로필이 ID 로 참조한다.",
      "같은 조직 정보를 어디에 두는가")

d.box(16, PY, 416, PH, PAPER, WARN, 1.2)
d.box(448, PY, 416, PH, PAPER, ACC, 1.4)
d.t(32, 124, "비정규화 — 프로필마다 복제", 14, INK, KR, "start", 600)
d.t(464, 124, "정규화 — 조직 엔티티와 ID", 14, INK, KR, "start", 600)

# 비정규화: 프로필 셋이 각자 로고 URL 을 들고 있다
for i in range(3):
    x = 32 + 128 * i
    d.box(x, 168, 112, 104, PAPER2, WARN, 1.2)
    d.t(x + 56, 192, f"프로필 {i + 1}", 13, INK, KR, "middle", 600)
    d.t(x + 56, 220, "organization", 12, MUTED, MONO)
    d.t(x + 56, 244, "로고 URL", 12, WARN, KR)
d.t(224, 336, "로고를 바꾸면 옛 URL 을 전부 갱신", 12, WARN, KR)

# 정규화: 조직 엔티티 하나, 프로필 셋이 ID 로 참조
d.box(480, 144, 352, 56, PAPER2, OK, 1.4)
d.t(656, 168, "조직 엔티티", 13, INK, KR, "middle", 600)
d.t(656, 188, "이름 · 로고 URL · 기타 속성", 12, MUTED, KR)
for i in range(3):
    x = 480 + 120 * i
    d.box(x, 256, 112, 48, PAPER2, INFO, 1.2)
    d.t(x + 56, 286, f"프로필 {i + 1}", 13, INK, KR)
    d.arrow([(x + 56, 252), (x + 56, 204)], MUTED, "ar", 1.4)
    d.chip(x + 56, 228, "조직 ID", MUTED, 11)
d.t(656, 336, "로고 갱신은 한 곳", 12, OK, KR)

d.legend(LEG, [("핵심 — 정규화", ACC), ("복제 · 갱신 비용", WARN), ("한 번 저장", OK), ("프로필", INFO)])
d.save("03-02.normalization.svg")
