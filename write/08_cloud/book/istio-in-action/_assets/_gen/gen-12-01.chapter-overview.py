# 12-01 전체 지도 — 절 여덟을 읽는 순서로 잇는다.
# 본문: "칸마다 절 번호와 그 절이 답하는 것 하나", "색이 붙은 칸이 클러스터 경계가 유일하게 드러나는 자리".
# 근거(원문 12.3.7 NOTE): east-west 게이트웨이가 TLS 를 종료하지 않아 원격 클러스터 안의 분산은 균등하지 않다.
# 타입 스펙: type-process — 절마다 같은 의미 슬롯(번호 · 이름 · 답하는 것)이 반복되고 화살표가 읽는 순서를 나른다.
#           축약: 주체(lane)가 없는 단계 지도라 카드 한 줄 stride 로 놓는다(01~11 과 같은 관례).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

# 폭은 계약의 본문 삽입용 상한(880~1000) 안으로 두고, 4 열을 2 열로 접어 담는다.
# 계약: "넓은 캔버스에 담기지 않으면 폭을 늘리지 말고 배치를 바꾼다."
COLS, CW, CH, GAP, VGAP, X0, Y0 = 2, 396, 100, 16, 56, 36, 104
cards = [
    ("§1", "묶으려면 셋이 필요하다", "발견 · 연결 · 공통 신뢰"),
    ("§2", "컨트롤 플레인을 어디 둘까", "가용성과 자원의 거래"),
    ("§3", "남의 API 서버를 읽는 권한", "토큰 하나에 실리는 무게"),
    ("§4", "같은 뿌리에서 갈라진 인증서", "중간 CA 를 꽂는다"),
    ("§5", "식별자 셋이 지형을 정한다", "메시 · 클러스터 · 네트워크"),
    ("§6", "동서로 지나는 관문", "SNI 에 목적지를 싣는다"),
    ("§7", "가까운 곳부터 쓰고 넘긴다", "우선순위와 페일오버"),
    ("§8", "경계가 드러나는 한 자리", "게이트웨이 뒤는 균등하지 않다"),
]
FOCAL = 7
ROWS = -(-len(cards) // COLS)
BOTTOM = Y0 + ROWS * (CH + VGAP) - VGAP
LEGY = BOTTOM + 48
W, H = 880, LEGY + 40

d = D(W, H, "ISTIO IN ACTION · 12-01",
      "전제 셋을 채우면 나머지는 경계를 모른다 — 읽는 순서",
      "12장 노트의 절 여덟을 읽는 순서로 이은 지도. 앞의 넷이 클러스터를 하나로 묶는 전제를 세우고, "
      "가운데 둘이 그것을 실제로 세우며, 뒤의 둘이 경계를 넘어도 그대로인지 확인한다.",
      "저자가 반복하는 문장은 추가 설정 없이 그대로 작동한다는 것입니다")

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

d.legend(LEGY, [("경계가 드러나는 유일한 자리", ACC), ("경계를 감추는 절", MUTED)])
d.save("12-01.chapter-overview.svg")
