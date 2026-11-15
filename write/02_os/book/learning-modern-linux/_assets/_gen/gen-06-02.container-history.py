# 06-02 §1 — 컨테이너가 주류가 되기까지의 시도들.
# 원문("Containers"): "Containers are, per se, nothing new in Linux. However, they've enjoyed mainstream
#       adoption only due to Docker, starting in roughly 2014. Before that, we had a number of attempts
#       to introduce containers, often targeting system administrators rather than developers, including
#       the following: Linux-VServer (2001), OpenVZ (2005), LXC (2008), Let Me Contain That for You
#       (lmctfy) (2013)."
#       "What all of these approaches have in common is that they use the basic building blocks the Linux
#       kernel provides, such as namespaces or cgroups, to allow users to run applications."
#       "Docker innovated on the concept and introduced two groundbreaking elements: a standardized way
#       to define the packaging via container images and a human-friendly user interface (for example,
#       docker run)."
# 타입 스펙: type-timeline — 시간축 위의 사건과 그 성격 변화. accent 는 성격이 바뀐 한 점.
#           축약: 연도는 원문이 준 것만 찍었고 그 사이의 커널 기능 도입 시점은 §2 표에 있다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 504
d = D(W, H, "LEARNING MODERN LINUX · 06-02 §1",
      "컨테이너는 오래됐고 Docker 는 새롭다",
      "저자가 든 다섯 사건을 시간축에 놓은 것. 앞의 넷은 같은 커널 재료를 쓰면서 주로 시스템 "
      "관리자를 겨냥했고, 2014년에 겨냥하는 사람이 바뀐다.",
      "재료는 내내 같았고 바뀐 것은 감싸는 방식입니다")

X0, X1, AY = 64, 816, 204
d.path(f"M {X0} {AY} L {X1} {AY}", MUTED, 1.4, m="ar")
d.o.append(f'<rect x="{X0}" y="{AY - 14}" width="{X1 - X0 - 168}" height="28" rx="4" '
           f'fill="{INFO}10" stroke="none"/>')

events = [
    ("2001", "Linux-VServer", INFO),
    ("2005", "OpenVZ", INFO),
    ("2008", "LXC", INFO),
    ("2013", "lmctfy", INFO),
    ("2014", "Docker", ACC),
]
span = (X1 - X0 - 40) / (len(events) - 1)
for i, (year, name, col) in enumerate(events):
    x = X0 + 20 + i * span
    focal = (col is ACC)
    r = 9 if focal else 6
    d.o.append(f'<circle cx="{x}" cy="{AY}" r="{r}" fill="{col}" stroke="none"/>')
    d.t(x, AY - 34, year, 12.5, col, MONO, "middle", 600)
    d.t(x, AY + 44, name, 13.5 if focal else 12.5, col, KR if focal else MONO, "middle",
        600 if focal else 400)

# 두 상자 높이 112: 마지막 줄 아래 여백을 첫 줄 위 여백(약 18px)과 맞춘다
BY = AY + 60
d.tone(64, BY, 400, 112, INFO)
d.t(84, BY + 28, "앞의 넷이 공통으로 가진 것", 13, INK, KR, "start", 600)
d.t(84, BY + 52, "리눅스 커널의 기본 재료 사용", 11.5, MUTED, KR, "start")
d.t(84, BY + 72, "네임스페이스 · cgroups", 11.5, MUTED, KR, "start")
d.t(84, BY + 90, "주 대상은 개발자보다 시스템 관리자", 11.5, MUTED, KR, "start")

d.o.append(f'<rect x="480" y="{BY}" width="336" height="112" rx="8" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(500, BY + 28, "Docker 가 개념 위에 얹은 둘", 13, ACC, KR, "start", 600)
d.t(500, BY + 52, "컨테이너 이미지를 통한 표준화된 패키징", 11.5, ACC, KR, "start")
d.t(500, BY + 72, "사람 친화적인 사용자 인터페이스", 11.5, ACC, KR, "start")
d.t(500, BY + 90, "예: docker run 한 줄", 11.5, MUTED, KR, "start")

OY = BY + 112 + 16
d.tone(64, OY, 752, 40, MUTED)
d.t(84, OY + 26, "OCI 핵심 명세 셋의 바탕 — 런타임 · 이미지 포맷 · 배포",
    12, MUTED, KR, "start")

d.legend(OY + 40 + 24, [("같은 재료를 쓴 시도들", INFO), ("겨냥하는 사람이 바뀐 자리", ACC)])
d.save("06-02.container-history.svg")
print("ok 06-02.container-history")
