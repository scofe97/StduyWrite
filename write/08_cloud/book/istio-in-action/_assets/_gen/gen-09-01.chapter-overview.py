# 09-01 학습 목표 뒤 전체 지도 — 절 여덟을 읽는 순서로 잇는다.
# 본문: "칸마다 절 번호와 그 절이 답하는 질문 하나", "색이 붙은 칸이 실무에서 가장 많이 다치는 자리".
# 타입 스펙: type-process — 절마다 같은 의미 슬롯(번호 · 이름 · 질문)이 반복되고 화살표가 읽는 순서를 나른다.
#           축약: 주체(lane)가 없는 단계 지도라 카드 한 줄 stride 로 놓는다(03~08 과 같은 관례).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 1240, 432
d = D(W, H, "ISTIO IN ACTION · 09-01",
      "거의 안전한 기본값을 닫아 가는 순서 — 읽는 순서",
      "9장 노트의 절 여덟을 읽는 순서로 이은 지도. §1~§3 이 신원과 기본값 이야기이고, "
      "§4~§6 이 인가 정책의 규칙, §7~§8 이 최종 사용자와 외부 위임이다.",
      "§4 가 디버깅 시간을 가장 많이 삼키는 자리입니다")

CW, CH, GAP, X0 = 280, 96, 16, 36
Y1, Y2 = 104, 248
cards = [
    ("§1", "IP 가 신원이던 자리", "SPIFFE · SVID"),
    ("§2", "리소스 셋의 분업", "필터 메타데이터가 잇는다"),
    ("§3", "기본이 열려 있는 이유", "PERMISSIVE · 범위 셋"),
    ("§4", "허용 하나가 나머지를 닫는다", "catch-all DENY 를 먼저"),
    ("§5", "정책이 평가되는 순서", "CUSTOM → DENY → ALLOW"),
    ("§6", "규칙이 걸리는 조건", "묶음 사이 AND · 안은 OR"),
    ("§7", "두 계층의 두 신원", "principals · requestPrincipals"),
    ("§8", "판단을 밖으로 내보낼 때", "CUSTOM + ExtAuthz"),
]
def pos(i):
    if i < 4: return X0 + i * (CW + GAP), Y1
    return X0 + (i - 4) * (CW + GAP), Y2
def card(i, focal=False):
    x, y = pos(i); n, title, q = cards[i]
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{CW}" height="{CH}" rx="8" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y, CW, CH, PAPER2, RULE, 1.0, 8)
    d.t(x + 16, y + 26, n, 11, ACC if focal else SOFT, MONO, "start", 600)
    d.t(x + 16, y + 52, title, 13, ACC if focal else INK, KR, "start", 600)
    d.t(x + 16, y + 76, q, 11, MUTED, KR, "start")
for i in range(7):
    x1, y1 = pos(i); x2, y2 = pos(i + 1)
    if y1 == y2:
        d.arrow([(x1 + CW, y1 + CH / 2), (x2 - 2, y2 + CH / 2)], MUTED, "ar", 1.4)
    else:
        d.path(f"M {x1 + CW / 2} {y1 + CH} L {x1 + CW / 2} 224 L {x2 + CW / 2} 224 L {x2 + CW / 2} {y2 - 2}", MUTED, 1.4, m="ar")
for i in range(8):
    card(i, focal=(i == 3))
d.legend(376, [("기본값이 조용히 뒤집히는 자리", ACC)])
d.save("09-01.chapter-overview.svg")
