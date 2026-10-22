# 타입 스펙: type-architecture — 키워드 개념도. 리스크·위협·완화 용어에서 출발해 공격 벡터와 체이닝, 보안 경계, 멀티테넌시를 거쳐 보안 원칙으로 가는 3행 × 3열 노드 격자. focal 은 보안 경계.
# 사실 출처: 노트 L21~L23(핵심 요약), L49~L51(세 용어), L65~L67·L83(공격 벡터 9종), L103~L109(보안 경계), L115~L120(체이닝), L122·L128(멀티테넌시), L160(컨테이너 < VM), L178~L190(원칙 5가지)
import sys, pathlib
ASSETS = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ASSETS))
from dd import D, INK, MUTED, SOFT, ACC, OK, BAD, INFO, KR, MONO

COL_X, STRIDE, NW, NH = 60, 340, 216, 64
ROW_Y, ROW_STRIDE = 112, 128
W, H = 984, 536


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def fit(t, size, limit):
    w = sum(size if "가" <= c <= "힣" else size * 0.62 for c in t)
    assert w <= limit, (t, w, limit)


def nx(j):
    return COL_X + j * STRIDE


def ny(i):
    return ROW_Y + i * ROW_STRIDE


d = D(W, H, "ARCHITECTURE · 01-01 OVERVIEW",
      "컨테이너 보안은 새 경계를 어디에 세우고 어떻게 지킬지의 문제입니다",
      "01-01 의 키워드 개념도. 윗줄은 리스크가 위협을 거쳐 완화로 이어지는 용어 구분이다. "
      "가운데 줄은 공격 벡터 9종이 체이닝으로 이어져 보안 경계를 넘는 모습이다. "
      "아랫줄은 경계의 강도를 정하는 멀티테넌시와 그 판단에 쓰는 보안 원칙이다.",
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


def harrow(i, j, label):
    y = ny(i) + NH / 2
    x1, x2 = nx(j) + NW, nx(j + 1)
    d.arrow([(x1 + 2, y), (x2 - 4, y)], SOFT, "soft", 1.3)
    d.t((x1 + x2) / 2, y - 9, label, 12, MUTED, kr(label), "middle", 600)


def wrap(i, label):
    # 오른쪽 끝 노드 아래에서 내려와 왼쪽 끝 노드 위로 들어가는 줄 바꿈 화살표
    xa, xb = nx(2) + NW / 2, nx(0) + NW / 2
    y1, y2 = ny(i) + NH, ny(i + 1)
    ym = y1 + 32
    d.arrow([(xa, y1 + 2), (xa, ym), (xb, ym), (xb, y2 - 4)], SOFT, "soft", 1.3)
    d.t((xa + xb) / 2, ym - 7, label, 12, MUTED, kr(label), "middle", 600)


for i, sec in enumerate(("§1", "§2~3", "§4~5")):
    d.chip(34, ny(i) + NH / 2 - 4, sec, MUTED, 11, 4)

node(0, 0, "리스크", "문제와 그 여파")
node(0, 1, "위협", "리스크에 이르는 경로", BAD)
node(0, 2, "완화", "경로를 막는 대응책", OK)
harrow(0, 0, "가는 길")
harrow(0, 1, "막는 것")
wrap(0, "위협 모델로 이어짐")

node(1, 0, "공격 벡터 9종", "생애주기 단계별", BAD)
node(1, 1, "체이닝 4단계", "벡터를 이어 붙임", BAD)
node(1, 2, "보안 경계", "넘으려면 다른 권한", ACC)
harrow(1, 0, "이어 붙임")
harrow(1, 1, "차례로 넘음")
wrap(1, "강도는 공유가 정함")

node(2, 0, "멀티테넌시", "누구와 무엇을 공유")
node(2, 1, "컨테이너 < 가상머신", "커널 공유 대 분리")
node(2, 2, "보안 원칙 5가지", "최소 권한 · 심층 방어 외", OK)
harrow(2, 0, "격리 강도")
harrow(2, 1, "판단 잣대")

d.legend(472, [("공격 쪽", BAD), ("핵심 접점", ACC), ("방어 쪽", OK)])
d.save(str(ASSETS / "01-01.chapter-overview.svg"))
print("ok 01-01 overview")
