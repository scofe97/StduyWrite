# 07-01 학습 목표 뒤 전체 지도 — 절 여덟을 읽는 순서로 잇는다.
# 본문: "칸마다 절 번호와 그 절이 답하는 질문 하나", "색이 붙은 칸이 이 장의 나머지 절반을 여는 자리".
# 타입 스펙: type-process — 절마다 같은 의미 슬롯(번호 · 이름 · 질문)이 반복되고 화살표가 읽는 순서를 나른다.
#           축약: 주체(lane)가 없는 단계 지도라 §1 lanes·§2 공식 대신 카드 한 줄 stride 로 놓는다(03~06 과 같은 관례).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 1240, 432
d = D(W, H, "ISTIO IN ACTION · 07-01",
      "미리 정하지 않았던 것을 나중에 세려면 — 읽는 순서",
      "7장 노트의 절 여덟을 읽는 순서로 이은 지도. 앞의 다섯 절이 이미 있는 값을 꺼내 보는 이야기이고, "
      "§6 부터 무엇을 셀지 자체를 바꾸는 이야기로 넘어간다.",
      "앞의 다섯은 꺼내 보는 이야기입니다. §6 부터가 무엇을 셀지 바꾸는 이야기입니다")

CW, CH, GAP, X0 = 280, 96, 16, 36
Y1, Y2 = 104, 248
cards = [
    ("§1", "관측 가능성 중 Istio의 몫", "모니터링은 부분집합"),
    ("§2", "어디를 물으면 무엇이 나오나", "표면 넷 · 표준 메트릭 여섯"),
    ("§3", "잘라 둔 것을 되살리면", "proxyStatsMatcher"),
    ("§4", "컨트롤 플레인이 말하는 것", ":15014 · xDS 푸시"),
    ("§5", "긁어 가게 만드는 두 리소스", "ServiceMonitor · PodMonitor"),
    ("§6", "메트릭 · 차원 · 속성", "차원 하나가 줄을 가른다"),
    ("§7", "차원을 더할 때 두 곳", "설정 + 애노테이션"),
    ("§8", "새 메트릭과 새 속성", "CEL · attribute-gen"),
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
    card(i, focal=(i == 5))
d.legend(376, [("무엇을 셀지 바꾸는 이야기가 열리는 자리", ACC)])
d.save("07-01.chapter-overview.svg")
