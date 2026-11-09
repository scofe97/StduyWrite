# 10-01 §5 — Many 가 되려면 스토리지 쪽이 받쳐 줘야 한다
# access mode 는 요구일 뿐이고 실제로 되느냐는 밑바탕 스토리지가 정한다. 그러니 모드 이름이
# 아니라 그것을 가능하게 하는 기전이 그림의 중심이어야 한다.
# 타입 스펙: type-dp-security-matrix.md — 행은 모드 둘, 열은 요구 · 그것을 가능하게 하는 기전 · 실제 예다. 모드 이름이 아니라
#           기전 열이 판정 축이라는 것이 논지다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, MUTED, SOFT, PAPER2, KR, MONO
import ddx

d = D(920, 580, "KUBERNETES IN ACTION · 10-01",
      "Many 를 가능하게 하는 것은 스토리지 쪽이다",
      "access mode 는 요구를 적는 자리일 뿐이다. 여러 노드가 동시에 쓸 수 있느냐는 밑바탕 스토리지가 "
      "그런 접근을 지원하느냐에 달렸다.",
      "블록 스토리지는 대개 Many 를 못 준다")

def row(y0, label, mode, submode, how, examples, c, focal):
    ddx.band(d, y0, y0 + 172, label, x=20, w=880, focal=focal, bar=ACC if focal else None)
    ddx.node(d, 135, y0 + 94, mode, submode, 170, 76, c)
    d.box(280, y0 + 49, 380, 90, PAPER2, c, 1.1, 6)
    d.t(470, y0 + 82, how[0], 13, c, KR, "middle", 600)
    d.t(470, y0 + 108, how[1], 12, MUTED, KR)
    d.path(f"M 225 {y0+94} L 275 {y0+94}", c, 1.4, m="ok" if c is OK else "acc")
    d.box(675, y0 + 49, 215, 90, PAPER2, SOFT, 0.8, 6)
    d.t(782, y0 + 82, examples[0], 12, SOFT, KR)
    d.t(782, y0 + 108, examples[1], 12, SOFT, KR)

row(96, "ReadWriteMany", "RWX", "요구",
    ("파일 스토리지가 동시 쓰기를 받아 준다", "잠금과 일관성을 스토리지가 맡는다"),
    ("NFS · CephFS · EFS", "블록 스토리지로는 대개 안 된다"), OK, False)

row(284, "ReadOnlyMany", "ROX", "요구",
    ("같은 내용을 여러 곳에서 읽기만 한다", "access mode 가 쓰기를 막지는 않는다"),
    ("dataSourceRef 로 복제해", "각자 자기 볼륨을 쓰는 길도 있다"), ACC, True)

d.t(24, 484, "RWX 를 적어도 지원 안 하는 스토리지의 PVC 는 Pending", 12, MUTED, KR, "start")
d.t(24, 508, "읽기만 여럿 필요: ROX 대신 dataSourceRef 로 볼륨 복제", 12, MUTED, KR, "start")
d.legend(532, [("동시 쓰기", OK), ("읽기 전용 · 복제", ACC)])
d.save("10-01-rwx-rox-mechanism.svg")
print("ok")
