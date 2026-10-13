# 타입 스펙: type-flowchart — 색인 크기에서 시작해 두 판단(한 서버 메모리에 들어가나·읽기가 한 서버를 넘나)을 거쳐 읽기 복제본으로 가는 판단 흐름. 초점은 읽기 복제본 추가.
# 사실 출처: 추출본 v1.txt 3860~3890행(쿼드트리 색인 1.71G 메모리, 지오해시 색인의 저장 요구도 비슷, 전체가 현대 DB 서버의 작업 집합에 들어감, 읽기량에 따라 한 서버의 CPU·네트워크가 모자랄 수 있음,
#   읽기 부하를 퍼뜨리는 방법은 읽기 복제본 추가와 샤딩, 샤딩은 복잡하고 애플리케이션 계층에 로직이 필요, 이 경우 샤딩할 강한 기술 이유가 없어 복제본 권고).
# Layout conventions: 타원 폭 220·높이 40(rx 20), 마름모 폭 320·높이 88, 사각형 높이 52, 층 간격 44, 예 는 아래·아니오 는 오른쪽, 모든 갈래에 라벨. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 960, 584
d = D(W, H, "BYTEBYTEGO · 09-01 §6",
      "색인 크기가 정해 주는 순서: 메모리에 들어가면 복제본이다",
      "1.71 GB 색인은 한 서버의 작업 집합에 들어가므로 모자란 것은 읽기 처리량뿐이고, 읽기 복제본이 그 부하를 퍼뜨립니다.",
      "1.71 GB 는 쿼드트리 색인 크기에 대한 설계 가정이고 지오해시 색인도 비슷합니다")


def fam(s):
    return KR if any("가" <= ch <= "힣" for ch in s) else MONO


def diamond(cx, cy, w, h, text):
    pts = f"{cx},{cy - h / 2} {cx + w / 2},{cy} {cx},{cy + h / 2} {cx - w / 2},{cy}"
    d.o.append(f'<polygon points="{pts}" fill="{INFO}14" stroke="{INFO}" stroke-width="1.2"/>')
    d.t(cx, cy + 5, text, 13, INK, fam(text), "middle", 600)


def rect(cx, y, w, h, title, sub=None, focal=False):
    x = cx - w / 2
    if focal:
        d.tone(x, y, w, h, ACC, 6, "14", 1.4)
    else:
        d.box(x, y, w, h, PAPER2, RULE, 0.9, 6)
    col = ACC if focal else INK
    if sub:
        d.t(cx, y + 22, title, 13, col, fam(title), "middle", 600)
        d.t(cx, y + 42, sub, 12, MUTED, fam(sub), "middle")
    else:
        d.t(cx, y + h / 2 + 5, title, 13, col, fam(title), "middle", 600)


MX, RX = 360, 724
D1, D2, END = 208, 340, 444
# 화살표 먼저.
d.arrow([(MX, 140), (MX, D1 - 44)], MUTED, "ar", 1.4)
d.arrow([(MX, D1 + 44), (MX, D2 - 44)], MUTED, "ar", 1.4)
d.arrow([(MX, D2 + 44), (MX, END)], ACC, "acc", 1.4)
d.arrow([(MX + 160, D1), (RX - 112, D1)], MUTED, "ar", 1.4)
d.arrow([(MX + 160, D2), (RX - 112, D2)], MUTED, "ar", 1.4)

# 노드.
d.tone(MX - 110, 100, 220, 40, INFO, 20, "14", 1.2)
d.t(MX, 125, "쿼드트리 색인 1.71 GB", 13, INK, KR, "middle", 600)
diamond(MX, D1, 320, 88, "한 서버 메모리에 들어가나?")
diamond(MX, D2, 320, 88, "읽기가 한 서버를 넘나?")
rect(MX, END, 240, 52, "읽기 복제본 추가", "쓰기는 주 DB 한 곳", focal=True)
rect(RX, D1 - 26, 224, 52, "샤딩 검토", "색인이 한 서버를 넘을 때")
rect(RX, D2 - 26, 224, 52, "서버 한 대", "읽기 확장 불필요")

d.chip(MX, (D1 + 44 + D2 - 44) / 2, "예", OK, 12)
d.chip(MX, (D2 + 44 + END) / 2, "예", OK, 12)
d.chip((MX + 160 + RX - 112) / 2, D1, "아니오", WARN, 12)
d.chip((MX + 160 + RX - 112) / 2, D2, "아니오", WARN, 12)

d.legend(H - 48, [("고르는 답", ACC), ("판단", INFO), ("예", OK), ("아니오", WARN)])
d.save("09-01.size-decision.svg")
