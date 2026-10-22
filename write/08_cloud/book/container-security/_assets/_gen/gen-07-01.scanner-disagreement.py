# 타입 스펙: type-process — 스캐너 한 번의 실행을 패키지 식별 · 피드 대조 · 결과 보고 세 단계로 나누고, 단계마다 결과가 갈리는 지점을 같은 슬롯(이름 · 값 · 오탐/미탐/정책 칩)으로 반복해 다섯 이유를 배치한다. focal 은 올바른 결과 집합이 없다는 결론 띠.
# 사실 출처: 노트 L154~L162(다섯 이유 표 · 스캐너 자체 버그), L164(올바른 결과 집합은 없다). 세 단계로 묶은 배치는 이 그림의 정리이며 책이 단계를 명시한 것은 아니다.
# Layout conventions: 열 폭 288 · 칸 사이 24(x=24·336·648), 머리 h=44, 카드 h=104 · stride 116. 모든 좌표 4의 배수.
import sys, pathlib
ASSETS = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ASSETS))
from dd import D, INK, MUTED, SOFT, ACC, OK, WARN, BAD, INFO, KR, MONO, RULE

W, H = 960, 512
COLX = [24, 336, 648]
CW = 288
HY = 100
CY0, CH, STRIDE = 164, 104, 116


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def fit(t, size, limit):
    w = sum(size if "가" <= c <= "힣" else size * 0.62 for c in t)
    assert w <= limit, (t, w, limit)


d = D(W, H, "CONTAINER SECURITY · 07-01 §4",
      "같은 이미지가 스캐너마다 다르게 나오는 이유는 세 단계에 흩어져 있습니다",
      "스캐너 한 번의 실행을 패키지 식별, 피드 대조, 결과 보고 세 단계로 나누면 패키지 이름과 하위 패키지는 식별 단계에서, "
      "정보 출처와 낡은 출처는 피드 대조 단계에서, 고치지 않기로 한 취약점은 결과 보고 단계에서 결과가 갈린다.",
      "오탐은 없는 취약점을 보고하는 것이고, 미탐은 있는 취약점을 놓치는 것입니다.")

HEADS = ["패키지 식별", "피드 대조", "결과 보고"]
for j, name in enumerate(HEADS):
    x = COLX[j]
    d.box(x, HY, CW, 44, "#161B22", RULE, 1.0)
    d.t(x + CW / 2, HY + 28, name, 14, INK, KR, "middle", 600)
    if j < 2:
        d.arrow([(x + CW + 2, HY + 22), (COLX[j + 1] - 4, HY + 22)], SOFT, "soft", 1.3)

# (열, 줄, 이름, 값1, 값2, 칩들)
CARDS = [
    (0, 0, "하위 패키지", "Ubuntu bind 의 문서 하위 패키지", "전체 설치로 가정", [("오탐", WARN)]),
    (0, 1, "패키지 이름", "소스 이름 shadow (Debian)", "바이너리 login · passwd · uidmap", [("미탐", BAD)]),
    (1, 0, "정보 출처", "NVD 만 읽음 · 백포트를 모름", "Red Hat 피드 둘 (OVAL: 수정 있는 것만)", [("오탐", WARN)]),
    (1, 1, "낡은 출처", "alpine-secdb → aports 로 이전", "옛 피드만 읽으면 갱신을 놓침", [("오탐", WARN), ("미탐", BAD)]),
    (2, 0, "고치지 않기로 한 것", "수정을 포기한 취약점", "결과에 넣을지는 도구 개발자의 판단", [("정책 차이", INFO)]),
    (2, 1, "그 밖", "스캐너 자체의 버그", "보안 권고 피드의 결함", [("오탐", WARN), ("미탐", BAD)]),
]
for col, row, name, v1, v2, chips in CARDS:
    x = COLX[col]
    y = CY0 + row * STRIDE
    fit(name, 14, 150)
    fit(v1, 12, CW - 24)
    fit(v2, 12, CW - 24)
    d.box(x, y, CW, CH, "#161B22", RULE, 1.0)
    d.t(x + 16, y + 30, name, 14, INK, KR, "start", 600)
    d.line(x + 16, y + 44, x + CW - 16, y + 44, RULE, 0.8)
    d.t(x + 16, y + 68, v1, 12, MUTED, kr(v1), "start")
    d.t(x + 16, y + 90, v2, 12, MUTED, kr(v2), "start")
    cx = x + CW - 16
    for lab, c in reversed(chips):
        w = len(lab) * 12 + 14
        d.chip(cx - w / 2, y + 24, lab, c, 12)
        cx -= w + 8

# 결론 띠
BY = 408
d.tone(24, BY, 912, 48, ACC, 6, "1F", 1.4)
d.t(480, BY + 30, "같은 이미지 · 다른 결과 · 올바른 결과 집합은 없음", 14, ACC, KR, "middle", 600)

d.legend(472, [("오탐", WARN), ("미탐", BAD), ("정책 차이", INFO), ("결론", ACC)])
d.save(str(ASSETS / "07-01.scanner-disagreement.svg"))
print("ok 07-01 scanner-disagreement")
