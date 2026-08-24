# 02-03 §전체도 — 번호가 다르면 격리, 같으면 공유
# 실측: kiada 와 web1 의 uts·pid·net 번호는 다르고 user·time 번호는 같다.
#       cgroup: docker --memory=100m → memory.max = 104857600 에 박힌다(커널이 강제).
# 타입 스펙: 두 컨테이너의 같은 항목을 나란히 놓고 같은지 다른지를 판정하는 일이라 비교 행렬.
#           옛 판은 상자 안에 번호를 늘어놓아 '같다/다르다' 를 독자가 대조해야 했다.
#           판정 열을 만들어 그 대조를 그림이 대신한다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO
import ddx

W, H = 1000, 700
d = D(W, H, "KUBERNETES IN ACTION · 02-03",
      "번호가 다르면 격리, 같으면 공유다",
      "같은 커널 위에서 도는 두 컨테이너의 네임스페이스 번호를 나란히 놓으면 무엇이 갈리고 "
      "무엇이 겹치는지가 그대로 드러난다. 자원량은 별개 축이라 cgroup 이 따로 강제한다.",
      lead="컨테이너는 감싸인 것이 아니라 네임스페이스가 배정된 프로세스다")

ddx.band(d, 104, 644, "네임스페이스는 '무엇을 볼 수 있나', cgroup 은 '얼마나 쓸 수 있나' — 축이 둘이다")

ddx.matrix(
    d, x0=36, hdr_y=190, row_h=80, gap=10, focal_col=3,
    cols=[(200, "네임스페이스"), (250, "kiada (node app.js)"),
          (250, "web1 (nginx)"), (228, "판정")],
    rows=[
        ([("uts", "호스트명"), ("4026534383", ""), ("4026534113", ""),
          ("다르다 → 격리", "각자 호스트명을 본다")], INFO),
        ([("pid", "프로세스 번호"), ("4026534385", "안에선 PID 1"), ("4026534115", "안에선 PID 1"),
          ("다르다 → 격리", "각자 1번부터 센다")], INFO),
        ([("net", "네트워크·IP·포트"), ("4026534387", "자기 eth0"), ("4026534117", "자기 eth0"),
          ("다르다 → 격리", "같은 포트를 써도 된다")], INFO),
        ([("user", "UID/GID"), ("4026531837", ""), ("4026531837", ""),
          ("같다 → 공유", "Docker 기본은 안 나눈다")], WARN),
        ([("time", "시스템 시계"), ("4026531834", ""), ("4026531834", ""),
          ("같다 → 공유", "시계를 함께 쓴다")], WARN),
    ])

d.o.append(f'<rect x="36" y="562" width="928" height="60" rx="8" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(56, 588, "cgroup — 별개 축", 12, ACC, KR, "start", 600)
d.t(56, 608, "docker --memory=100m → memory.max = 104857600 에 박힌다. 표시가 아니라 커널이 "
             "강제하는 실제 한도다.", 10, SOFT, KR, "start")

d.legend(660, [("번호가 달라 격리되는 것", INFO), ("번호가 같아 공유되는 것", WARN),
               ("자원량을 정하는 다른 축", ACC)])
d.save("02-03-namespace-cgroup-overview.svg")
print("ok namespace-cgroup-overview")
