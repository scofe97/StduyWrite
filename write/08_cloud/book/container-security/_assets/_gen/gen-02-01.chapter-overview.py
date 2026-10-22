# 타입 스펙: type-architecture — 키워드 개념도. 시스템 콜 → 파일 권한 → setuid, 그 후계자 capability, 어긋난 끝의 권한 상승, 막는 세 방법으로 이어지는 3행 × 3열 노드 격자. focal 은 권한 상승.
# 사실 출처: 노트 L21~L23(핵심 요약), L49~L62(시스템 콜), L74~L86(DAC·s 비트), L94~L105(setuid), L142·L152~L166(capability), L190~L198(권한 상승), L227~L230(해법)
import sys, pathlib
ASSETS = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ASSETS))
from dd import D, INK, MUTED, SOFT, ACC, OK, BAD, INFO, KR, MONO

COL_X, STRIDE, NW, NH = 60, 340, 216, 64
ROW_Y, ROW_STRIDE = 112, 120
W, H = 984, 500


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def fit(t, size, limit):
    w = sum(size if "가" <= c <= "힣" else size * 0.62 for c in t)
    assert w <= limit, (t, w, limit)


def nx(j):
    return COL_X + j * STRIDE


def ny(i):
    return ROW_Y + i * ROW_STRIDE


d = D(W, H, "ARCHITECTURE · 02-01 OVERVIEW",
      "시스템 콜과 파일 권한 위에 setuid 와 capability 가 얹히고, 어긋나면 권한 상승입니다",
      "02-01 의 키워드 개념도. 윗줄은 시스템 콜, 파일 권한 DAC, s 비트가 켜지는 setuid 가 이어지는 모습이다. "
      "가운데 줄은 setuid 를 잘게 쪼갠 capability, 필요 이상 부여하면 닿는 권한 상승, 컨테이너가 기본 root 라 경로가 짧아지는 모습이다. "
      "아랫줄은 권한 상승을 막는 setcap, no-new-privileges, 비root 실행 세 가지다.",
      lead="화살표 위 글자는 두 키워드의 관계, 왼쪽 칩은 그 줄을 다루는 절입니다.")


def node(i, j, title, sub, c=None):
    x, y = nx(j), ny(i)
    fit(title, 13, NW - 16)
    fit(sub, 12, NW - 16)
    if c:
        d.tone(x, y, NW, NH, c, 6, "14", 1.4 if c == ACC else 1.1)
    else:
        d.box(x, y, NW, NH)
    d.t(x + NW / 2, y + 27, title, 13, c or INK, kr(title), "middle", 600)
    d.t(x + NW / 2, y + 48, sub, 12, MUTED, kr(sub), "middle")


def harrow(i, j, label, back=False):
    y = ny(i) + NH / 2
    x1, x2 = nx(j) + NW, nx(j + 1)
    if back:
        d.arrow([(x2 - 2, y), (x1 + 4, y)], SOFT, "soft", 1.3)
    else:
        d.arrow([(x1 + 2, y), (x2 - 4, y)], SOFT, "soft", 1.3)
    d.t((x1 + x2) / 2, y - 9, label, 12, MUTED, kr(label), "middle", 600)


def wrap(i, label):
    # 오른쪽 끝 노드 아래에서 내려와 왼쪽 끝 노드 위로 들어가는 줄 바꿈 화살표
    xa, xb = nx(2) + NW / 2, nx(0) + NW / 2
    y1, y2 = ny(i) + NH, ny(i + 1)
    ym = y1 + 28
    d.arrow([(xa, y1 + 2), (xa, ym), (xb, ym), (xb, y2 - 4)], SOFT, "soft", 1.3)
    d.t((xa + xb) / 2, ym - 7, label, 12, MUTED, kr(label), "middle", 600)


for i, sec in enumerate(("§1~3", "§4~5", "해법")):
    d.chip(34, ny(i) + NH / 2 - 4, sec, MUTED, 11, 4)

node(0, 0, "시스템 콜", "300여 종 · 커널 하나")
node(0, 1, "파일 권한 · DAC", "rwx 세 묶음")
node(0, 2, "setuid 비트", "chmod +s · 소유자의 uid")
harrow(0, 0, "똑같이 필요")
harrow(0, 1, "추가 권한")
wrap(0, "잘게 쪼갠 후계자")

node(1, 0, "capability", "setcap cap_net_raw+p", INFO)
node(1, 1, "권한 상승", "원래 권한을 넘어섬", ACC)
node(1, 2, "컨테이너는 기본 root", "탈출하면 호스트 root", BAD)
harrow(1, 0, "과다 부여")
harrow(1, 1, "경로를 짧게", back=True)

# 권한 상승 아래로 내려가 세 해법으로 갈라지는 버스
bx = nx(1) + NW / 2
by = ny(1) + NH + 28
d.line(nx(0) + NW / 2, by, nx(2) + NW / 2, by, SOFT, 1.3)
d.arrow([(bx, ny(1) + NH + 2), (bx, ny(2) - 4)], SOFT, "soft", 1.3)
d.arrow([(nx(0) + NW / 2, by), (nx(0) + NW / 2, ny(2) - 4)], SOFT, "soft", 1.3)
d.arrow([(nx(2) + NW / 2, by), (nx(2) + NW / 2, ny(2) - 4)], SOFT, "soft", 1.3)
d.t(bx + 12, by - 7, "막는 방법", 12, MUTED, KR, "start", 600)

node(2, 0, "setcap 한 조각만", "setuid 대신", OK)
node(2, 1, "no-new-privileges", "--security-opt", OK)
node(2, 2, "비root 로 실행", "탈출해도 곧바로 root 아님", OK)

d.legend(456, [("권한 상승", ACC), ("위험", BAD), ("해법", OK), ("capability", INFO)])
d.save(str(ASSETS / "02-01.chapter-overview.svg"))
print("ok 02-01 overview")
