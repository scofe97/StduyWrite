# 02-04.two-tables — 목적지가 달라지면 어느 값이 달라지는가
# 본문 요구: §1 "MAC 은 홉마다 바뀌고 IP 는 끝까지 안 바뀝니다. 8.8.8.8 은 ip neigh 에
#           결코 나타나지 않습니다." 그리고 via 유무가 그 갈림을 정한다는 것.
# 타입 스펙: type-dp-security-matrix.md 의 값 대조 행 — 같은 단계를 두 목적지에 대해
#           나란히 놓고 어느 칸에서 값이 갈리는지 보인다. focal 열은 '찾는 MAC'.
#           data-flow 를 먼저 검토했으나 그 타입은 조직 역할별 파이프라인 전용이라 제외.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 524
d = D(W, H, "TWO TABLES · WHICH VALUE DIFFERS",
      "목적지가 바뀌면 MAC 이 바뀌고 IP 는 그대로다",
      "같은 인터페이스로 나가는 두 패킷이라도 목적지가 같은 링크에 있느냐에 따라 프레임에 적히는 "
      "MAC 이 달라집니다. IP 헤더의 목적지는 어느 경우에도 바뀌지 않습니다.",
      lead="라우팅이 다음 홉을 고르고, 이웃 테이블이 그것을 MAC 으로 번역한다")

COLS = [(180, "목적지"), (260, "걸리는 라우팅 줄"), (190, "찾는 MAC"), (240, "프레임에 적히는 것")]
ROWS = [([("192.168.139.238",),
          ("192.168.139.0/24", "via 없음 · scope link"),
          ("4a:05:d5:90:02:20", "목적지 자신의 것"),
          ("dst MAC = 목적지", "IP = 192.168.139.238")], OK),
        ([("8.8.8.8",),
          ("default via 192.168.139.1", "via 있음 · 다음 홉"),
          ("da:9b:d0:54:e0:02", "게이트웨이의 것"),
          ("dst MAC = 게이트웨이", "IP = 8.8.8.8 그대로")], INFO)]

ddx.matrix(d, 40, COLS, ROWS, hdr_y=192, row_h=88, gap=12, focal_col=2)

d.t(40, 432, "진하게 칠한 세 번째 칸이 두 행에서 갈리는 유일한 자리입니다. 네 번째 칸의 IP 는 두 경우 다 목적지 그대로입니다.",
    12, MUTED, KR, "start")
d.t(40, 454, "8.8.8.8 은 같은 링크에 없으므로 ip neigh 에 결코 나타나지 않습니다 — 물어볼 상대가 없습니다.",
    12, MUTED, KR, "start")
d.legend(470, [("같은 링크 — 직접", OK), ("다른 네트워크 — 게이트웨이 경유", INFO)])
d.save("02-04.two-tables.svg")
print("ok two-tables")
