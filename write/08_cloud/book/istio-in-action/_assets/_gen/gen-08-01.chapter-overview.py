# 08-01 학습 목표 뒤 전체 지도 — 절 여덟을 읽는 순서로 잇는다.
# 본문: "칸마다 절 번호와 그 절이 답하는 질문 하나", "색이 붙은 칸이 이 장의 무게가 실린 자리".
# 타입 스펙: type-process — 절마다 같은 의미 슬롯(번호 · 이름 · 질문)이 반복되고 화살표가 읽는 순서를 나른다.
#           축약: 주체(lane)가 없는 단계 지도라 카드 한 줄 stride 로 놓는다(03~07 과 같은 관례).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 1240, 432
d = D(W, H, "ISTIO IN ACTION · 08-01",
      "메시가 절반까지만 해 주는 일 — 읽는 순서",
      "8장 노트의 절 여덟을 읽는 순서로 이은 지도. §1~§2 가 그리는 화면 이야기이고, "
      "§3 부터 §7 까지가 추적 하나에 매달린 절반이며, §8 이 메시 자신을 아는 화면이다.",
      "§3 이 프록시의 몫과 애플리케이션의 몫이 갈리는 자리입니다")

CW, CH, GAP, X0 = 280, 96, 16, 36
Y1, Y2 = 104, 248
cards = [
    ("§1", "세 화면이 답하는 질문", "재료와 그리는 대상"),
    ("§2", "Istio 가 만들어 둔 대시보드", "배포에서 빠진 여섯"),
    ("§3", "스팬은 프록시, 트레이스는 앱", "인과는 앱만 안다"),
    ("§4", "추적을 켜는 자리", "MeshConfig · 애노테이션"),
    ("§5", "얼마나 자주, 지금 이것만", "sampling · force-trace"),
    ("§6", "스팬에 우리 말을 붙이기", "리터럴 · 환경 · 헤더"),
    ("§7", "정적 설정을 갈아 끼웠을 때", "병합이 아니라 대체"),
    ("§8", "Kiali 가 세는 단위", "워크로드와 애플리케이션"),
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
    card(i, focal=(i == 2))
d.legend(376, [("프록시의 몫과 애플리케이션의 몫이 갈리는 자리", ACC)])
d.save("08-01.chapter-overview.svg")
