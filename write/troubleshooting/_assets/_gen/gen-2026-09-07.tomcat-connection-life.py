# 2026-09-07 D1 곁가지 — accept 큐 100 과 max-connections 8192 와 스레드 200 이
# 왜 동시에 말이 되는가. 학습자가 "100개인데 8192를 어떻게 무느냐"고 물어 남긴다.
# 타입 스펙: type-state — 연결 하나의 상태 전이. 전이 라벨은 무엇이 그 전이를 일으키는지를
#           적고, focal 은 세 상한이 어긋나 보이게 만드는 상태 하나(keep-alive idle).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, INFO, PAPER2, RULE, KR, MONO

W, H = 836, 664
X = [148, 406, 664]
SW, SH = 200, 68
Y1, Y2, Y3 = 144, 304, 448

d = D(W, H, "TROUBLESHOOTING DRILL · 2026-09-07 D1",
      "톰캣 연결 하나의 수명",
      "accept 큐와 연결 목록과 스레드 풀은 서로 다른 구간을 센다. 한 연결이 이 상태들을 지나는 동안 "
      "어느 상한에 걸리는지가 달라지기 때문에, 100 과 8192 와 200 이 동시에 성립한다.",
      lead="keep-alive 로 쉬는 연결은 목록을 차지하지만 스레드는 쓰지 않습니다")

def state(cx, y, name, sub, cap, c=None, focal=False, cap_right=False):
    if focal or c:
        d.tone(cx - SW / 2, y, SW, SH, c or ACC, 6)
    else:
        d.box(cx - SW / 2, y, SW, SH, PAPER2, RULE, 1.0, 6)
    col = (c or ACC) if (focal or c) else INK
    d.t(cx, y + 26, name, 13, col, KR, "middle", 600)
    d.t(cx, y + 46, sub, 11, MUTED, KR)
    # 오른쪽 끝 열은 바깥으로 나가므로 캡션을 상자 아래에 둔다.
    d.t(cx, y + SH + 18, cap, 11, SOFT, MONO)

d.arrow([(X[0] + SW / 2, Y1 + SH / 2), (X[1] - SW / 2 - 4, Y1 + SH / 2)], MUTED, "ar", 1.4)
d.arrow([(X[1] + SW / 2, Y1 + SH / 2), (X[2] - SW / 2 - 4, Y1 + SH / 2)], MUTED, "ar", 1.4)
d.arrow([(X[2] - 48, Y1 + SH), (X[2] - 48, Y2 - 4)], MUTED, "ar", 1.4)
d.arrow([(X[2] + 48, Y2), (X[2] + 48, Y1 + SH + 4)], ACC, "ar", 1.4)
d.arrow([(X[2], Y2 + SH), (X[2], Y3 - 4)], SOFT, "ar", 1.2, dash="4 4")

state(X[0], Y1, "accept 큐 대기", "커널이 물고 있음", "accept-count 100")
state(X[1], Y1, "수락됨", "톰캣이 목록에 등록", "max-connections 8192")
state(X[2], Y1, "요청 처리 중", "스레드 점유", "threads.max 200")
state(X[2], Y2, "keep-alive 유휴", "스레드 반납 · 연결 유지", "max-connections 8192", focal=True, cap_right=True)
state(X[2], Y3, "종료", "목록에서 빠짐", "", c=INFO)

d.t((X[0] + X[1]) / 2, Y1 + 8, "accept()", 11, MUTED, MONO)
d.t((X[1] + X[2]) / 2, Y1 + 8, "요청 도착", 11, MUTED, KR)
d.t(X[2] - 56, Y2 - 24, "응답 완료", 11, MUTED, KR, "end")
d.t(X[2] + 56, Y2 - 24, "다음 요청", 11, ACC, KR, "start", 600)
d.t(X[2] + 16, Y3 - 24, "keep-alive 타임아웃", 11, SOFT, KR, "start")

d.t(36, Y3 + 92, "대기 줄은 통과 지점입니다. 톰캣이 계속 꺼내가므로 평소엔 비어 있고, 꺼내가는 속도보다", 12, INK, KR, "start")
d.t(36, Y3 + 114, "들어오는 속도가 빠른 순간에만 100 이 찹니다. 그래서 큐를 늘리는 것은 시간을 버는 일이고,", 12, MUTED, KR, "start")
d.t(36, Y3 + 136, "원인 제거는 앱이 왜 못 꺼내가는지를 고치는 쪽입니다.", 12, MUTED, KR, "start")

d.legend(H - 52, [("스레드를 안 쓰면서 목록만 차지하는 상태", ACC), ("연결 종료", INFO)])
d.save("2026-09-07.tomcat-connection-life.svg")
print("ok tomcat-connection-life")
