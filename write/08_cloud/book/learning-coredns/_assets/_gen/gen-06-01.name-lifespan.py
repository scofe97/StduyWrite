# 06-01 §7 — 파드를 지웠다 다시 만들 때 이름이 이어지는지가 워크로드 종류로 갈린다.
# 원문 근거: StatefulSet 은 "sets the hostname based on an ordinal number (0, 1, 2, etc.) and keeps
#            this name even if the pod is deleted and recreated (a Deployment would generate a new pod
#            name in this case). This provides a stable network identity for the pod." /
#            원서 Example 6-10 은 파드 넷을 강제로 지운 뒤 같은 서수 이름과 바뀐 IP 를 보인다.
#            StatefulSet 행의 두 주소는 Example 6-9(10.5.109.14) 와 6-10(10.5.109.15) 의 실제 값이다.
#            Deployment 행은 원서에 대응 값이 없어 자리표시자로 둔다 — 없는 값을 지어내지 않는다.
# 타입 스펙: type-gantt — 막대가 끊기느냐 이어지느냐가 곧 그 이름의 수명이다.
#           축약: 가로축이 날짜가 아니라 파드 생애의 네 구간이다(같은 폴더 02-01·05-01 과 같은 축약).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, RULE, BAD, INFO, KR, MONO

W, H = 1000, 616
d = D(W, H, "LEARNING COREDNS · 06-01 §7",
      "지웠다 다시 만들면 무엇이 이어지는가",
      "가로축은 파드 생애의 네 구간이다. 삭제 경계를 관통하는 막대가 하나뿐이고, "
      "그것이 StatefulSet 이 주는 안정적인 네트워크 신원이다.",
      "경계를 넘는 막대가 하나뿐입니다")

LX, TX, TW = 20, 240, 700
COLS = ["처음 뜸", "운영 중", "다시 뜸", "그 뒤"]
PITCH = TW / len(COLS)

for i, nm in enumerate(COLS):
    d.t(TX + PITCH * i + PITCH / 2, 116, nm, 12, SOFT, KR)
d.line(TX, 128, TX + TW, 128, RULE, 1.0)

rows = [
    ("파드 이름", 0, 2, BAD, "headless-<해시>-<무작위>"),
    ("파드 IP", 0, 2, INFO, "할당된 주소"),
    ("파드 이름", 0, 4, ACC, "headless-0 · 그대로"),
    ("파드 IP", 0, 2, INFO, "10.5.109.14"),
]
extra = [
    (0, 2, 2, BAD, "headless-<다른 해시>-<무작위>"),
    (1, 2, 2, INFO, "새 주소"),
    (3, 2, 2, INFO, "10.5.109.15"),
]


def row_y(k):
    return 172 + k * 44 + (28 if k >= 2 else 0)


d.box(224, 156, 752, 108, PAPER, RULE, 0.8, 6)
d.t(232, 176, "Deployment", 9, SOFT, MONO, "start", 600)
d.box(224, 272, 752, 108, PAPER, RULE, 0.8, 6)
d.t(232, 292, "StatefulSet", 9, SOFT, MONO, "start", 600)


def bar(ry, start, span, color, label):
    x = TX + PITCH * start
    w = PITCH * span
    d.tone(x + 6, ry + 4, w - 12, 26, color, 4, "16", 1.2)
    d.t(x + w / 2, ry + 22, label, 12, color, KR if any("가" <= c <= "힣" for c in label) else MONO)


for k, (nm, start, span, color, label) in enumerate(rows):
    ry = row_y(k)
    d.t(LX, ry + 22, nm, 13, INK, KR, "start", 600)
    for s in range(1, len(COLS)):
        c = ACC if s == 2 else RULE
        d.line(TX + PITCH * s, ry - 2, TX + PITCH * s, ry + 36, c, 0.8 if s != 2 else 1.2, "3 5")
    bar(ry, start, span, color, label)

for k, start, span, color, label in extra:
    bar(row_y(k), start, span, color, label)

d.t(TX + PITCH * 2, 412, "삭제와 재생성 — 여기서 무엇이 끊기는가", 13, ACC, KR)
d.t(LX, 448, "Deployment 는 새 파드 이름을 만들어 낸다. IP 는 어느 쪽이든 바뀐다", 13, MUTED, KR, "start")
d.t(LX, 472, "그래서 이름으로 상대를 고정해야 하는 워크로드는 StatefulSet 을 골라야 한다", 13, MUTED, KR, "start")

d.legend(500, [("끊기고 새로 생긴다", BAD), ("어차피 바뀐다", INFO), ("유일하게 이어진다", ACC)])
d.save("06-01.name-lifespan.svg")
