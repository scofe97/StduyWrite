# 10-01 전체 지도 — 절 여덟을 읽는 순서로 잇는다.
# 본문: "칸마다 절 번호와 그 절이 좁혀 주는 것 하나", "색이 붙은 칸이 저자가 대개 여기서 끝난다고 적은 자리".
# 근거(원문 10.2.3 끝): "Both the analyze and describe subcommands ... are usually enough to suggest fixes."
# 타입 스펙: type-process — 절마다 같은 의미 슬롯(번호 · 이름 · 좁히는 것)이 반복되고 화살표가 읽는 순서를 나른다.
#           축약: 주체(lane)가 없는 단계 지도라 카드 한 줄 stride 로 놓는다(01~09 와 같은 관례).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 1240, 520
d = D(W, H, "ISTIO IN ACTION · 10-01",
      "프록시는 다 알고 있고 사람은 못 읽는다 — 읽는 순서",
      "10장 노트의 절 여덟을 읽는 순서로 이은 지도. 앞의 셋이 의심 범위를 자동으로 좁히고, "
      "가운데 셋이 설정과 로그를 손으로 열며, 마지막 둘이 누가 무엇을 세는지를 가른다.",
      "도구가 여럿인 것은 기능이 달라서가 아니라 좁히는 단계가 달라서입니다")

CW, CH, GAP, X0 = 280, 96, 16, 36
Y1, Y2 = 104, 248
cards = [
    ("§1", "요청에 넷이 관여한다", "가장 흔한 원인은 설정 실수"),
    ("§2", "컨트롤 플레인을 지운다", "동기화가 끝났는지부터"),
    ("§3", "자동 분석기 셋", "적용 전과 후, 넓게와 좁게"),
    ("§4", "13,934줄을 넷으로 자른다", "명령 · 설정 · 리소스의 대응"),
    ("§5", "이름 한 줄이 조건 넷", "리스너에서 엔드포인트까지"),
    ("§6", "요청이 끝난 자리가 남는다", "응답 플래그가 지목하는 층"),
    ("§7", "스코프를 골라 올린다", "ID 로 한 요청을 묶는다"),
    ("§8", "둘이 다르게 센다", "파드 하나를 지목한다"),
]
FOCAL = 2
def pos(i):
    if i < 4: return X0 + i * (CW + GAP), Y1
    return X0 + (i - 4) * (CW + GAP), Y2
def card(i):
    x, Y = pos(i); n, title, q = cards[i]; focal = (i == FOCAL)
    if focal:
        d.o.append(f'<rect x="{x}" y="{Y}" width="{CW}" height="{CH}" rx="8" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, Y, CW, CH, PAPER2, RULE, 1.0, 8)
    d.t(x + 16, Y + 26, n, 11, ACC if focal else SOFT, MONO, "start", 600)
    d.t(x + 16, Y + 52, title, 13, ACC if focal else INK, KR, "start", 600)
    d.t(x + 16, Y + 76, q, 11, MUTED, KR, "start")
for i in range(7):
    x1, y1 = pos(i); x2, y2 = pos(i + 1)
    if y1 == y2:
        d.arrow([(x1 + CW, y1 + CH / 2), (x2 - 2, y2 + CH / 2)], MUTED, "ar", 1.4)
    else:
        d.path(f"M {x1 + CW / 2} {y1 + CH} L {x1 + CW / 2} 224 L {x2 + CW / 2} 224 L {x2 + CW / 2} {y2 - 2}", MUTED, 1.4, m="ar")
for i in range(8):
    card(i)

d.t(32, 396, "앞의 셋에서 끝나면 뒤의 다섯을 열 일이 없다 — 이 장의 도구는 전부 범위를 줄이는 도구다", 11, SOFT, KR, "start")
d.t(32, 420, "저자가 든 예제는 DestinationRule 하나가 빠져 모든 요청이 503 으로 실패하는 상황이다", 11, MUTED, KR, "start")
d.legend(444, [("저자가 대개 여기서 끝난다고 적은 자리", ACC), ("더 내려가야 할 때 여는 절", MUTED)])
d.save("10-01.chapter-overview.svg")
