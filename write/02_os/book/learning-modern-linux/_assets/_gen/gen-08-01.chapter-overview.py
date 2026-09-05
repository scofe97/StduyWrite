# 08-01 학습 목표 뒤 전체 지도 — 절 일곱을 읽는 순서로.
# 원문 8장 서두: "To establish a common vocabulary, we'll first review different signal types you might
#       come across, such as system or application logs, metrics, and process traces. We'll also have a
#       look at how to go about troubleshooting and measuring performance. Next, we'll focus on logs
#       specifically, reviewing different options and semantics."
# 타입 스펙: type-process — 절마다 같은 의미 슬롯(번호 · 이름 · 그 절이 답하는 물음)이 반복되고
#           읽는 순서가 화살표로 흐른다. 축약: 주체 lane 이 없어 카드 격자 stride 로 놓는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 588
d = D(W, H, "LEARNING MODERN LINUX · 08-01",
      "재는 것은 바깥이고 알고 싶은 것은 안이다",
      "8장 첫 구간의 절 일곱을 읽는 순서로 이은 지도. 1~3절이 어휘를 세우고 4~7절이 로그 하나를 판다.",
      "저자는 이 장의 대부분을 로그에 쓰겠다고 미리 밝힙니다")

CW, CH, GAPX, GAPY, X0, Y0 = 272, 96, 12, 20, 20, 116
cards = [
    ("§1", "원인 좁히기", "느리다는 신고에서 무엇부터 보나"),
    ("§2", "신호가 흐르는 길", "로그는 어디서 나서 어디로 가나"),
    ("§3", "신호 셋", "무엇을 켤지 어떻게 고르나"),
    ("§4", "로그의 해부", "무엇을 구조화하라는 말인가"),
    ("§5", "/var/log", "장애 때 어느 파일을 여나"),
    ("§6", "Syslog 와 RFC 5424", "어느 필드가 항상 있나"),
    ("§7", "journalctl", "tail 이 안 통하면 무엇을 치나"),
]


def pos(i):
    return X0 + (i % 3) * (CW + GAPX), Y0 + (i // 3) * (CH + GAPY)


for i in range(len(cards) - 1):
    x1, y1 = pos(i); x2, y2 = pos(i + 1)
    if y1 == y2:
        d.arrow([(x1 + CW, y1 + CH / 2), (x2 - 2, y2 + CH / 2)], MUTED, "ar", 1.3)
    else:
        bus = y1 + CH + 10
        d.path(f"M {x1 + CW / 2} {y1 + CH} L {x1 + CW / 2} {bus} "
               f"L {x2 + CW / 2} {bus} L {x2 + CW / 2} {y2 - 2}", MUTED, 1.3, m="ar")

for i, (n, title, q) in enumerate(cards):
    x, y = pos(i)
    focal = (i == 1)
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{CW}" height="{CH}" rx="8" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y, CW, CH, PAPER2, RULE, 1.0, 8)
    d.t(x + 16, y + 26, n, 12, ACC if focal else SOFT, MONO, "start", 600)
    d.t(x + 16, y + 54, title, 14, ACC if focal else INK, KR, "start", 600)
    d.t(x + 16, y + 78, q, 11.5, MUTED, KR, "start")

d.legend(524, [("바깥을 재서 안을 판정한다는 정의가 서는 자리", ACC)])
d.save("08-01.chapter-overview.svg")
print("ok 08-01.chapter-overview")
