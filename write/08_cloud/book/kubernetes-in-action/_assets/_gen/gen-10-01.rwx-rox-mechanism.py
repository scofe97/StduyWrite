# 10-01 §5 — Many 가 되려면 스토리지 쪽이 받쳐 줘야 한다
# access mode 는 요구일 뿐이고 실제로 되느냐는 밑바탕 스토리지가 정한다. 그러니 모드 이름이
# 아니라 그것을 가능하게 하는 기전이 그림의 중심이어야 한다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, WARN, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO
import ddx

d = D(1240, 688, "KUBERNETES IN ACTION · 10-01",
      "Many 를 가능하게 하는 것은 스토리지 쪽이다",
      "access mode 는 요구를 적는 자리일 뿐이다. 여러 노드가 동시에 쓸 수 있느냐는 밑바탕 스토리지가 "
      "그런 접근을 지원하느냐에 달렸다.",
      "블록 스토리지는 대개 Many 를 못 준다")

def row(y0, label, mode, how, examples, c, focal):
    ddx.band(d, y0, y0 + 216, label, x=24, w=1172, focal=focal, bar=ACC if focal else None)
    ddx.node(d, 190, y0 + 116, mode, "요구", 220, 76, c)
    d.box(400, y0 + 66, 460, 100, PAPER2, c, 1.1, 6)
    d.t(630, y0 + 100, how[0], 12, c, KR, "middle", 600)
    d.t(630, y0 + 126, how[1], 11, MUTED, KR)
    d.path(f"M 302 {y0+116} L 392 {y0+116}", c, 1.4, m="ok" if c is OK else "acc")
    d.t(1020, y0 + 106, examples[0], 11, SOFT, KR)
    d.t(1020, y0 + 128, examples[1], 11, SOFT, KR)

row(100, "ReadWriteMany", "RWX", ("파일 스토리지가 동시 쓰기를 받아 준다", "잠금과 일관성을 스토리지가 맡는다"),
    ("NFS · CephFS · EFS", "블록 스토리지로는 안 된다"), OK, False)
row(340, "ReadOnlyMany", "ROX", ("같은 내용을 여러 곳에서 읽기만 한다", "쓰기가 없어 충돌이 없다"),
    ("dataSourceRef 로 복제해", "각자 자기 볼륨을 쓰는 길도 있다"), ACC, True)

d.t(24, 596, "그래서 RWX 를 적었다고 되는 것이 아니다. 프로비저닝하는 스토리지가 그 모드를 지원하지 않으면 "
             "PVC 가 Pending 에 머문다.", 11, MUTED, KR, "start")
d.t(24, 618, "읽기만 여럿 필요하다면 ROX 대신 dataSourceRef 로 볼륨을 복제해 각자 쓰게 하는 편이 제약이 적다.",
     11, MUTED, KR, "start")
d.legend(640 - 4, [("동시 쓰기", OK), ("읽기만 · 복제", ACC)])
d.save("10-01-rwx-rox-mechanism.svg")
print("ok")
