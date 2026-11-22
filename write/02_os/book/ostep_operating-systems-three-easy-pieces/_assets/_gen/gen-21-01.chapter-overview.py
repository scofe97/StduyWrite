# 21-01 개념도 — 만든 쪽 스레드와 새 스레드 두 줄 사이에, 값을 넘기고 받는 호출과 공유 변수를 지키는 락·신호가 어디에 끼는지.
# 본문 근거: 이 노트 1절(create 가 인자를 넘김), 2절(join 이 반환값을 받음), 3절(락이 공유 변수 둘레를 감쌈), 4절(wait 는 락을 놓고 잠들고 signal 이 깨움), 5절(링크와 지침).
# 값 근거: 개념 도식이라 값은 없다. 함수 이름과 인자 표기는 OSTEP 27장 §27.1~27.5 에 나오는 것만 쓴다.
# 공식 근거: OSTEP 27장 — pthread_create 는 시작 함수와 인자 하나를, pthread_join 은 반환값을 다룬다. 락은 임계 구역을 감싸고, 조건 변수는 wait 가 락을 놓고 잠든다.
# 타입 스펙: type-swimlane — 스레드 둘을 레인으로 놓고 레인을 가로지르는 화살표(인자·반환값·깨움)를 핸드오프로 그린다.
#   고른 이유: 이 장의 줄기는 「두 실행 흐름 사이에 네 도구가 끼는 자리」라서 행위자별 레인과 레인 경계를 넘는 화살표가 그대로 맞다.
#   스펙에 공식이 없어 좌표는 4 의 배수로 잡았다. 레인 사이 가운데 띠에 공유 변수를 두어 두 레인이 함께 건드리는 자리를 보인다.
#   (옛 판의 다섯 단계 가로 표는 쓰지 않는다.)
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, INFO, KR, MONO

W, H = 984, 608


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


d = D(W, H, "SWIMLANE · 21-01 OVERVIEW",
      "만든 쪽과 새 스레드 사이에 인자·반환값·락·신호가 끼는 자리",
      "21-01 의 키워드 개념도. 위 줄은 스레드를 만드는 쪽이고 아래 줄은 새 스레드다. "
      "pthread_create 가 새 줄을 시작시키며 인자를 넘기고, 새 줄이 끝나면 pthread_join 이 반환값을 받는다. "
      "두 줄이 함께 건드리는 공유 변수는 가운데 있고 pthread_mutex_lock 과 unlock 이 그 둘레를 감싼다. "
      "pthread_cond_wait 는 락을 놓고 잠들고 pthread_cond_signal 이 깨운다. 빌드와 사용 지침은 곁가지다.")


def node(x, y, w, h, title, sub, c, sec):
    d.tone(x, y, w, h, c, 6, "14", 1.1)
    d.chip(x + 24, y + 14, sec, c, 11)
    d.t(x + w / 2, y + 40, title, 14, c, kr(title), "middle", 600)
    d.t(x + w / 2, y + 58, sub, 13, MUTED, kr(sub), "middle")


# 레인 둘
LX, LW = 24, 936
for y, name in ((104, "만든 쪽 스레드"), (436, "새 스레드")):
    d.box(LX, y, LW, 100, "#161B22", RULE, 1.0, 8)
    d.t(LX + 16, y + 54, name, 13, MUTED, KR, "start", 600)

# 레인 안 노드 — 세 열
NW, NH = 184, 64
C1, C2, C3 = 184, 468, 752
TOP, BOT = 124, 456
node(C1, TOP, NW, NH, "pthread_create", "시작 함수와 인자 하나", INFO, "§1")
node(C2, TOP, NW, NH, "pthread_cond_wait", "락을 놓고 잠듦", OK, "§4")
node(C3, TOP, NW, NH, "pthread_join", "끝나기를 기다림", INFO, "§2")
node(C1, BOT, NW, NH, "시작 함수", "void * 받고 돌려줌", INFO, "§1")
node(C2, BOT, NW, NH, "pthread_cond_signal", "조건이 바뀌었음을 알림", OK, "§4")
node(C3, BOT, NW, NH, "스레드가 끝남", "반환값은 heap 에", INFO, "§2")

# 가운데 띠 — 락이 감싼 공유 변수
FX, FY, FW, FH = 440, 260, 240, 124
d.tone(FX, FY, FW, FH, OK, 6, "14", 1.1)
d.chip(FX + 24, FY + 14, "§3", OK, 11)
d.t(FX + FW / 2, FY + 42, "pthread_mutex_lock · unlock", 12, OK, MONO, "middle", 600)
d.tone(FX + 16, FY + 56, FW - 32, 56, ACC, 6, "1e", 1.4)
d.t(FX + FW / 2, FY + 82, "공유 변수", 14, ACC, KR, "middle", 700)
d.t(FX + FW / 2, FY + 100, "건드리는 순서가 정확성", 13, MUTED, KR, "middle")

# 가운데 열 — 락을 쥐고 공유 변수를 건드린다
d.arrow([(560, 190), (560, 258)], OK, "ok", 1.5)
d.t(572, 228, "락을 쥐고 확인", 13, MUTED, KR, "start", 600)
d.arrow([(560, 454), (560, 386)], OK, "ok", 1.5)
d.t(572, 424, "락을 쥐고 바꿈", 13, MUTED, KR, "start", 600)

# 레인을 가로지르는 값의 이동 — 인자는 아래로, 반환값은 위로
d.arrow([(276, 190), (276, 454)], INFO, "info", 1.5)
d.t(288, 326, "인자를 넘김", 13, MUTED, KR, "start", 600)
d.arrow([(844, 454), (844, 190)], INFO, "info", 1.5)
d.t(856, 326, "반환값을 받음", 13, MUTED, KR, "start", 600)

# 신호 — 아래 줄이 알리면 위 줄이 깨어난다
d.arrow([(654, 488), (702, 488), (702, 156), (654, 156)], OK, "ok", 1.5)
d.t(714, 326, "깨움", 13, MUTED, KR, "start", 600)

# 곁가지 — 빌드와 사용 지침
node(24, 288, 146, 64, "빌드와 사용 지침", "-pthread 로 링크", MUTED, "§5")

d.legend(H - 40, [("생성 · 값 전달", INFO), ("락 · 신호", OK), ("핵심 한 곳", ACC), ("곁가지", MUTED)])
d.save("21-01.chapter-overview.svg")
print("ok 21-01 chapter-overview")
