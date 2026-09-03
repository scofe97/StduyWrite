# 06-01 학습 목표 뒤 전체 지도 — 절 여덟을 읽는 순서로 잇는다.
# 본문: "칸마다 절 번호와 그 절이 답하는 질문 하나", "색이 붙은 칸이 같은 도구가 장애를 키우는 쪽으로 뒤집히는 자리".
# 타입 스펙: type-process — 절마다 같은 의미 슬롯(번호 · 이름 · 질문)이 반복되고 화살표가 읽는 순서를 나른다.
#           축약: 주체(lane)가 없는 단계 지도라 §1 lanes·§2 공식 대신 카드 한 줄 stride 로 놓는다(03~05 와 같은 관례).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

# 폭은 계약의 본문 삽입용 상한(880~1000) 안으로 두고, 4 열을 2 열로 접어 담는다.
# 계약: "넓은 캔버스에 담기지 않으면 폭을 늘리지 말고 배치를 바꾼다."
COLS, CW, CH, GAP, VGAP, X0, Y0 = 2, 396, 100, 16, 56, 36, 104
cards = [
    ("§1", "라이브러리가 남긴 것", "Finagle · Hystrix · Ribbon"),
    ("§2", "클라이언트가 고르는 엔드포인트", "세 알고리즘의 백분위"),
    ("§3", "가까운 곳부터 넘어간다", "이상치 감지가 전제"),
    ("§4", "가장 짧은 타임아웃이 이긴다", "느린 응답 → 빠른 실패"),
    ("§5", "재시도가 감추는 실패", "최대 3회 · 백오프 25ms"),
    ("§6", "재시도가 키우는 부하", "thundering herd"),
    ("§7", "커넥션 풀이 끊는 순간", "대기 큐가 끊는다"),
    ("§8", "아픈 엔드포인트를 뺀다", "n × baseEjectionTime"),
]
FOCAL = 5
ROWS = -(-len(cards) // COLS)
BOTTOM = Y0 + ROWS * (CH + VGAP) - VGAP
LEGY = BOTTOM + 48
W, H = 880, LEGY + 40

d = D(W, H, "ISTIO IN ACTION · 06-01",
      "실패를 견디는 일을 프록시로 옮겼을 때 — 읽는 순서",
      "6장 노트의 절 여덟을 읽는 순서로 이은 지도. 로드밸런싱·지역 인식·타임아웃·재시도·서킷 브레이킹이 차례로 나오고, §6 에서 같은 도구가 장애를 키우는 쪽으로 뒤집힌다.",
      "설정 하나하나가 새 관찰 대상을 만듭니다. §6 은 그 도구가 반대로 작동하는 자리")

def pos(i):
    r, c = divmod(i, COLS)
    return X0 + c * (CW + GAP), Y0 + r * (CH + VGAP)

for i in range(len(cards) - 1):
    x1, y1 = pos(i); x2, y2 = pos(i + 1)
    if y1 == y2:
        d.arrow([(x1 + CW, y1 + CH / 2), (x2 - 2, y2 + CH / 2)], MUTED, "ar", 1.4)
    else:
        my = y1 + CH + VGAP / 2
        d.path(f"M {x1 + CW / 2} {y1 + CH} L {x1 + CW / 2} {my} "
               f"L {x2 + CW / 2} {my} L {x2 + CW / 2} {y2 - 2}", MUTED, 1.4, m="ar")

for i, (num, title, q) in enumerate(cards):
    x, y = pos(i); focal = (i == FOCAL)
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{CW}" height="{CH}" rx="8" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y, CW, CH, PAPER2, RULE, 1.0, 8)
    d.t(x + 20, y + 28, num, 11, ACC if focal else SOFT, MONO, "start", 600)
    d.t(x + 20, y + 56, title, 14, ACC if focal else INK, KR, "start", 600)
    d.t(x + 20, y + 82, q, 12, MUTED, KR, "start")

d.legend(LEGY, [("도구가 반대로 작동하는 자리", ACC)])
d.save("06-01.chapter-overview.svg")
