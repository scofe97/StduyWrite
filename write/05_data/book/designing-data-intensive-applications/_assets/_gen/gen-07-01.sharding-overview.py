# 07-01 §1 샤딩과 복제의 결합 — 노드마다 특정 샤드의 리더이자 다른 샤드의 팔로워를 겸하는 단일 리더 복제와 샤딩 배치.
# 사실 출처: 07-01 본문 §1(L28~L30), DDIA 2판 7장 Figure 7-1 "Combining replication and sharding" (PDF 2쪽).
# 노드별 샤드·역할은 Figure 7-1 그대로. 그림의 복제 스트림 네 갈래 중 샤드 1·4 만 그린다. 리더는 쓰기를 받는다(Writing to shard 4).
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 880
H = 588
LEG = 536

d = D(W, H, "07-01 · §1 ARCHITECTURE", "단일 리더 복제와 샤딩의 결합 배치",
      "각 노드는 특정 샤드의 리더 역할을 맡으면서 동시에 다른 샤드의 팔로워를 겸하여 내결함성과 수평 확장을 함께 달성한다.",
      "노드별 다중 샤드 분산 · 샤드당 단일 리더 전담 · 복제 스트림 전파 · 내결함성과 쓰기 확장 결합")

# 2x2 노드 배치
NW = 388
NH = 144
XL = 36
XR = 456
YT = 96
YB = 312

# 노드 외곽 상자
nodes_def = [
    ("노드 1", XL, YT, [
        ("샤드 1", "리더", "쓰기 수신", OK),
        ("샤드 2", "팔로워", "복제 수신", INFO),
        ("샤드 3", "팔로워", "복제 수신", INFO),
    ]),
    ("노드 2", XR, YT, [
        ("샤드 2", "팔로워", "복제 수신", INFO),
        ("샤드 3", "리더", "쓰기 수신", OK),
        ("샤드 4", "팔로워", "복제 수신", INFO),
    ]),
    ("노드 3", XL, YB, [
        ("샤드 1", "팔로워", "복제 수신", INFO),
        ("샤드 2", "리더", "쓰기 수신", OK),
        ("샤드 4", "팔로워", "복제 수신", INFO),
    ]),
    ("노드 4", XR, YB, [
        ("샤드 1", "팔로워", "복제 수신", INFO),
        ("샤드 3", "팔로워", "복제 수신", INFO),
        ("샤드 4", "리더", "쓰기 수신", ACC),  # FOCAL
    ]),
]

SW = 114
SH = 100
SGAP = 10
SPAD_X = 12
SPAD_Y = 32

for n_title, nx, ny, shards in nodes_def:
    d.box(nx, ny, NW, NH, PAPER2, RULE, 1.0)
    d.t(nx + 16, ny + 22, n_title, 12.5, INK, KR, "start", 600)

    for i, (s_name, s_role, s_desc, s_color) in enumerate(shards):
        sx = nx + SPAD_X + i * (SW + SGAP)
        sy = ny + SPAD_Y
        is_focal = (s_color == ACC)

        if is_focal:
            d.tone(sx, sy, SW, SH, ACC, 6, "18", 1.4)
        elif s_color == OK:
            d.tone(sx, sy, SW, SH, OK, 6, "14", 1.1)
        else:
            d.box(sx, sy, SW, SH, PAPER, RULE, 0.8)

        d.chip(sx + SW / 2, sy + 16, s_name, s_color, 11)
        d.t(sx + SW / 2, sy + 48, s_role, 13, INK if is_focal else s_color, KR, "middle", 600 if s_color != INFO else 500)
        d.t(sx + SW / 2, sy + 74, s_desc, 11.5, MUTED, KR, "middle")

# 중간 통로(y=240~312)를 통한 복제 스트림 화살표
# 1. 샤드 1 복제 스트림 (노드 1 리더 -> 노드 3 팔로워, 노드 4 팔로워)
# 노드 1 샤드 1 리더 중심: x = XL + 12 + 57 = 105, y = YT + 32 + 100 = 228 (노드 1 바닥: 240)
d.arrow([(105, 240), (105, YB + 32)], OK, "ok", 1.4)  # 직하강 to 노드 3 샤드 1
# 칩(cx=290, w~130 -> 225~355)을 건너뛰는 L자 화살표
d.path(f"M 115 240 L 115 264 L 210 264", OK, 1.2)
d.arrow([(370, 264), (XR + 12 + 57, 264), (XR + 12 + 57, YB + 32)], OK, "ok", 1.2)
d.chip(290, 264, "샤드 1 복제 스트림", OK, 11)

# 2. 샤드 4 복제 스트림 (노드 4 샤드 4 리더(focal) -> 노드 2 팔로워, 노드 3 팔로워)
# 노드 4 샤드 4 리더 중심: x = XR + 12 + 2*124 + 57 = 773
d.arrow([(773, 312), (773, YT + NH)], ACC, "acc", 1.5)  # 직상승 to 노드 2 샤드 4
# 칩(cx=640, w~134 -> 573~707)을 건너뛰는 경로. 샤드 1 세로선(x=525)이 칩을 뚫지 않게 오른쪽에 둔다
d.path(f"M 760 312 L 760 288 L 715 288", ACC, 1.3)
d.arrow([(565, 288), (XL + 12 + 2*124 + 57, 288), (XL + 12 + 2*124 + 57, YB + 32)], ACC, "acc", 1.3)
d.chip(640, 288, "샤드 4 복제 스트림", ACC, 11)

# 하단 클라이언트 쓰기 요청 (Figure 7-1 오른쪽 아래 쓰기 요청 반영)
CY = YB + NH + 26
d.box(XR + 90, CY, 220, 34, PAPER, ACC, 1.0)
d.t(XR + 200, CY + 22, "클라이언트 샤드 4 쓰기 요청", 12, ACC, KR, "middle", 600)
# 클라이언트 -> 노드 4 샤드 4 리더 화살표 (길이 26px)
d.arrow([(XR + 200, CY), (XR + 200, YB + NH)], ACC, "acc", 1.4)

# 하단 범례
d.legend(LEG, [
    ("샤드 리더 (쓰기 수신)", OK),
    ("샤드 팔로워 (복제 수신)", INFO),
    ("클라이언트 대상 샤드 리더", ACC),
])

d.save("07-01.sharding-overview.svg")
