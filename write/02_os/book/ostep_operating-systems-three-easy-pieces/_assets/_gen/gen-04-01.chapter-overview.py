# 04-01 개념도 — 제한된 직접 실행은 프로그램을 CPU 에서 그대로 돌리되, trap 으로 커널에 들어가고 타이머 인터럽트로 통제권을 되찾으며, 프로세스 전환은 swtch 가 맡는다.
# 본문 요구(04-01 「학습 목표」 개념도 문단): 1행 직접 실행·통제 상실·제한된 직접 실행(§1), 2행 사용자 모드·trap·return-from-trap(§2),
#           3행 협력 방식·타이머 인터럽트·통제권 회수(§3), 4행 스케줄러·swtch·프로세스 B(§4), 5행 인터럽트 중 인터럽트·인터럽트 끄기·락(§5), 6행 시스템 콜 비용·문맥 교환 비용·비용 추정(§5), 7행 시스템 콜·Sentry·호스트 커널(§6).
# 값 근거: 개념도라 값은 없다.
# 공식 근거: OSTEP 6장 §6.1~§6.5, gVisor 플랫폼 문서(systrap·KVM).
# 타입 스펙: type-architecture — 키워드 개념도. 7행 × 3열 노드 격자(27-01 개념도와 같은 공식: 열 x = 60 + j·340, 노드 216×64), 행 안은 가로 화살표.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, KR, MONO

COL_X, STRIDE, NW, NH = 60, 340, 216, 64
ROW_Y, ROW_STRIDE = 112, 104
W, H = 984, 880


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def nx(j):
    return COL_X + j * STRIDE


def ny(i):
    return ROW_Y + i * ROW_STRIDE


d = D(W, H, "ARCHITECTURE · 04-01 OVERVIEW",
      "제한된 직접 실행은 속도를 지키면서 통제권을 놓지 않는다",
      "04-01 의 키워드 개념도. 1행은 프로그램을 CPU 에서 그대로 돌리면 빠르지만 통제를 잃으므로 제한된 직접 실행이 필요하다는 문제다. "
      "2행은 사용자 모드 프로그램이 trap 으로 커널에 들어갔다가 return-from-trap 으로 돌아오는 시스템 콜 경로다. "
      "3행은 협력 방식이 무한 루프 앞에서 막히므로 타이머 인터럽트로 통제권을 되찾는 방법이다. "
      "4행은 스케줄러가 프로세스를 바꾸기로 하면 swtch 가 커널 레지스터를 교체해 B 를 실행하는 문맥 교환이다. "
      "5행은 인터럽트 처리 중 또 인터럽트가 오는 문제와 그 대응이고, 6행은 시스템 콜과 문맥 교환의 비용을 재는 방법이며, 7행은 gVisor 가 시스템 콜을 처리하는 쪽을 Sentry 로 바꾸는 방식이다.",
      lead="화살표 위 글자는 두 키워드의 관계, 왼쪽 칩은 그 줄을 다루는 절입니다.")


def node(i, j, title, sub, c=None):
    x, y = nx(j), ny(i)
    if c:
        d.tone(x, y, NW, NH, c, 6, "14", 1.4 if c == ACC else 1.1)
    else:
        d.box(x, y, NW, NH)
    d.t(x + NW / 2, y + 27, title, 14, c or INK, kr(title), "middle", 600)
    d.t(x + NW / 2, y + 48, sub, 13, MUTED, kr(sub), "middle")


def harrow(i, j, label, c=SOFT, m="soft"):
    y = ny(i) + NH / 2
    x1, x2 = nx(j) + NW, nx(j + 1)
    d.arrow([(x1 + 2, y), (x2 - 4, y)], c, m, 1.3)
    d.t((x1 + x2) / 2, y - 9, label, 13, MUTED, kr(label), "middle", 600)


for i, sec in enumerate(("§1", "§2", "§3", "§4", "§5", "§5", "§6")):
    d.chip(34, ny(i) + NH / 2 - 4, sec, MUTED, 12)

node(0, 0, "직접 실행", "CPU 에서 그대로", INFO)
node(0, 1, "통제 상실", "아무 일이나 가능", WARN)
node(0, 2, "제한된 직접 실행", "속도와 통제를 함께", ACC)
harrow(0, 0, "제한이 없으면")
harrow(0, 1, "둘을 함께 얻으려")

node(1, 0, "사용자 모드", "제한된 연산만", INFO)
node(1, 1, "trap", "행선지는 trap table", INFO)
node(1, 2, "return-from-trap", "사용자 모드로 복귀", OK)
harrow(1, 0, "시스템 콜로")
harrow(1, 1, "일을 마치면")

node(2, 0, "협력 방식", "넘겨주길 기다림", WARN)
node(2, 1, "타이머 인터럽트", "하드웨어가 강제", ACC)
node(2, 2, "통제권 회수", "핸들러가 실행됨", OK)
harrow(2, 0, "무한 루프면")
harrow(2, 1, "일정 시간마다")

node(3, 0, "스케줄러", "계속할지 바꿀지", INFO)
node(3, 1, "swtch()", "커널 레지스터 교체", INFO)
node(3, 2, "프로세스 B 실행", "return-from-trap 으로", OK)
harrow(3, 0, "B 로 바꾸기로 하면")
harrow(3, 1, "스택을 바꾼 뒤")

node(4, 0, "인터럽트 중 인터럽트", "커널이 감당할 문제", WARN)
node(4, 1, "인터럽트 끄기", "처리 중엔 전달 안 됨", INFO)
node(4, 2, "락", "커널 자료 구조 보호", OK)
harrow(4, 0, "단순한 대응은")
harrow(4, 1, "자료 구조는")

node(5, 0, "시스템 콜 비용", "0 바이트 read 반복", INFO)
node(5, 1, "문맥 교환 비용", "파이프 두 개로 왕복", INFO)
node(5, 2, "비용 추정", "반복 횟수로 나눔", OK)
harrow(5, 0, "같은 방식으로")
harrow(5, 1, "CPU 하나에 묶고")

node(6, 0, "시스템 콜", "받는 쪽이 바뀜", INFO)
node(6, 1, "Sentry", "gVisor 의 응용 커널", ACC)
node(6, 2, "호스트 커널", "필요한 일만 받음", OK)
harrow(6, 0, "플랫폼이 가로채")
harrow(6, 1, "필요한 일만 요청")

d.legend(H - 40, [("호출 · 동작", INFO), ("결과 · 이점", OK), ("대가 · 위험", WARN), ("핵심 문제", ACC)])
d.save("04-01.chapter-overview.svg")
print("ok 04-01 overview")
