# 10-03 §2 — PVC·PV 와 같은 짝 구조를 한 층 더
# 오브젝트 넷을 나열하면 외울 것이 넷이 된다. 이미 아는 PVC·PV 짝과 대응시키면 하나만
# 새로 배우면 되므로, 그 대응이 그림의 뼈대여야 한다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO
import ddx

d = D(1220, 620, "KUBERNETES IN ACTION · 10-03",
      "이미 아는 짝 구조가 한 층 더 있을 뿐",
      "VolumeSnapshot 은 PVC 자리에, VolumeSnapshotContent 는 PV 자리에 대응한다. "
      "요구하는 오브젝트와 실체를 가리키는 오브젝트로 갈리는 모양이 같다.",
      "새로 배울 것은 클래스 하나와 dataSource 하나")

def pair(y0, label, req, real, cls, c, focal):
    ddx.band(d, y0, y0 + 184, label, x=24, w=1172, focal=focal, bar=ACC if focal else None)
    ddx.node(d, 240, y0 + 104, req[0], req[1], 300, 84, c)
    ddx.node(d, 700, y0 + 104, real[0], real[1], 340, 84, c)
    d.path(f"M 392 {y0+104} L 528 {y0+104}", c, 1.4, m="ok" if c is OK else "acc")
    d.t(460, y0 + 84, "바인딩", 10, SOFT, KR)
    d.t(1030, y0 + 96, cls[0], 11, SOFT, KR)
    d.t(1030, y0 + 118, cls[1], 11, SOFT, KR)

pair(100, "이미 아는 것", ("PVC", "얼마나 · 어떻게 쓸지"), ("PV", "만들어진 볼륨"),
     ("StorageClass 가", "만드는 방법을 정한다"), OK, False)
pair(308, "스냅샷도 같은 모양", ("VolumeSnapshot", "어느 PVC 를 찍을지"),
     ("VolumeSnapshotContent", "실제로 찍힌 스냅샷"),
     ("VolumeSnapshotClass 가", "만드는 방법을 정한다"), ACC, True)

d.t(24, 536, "복원은 반대 방향이다 — 새 PVC 의 dataSource 에 VolumeSnapshot 을 적으면 그 스냅샷에서 "
             "볼륨이 만들어진다.", 11, MUTED, KR, "start")
d.t(24, 558, "스냅샷 기능은 CSI 드라이버가 지원해야 쓸 수 있고, 별도의 snapshot controller 설치가 필요하다.",
     11, MUTED, KR, "start")
d.legend(584, [("아는 짝", OK), ("같은 모양의 새 짝", ACC)])
d.save("10-03-volumesnapshot-objects.svg")
print("ok")
