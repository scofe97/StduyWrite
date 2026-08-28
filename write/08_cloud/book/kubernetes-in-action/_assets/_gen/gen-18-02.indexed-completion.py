# 18-02 §4 — 템플릿 하나로 서로 다른 몫을 맡는다
# 인덱스가 붙는다는 사실만으로는 쓸모가 안 보인다. 그 번호로 각자 다른 데이터를 집는다는
# 결과까지 그려야 "왜 번호를 주나"가 답해진다.
# 타입 스펙: type-tree.md — 템플릿 하나가 부모이고 인덱스 파드들이 자식이다. 줄기에서 직각으로 갈라지는 연결선,
#           깊이 2 · 너비 4 로 정본 상한 안에 있다.
#           type-dependency 정본은 트리로 표현 못 하는 두 가지(한 노드에 부모가 둘인 팬인, 순환)를
#           위한 타입이고 '둘 다 없으면 Tree 를 쓰고 그렇다고 밝히라'고 명시한다. 여기엔 둘 다 없다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO
import ddx

d = D(1220, 620, "KUBERNETES IN ACTION · 18-02",
      "같은 템플릿, 다른 몫",
      "completionMode 를 Indexed 로 두면 파드마다 0 부터 번호가 붙는다. 그 번호를 환경변수와 "
      "어노테이션으로 받아 각자 처리할 범위를 스스로 계산한다.",
      "completions 12 · 템플릿은 하나")

ddx.node(d, 170, 300, "Pod 템플릿", "하나뿐이다", 220, 88, INFO)
d.t(170, 372, "completionMode: Indexed", 10, MUTED, MONO)

# 하나의 템플릿에서 넷으로 비스듬히 뻗지 않는다. 줄기(x=400)는 중립색으로 세우고 색은
# 갈라진 팔에만 준다 — 공유 구간이 초점색으로 덮이는 것도 함께 막는다.
d.path("M 282 300 L 400 300", SOFT, 1.2)
d.path("M 400 190 L 400 418", SOFT, 1.2)
for i, idx in enumerate((0, 1, 2, 11)):
    cy = 190 + i * 76
    if i == 3:
        d.t(700, cy - 34, "…", 14, SOFT, KR)
    c = ACC if i == 0 else INFO
    d.box(520, cy - 26, 360, 52, PAPER2, c, 1.1, 5)
    d.t(545, cy + 4, f"파드 index {idx}", 11, c, MONO, "start", 600)
    # x=760 에서 왼쪽 정렬하면 22~24 글자짜리 mono 가 상자 오른쪽 변(x=880)을 넘었다.
    # 오른쪽 정렬로 바꿔 인덱스 자릿수가 늘어도 상자 안에 머물게 한다.
    d.t(860, cy + 4, f"JOB_COMPLETION_INDEX={idx}", 10, MUTED, MONO, "end")
    d.path(f"M 400 {cy} L 512 {cy}", c, 1.2, m="acc" if i == 0 else "info")

d.box(940, 164, 240, 288, PAPER, RULE, 0.9, 8)
d.t(1060, 192, "각자 맡는 몫", 11, SOFT, KR)
for i, (idx, rng) in enumerate(((0, "0 ~ 999"), (1, "1000 ~ 1999"), (2, "2000 ~ 2999"), (11, "11000 ~ 11999"))):
    d.t(1060, 236 + i * 44, rng, 11, ACC if i == 0 else MUTED, MONO)

d.t(24, 508, "번호가 없으면(NonIndexed) 파드들이 서로 구분되지 않아, 누가 무엇을 맡을지 밖에서 정해 줘야 한다. "
             "그 조율을 큐로 미는 방법이 18-03 이다.", 11, MUTED, KR, "start")
d.legend(536, [("템플릿과 파드", INFO), ("번호가 정하는 몫", ACC)])
d.save("18-02-indexed-completion.svg")
print("ok")
