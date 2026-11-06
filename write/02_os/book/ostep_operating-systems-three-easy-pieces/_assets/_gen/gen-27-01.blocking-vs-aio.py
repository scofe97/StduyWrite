# 27-01 ### 2 — 같은 디스크 읽기를 블로킹 read() 로 하면 장치 대기 동안 이벤트 루프가 서고, aio_read() 로 넘기면 요청만 내고 돌아와 다른 이벤트를 처리한 뒤 aio_error()·aio_return() 으로 결과를 받는다.
# 본문 근거: 이 노트 ### 2 「블로킹 호출과 비동기 I/O」.
# 검증 근거: Linux 7.2.12 에서 evsrv.c 의 SLOW 요청(sleep 2초)이 진행 중일 때 0.3초 뒤 들어온 TIME 요청이 1,709 ms 뒤에 답함(macOS 1,708 ms).
#            같은 서버의 FILE 요청은 aio_read → aio_error → aio_return 순서로 400,001 바이트를 16 KiB 씩 읽어 원본과 cmp 로 동일함을 확인.
# 공식 근거: Linux man-pages 6.19 aio_read(3)(요청을 큐에 넣는 즉시 반환), aio_error(3)(EINPROGRESS·ECANCELED·0·양수 오류 번호), aio_return(3)(완료 뒤 한 번만 호출).
# 타입 스펙: type-swimlane — 두 레인(블로킹 호출·비동기 호출).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, OK, WARN, BAD, INFO, KR, MONO

W, H = 880, 432
d = D(W, H, "OSTEP · 27-01 §2",
      "블로킹 호출은 루프를 세우고 aio_read 는 루프를 계속 돌린다",
      "위 레인은 핸들러가 read() 를 부르면 장치 대기 동안 이벤트 루프가 멈추고 대기 중이던 요청이 그 뒤에야 처리되는 흐름이다. "
      "아래 레인은 핸들러가 aio_read() 로 요청만 내고 돌아와 루프가 다른 이벤트를 처리하다가, aio_error() 가 EINPROGRESS 가 아닌 값을 돌려주면 aio_return() 으로 읽은 바이트 수를 받는 흐름이다.",
      "막힐 수 있는 일을 루프 밖으로 넘겨야 루프가 선 채 기다리지 않습니다")

BW, BH, PITCH, X0 = 140, 76, 168, 24
LANE_X, LANE_W, LANE_H = 12, 856, 132
A_Y, B_Y = 96, 244


def lane(y, name):
    d.o.append(f'<rect x="{LANE_X}" y="{y}" width="{LANE_W}" height="{LANE_H}" rx="8" fill="{SOFT}0A" stroke="{SOFT}" stroke-width="0.9"/>')
    d.t(LANE_X + 12, y + 20, name, 12, MUTED, KR, "start", 600)


def lane_steps(y, items):
    by = y + 40
    for i, (title, sub, c) in enumerate(items):
        x = X0 + i * PITCH
        d.tone(x, by, BW, BH, c, 6, "14", 1.4 if c == ACC else 1.1)
        d.t(x + BW / 2, by + 32, title, 12.5, INK, KR, "middle", 600)
        d.t(x + BW / 2, by + 56, sub, 12, MUTED, KR)
        if i < len(items) - 1:
            d.path(f"M {x + BW + 2} {by + BH / 2} L {x + PITCH - 2} {by + BH / 2}", MUTED, 1.4, m="ar")


lane(A_Y, "블로킹 호출(read()·sleep())을 부른 경우")
lane_steps(A_Y, [
    ("핸들러", "이벤트 처리 시작", SOFT),
    ("read()", "디스크 요청", INFO),
    ("장치 대기", "이벤트 루프 정지", ACC),
    ("read() 반환", "처리 재개", INFO),
    ("다음 이벤트", "밀려 있던 요청", SOFT),
])
d.chip(680, A_Y + 16, "SLOW(2초) 동안 TIME 1,709 ms 지연", ACC, 12)

lane(B_Y, "aio_read() 로 넘긴 경우")
lane_steps(B_Y, [
    ("핸들러", "이벤트 처리 시작", SOFT),
    ("aio_read()", "요청만 내고 반환", INFO),
    ("다른 이벤트", "루프가 계속 돎", OK),
    ("aio_error()", "EINPROGRESS 아니면 끝", INFO),
    ("aio_return()", "읽은 바이트 수", INFO),
])

d.legend(392, [("응용의 핸들러", SOFT), ("I/O 를 맡기는 호출", INFO), ("루프가 멈추는 자리", ACC), ("루프가 도는 자리", OK)])
d.save("27-01.blocking-vs-aio.svg")
