# 02-02 학습 목표 뒤 전체 지도 — 절 여덟을 읽는 순서로 잇는다.
# 타입 스펙: type-process — 절마다 같은 의미 슬롯(번호 · 이름 · 질문)이 반복되고 화살표가 읽는 순서를 나른다.
#           축약: 주체(lane)가 없는 단계 지도라 카드 격자 stride 로 놓는다(같은 폴더 관례).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 812
d = D(W, H, "LEARNING COREDNS · 02-02",
      "레코드 한 줄을 읽을 수 있으면 존 파일이 읽힌다",
      "2장 후반부의 절 여덟을 읽는 순서로 이은 지도. 1~2절이 모든 레코드에 공통인 한 줄의 문법이고, "
      "3~7절이 타입별 RDATA, 8절이 그 전부가 한 파일에 모인 모습이다.",
      "8절의 존 파일 한 장이 앞의 일곱 절을 되짚습니다")

CW, CH, GAP, X0 = 400, 104, 20, 20
ROWS = [104, 232, 360, 488]
cards = [
    ("§1", "레코드 한 줄은 다섯 칸", "NAME TTL CLASS TYPE RDATA"),
    ("§2", "빈칸은 앞줄에서 물려받는다", "생략이 문법의 일부다"),
    ("§3", "주소와 별칭", "CNAME 에 붙는 세 규칙"),
    ("§4", "우선순위로 고르는 레코드", "MX 의 선호도, SRV 의 가중치"),
    ("§5", "위임을 실제로 그리는 레코드", "NS 는 두 존에 함께 산다"),
    ("§6", "거꾸로 찾기", "주소를 뒤집어 이름으로"),
    ("§7", "존 전체의 매개변수", "SOA 일곱 칸과 세 타이머"),
    ("§8", "존 파일 한 장 읽기", "앞의 일곱 절이 한자리에"),
]
def pos(i):
    return X0 + (i % 2) * (CW + GAP), ROWS[i // 2]

for i in range(len(cards) - 1):
    x1, y1 = pos(i); x2, y2 = pos(i + 1)
    if y1 == y2:
        d.arrow([(x1 + CW, y1 + CH / 2), (x2 - 2, y2 + CH / 2)], MUTED, "ar", 1.4)
    else:
        bus = y1 + CH + 12
        d.path(f"M {x1 + CW / 2} {y1 + CH} L {x1 + CW / 2} {bus} L {x2 + CW / 2} {bus} L {x2 + CW / 2} {y2 - 2}",
               MUTED, 1.4, m="ar")

for i, (n, title, q) in enumerate(cards):
    x, y = pos(i); focal = (i == 7)
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{CW}" height="{CH}" rx="8" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y, CW, CH, PAPER2, RULE, 1.0, 8)
    d.t(x + 18, y + 26, n, 12, ACC if focal else SOFT, MONO, "start", 600)
    d.t(x + 18, y + 56, title, 16, ACC if focal else INK, KR, "start", 600)
    d.t(x + 18, y + 84, q, 13, MUTED, KR, "start")

d.legend(752, [("앞의 전부가 모이는 자리", ACC)])
d.save("02-02.chapter-overview.svg")
