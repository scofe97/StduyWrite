# 11-03 §2 — 커널에 컨테이너는 없다. namespace 와 cgroup 을 유저 공간이 묶은 것이다.
# 타입 스펙: type-process — 두 재료가 각각 무엇을 맡고 어떻게 합쳐지는지의 조립 지도다.
#           축약: 주체(lane)가 없는 조립 지도라 §1 lanes 와 §2 공식을 쓰지 않고 카드 stride 로 놓는다
#           (visual-diagram-selection §알려진 공백 "주체 없는 단계 지도" 관례).
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 928, 540
CW, CH, GAP, X0, Y = 424, 224, 32, 24, 128

d = DK(W, H, "SYSTEMS PERFORMANCE · 11-03 §2",
       "컨테이너 = namespace + cgroup",
       "Linux 커널에는 컨테이너라는 개념이 없다. namespace 가 보이는 것을 가리고 cgroup 이 쓸 수 있는 양을 막으며, 유저 공간 소프트웨어가 둘을 묶어 컨테이너라 부른다.",
       "커널에 통일된 컨테이너 ID 가 없다는 점이 관측을 어렵게 만듭니다")

CARDS = [
    ("namespace", "격리 — 무엇이 보이는가", INFO,
     ["시스템 뷰를 필터링해 자기 자원만", "보게 합니다.", "", "pid · net · mnt · ipc · uts", "user · cgroup · time"],
     "컨테이너마다 PID 1 이 따로 있습니다"),
    ("cgroup", "제한 — 얼마나 쓰는가", ACC,
     ["자원 사용량에 한계를 겁니다.", "", "cpu · cpuset · memory", "blkio · pids", "net_cls · net_prio"],
     "하드 한계와 공유 기반 소프트 한계"),
]

for i, (name, tag, c, body, foot) in enumerate(CARDS):
    x = X0 + i * (CW + GAP)
    if c is ACC: d.tone(x, Y, CW, CH, c, 8)
    else: d.box(x, Y, CW, CH, PAPER2, RULE, 1.0, 8)
    d.t(x + 16, Y + 30, name, 15, c, KR, "start", 600)
    d.t(x + 16, Y + 52, tag, 13, MUTED, KR, "start")
    d.line(x + 16, Y + 66, x + CW - 16, Y + 66, RULE, 0.8)
    for j, line in enumerate(body):
        if line:
            fam = MONO if "·" in line and not any('가' <= ch <= '힣' for ch in line) else KR
            d.t(x + 16, Y + 90 + j * 20, line, 13, MUTED, fam, "start")
    d.t(x + 16, Y + CH - 18, foot, 13, c, KR, "start")

YB = Y + CH + 40
d.t(X0, YB, "유저 공간 소프트웨어(Docker 등)가 이 둘을 조합해 컨테이너를 만듭니다", 13, MUTED, KR, "start")
d.t(X0, YB + 24, "Kubernetes 는 여러 컨테이너가 같은 namespace 를 공유하는 Pod 로 묶어 localhost 통신을 가능하게 합니다",
    13, SOFT, KR, "start")

d.legend(YB + 48, [("쓸 수 있는 양을 막는 쪽", ACC), ("보이는 것을 가리는 쪽", INFO)])
d.save("11-03.container-namespace-cgroup.svg")
