# 01-01 §8 저자가 인정하는 단점 셋.
# 본문: (1) 요청 경로에 미들웨어가 하나 더 들어가 디버깅이 어려워진다.
#       (2) 테넌시·격리 모델이 없으면 설정 실수 하나가 다수 서비스에 파급된다.
#       (3) 또 하나의 계층이 곧 또 하나의 복잡성이고, 무엇보다 기존 조직 프로세스·거버넌스·팀 사이에
#           어떻게 통합할지가 어렵다.
# 저자는 기술적 난이도보다 조직 통합을 더 어려운 문제로 놓았다 — 그래서 아래로 갈수록 어려워지는 층이다.
# 타입 스펙: type-layers — 위아래로 쌓인 난이도. 층 3, 층 높이 76, 왼쪽 여백에 방향 표시,
#           초점 1층(저자가 가장 어렵다고 놓은 조직 층).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 1160, 520
d = D(W, H, "ISTIO IN ACTION · 01-01 §8",
      "아래로 갈수록 기술이 아니라 사람 문제가 된다",
      "저자가 든 단점 셋을 그가 놓은 난이도 순으로 쌓았다. 색이 붙은 층이 저자가 마지막에 두고 "
      "가장 어렵다고 적은 자리다. 도입 판단이 걸리는 곳도 대개 여기다.",
      "저자는 기술적 난이도보다 조직 통합을 더 어려운 문제로 놓았습니다")

LX, LW, LH, Y0 = 210, 870, 76, 132
rows = [
    ("REQUEST", "요청 경로", "미들웨어가 하나 더 들어간다", "프록시가 낯설면 블랙박스가 된다", False),
    ("TENANCY", "테넌시", "격리 모델이 없으면", "설정 실수 하나가 다수 서비스에 파급", False),
    ("ORG", "조직", "프로세스 · 거버넌스 · 팀", "저자가 가장 어렵다고 놓은 자리", True),
]
for i, (tag, name, mid, right, focal) in enumerate(rows):
    y = Y0 + i * LH
    if focal:
        d.o.append(f'<rect x="{LX}" y="{y}" width="{LW}" height="{LH}" rx="4" fill="{ACC}10" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(LX, y, LW, LH, PAPER2, RULE, 1.0, 4)
    d.t(LX + 20, y + 44, tag, 9, SOFT, MONO, "start", 600)
    d.t(LX + 128, y + 44, name, 15, ACC if focal else INK, KR, "start", 600)
    d.t(LX + 260, y + 44, mid, 11, ACC if focal else MUTED, KR, "start")
    d.t(LX + LW - 20, y + 44, right, 9, MUTED, KR, "end")

d.path(f"M {LX - 44} {Y0 + 8} L {LX - 44} {Y0 + 3 * LH - 8}", MUTED, 1.2, m="ar")
d.t(LX - 60, Y0 + 24, "난이도", 9, SOFT, KR, "end")
d.t(LX - 60, Y0 + 3 * LH - 24, "높아진다", 9, SOFT, KR, "end")

d.t(32, 412, "메시의 가치는 안에서 도는 서비스 수에 비례하므로 넓힐수록 두 번째 층의 위험도 함께 커진다", 11, SOFT, KR, "start")
d.t(32, 436, "저자는 서비스 메시가 유일한 해법도 아니고 단점이 없지도 않다고 못 박는다", 11, MUTED, KR, "start")
d.legend(456, [("저자가 가장 어렵다고 놓은 층", ACC), ("기술로 다루는 층", MUTED)])
d.save("01-01.three-costs.svg")
