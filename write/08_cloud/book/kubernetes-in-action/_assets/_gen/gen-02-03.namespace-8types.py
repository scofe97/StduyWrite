# 02-03 §네임스페이스 8종류 — 각자 다른 자원을 격리한다
# 본문·실측: mnt·pid·net·ipc·uts·cgroup 은 Docker 기본이 격리, user·time 은 기본 공유.
#   pid → 안에서 1번부터 새로 셈(node = 안:1 / 밖:32687), uts → 호스트명이 컨테이너 ID,
#   user → 안 root 가 호스트 root 라 보안이 약해진다, time → 시계 공유.
# 타입 스펙: type-dp-security-matrix.md — 여덟 개를 한 축으로 세우면 행이 여덟이라 세로로 길어지고, 두 줄짜리 셀은
#           행 높이가 76px 아래로 못 내려간다. 대신 카드 격자로 두어 격리 여섯과 공유 둘이
#           한 화면에서 갈리게 했다 — 개수를 세는 것이 이 그림의 일이다.
#           여덟 종류를 같은 슬롯(이름 · 격리 여부 · 무엇을 · 결과)으로 4×2 격자에 늘어놓았다.
#           칸 사이에 순서가 없고 격리 여섯과 공유 둘을 세는 것이 이 그림의 일이다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO
import ddx

W, H = 1000, 640
d = D(W, H, "KUBERNETES IN ACTION · 02-03",
      "여덟 종류 중 여섯이 격리되고 둘은 호스트와 공유된다",
      "컨테이너는 무언가에 감싸인 것이 아니라, 이 네임스페이스들이 동시에 배정된 프로세스다. "
      "격리 여부가 종류마다 다르므로 경계가 딱 떨어지지 않는다.",
      lead="Docker 기본값 기준이다 — user 를 안 나누므로 안의 root 가 호스트 root 다")

CARD_W, CARD_H, GX, GY = 222, 148, 16, 16
X0, Y0 = 32, 216

ddx.band(d, 104, 584, "격리 여부는 종류마다 다르다 — 그래서 '컨테이너 경계' 가 한 줄로 그어지지 않는다")

CARDS = [
    ("mnt", "파일시스템·마운트 지점", "자기만의 루트(/) 를 본다", INFO),
    ("pid", "프로세스 번호", "안에서 1번부터 새로 센다", INFO),
    ("net", "네트워크 장치·포트", "자기 eth0·IP·포트를 가진다", INFO),
    ("ipc", "프로세스 간 통신", "공유 메모리·큐가 갈린다", INFO),
    ("uts", "호스트명·도메인명", "호스트명이 컨테이너 ID 다", INFO),
    ("cgroup", "cgroup 루트 디렉터리", "자기 cgroup 트리만 본다", INFO),
    ("user", "사용자·그룹 ID", "안 root = 호스트 root", WARN),
    ("time", "시스템 클록 오프셋", "시계를 호스트와 함께 쓴다", WARN),
]
for i, (name, what, effect, c) in enumerate(CARDS):
    cx = X0 + (i % 4) * (CARD_W + GX)
    cy = Y0 + (i // 4) * (CARD_H + GY)
    d.box(cx, cy, CARD_W, CARD_H, PAPER2, c, 1.1, 6)
    d.t(cx + CARD_W // 2, cy + 34, name, 15, c, MONO, "middle", 600)
    d.chip(cx + CARD_W // 2, cy + 60, "격리" if c is INFO else "기본 공유", c, 10)
    d.t(cx + CARD_W // 2, cy + 96, ddx.fit(what, 11, CARD_W - 20, name), 11, MUTED, KR)
    d.t(cx + CARD_W // 2, cy + 122, ddx.fit(effect, 10, CARD_W - 16, name), 10, SOFT, KR)

d.t(36, 552, "직접 확인하려면 readlink /proc/1/ns/uts 를 두 컨테이너에서 비교한다 — "
             "번호가 다르면 격리, 같으면 공유다.", 12, MUTED, KR, "start")
d.legend(600, [("Docker 기본이 격리하는 것", INFO), ("호스트와 공유하는 것", WARN)])
d.save("02-03-namespace-8types.svg")
print("ok namespace-8types")
