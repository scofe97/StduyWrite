# 05-03 §2 — 컨트롤러는 무엇으로 만들어져 어디서 도는가.
# 원문 5.5.1·5.5.2 곁상자: "a logically centralized controller ... in practice implemented on
#       several servers that provide fault tolerance, high availability, or performance" ·
#       ONOS 는 "distributed core, replicated over multiple servers" · ORION 의 NIB 는 초당 약
#       백만 건의 읽기·쓰기를 처리한다.
# 노트의 읽기: 2026-09-10 학습자가 "컨트롤러가 정확히 뭐임?", "관리 노드가 3개면 서로 이야기
#       안 하나?" 로 두 번 막혀 추가했다. 서버 대수 셋은 예시다 — 원문은 수를 적지 않는다.
# 타입 스펙: type-deployment — 무엇이 어느 호스트에서 몇 벌 도는가. 복제본 배지와 존 경계를 쓴다.
#       축약: 원문이 버전을 적지 않아 아티팩트 칩의 버전 태그 자리에 역할이나 원문의 수치를 적었다.
#       OpenFlow 의 포트 번호도 원문에 없어 프로토콜 이름만 단다.
import sys; sys.path.insert(0, ".")
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, KR, MONO

W, H = 920, 700
d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 05-03 §2",
      "컨트롤러는 서버 위에서 도는 소프트웨어입니다",
      "논리적으로 중앙인 SDN 컨트롤러가 실제로는 여러 서버에 흩어져 상태를 복제하고, 스위치에게는 "
      "하나의 서비스로 보이는 배치. 서버끼리는 합의로 이야기하고, 스위치와는 남향 인터페이스로 이야기한다.",
      "밖에서 보면 하나, 안에서 보면 여럿입니다")


def zone(x, y, w, h, label):
    d.box(x, y, w, h, "none", "rgba(245,245,245,0.20)", 1.0, 8)
    tw = sum(11.0 if "가" <= c <= "힣" else 6.0 for c in label) + 16
    d.box(x + 16, y - 8, tw, 16, PAPER, "none", 0, 2)
    d.t(x + 24, y + 4, label, 11, SOFT, KR, "start")


def chip(x, y, w, name, tag):
    d.box(x, y, w, 28, "rgba(245,245,245,0.05)", MUTED, 0.9, 4)
    d.t(x + 12, y + 19, name, 12, INK, KR, "start")
    d.t(x + w - 12, y + 19, tag, 12, MUTED, MONO, "end")


def node(x, y, w, h, tag, name, sub, badge=None, hot=False):
    c = ACC if hot else RULE
    d.box(x, y, w, h, f"{ACC}12" if hot else PAPER2, c, 1.4 if hot else 1.0, 6)
    d.box(x + 10, y + 10, 52, 18, PAPER, MUTED, 0.9, 2)
    d.t(x + 36, y + 23, tag, 11, MUTED, MONO)
    if badge:
        d.box(x + w - 52, y + 10, 42, 18, PAPER, INK, 0.9, 2)
        d.t(x + w - 31, y + 23, badge, 11, INK, MONO)
    d.t(x + w / 2, y + 58, name, 15, ACC if hot else INK, KR, "middle", 600)
    d.t(x + w / 2, y + 78, sub, 12, MUTED, KR)


zone(40, 110, 840, 240, "제어 평면 — 논리적으로 하나")
zone(40, 400, 840, 148, "데이터 평면")

node(72, 150, 320, 168, "SERVER", "제어 서버 1", "지금 상태를 쓰는 쪽", hot=True)
chip(96, 244, 272, "컨트롤러와 제어 앱", "한 묶음")
chip(96, 282, 272, "ORION 의 NIB 저장소", "약 100만 건/초")

node(528, 150, 320, 168, "SERVER", "제어 서버 2·3", "같은 것을 나눠 듭니다", badge="x2")
chip(552, 244, 272, "같은 컨트롤러 소프트웨어", "복제본")
chip(552, 282, 272, "NIB 사본", "복제본")

node(290, 424, 340, 100, "SWITCH", "패킷 스위치", "흐름 표에 일치와 동작을 싣습니다", badge="x4")

# 서버끼리 — 상태 복제와 합의
d.path("M 392 236 L 528 236", ACC, 1.4, dash="5 4")
d.t(460, 214, "상태 복제 · 합의", 12, ACC, KR, "middle", 600)
d.t(460, 338, "여기서 순서와 일관성을 맞춥니다", 12, MUTED, KR)

# 존을 건너는 길 — 남향 인터페이스
d.path("M 232 318 L 232 376 L 366 376 L 366 424", INFO, 1.4, m="info")
d.t(300, 368, "OpenFlow", 12, INFO, MONO)
d.path("M 688 318 L 688 376 L 554 376 L 554 424", INFO, 1.4, m="info")
d.t(620, 368, "OpenFlow", 12, INFO, MONO)

d.t(12, 584, "스위치는 서버가 몇 대인지 모릅니다. 하나의 컨트롤러와 이야기한다고 여깁니다.",
    13, MUTED, KR, "start")
d.t(12, 606, "서버를 나누는 이유는 장애 대비와 성능입니다. 쓰기를 한 서버가 맡는 이 모양은 여러 구현 가운데 하나입니다.",
    13, MUTED, KR, "start")

d.legend(636, [("논리적 중앙의 주 인스턴스와 복제", ACC), ("존을 건너는 남향 인터페이스", INFO)])
d.t(W - 12, 684, "KUROSE-ROSS 9E FIG 5.15 · 5.17 · 5.18", 8, SOFT, MONO, "end")

d.save("05-03.controller-reality.svg")
print("ok 05-03.controller-reality")
