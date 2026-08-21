# 16-01 §MySQL 싱글턴 랩
# 다섯 상자를 잇는 레시피로 그리면 본문의 요점이 통째로 빠진다. 본문이 힘주어 답하는 것은
# 순서가 아니라 "왜 이 두 단계가 더 있는가" 다 — PVC 한 단계와, 파드 하나짜리 ReplicaSet.
# 그래서 둘을 "없으면 무슨 일이 나는가" 로 아래에 달아 두고 사슬은 뼈대만 남긴다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, PAPER, RULE, KR, MONO
import ddx

W, H = 1240, 576
d = D(W, H, "KUBERNETES UP AND RUNNING · 16-01",
      "군더더기로 보이는 두 단계에 이유가 있다",
      "NFS 를 가리키는 PersistentVolume 에서 시작해 Service 로 노출하기까지, 복제 없는 MySQL "
      "하나를 세우는 완결 레시피다.",
      "화살표는 데이터가 흐르는 방향이 아니라 만드는 순서다")

CY = 240
d.box(24, 185, 210, 110, PAPER2, RULE, 1.1, 6)
d.t(129, 222, "PersistentVolume", 12, INK, KR, "middle", 600)
d.t(129, 244, "nfs · 192.168.0.1", 10, SOFT, MONO)
d.t(129, 262, "1Gi · ReadWriteMany", 10, SOFT, MONO)
d.t(129, 280, "labels: volume=my-volume", 9, SOFT, MONO)

d.box(321, 185, 210, 110, PAPER2, RULE, 1.1, 6)
d.t(426, 222, "PersistentVolumeClaim", 12, INK, KR, "middle", 600)
d.t(426, 244, "requests 1Gi", 10, SOFT, MONO)
d.t(426, 268, "selector 로 위 볼륨을 찾는다", 10, SOFT, KR)

d.box(618, 160, 300, 170, PAPER, RULE, 1.0, 8)
d.t(768, 182, "ReplicaSet · replicas 1", 11, SOFT, KR)
d.box(638, 196, 260, 118, PAPER2, RULE, 1.1, 6)
d.t(768, 222, "파드 — image: mysql", 12, INK, KR, "middle", 600)
d.t(768, 246, "livenessProbe · tcpSocket 3306", 10, SOFT, MONO)
d.t(768, 268, "mountPath /var/lib/mysql", 10, SOFT, MONO)
d.t(768, 292, "라벨 app: mysql", 10, SOFT, KR)

d.box(1005, 185, 210, 110, PAPER2, RULE, 1.1, 6)
d.t(1110, 222, "Service", 12, INK, KR, "middle", 600)
d.t(1110, 246, "port 3306", 10, SOFT, MONO)
d.t(1110, 270, "이름으로 부른다", 10, SOFT, KR)

for x0, x1, chip in ((234, 317, "volume 라벨"), (531, 614, "claimName"), (918, 1001, "app 라벨")):
    d.path(f"M {x0} {CY} L {x1} {CY}", MUTED, 1.5, m="ar")
    d.chip((x0 + x1) / 2, CY - 24, chip, SOFT)

def why(x, w, y0, y1, anchor_x, anchor_y, title, lines):
    d.o.append(f'<rect x="{x}" y="{y0}" width="{w}" height="{y1-y0}" rx="8" '
               f'fill="{ACC}0A" stroke="{ACC}" stroke-width="1.3"/>')
    d.line(anchor_x, anchor_y, anchor_x, y0, ACC, 1.2, "5 4")
    d.t(x + 22, y0 + 28, title, 13, ACC, KR, "start", 600)
    for i, ln in enumerate(lines):
        d.t(x + 22, y0 + 52 + i * 21, ln, 11, MUTED, KR, "start")

why(24, 580, 366, 462, 426, 295, "PVC 라는 한 단계를 왜 더 두는가",
    ["볼륨을 파드 명세 안에 직접 선언할 수도 있다.",
     "그러면 그 명세가 특정 볼륨 제공자에 묶인다.",
     "청구를 거치면 파드 명세가 클라우드에 중립으로 남는다."])
why(636, 580, 366, 462, 768, 330, "파드 하나에 왜 ReplicaSet 인가",
    ["한 번 머신에 스케줄된 맨 파드는 그 머신에 영원히 묶인다.",
     "머신이 죽으면 상위 컨트롤러가 없는 파드는 함께 사라지고",
     "다른 곳에 다시 스케줄되지 않는다."])

d.t(24, 490, "원서는 이 ReplicaSet 의 apiVersion 을 extensions/v1 로 적는다. 그런 버전은 존재한 적이 없고 현행은 apps/v1 이다 — 그대로 적용하면 실패한다.",
     11, MUTED, KR, "start")
d.t(24, 512, "비밀번호를 환경 변수로 넣은 것은 예제를 짧게 하려는 것이지 보안 모범 사례가 아니라고 책이 직접 적어 둔다.",
     11, MUTED, KR, "start")

d.legend(528, [("군더더기로 보이지만 이유가 있는 단계", ACC)])
d.save("16-01.mysql-singleton-lab.svg")
print("h 필요:", 528 + 48, " 실제:", H)
