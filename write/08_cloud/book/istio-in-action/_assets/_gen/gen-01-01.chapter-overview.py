# 01-01 본문 정리 앞 전체 지도 — 절 여덟을 읽는 순서로 잇는다.
# 본문: "칸마다 절 번호와 그 절의 요점 하나", "색이 붙은 칸이 저자가 스스로 단점을 꺼내 놓는 자리".
# 타입 스펙: type-process — 절마다 같은 의미 슬롯(번호 · 이름 · 요점)이 반복되고 화살표가 읽는 순서를 나른다.
#           축약: 주체(lane)가 없는 단계 지도라 카드 한 줄 stride 로 놓는다(02~09 와 같은 관례).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 1240, 432
d = D(W, H, "ISTIO IN ACTION · 01-01",
      "서비스 메시는 무엇을 인프라로 밀어냈는가 — 읽는 순서",
      "1장 노트의 절 여덟을 읽는 순서로 이은 지도. §1~§3 이 문제와 라이브러리 해법의 한계이고, "
      "§4~§5 가 프록시로 옮긴 결과, §6~§8 이 앞선 기술과의 비교와 저자가 인정한 대가다.",
      "§8 에서 저자가 스스로 단점 셋을 꺼내 놓습니다")

CW, CH, GAP, X0 = 280, 96, 16, 36
Y1, Y2 = 104, 248
cards = [
    ("§1", "인프라는 신뢰할 수 없다", "지연의 원인을 구분 못 한다"),
    ("§2", "애플리케이션 네트워킹 여덟", "패킷이 아니라 메시지 계층"),
    ("§3", "라이브러리로 풀면", "언어에 묶이고 갈라진다"),
    ("§4", "프록시로 옮기면", "프로세스 밖 L7 프록시"),
    ("§5", "데이터 · 컨트롤 플레인", "누가 무엇을 설정하는가"),
    ("§6", "ESB · API 게이트웨이", "범위를 좁혀 사일로를 피한다"),
    ("§7", "마이크로서비스가 아니어도", "모놀리스에도 붙는다"),
    ("§8", "저자가 인정하는 단점 셋", "기술보다 조직이 어렵다"),
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
    card(i, focal=(i == 7))
d.legend(376, [("저자가 스스로 대가를 꺼내는 자리", ACC)])
d.save("01-01.chapter-overview.svg")
