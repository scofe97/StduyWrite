# 03-03.chapter-overview — 타임아웃은 Dialer·context 로, 유휴 감지는 데드라인과 하트비트로 건다
# 본문 요구(03-03 「학습 목표」 개념도 문단): 첫째 줄 오류 판별(§1), 둘째 줄 연결 타임아웃(§2), 셋째 줄 다중 다이얼 취소(§3),
#           넷째 줄 데드라인과 복구(§4), 다섯째 줄 하트비트와 데드라인 전진(§5).
# 타입 스펙: type-architecture — 키워드 개념도. 5행 × 3열 노드 격자, 행 안은 가로 화살표, 행 사이는 필요할 때만 세로 화살표 하나.
#           관계 라벨은 화살표 위(가로) 또는 오른쪽(세로)에 둔다. 열 x = 60 + j·340, 노드 216×64, 행 y = 112 + i·128.
#           왼쪽 44px 열에는 그 행을 다루는 절 칩.
# 사실 출처: Network Programming with Go Ch.3 Reliable TCP Data Streams (Listing 3-4~3-12),
#           net.Error, net.Dialer, context.WithDeadline, os.ErrDeadlineExceeded, Pinger.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, KR, MONO

COL_X, STRIDE, NW, NH = 60, 340, 216, 64
ROW_Y, ROW_STRIDE = 112, 128
W, H = 984, 768


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def nx(j):
    return COL_X + j * STRIDE


def ny(i):
    return ROW_Y + i * ROW_STRIDE


d = D(W, H, "ARCHITECTURE · 03-03 OVERVIEW",
      "타임아웃은 Dialer·context 로, 유휴 감지는 데드라인과 하트비트로 건다",
      "03-03 의 키워드 개념도. 1행은 net.Error 의 Timeout() 으로 치명적 오류를 가르는 흐름이다. "
      "2행은 net.Dialer 와 context.WithDeadline 으로 연결 시도에 한도를 두는 제어다. "
      "3행은 단일 context 로 10개 다이얼러를 띄워 첫 응답 수신 후 나머지를 cancel() 로 일괄 취소하는 확장이다. "
      "4행은 SetDeadline 으로 무기한 블로킹을 끊고 만료 후 시각을 연장해 연결을 복구하는 원리다. "
      "5행은 데이터를 읽을 때마다 Pinger 의 타이머를 리셋하고 데드라인을 함께 연장하는 흐름이다.",
      lead="화살표 위 글자는 두 키워드의 관계, 왼쪽 칩은 그 줄을 다루는 절입니다.")


def node(i, j, title, sub, c=None):
    x, y = nx(j), ny(i)
    if c:
        d.tone(x, y, NW, NH, c, 6, "14", 1.1)
    else:
        d.box(x, y, NW, NH)
    d.t(x + NW / 2, y + 27, title, 14, c or INK, kr(title), "middle", 600)
    d.t(x + NW / 2, y + 48, sub, 11, MUTED, kr(sub), "middle")


def harrow(i, j, label, c=SOFT, m="soft"):
    y = ny(i) + NH / 2
    x1, x2 = nx(j) + NW, nx(j + 1)
    d.arrow([(x1 + 2, y), (x2 - 4, y)], c, m, 1.3)
    d.t((x1 + x2) / 2, y - 9, label, 11, c if c != SOFT else MUTED, kr(label), "middle", 600)


def varrow(i, j, label):
    x = nx(j) + NW / 2
    y1, y2 = ny(i) + NH, ny(i + 1)
    d.arrow([(x, y1 + 2), (x, y2 - 4)], SOFT, "soft", 1.3)
    d.t(x + 10, (y1 + y2) / 2 + 4, label, 11, MUTED, kr(label), "start", 600)


for i, sec in enumerate(("§1", "§2", "§3", "§4", "§5")):
    d.chip(34, ny(i) + NH / 2 - 4, sec, MUTED, 11, 4)

node(0, 0, "net.Error", "오류 성격 검사")
node(0, 1, "Timeout()", "타임아웃 여부 판별", INFO)
node(0, 2, "치명적 오류", "재시도 없이 즉시 반환", WARN)
harrow(0, 0, "타입 단언")
harrow(0, 1, "false 면")

node(1, 0, "DialTimeout", "OS 기본 대기 방지")
node(1, 1, "WithDeadline", "5초 절대 시각 context", INFO)
node(1, 2, "ctx.Done()", "시한 만료 시 연결 중단", WARN)
harrow(1, 0, "context 로 바꾸면")
harrow(1, 1, "DialContext 에 주입")

node(2, 0, "단일 context", "10개 다이얼러에 주입")
node(2, 1, "첫 응답 수신", "<-res 로 승자 결정", OK)
node(2, 2, "패배 다이얼러 정리", "c.Close() 및 Done 탈출", INFO)
harrow(2, 0, "가장 먼저 성공 시")
harrow(2, 1, "cancel() 호출로")

node(3, 0, "SetDeadline", "5초 절대 시각 설정", INFO)
node(3, 1, "os.ErrDeadlineExceeded", "무기한 블로킹 탈출", WARN)
node(3, 2, "연결 객체 복구", "소켓 유지 후 후속 I/O", OK)
harrow(3, 0, "유휴 시한 만료")
harrow(3, 1, "미래 시각 재설정")

node(4, 0, "Pinger", "주기적 ping 전송", INFO)
node(4, 1, "타이머 리셋", "reset <- 0 으로 재설정")
node(4, 2, "데드라인 전진", "SetDeadline 으로 5초 연장", OK)
harrow(4, 0, "상대 데이터 수신 시")
harrow(4, 1, "같은 읽기에서 함께")

varrow(3, 0, "유휴 끊김 방지")

d.legend(712, [("시간 · 제어 장치", INFO), ("오류 · 만료", WARN), ("연결 유지 · 복구", OK)])
d.save("03-03.chapter-overview.svg")
print("ok 03-03 overview")
