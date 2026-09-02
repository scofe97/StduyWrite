# 03-02 학습 목표 뒤 전체 지도 — 절 여덟을 읽는 순서로 잇는다.
# 타입 스펙: type-process — 절마다 같은 의미 슬롯(번호 · 이름 · 질문)이 반복되고 화살표가 읽는 순서를 나른다.
#           축약: 주체(lane)가 없는 단계 지도라 카드 격자 stride 로 놓는다(같은 폴더 관례).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 812
d = D(W, H, "LEARNING COREDNS · 03-02",
      "플러그인 일곱이면 서버 하나가 선다",
      "3장 후반부의 절 여덟을 읽는 순서로 이은 지도. 1절이 모든 플러그인에 걸리는 전제이고, "
      "2~6절이 기본 플러그인 일곱, 7절이 여러 플러그인이 공유하는 옵션, 8절이 완성된 설정 셋이다.",
      "8절에서 앞의 일곱 절이 세 벌의 Corefile 로 모입니다")

CW, CH, GAP, X0 = 400, 104, 20, 20
ROWS = [104, 232, 360, 488]
cards = [
    ("§1", "순서는 빌드 때 정해진다", "선언 순서는 처리 순서가 아니다"),
    ("§2", "root 와 file", "주 서버를 세우는 둘"),
    ("§3", "secondary", "받아 오고, 저장하지 않는다"),
    ("§4", "forward", "0.5초마다 건강을 묻는다"),
    ("§5", "cache", "성공과 부정을 따로 담는다"),
    ("§6", "errors 와 log", "둘 다 표준 출력으로 간다"),
    ("§7", "공유 옵션 셋", "fallthrough · tls · transfer to"),
    ("§8", "완성된 Corefile 셋", "캐싱 전용 · 주 서버 · 보조 서버"),
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
d.save("03-02.chapter-overview.svg")
