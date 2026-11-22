# 20-01 개념도 — 스레드가 주소 공간을 함께 쓰고 실행 순서가 정해지지 않는 두 사실이 한 자리에서 만나 갱신 하나를 지우고, 그 구간을 한 번에 한 스레드만 지나게 하는 길이 뒤따른다.
# 본문 요구(20-01 「학습 목표」 개념도 문단): 왼쪽 원인 둘(스레드 §1, 주소 공간 공유 §1, 실행 순서 비결정 §3, 곁가지로 쓰는 이유 §2),
#           가운데 경쟁 상태 장면(§4), 오른쪽 대응(임계 구역·상호 배제·원자성·동기화 기본 요소 §5, 조건 변수 예고 §5).
# 값 근거: OSTEP 26장 그림 26.7 — 카운터는 50 에서 51 로만 늘고 올바른 값은 52 다(본문 「갱신이 사라지는 순서」).
# 공식 근거: OSTEP 26장 §26.1~§26.5 (VERSION 1.10).
# 타입 스펙: type-architecture — 구성요소를 존으로 묶고 라벨 붙은 화살표로 잇는 노드 그래프. 고른 이유: 이 장의 줄기가
#             「두 원인이 한 사건으로 모이고 대응이 이어진다」는 인과 합류라 순서표나 격자로는 모임이 안 보인다. 합류하는 화살표와
#             존 세 칸을 그릴 수 있는 가장 가까운 타입이라 골랐다. 스펙에 합류 전용 공식은 없어 좌표는 4 의 배수 stride 로 직접 잡았다.
#             (옛 판의 6행 × 3열 격자 공식 열 x = 60 + j·340 은 쓰지 않는다.)
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, INFO, KR, MONO

W, H = 984, 700


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


d = D(W, H, "ARCHITECTURE · 20-01 OVERVIEW",
      "주소 공간 공유와 실행 순서가 만나 갱신이 사라지고 상호 배제가 필요하다",
      "20-01 의 키워드 개념도. 왼쪽에서 스레드가 두 사실을 낳는다. 하나는 주소 공간을 함께 쓴다는 것이고 다른 하나는 실행 순서를 스케줄러가 정해 미리 알 수 없다는 것이다. "
      "두 사실은 가운데 한 자리에서 만난다. 공유 카운터를 읽고 더하고 쓰는 사이에 전환이 끼어들면 스레드 1 이 읽은 값으로 덮어써 갱신 하나가 사라지고 카운터는 52 가 아니라 51 이 된다. "
      "오른쪽은 그 구간을 임계 구역으로 보고 상호 배제로 지키는 길이다. 그러려면 원자성이 필요하고 하드웨어와 운영체제가 동기화 기본 요소를 만든다. 조건 변수는 뒤 장들의 몫이다.",
      lead="화살표 위 글자는 두 요소의 관계, 칩은 그 요소를 다루는 절, 왼쪽에서 오른쪽으로 읽습니다.")


def node(x, y, w, h, title, sub, c, sec, sub2=None):
    d.tone(x, y, w, h, c, 6, "14", 1.1)
    d.chip(x + 24, y + 14, sec, c if c != MUTED else MUTED, 11)
    d.t(x + w / 2, y + 40, title, 14, c, kr(title), "middle", 600)
    d.t(x + w / 2, y + 58, sub, 13, MUTED, kr(sub), "middle")
    if sub2:
        d.t(x + w / 2, y + 74, sub2, 13, MUTED, kr(sub2), "middle")


# 구역 머리
for x, x2, cap in ((24, 336, "원인"), (456, 696, "깨지는 장면"), (804, 950, "막는 길")):
    d.t(x, 112, cap, 13, MUTED, KR, "start", 600)
    d.line(x, 120, x2, 120, RULE, 0.8)

# 구역 1 — 원인 둘
C0, C1 = 24, 204
node(C0, 340, 132, 64, "스레드", "실행 지점이 여럿", INFO, "§1")
node(C1, 200, 132, 64, "주소 공간 공유", "코드·힙·전역 변수", INFO, "§1")
node(C1, 476, 132, 64, "실행 순서 비결정", "스케줄러가 정함", INFO, "§3")
node(C0, 460, 132, 84, "쓰는 두 이유", "병렬성", MUTED, "§2", "입출력 겹치기")
d.arrow([(158, 372), (180, 372), (180, 232), (202, 232)], SOFT, "soft", 1.3)
d.arrow([(158, 372), (180, 372), (180, 508), (202, 508)], SOFT, "soft", 1.3)
d.arrow([(90, 406), (90, 456)], SOFT, "soft", 1.3, "4 3")

# 구역 2 — 깨지는 장면 (가장 크게)
SX, SY, SW, SH = 456, 132, 240, 480
d.box(SX, SY, SW, SH, "#161B22", RULE, 1.0, 8)
d.t(SX + 16, SY + 30, "경쟁 상태", 17, INK, KR, "start", 700)
d.chip(SX + SW - 28, SY + 24, "§4", MUTED, 11)
d.t(SX + 16, SY + 52, "공유 카운터 갱신", 13, MUTED, KR, "start")
steps = (("스레드 1", "읽고 더함 · eax 51"),
         ("전환 · 스레드 2", "50 을 읽고 51 을 씀"),
         ("스레드 1 이 돌아옴", "eax 51 을 씀"))
for i, (a, b) in enumerate(steps):
    y = 204 + i * 100
    d.tone(SX + 16, y, 208, 60, INFO, 6, "14", 1.1)
    d.t(SX + SW / 2, y + 26, a, 14, INFO, KR, "middle", 600)
    d.t(SX + SW / 2, y + 46, b, 13, MUTED, KR, "middle")
    if i < 2:
        d.arrow([(SX + SW / 2, y + 63), (SX + SW / 2, y + 97)], MUTED, "ar", 1.3)
d.arrow([(SX + SW / 2, 467), (SX + SW / 2, 497)], ACC, "acc", 1.4)
d.tone(SX + 16, 500, 208, 96, ACC, 6, "1e", 1.4)
d.t(SX + SW / 2, 530, "잃어버린 갱신", 16, ACC, KR, "middle", 700)
d.t(SX + SW / 2, 554, "counter 는 50 에서 51 로만", 13, MUTED, KR, "middle")
d.t(SX + SW / 2, 574, "올바른 값은 52", 13, MUTED, KR, "middle")

# 두 원인이 가운데로 모이는 화살표
d.arrow([(338, 232), (454, 232)], INFO, "info", 1.5)
d.t(396, 222, "함께 쓰므로", 13, MUTED, KR, "middle", 600)
d.arrow([(338, 508), (454, 508)], INFO, "info", 1.5)
d.t(396, 498, "전환이 끼어들면", 13, MUTED, KR, "middle", 600)

# 구역 3 — 막는 길
C3, NW3, NH3 = 804, 146, 64
nodes3 = (("임계 구역", "공유 변수를 만짐", INFO, "§5"),
          ("상호 배제", "한 번에 한 스레드", OK, "§5"),
          ("원자성", "전부 아니면 전무", OK, "§5"),
          ("동기화 기본 요소", "하드웨어와 운영체제", OK, "§5"),
          ("조건 변수", "뒤 장들의 몫", MUTED, "§5"))
labels3 = ("바라는 성질", "얻으려면", "얻는 길", "뒤 장들")
for i, (a, b, c, s) in enumerate(nodes3):
    node(C3, 132 + i * 104, NW3, NH3, a, b, c, s)
for i, lab in enumerate(labels3):
    y0 = 132 + i * 104 + NH3
    m = "ok" if i < 3 else "soft"
    cc = OK if i < 3 else SOFT
    d.arrow([(830, y0 + 3), (830, y0 + 37)], cc, m, 1.4, None if i < 3 else "4 3")
    d.t(842, y0 + 25, lab, 13, MUTED, KR, "start", 600)
d.arrow([(698, 164), (802, 164)], INFO, "info", 1.5)
d.t(750, 154, "그 구간이", 13, MUTED, KR, "middle", 600)

d.legend(H - 40, [("전제 · 문제", INFO), ("대응", OK), ("핵심 문제", ACC), ("곁가지 · 예고", MUTED)])
d.save("20-01.chapter-overview.svg")
print("ok 20-01 overview")
