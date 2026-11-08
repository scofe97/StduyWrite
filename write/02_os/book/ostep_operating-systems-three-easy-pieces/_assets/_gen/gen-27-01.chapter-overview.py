# 27-01 개념도 — 이벤트 루프와 select() 로 스레드 없이 동시 요청을 받고, 막히는 호출은 aio_read 로 넘기며, 비동기 뒤의 상태는 job_t 로 넘긴다.
# 본문 요구(27-01 「학습 목표」 개념도 문단): 1행 이벤트 루프·select()·락 불필요(§1), 2행 블로킹 호출·루프 정지·TIME 지연(§2),
#           3행 aio_read·aio_error·aio_return(§3), 4행 job_t·재호출·close(§4), 5행 스레드·이벤트·세 원칙(§5).
# 검증 근거: macOS(Darwin 25.6, 2026-11-08 재실행)에서 SLOW 뒤 TIME 지연 1,709 ms(Linux 7.2.12, macOS 재실행 1,702 ms), 400,001 바이트 FILE 은 aio_read 완료 25회(16,384 바이트 24회 + 6,785 바이트 1회)와 0 바이트 1회로 끝남.
# 공식 근거: Linux man-pages 6.19 select(2), aio_read(3), aio_error(3), aio_return(3).
# 타입 스펙: type-architecture — 키워드 개념도. 5행 × 3열 노드 격자(03-02 개념도와 같은 공식: 열 x = 60 + j·340, 노드 216×64), 행 안은 가로 화살표.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, KR, MONO

COL_X, STRIDE, NW, NH = 60, 340, 216, 64
ROW_Y, ROW_STRIDE = 112, 124
W, H = 984, 756


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def nx(j):
    return COL_X + j * STRIDE


def ny(i):
    return ROW_Y + i * ROW_STRIDE


d = D(W, H, "ARCHITECTURE · 27-01 OVERVIEW",
      "이벤트 루프는 막히는 일을 루프 밖으로 넘긴다",
      "27-01 의 키워드 개념도. 1행은 이벤트 루프가 select() 로 준비된 fd 를 골라 핸들러를 하나씩 돌리므로 락이 필요 없다는 구조다. "
      "2행은 핸들러 안의 블로킹 호출이 루프를 세워 다른 요청의 응답이 1,709 ms 밀린 실험이다. "
      "3행은 aio_read 로 요청만 내고 aio_error 로 완료를 확인한 뒤 aio_return 으로 읽은 바이트 수를 받는 비동기 읽기다. "
      "4행은 완료 핸들러가 쓸 소켓과 읽은 위치를 job_t 에 남겨 다음 aio_read 를 이어 내는 상태 넘기기다. "
      "5행은 스레드 서버와 이벤트 서버를 비교하고 병행성을 고르는 세 원칙으로 마무리한다.",
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


for i, sec in enumerate(("§1", "§2", "§3", "§4", "§5")):
    d.chip(34, ny(i) + NH / 2 - 4, sec, MUTED, 12)

node(0, 0, "이벤트 루프", "핸들러를 하나씩", INFO)
node(0, 1, "select()", "준비된 fd 만 남김", INFO)
node(0, 2, "락 불필요", "한 번에 핸들러 하나", OK)
harrow(0, 0, "fd 집합을 넘겨")
harrow(0, 1, "단일 CPU 에서")

node(1, 0, "블로킹 호출", "핸들러 안 sleep(2)", WARN)
node(1, 1, "루프 정지", "다음 이벤트를 못 꺼냄", ACC)
node(1, 2, "TIME 지연", "1,709 ms", WARN)
harrow(1, 0, "서버 전체가")
harrow(1, 1, "뒤 요청의 응답이")

node(2, 0, "aio_read()", "요청만 내고 반환", INFO)
node(2, 1, "aio_error()", "EINPROGRESS 확인", INFO)
node(2, 2, "aio_return()", "읽은 바이트 수", OK)
harrow(2, 0, "완료 여부를 묻고")
harrow(2, 1, "끝났으면 한 번만")

node(3, 0, "job_t {sd, off}", "continuation", WARN)
node(3, 1, "aio_read 재호출", "off 부터 다시", INFO)
node(3, 2, "n = 0 → close", "파일 끝", OK)
harrow(3, 0, "읽은 만큼 off 증가")
harrow(3, 1, "0 바이트를 받으면")

node(4, 0, "스레드 서버", "운영체제가 순서를 고름")
node(4, 1, "이벤트 서버", "응용이 순서를 고름")
node(4, 2, "세 원칙", "단순하게 · 필요할 때만", OK)
harrow(4, 0, "스케줄링 주체 이동")
harrow(4, 1, "어느 쪽도 정답 아님")

d.legend(716, [("호출 · 동작", INFO), ("결과 · 이점", OK), ("대가 · 위험", WARN), ("핵심 문제", ACC)])
d.save("27-01.chapter-overview.svg")
print("ok 27-01 overview")
