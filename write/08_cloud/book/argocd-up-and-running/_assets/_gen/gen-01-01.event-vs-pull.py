# 01-01 §2 — 이벤트 기반 CD 는 이벤트가 파이프라인을 한 번 실행하고 끝나지만, GitOps 의 pull 은 Git 과 클러스터를 반복해서 비교하고 맞춘다.
# 본문 근거: 이 노트 ### 2 「GitOps 네 원칙과 pull 방식」.
# 공식 근거: opengitops.dev GitOps Principles v1.0.0 의 3원칙(Pulled Automatically)·4원칙(Continuously Reconciled),
#            argo-cd.readthedocs.io stable core_concepts(Refresh · Sync) 와 operator-manual/architecture 의 application controller.
# 타입 스펙: type-swimlane — 이벤트 기반 CD 레인과 Argo CD 레인.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, OK, WARN, BAD, INFO, KR, MONO

W, H = 880, 484
d = D(W, H, "ARGO CD UP AND RUNNING · 01-01 §2",
      "이벤트 기반 CD 와 Argo CD 의 움직임",
      "위 레인은 Git 변경 이벤트가 웹훅으로 파이프라인을 호출하고 파이프라인이 클러스터에 적용한 뒤 끝나는 이벤트 기반 흐름이고, "
      "아래 레인은 Argo CD 가 정해진 주기로 Git 을 가져와 Live state 와 비교하고 OutOfSync 면 자동 Sync 를 켠 경우 Sync 한 뒤 다시 처음으로 돌아가는 pull 흐름이다.",
      "이벤트 기반 CD 는 한 번 실행하고 끝나고, Argo CD 는 주기마다 비교하고 자동 Sync 를 켜면 Sync 까지 반복합니다")

BW, BH, PITCH, X0 = 190, 76, 212, 24
LANE_X, LANE_W, LANE_H = 12, 856, 156
A_Y, S_Y = 96, 268


def lane(y, name):
    d.o.append(f'<rect x="{LANE_X}" y="{y}" width="{LANE_W}" height="{LANE_H}" rx="8" fill="{SOFT}0A" stroke="{SOFT}" stroke-width="0.9"/>')
    d.t(LANE_X + 12, y + 20, name, 12, MUTED, KR, "start", 600)


def lane_steps(y, items):
    by = y + 40
    for i, (title, sub, c, fam) in enumerate(items):
        x = X0 + i * PITCH
        d.tone(x, by, BW, BH, c, 6, "14", 1.4 if c == ACC else 1.1)
        d.t(x + BW / 2, by + 32, title, 13, INK, fam, "middle", 600)
        d.t(x + BW / 2, by + 56, sub, 11, MUTED, KR)
        if i < len(items) - 1:
            d.path(f"M {x + BW + 2} {by + BH / 2} L {x + PITCH - 2} {by + BH / 2}", MUTED, 1.4, m="ar")


lane(A_Y, "이벤트 기반 CD")
lane_steps(A_Y, [
    ("Git 변경", "이벤트 발생", INFO, KR),
    ("웹훅", "파이프라인 호출", INFO, KR),
    ("파이프라인", "빌드·배포 단계", INFO, KR),
    ("클러스터 적용", "1회 실행", SOFT, KR),
])
lane(S_Y, "Argo CD (pull)")
lane_steps(S_Y, [
    ("Git 폴링", "정해진 주기", INFO, KR),
    ("Refresh", "Git 과 Live state 비교", ACC, MONO),
    ("OutOfSync", "차이 발견", WARN, MONO),
    ("Sync", "자동 Sync 를 켠 경우", OK, MONO),
])
# 마지막 단계에서 처음으로 돌아가는 반복 경로
by = S_Y + 40
x1c, x4c = X0 + BW / 2, X0 + 3 * PITCH + BW / 2
ry = by + BH + 20
d.path(f"M {x4c} {by + BH + 2} L {x4c} {ry} L {x1c} {ry} L {x1c} {by + BH + 4}", ACC, 1.5, m="acc")
d.chip((x1c + x4c) / 2, ry, "반복", ACC, 12)

d.legend(440, [("수집과 트리거", INFO), ("비교", ACC), ("차이 발견", WARN), ("적용", OK), ("1회성 끝점", SOFT)])
d.save("01-01.event-vs-pull.svg")
