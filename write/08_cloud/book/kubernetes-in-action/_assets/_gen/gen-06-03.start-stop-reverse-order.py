# 06-03 §7 — 시작과 종료는 서로 역순이다
# 본문 실측 로그(--timestamps 정렬):
#   05:22:17 sidecar STARTED · 05:22:19 main-a STARTED · 05:22:20 main-b STARTED
#   05:22:45 main-a PRE-STOP · :46 main-b SIGTERM · :47 main-a SIGTERM · :48 sidecar SIGTERM
# "main-a 와 main-b 의 1초 차이는 kubelet 의 생성 시차일 뿐이며, 이 관찰만으로 병렬성이나
#  시작 순서를 보장할 수 없습니다."
# 타입 스펙: type-timeline.md — 사건이 시간축 위에 있고 간격이 같지 않다. 관례대로 간격을
#           초에 비례해 두고(1초 = 200px) 사이드카는 milestone 으로 크게 찍는다.
#           역순 자체가 요점이므로 두 축의 사이드카를 잇는 선을 직각으로 가로질러 놓는다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO
import ddx

W, H = 1000, 632
d = D(W, H, "KUBERNETES IN ACTION · 06-03",
      "사이드카는 맨 먼저 뜨고 맨 나중에 죽는다",
      "네이티브 사이드카는 주 컨테이너보다 먼저 시작하고, 주 컨테이너가 전부 종료된 뒤에 "
      "종료된다. 주 컨테이너끼리의 1~2초 차이는 kubelet 의 생성 시차일 뿐 순서 보장이 아니다.",
      lead="이 순서 보장은 initContainers + restartPolicy: Always 에만 적용된다")

SEC0, PITCH = 180, 200          # 1초 = 200px — 간격을 초에 비례해 둔다
def x_of(sec_offset):
    return SEC0 + sec_offset * PITCH

UP, DOWN = 274, 452             # 두 축의 기준선
LINK_Y = 364

ddx.band(d, 104, 576, "일반 containers 에 둔 사이드카는 주 컨테이너와 동급이라 이 순서를 보장받지 못한다")

def track(base_y, label, events, span):
    d.t(40, base_y - 62, label, 12, SOFT, KR, "start", 600)
    d.line(140, base_y, 900, base_y, RULE, 1.0)
    for off, name, stamp, focal in events:
        x = x_of(off)
        r = 6 if focal else 4
        c = ACC if focal else MUTED
        d.o.append(f'<circle cx="{x}" cy="{base_y}" r="{r}" fill="{c}"/>')
        d.t(x, base_y - 32, name, 12, c, MONO, "middle", 600)
        d.t(x, base_y - 14, stamp, 10, SOFT, MONO)
    a, b = span
    d.path(f"M {x_of(a)} {base_y+16} L {x_of(a)} {base_y+28} L {x_of(b)} {base_y+28} "
           f"L {x_of(b)} {base_y+16}", MUTED, 1.2)
    d.t((x_of(a) + x_of(b)) // 2, base_y + 48, "주 컨테이너끼리는 병렬 — 순서 보장 없음",
        11, MUTED, KR)

track(UP, "▶ 시작", [(0, "sidecar", "05:22:17", True),
                     (2, "main-a", "05:22:19", False),
                     (3, "main-b", "05:22:20", False)], (2, 3))
track(DOWN, "■ 종료", [(0, "main-a", "05:22:45 preStop", False),
                       (1, "main-b", "05:22:46 SIGTERM", False),
                       (2, "main-a", "05:22:47 SIGTERM", False),
                       (3, "sidecar", "05:22:48 SIGTERM", True)], (0, 2))

# 역순 — 같은 사이드카가 한쪽 끝에서 반대쪽 끝으로 간다
d.path(f"M {x_of(0)} {UP+16} L {x_of(0)} {LINK_Y} L {x_of(3)} {LINK_Y} L {x_of(3)} {DOWN-46}",
       ACC, 1.5, m="acc", dash="6 5")
d.chip((x_of(0) + x_of(3)) // 2, LINK_Y, "같은 사이드카 — 맨 앞에서 맨 뒤로", ACC, 11)

d.t(36, 528, "main-a 의 preStop 이 SIGTERM 을 2초 미뤘고(45 → 47), 그 뒤에야 사이드카가 "
             "SIGTERM 을 받았다.", 12, MUTED, KR, "start")
d.t(36, 548, "사이드카는 주 컨테이너가 다 죽을 때까지 곁을 지킨다 — 로깅·프록시가 그래야 하는 "
             "부가 기능이기 때문이다.", 12, MUTED, KR, "start")
d.legend(592, [("사이드카 — 순서가 보장되는 자리", ACC)])
d.save("06-03-start-stop-reverse-order.svg")
print("ok start-stop-reverse-order")
