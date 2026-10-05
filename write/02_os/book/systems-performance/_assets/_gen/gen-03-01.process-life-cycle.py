# 03-01 §7 — 프로세스 수명주기: 원서 그림 3.8 의 다섯 상태와 전이.
# 타입 스펙: type-state — 상태 다섯(Idle·ready-to-run·on-proc·sleep·zombie)과 라벨 붙은 전이.
#           축약: 곡선 대신 직각 경로(dd-lint 대각선 금지). on-proc → ready-to-run 은 위로 ㄷ자,
#           block·wakeup 은 아래 sleep 을 거치는 ㄷ자. 원서 그림이 이름을 붙이지 않은 두 전이는
#           본문 서술(런큐에서 차례를 기다림)에서 라벨을 가져왔다. focal 은 출구가 셋인 on-proc.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, INFO, OK, WARN, BAD, PAPER, PAPER2, RULE, KR, MONO

W, H = 976, 536
SW, SH, CY = 140, 52, 268          # 상태 상자 폭·높이, 가운데 줄 y
XS = {"idle": 96, "ready": 288, "proc": 512, "zombie": 736}   # 상자 왼쪽 x
SLEEP_X, SLEEP_Y = 368, 388

d = DK(W, H, "SYSTEMS PERFORMANCE · 03-01 §7",
       "프로세스 수명주기 — 다섯 상태와 전이",
       "생성된 프로세스는 Idle 을 거쳐 런큐(ready-to-run)에서 차례를 기다리고, CPU 위(on-proc)에서 선점·블록·종료 셋 중 하나로 나간다. 블록된 프로세스는 깨어나면 CPU 가 아니라 런큐로 돌아간다(원서 그림 3.8, 단순화).",
       "깨어난 프로세스는 런큐부터 다시 섭니다")

def state(key, x, y, name, sub, c=None):
    if c: d.tone(x, y, SW, SH, c, 8)
    else: d.box(x, y, SW, SH, PAPER2, RULE, 1.0, 8)
    d.t(x + SW / 2, y + 23, name, 14, c if c else INK, MONO, "middle", 600)
    d.t(x + SW / 2, y + 41, sub, 12, MUTED, KR)

top = CY - SH / 2
state("idle", XS["idle"], top, "Idle", "생성 직후")
state("ready", XS["ready"], top, "ready-to-run", "런큐에서 대기")
state("proc", XS["proc"], top, "on-proc", "CPU 에서 실행", ACC)
state("zombie", XS["zombie"], top, "zombie", "reap 대기")
state("sleep", SLEEP_X, SLEEP_Y, "sleep", "I/O 등으로 블록", INFO)

# 시작 점 → Idle (creation)
d.o.append(f'<circle cx="48" cy="{CY}" r="6" fill="{INK}"/>')
d.arrow([(56, CY), (XS["idle"] - 4, CY)], MUTED, "ar", 1.4)
d.t(48, CY - 20, "creation", 12, SOFT, MONO)
# Idle → ready
d.arrow([(XS["idle"] + SW, CY), (XS["ready"] - 4, CY)], MUTED, "ar", 1.4)
d.t((XS["idle"] + SW + XS["ready"]) / 2, CY - 12, "실행 가능", 12, SOFT, KR)
# ready → proc
d.arrow([(XS["ready"] + SW, CY), (XS["proc"] - 4, CY)], MUTED, "ar", 1.4)
d.t((XS["ready"] + SW + XS["proc"]) / 2, CY - 12, "차례가 옴", 12, SOFT, KR)
# proc → ready (위로 ㄷ자)
px, rx, yt = XS["proc"] + SW / 2, XS["ready"] + SW / 2, top - 52
d.arrow([(px, top), (px, yt), (rx, yt), (rx, top - 4)], WARN, "warn", 1.5)
d.t((px + rx) / 2, yt - 10, "preempted · time quantum expired", 13, WARN, MONO, "middle", 600)
# proc → sleep (block)
bx = XS["proc"] + 60
d.arrow([(bx, top + SH), (bx, SLEEP_Y + SH / 2), (SLEEP_X + SW + 4, SLEEP_Y + SH / 2)], INFO, "info", 1.5)
d.t(bx + 12, top + SH + 40, "block", 13, INFO, MONO, "start", 600)
# sleep → ready (wakeup)
wx = XS["ready"] + 32
d.arrow([(SLEEP_X - 0, SLEEP_Y + SH / 2), (wx, SLEEP_Y + SH / 2), (wx, top + SH + 4)], OK, "ok", 1.5)
d.t(wx - 12, top + SH + 40, "wakeup", 13, OK, MONO, "end", 600)
# proc → zombie (exit)
d.arrow([(XS["proc"] + SW, CY), (XS["zombie"] - 4, CY)], MUTED, "ar", 1.4)
d.t((XS["proc"] + SW + XS["zombie"]) / 2, CY - 12, "exit", 12, SOFT, MONO)
# zombie → 끝 점 (termination)
ex = XS["zombie"] + SW + 40
d.arrow([(XS["zombie"] + SW, CY), (ex - 12, CY)], MUTED, "ar", 1.4)
d.o.append(f'<circle cx="{ex}" cy="{CY}" r="8" fill="none" stroke="{INK}" stroke-width="1.4"/><circle cx="{ex}" cy="{CY}" r="5" fill="{INK}"/>')
d.t(ex, CY + 48, "termination", 12, SOFT, MONO)

d.legend(472, [("출구가 셋인 상태", ACC), ("CPU 를 내놓음", WARN), ("블록", INFO), ("깨어남", OK)])
d.save("03-01.process-life-cycle.svg")
