# 01-01 학습 목표 뒤 전체 지도 — 절 여섯을 읽는 순서로 잇는다.
# 본문: "칸마다 절 번호와 그 절이 답하는 질문 하나", "색이 붙은 칸이 이 장이 대가를 값매기는 자리".
# 타입 스펙: type-process — 절마다 같은 의미 슬롯(번호 · 이름 · 질문)이 반복되고 화살표가 읽는 순서를 나른다.
#           축약: 주체(lane)가 없는 단계 지도라 카드 격자 stride 로 놓는다(같은 폴더 관례).
# 캔버스는 880 폭으로 좁게 잡는다 — 본문에서 width:100% 로 늘어나므로 viewBox 가 좁을수록 글자가 크게 보인다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 552
d = D(W, H, "LEARNING COREDNS · 01-01",
      "CoreDNS 는 무엇을 포기하고 무엇을 얻었는가",
      "1장 노트의 절 여섯을 읽는 순서로 이은 지도. 1절이 컨테이너 환경이 낳은 문제이고, "
      "2~4절이 Caddy 에서 물려받은 셋, 5절이 그 대가로 포기한 것, 6절이 쿠버네티스 기본값이 되기까지의 연표다.",
      "5절에서 못 하는 것을 표로 못 박습니다")

CW, CH, GAP, X0 = 400, 104, 20, 20
ROWS = [104, 232, 360]
cards = [
    ("§1", "컨테이너는 계속 뜨고 진다", "지금 떠 있는 목록을 어떻게 얻나"),
    ("§2", "그래서 Caddy 를 포크했다", "물려받은 셋이 이 장의 뼈대"),
    ("§3", "안 켠 플러그인은 안 돈다", "설정하지 않으면 코드가 없다"),
    ("§4", "Go 의 메모리 안전성", "BIND 가 수십 년 겪은 오류"),
    ("§5", "재귀는 포워더에 맡긴다", "못 하는 것을 표로 못 박는다"),
    ("§6", "쿠버네티스 기본값까지", "2016 포크에서 2019 졸업으로"),
]
def pos(i):
    return X0 + (i % 2) * (CW + GAP), ROWS[i // 2]

for i in range(5):
    x1, y1 = pos(i); x2, y2 = pos(i + 1)
    if y1 == y2:
        d.arrow([(x1 + CW, y1 + CH / 2), (x2 - 2, y2 + CH / 2)], MUTED, "ar", 1.4)
    else:
        bus = y1 + CH + 12
        d.path(f"M {x1 + CW / 2} {y1 + CH} L {x1 + CW / 2} {bus} L {x2 + CW / 2} {bus} L {x2 + CW / 2} {y2 - 2}",
               MUTED, 1.4, m="ar")

for i, (n, title, q) in enumerate(cards):
    x, y = pos(i); focal = (i == 4)
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{CW}" height="{CH}" rx="8" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y, CW, CH, PAPER2, RULE, 1.0, 8)
    d.t(x + 18, y + 26, n, 12, ACC if focal else SOFT, MONO, "start", 600)
    d.t(x + 18, y + 56, title, 16, ACC if focal else INK, KR, "start", 600)
    d.t(x + 18, y + 84, q, 13, MUTED, KR, "start")

d.legend(492, [("이 장이 대가를 값매기는 자리", ACC)])
d.save("01-01.chapter-overview.svg")
