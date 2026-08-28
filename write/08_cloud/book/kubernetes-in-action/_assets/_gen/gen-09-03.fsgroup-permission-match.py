# 09-03 §4 — 두 곳을 동시에 손대야 칸이 맞는다
# 본문이 "fsGroup 은 두 가지를 동시에 한다"고 못박고 실측(groups 1000 → 1000,2000)을 든다.
# 그러니 파일 쪽과 프로세스 쪽을 나란히 놓고, 맞물리는 칸이 어디인지가 보여야 한다.
# 타입 스펙: type-dp-security-matrix.md — 행은 fsGroup 유무 두 경우, 열은 볼륨 파일 쪽 · 프로세스 쪽 · 판정이다. 두 칸의 그룹 값이
#           맞물리는지가 판정 열을 정한다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, BAD, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO
import ddx

d = D(1240, 700, "KUBERNETES IN ACTION · 09-03",
      "파일 쪽과 프로세스 쪽을 동시에 손댄다",
      "fsGroup 은 볼륨 파일의 그룹 소유권을 지정 gid 로 바꾸고, 동시에 프로세스를 그 gid 의 보충 그룹 "
      "멤버로 넣는다. 두 쪽이 같이 움직여야 그룹 칸 매칭이 성립한다.",
      "kind 실측 — groups 1000 → 1000,2000 · 파일 그룹 root → 2000")

def scene(y0, label, fgroup, pgroups, verdict, c):
    ddx.band(d, y0, y0 + 216, label, x=24, w=1172)
    d.box(80, y0 + 64, 420, 108, PAPER, RULE, 0.9, 8)
    d.t(290, y0 + 90, "볼륨 파일", 11, SOFT, KR)
    d.t(110, y0 + 126, "-rw-r-----", 12, MUTED, MONO, "start")
    d.t(280, y0 + 126, f"root  {fgroup}", 12, c, MONO, "start")
    d.t(110, y0 + 152, "그룹만 읽을 수 있다", 10, SOFT, KR, "start")

    d.box(560, y0 + 64, 420, 108, PAPER, RULE, 0.9, 8)
    d.t(770, y0 + 90, "envoy 프로세스", 11, SOFT, KR)
    d.t(590, y0 + 126, "uid 1000", 12, MUTED, MONO, "start")
    d.t(740, y0 + 126, f"groups {pgroups}", 12, c, MONO, "start")
    d.t(590, y0 + 152, "이 목록에 파일 그룹이 있어야 읽는다", 10, SOFT, KR, "start")

    d.path(f"M 504 {y0+118} L 556 {y0+118}", c, 1.4,
           m="bad" if c is BAD else "acc", dash="5 5" if c is BAD else None)
    ddx.tag(d, 1090, y0 + 118, verdict, c, 170)

scene(100, "fsGroup 이 없을 때", "root", "1000", "읽지 못한다", BAD)
scene(340, "fsGroup: 2000 을 주면", "2000", "1000,2000", "읽는다", ACC)

d.t(24, 596, "이름이 비슷한 필드와 방향을 헷갈리지 않는 게 중요하다. runAsUser·runAsGroup 은 프로세스의 신분을 정하고, "
             "fsGroup 은 파일의 그룹 소유권을 정한다.", 11, MUTED, KR, "start")
d.t(24, 618, "그리고 fsGroup 은 파일의 사용자 소유권은 바꾸지 못한다 — 그룹 소유권만 바꾼다.", 11, MUTED, KR, "start")
d.legend(644, [("칸이 안 맞는다", BAD), ("맞물린다", ACC)])
d.save("09-03-fsgroup-permission-match.svg")
print("ok")
