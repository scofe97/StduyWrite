# 12-01.channel-states — 채널이 지나는 상태와 상태마다 읽기·쓰기·닫기가 하는 일
# 본문 요구(12-01 §3 「채널의 상태별 동작」): 원문 표 12-1 을 이 노트의 go1.25.1 에서 직접 확인한 것.
#           원문의 "버퍼 있음·열림" 열은 빔·값 하나·가득으로 나눴고, 닫힌 버퍼 채널은 값을 다 읽으면
#           버퍼 없는 닫힌 채널과 같은 상태(닫힘 · 빔)로 합류한다.
# 타입 스펙: type-state — 상태는 둥근 상자, 시작은 채운 점, 전이 라벨은 사건(ch <- 7 · <-ch · close).
#           panic 은 종료 노드 하나로 모으고 "쓰기 · 닫기" 한 라벨로 잇는다(모든 상태에서 화살표를 긋지 않는다).
#           격자: 노드 220×124, 열 stride 310(간격 90), 행 stride 220(간격 96). viewBox 폭 1000.
#           focal 은 두 갈래가 합류하는 "닫힘 · 빔" 한 곳.
# 사실 출처: Learning Go 2판 12장 표 12-1 「How channels behave」, go1.25.1 로컬 실행(2026-10-27) —
#           cap 2 채널의 len 0·1·2, 버퍼 없는 채널 len 0 cap 0, 닫힌 채널 읽기 8 true → 9 true → 0 false,
#           panic 메시지 send on closed channel · close of closed channel · close of nil channel.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, BAD, PAPER2, KR, MONO

W, H = 1000, 748
NW, NH = 220, 124
CX = [100, 410, 720]          # 열 x, stride 310
RY = [112, 332, 552]          # 행 y, stride 220
TONE = {"ok": OK, "wait": INFO, "hang": WARN, "bad": BAD}

d = D(W, H, "STATE · 12-01 §3",
      "채널이 지나는 상태와 상태마다 읽기·쓰기·닫기가 하는 일",
      "cap 2 버퍼 채널은 쓰기마다 빔에서 값 하나, 가득으로 가고 읽기마다 되돌아온다. 빔에서 읽기는 쓸 때까지, 가득에서 쓰기는 읽을 때까지 기다린다. "
      "열린 채널을 close 하면 닫힘 상태가 되고, 값이 남았으면 남은 값과 true 를 차례로 돌려준 뒤 닫힘 · 빔이 된다. "
      "버퍼 없는 채널도 close 하면 같은 닫힘 · 빔으로 가며, 여기서 읽기는 제로 값과 false 다. "
      "닫힌 채널에 쓰거나 다시 닫으면 panic, nil 채널은 읽기·쓰기가 영원히 멈추고 닫으면 panic 이다.",
      lead="상자 안 세 줄은 그 상태에서 읽기·쓰기·닫기를 했을 때의 결과입니다. 버퍼 있는 채널은 cap 2 기준입니다.")


def node(x, y, name, sub, rows, focal=False):
    if focal:
        d.tone(x, y, NW, NH, ACC, 8, "12", 1.4)
    else:
        d.box(x, y, NW, NH, PAPER2, RULE, 1.0, 8)
    d.t(x + NW / 2, y + 24, name, 13, INK, KR, "middle", 600)
    d.t(x + NW / 2, y + 44, sub, 12, MUTED, MONO)
    for i, (op, res, lv) in enumerate(rows):
        yy = y + 72 + i * 20
        d.t(x + 18, yy, op, 13, MUTED, KR, "start")
        d.t(x + 58, yy, res, 13, TONE[lv], MONO if res.isascii() else KR, "start", 600)


def start(x, y, label):
    d.o.append(f'<circle cx="{x}" cy="{y}" r="6" fill="{INK}"/>')
    d.arrow([(x + 8, y), (CX[0] - 4, y)], MUTED, "ar", 1.4)
    d.t((x + CX[0]) / 2 + 2, y - 12, label, 12, MUTED, MONO)


# 1행: 열린 버퍼 채널(cap 2)
node(CX[0], RY[0], "열림 · 빔", "len 0 · cap 2",
     [("읽기", "쓸 때까지 기다림", "wait"), ("쓰기", "버퍼에 넣음", "ok"), ("닫기", "닫힘 · 빔으로", "ok")])
node(CX[1], RY[0], "열림 · 값 하나", "len 1 · cap 2",
     [("읽기", "맨 앞 값을 읽음", "ok"), ("쓰기", "버퍼에 넣음", "ok"), ("닫기", "닫힘 · 값 남음으로", "ok")])
node(CX[2], RY[0], "열림 · 가득", "len 2 · cap 2",
     [("읽기", "맨 앞 값을 읽음", "ok"), ("쓰기", "읽을 때까지 기다림", "wait"), ("닫기", "닫힘 · 값 남음으로", "ok")])
start(44, RY[0] + 62, "make")

# 2행: 닫힌 상태와 panic
node(CX[0], RY[1], "닫힘 · 빔", "len 0",
     [("읽기", "0, false", "ok"), ("쓰기", "PANIC", "bad"), ("닫기", "PANIC", "bad")], focal=True)
node(CX[1], RY[1], "닫힘 · 값 남음", "len 1~2",
     [("읽기", "남은 값, true", "ok"), ("쓰기", "PANIC", "bad"), ("닫기", "PANIC", "bad")])
d.tone(CX[2], RY[1], NW, NH, BAD, 8, "16", 1.2)
d.t(CX[2] + NW / 2, RY[1] + 30, "PANIC", 15, BAD, MONO, "middle", 600)
for i, msg in enumerate(["send on closed channel", "close of closed channel", "close of nil channel"]):
    d.t(CX[2] + NW / 2, RY[1] + 62 + i * 20, msg, 12, MUTED, MONO)

# 3행: 버퍼 없는 채널과 nil 채널
node(CX[0], RY[2], "열림 · 버퍼 없음", "len 0 · cap 0",
     [("읽기", "상대가 쓸 때까지", "wait"), ("쓰기", "상대가 읽을 때까지", "wait"), ("닫기", "닫힘 · 빔으로", "ok")])
start(44, RY[2] + 62, "make")
node(CX[1], RY[2], "nil", "var ch chan int",
     [("읽기", "영원히 멈춤", "hang"), ("쓰기", "영원히 멈춤", "hang"), ("닫기", "PANIC", "bad")])

# 1행 전이: 쓰기는 오른쪽, 읽기는 왼쪽
for a, b, w in ((0, 1, "ch <- 7"), (1, 2, "ch <- 8")):
    x1, x2 = CX[a] + NW, CX[b]
    y = RY[0] + 48
    d.arrow([(x1 + 4, y), (x2 - 6, y)], OK, "ok", 1.4)
    d.t((x1 + x2) / 2, y - 10, w, 12, OK, MONO, "middle", 600)
    y2 = RY[0] + 92
    d.arrow([(x2 - 4, y2), (x1 + 6, y2)], INFO, "info", 1.4)
    d.t((x1 + x2) / 2, y2 + 20, "<-ch", 12, INFO, MONO, "middle", 600)

# close: 열린 상태 → 닫힌 상태
bot0 = RY[0] + NH
d.arrow([(CX[0] + 110, bot0 + 4), (CX[0] + 110, RY[1] - 6)], MUTED, "ar", 1.4)
d.t(CX[0] + 120, bot0 + 52, "close", 12, MUTED, MONO, "start", 600)
d.arrow([(CX[1] + 80, bot0 + 4), (CX[1] + 80, RY[1] - 6)], MUTED, "ar", 1.4)
d.t(CX[1] + 70, bot0 + 52, "close", 12, MUTED, MONO, "end", 600)
d.arrow([(CX[2] + 110, bot0 + 4), (CX[2] + 110, bot0 + 48), (CX[1] + 160, bot0 + 48), (CX[1] + 160, RY[1] - 6)], MUTED, "ar", 1.4)
d.t(CX[2] + 40, bot0 + 38, "close", 12, MUTED, MONO, "middle", 600)
d.arrow([(CX[0] + 70, RY[2] - 4), (CX[0] + 70, RY[1] + NH + 6)], MUTED, "ar", 1.4)
d.t(CX[0] + 60, RY[2] - 40, "close", 12, MUTED, MONO, "end", 600)

# 닫힘 · 값 남음 → 닫힘 · 빔 (남은 값을 다 읽음)
ym = RY[1] + 62
d.arrow([(CX[1] - 4, ym), (CX[0] + NW + 6, ym)], ACC, "acc", 1.6)
d.t((CX[0] + NW + CX[1]) / 2, ym - 12, "다 읽음", 12, ACC, KR, "middle", 600)

# panic 으로 가는 길
d.arrow([(CX[1] + NW + 4, ym), (CX[2] - 6, ym)], BAD, "bad", 1.4)
d.t((CX[1] + NW + CX[2]) / 2, ym - 12, "쓰기·닫기", 12, BAD, KR, "middle", 600)
yb = RY[1] + NH + 48
d.arrow([(CX[0] + 170, RY[1] + NH + 4), (CX[0] + 170, yb), (CX[2] + 50, yb), (CX[2] + 50, RY[1] + NH + 6)], BAD, "bad", 1.4)
d.t((CX[1] + CX[1] + NW) / 2, yb - 10, "쓰기·닫기", 12, BAD, KR, "middle", 600)
yn = RY[2] + 62
d.arrow([(CX[1] + NW + 4, yn), (CX[2] + 160, yn), (CX[2] + 160, RY[1] + NH + 6)], BAD, "bad", 1.4)
d.t(CX[2] + 60, yn - 10, "close", 12, BAD, MONO, "middle", 600)

d.legend(RY[2] + NH + 24, [("값을 돌려줌 · 동작함", OK), ("상대를 기다림", INFO), ("영원히 멈춤", WARN), ("panic", BAD)])
d.save("12-01.channel-states.svg")
print("ok 12-01 states", W, H)
