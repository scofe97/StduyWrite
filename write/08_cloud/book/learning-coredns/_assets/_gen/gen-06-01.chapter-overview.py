# 06-01 학습 목표 뒤 전체 지도 — 절 여덟을 읽는 순서로 잇는다.
# 타입 스펙: type-process — 절마다 같은 의미 슬롯(번호 · 이름 · 한 줄)이 반복되고 화살표가 읽는 순서를 나른다.
#           축약: 주체(lane)가 없는 단계 지도라 카드 격자 stride 로 놓는다(같은 폴더 관례).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 744
d = D(W, H, "LEARNING COREDNS · 06-01",
      "무엇을 선언했느냐가 레코드 모양을 정한다",
      "6장 전반부의 절 여덟을 읽는 순서로 이은 지도. 1~3절이 쿠버네티스 쪽 사전 지식이고, "
      "4~8절이 그 위에 얹힌 DNS 명세다.",
      "4절의 한 필드가 이 편 전체의 갈림길입니다")

CW, CH, GAP, X0 = 400, 104, 20, 20
ROWS = [104, 232, 360, 488]
cards = [
    ("§1", "왜 하필 쿠버네티스가 먼저였나", "kube-dns 가 SkyDNS 기반이었다"),
    ("§2", "선언한 상태를 누가 지키는가", "조정 루프와 watch"),
    ("§3", "파드 IP 를 그대로 못 준다", "그래서 Service 자원이 있다"),
    ("§4", "clusterIP 한 필드의 갈림길", "부하 분산을 노드에서? 클라이언트에서?"),
    ("§5", "명세가 이름을 못 박아 둔다", "준수 조건이라 안 지킬 수 없다"),
    ("§6", "SRV 는 포트 이름을 요구한다", "이름 없는 포트는 SRV 가 없다"),
    ("§7", "이름이 살아남으려면 StatefulSet", "Deployment 는 이름이 하나로 뭉친다"),
    ("§8", "파드 A 레코드는 폐기됐다", "존재 확인을 안 해서 신원이 샌다"),
]


def pos(i):
    return X0 + (i % 2) * (CW + GAP), ROWS[i // 2]


for i in range(len(cards) - 1):
    x1, y1 = pos(i)
    x2, y2 = pos(i + 1)
    if y1 == y2:
        d.arrow([(x1 + CW, y1 + CH / 2), (x2 - 2, y2 + CH / 2)], MUTED, "ar", 1.4)
    else:
        bus = y1 + CH + 12
        d.path(f"M {x1 + CW / 2} {y1 + CH} L {x1 + CW / 2} {bus} L {x2 + CW / 2} {bus} L {x2 + CW / 2} {y2 - 2}",
               MUTED, 1.4, m="ar")

for i, (n, title, q) in enumerate(cards):
    x, y = pos(i)
    focal = (i == 3)
    if focal:
        d.tone(x, y, CW, CH, ACC, 8, "12", 1.4)
    else:
        d.box(x, y, CW, CH, PAPER2, RULE, 1.0, 8)
    d.t(x + 18, y + 26, n, 12, ACC if focal else SOFT, MONO, "start", 600)
    d.t(x + 18, y + 56, title, 16, ACC if focal else INK, KR, "start", 600)
    d.t(x + 18, y + 84, q, 13, MUTED, KR, "start")

d.t(20, 632, "1절부터 3절까지가 \"쿠버네티스는 어떻게 생겼나\"이고, 4절부터가 \"그래서 이름이 어떻게 나오나\"다", 13, MUTED, KR, "start")
d.t(20, 656, "8절은 명세가 스스로 걷어낸 규칙 하나를 보고 다음 편으로 넘긴다", 13, MUTED, KR, "start")

d.legend(684, [("한 필드가 전부를 가르는 절", ACC)])
d.save("06-01.chapter-overview.svg")
