# 06-01 §4 — 컨테이너 state 는 셋뿐이고, 익숙한 이름들은 그 아래 reason 이다
# 본문: "state 는 위 표의 세 가지로 고정돼 있고, 저 익숙한 이름들은 그중 Waiting 이나
#        Terminated state 가 가진 reason 필드 값입니다."
#       "Terminated 는 이름일 뿐 성공/실패가 아니다 — exitCode·reason 이 정한다."
# 타입 스펙: type-state.md — 전이는 셋, 재시작은 Terminated → Waiting 로 되돌아간다.
#           reason 은 상태가 아니므로 전이 위에 칸으로 올리지 않고 각 state 아래 목록으로
#           내려 붙인다. 그 층 나눔이 곧 본문이 바로잡으려는 오해다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO
import ddx

W, H = 1000, 712
d = D(W, H, "KUBERNETES IN ACTION · 06-01",
      "컨테이너 state 는 셋뿐 — 나머지 이름은 전부 reason 이다",
      "state 는 Waiting·Running·Terminated 셋으로 고정돼 있다. CrashLoopBackOff·OOMKilled 처럼 "
      "STATUS 칸에서 보는 이름들은 state 가 아니라 그 state 의 reason 필드 값이다.",
      lead="Unknown 은 Pod phase 이지 컨테이너 state 가 아니다 — 둘을 혼동하기 쉽다")

CY, BW, BH = 250, 200, 84
WAIT, RUNN, TERM = 220, 500, 780
ZONE_Y = 336

ddx.band(d, 104, 656, "state 는 고정 목록이고 reason 은 kubelet 이 정의한다 — 외울 것은 층 구조뿐이다")

def state(cx, name, sub, c, focal=False):
    x, y = cx - BW // 2, CY - BH // 2
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{BW}" height="{BH}" rx="8" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y, BW, BH, PAPER2, c, 1.1, 8)
    d.t(cx, CY - 12, name, 14, ACC if focal else c, MONO, "middle", 600)
    d.t(cx, CY + 14, ddx.fit(sub, 11, BW - 16, name), 11, MUTED, KR)

d.o.append(f'<circle cx="72" cy="{CY}" r="6" fill="{INK}"/>')
d.path(f"M 82 {CY} L {WAIT-BW//2-10} {CY}", MUTED, 1.5, m="ar")
d.t(96, CY - 16, "시작", 11, MUTED, KR, "start")

state(WAIT, "Waiting", "시작을 기다린다", WARN)
state(RUNN, "Running", "프로세스가 돌고 있다", OK)
state(TERM, "Terminated", "프로세스가 끝났다", ACC, focal=True)

for a, b, lab in ((WAIT, RUNN, "프로세스 실행"), (RUNN, TERM, "프로세스 종료")):
    d.path(f"M {a+BW//2+6} {CY} L {b-BW//2-10} {CY}", MUTED, 1.5, m="ar")
    d.t((a + b) // 2, CY - 16, lab, 11, MUTED, KR)

d.path(f"M {TERM+BW//2+6} {CY} L 920 {CY}", MUTED, 1.4, m="ar")
d.o.append(f'<circle cx="940" cy="{CY}" r="8" fill="none" stroke="{MUTED}" stroke-width="1.4"/>')
d.o.append(f'<circle cx="940" cy="{CY}" r="5" fill="{MUTED}"/>')

# 재시작 — Terminated 에서 Waiting 으로 되돌아간다. 위로 돌려 긋는다.
BACK = CY - BH // 2 - 28
d.path(f"M {TERM} {CY-BH//2-6} L {TERM} {BACK} L {WAIT} {BACK} L {WAIT} {CY-BH//2-10}",
       WARN, 1.4, m="warn", dash="6 5")
d.t(500, BACK - 10, "↺ 재시작 (restartPolicy 허용 시) — 이때도 Pod phase 는 Running 그대로", 11, WARN, KR)

# reason 층 — state 가 아니므로 아래로 내려 붙인다
# 4 단짜리 Waiting 열이 가장 길다 — 존 높이는 그 열(34 + 4*40 + 3*8 = 218)에 맞춘다
d.o.append(f'<rect x="40" y="{ZONE_Y}" width="912" height="238" rx="8" '
           f'fill="{RULE}" fill-opacity="0.03" stroke="{RULE}" stroke-width="1.0"/>')
# ring_label 을 쓰면 안 된다 — 불투명 PAPER 마스크가 x=66..561 을 덮어 Waiting(220)·
# Running(500) 에서 내려오는 연결선을 끊는다(렌더에서 확인). 마스크 없는 캡션을 왼쪽
# 여백에 두되, 연결선 첫 열(220) 앞에서 끝나도록 짧게 자른다. 나머지 설명은 산문이 맡는다.
d.t(40, ZONE_Y - 14, "reason — state 가 아니다", 11, SOFT, KR, "start")

RW, RH = 216, 40
REASONS = {
    WAIT: [("ContainerCreating", "이미지 pull·볼륨 마운트", WARN),
           ("PodInitializing", "주 컨테이너 미시작 → 05-03", WARN),
           ("CrashLoopBackOff", "재시작 반복 → 06-02", WARN),
           ("ImagePullBackOff", "이미지를 못 받음", WARN)],
    RUNN: [("reason 없음", "돌고 있으면 그냥 Running", OK)],
    TERM: [("Completed", "exitCode 0 — 성공", OK),
           ("Error", "exitCode ≠ 0 — 실패", BAD),
           ("OOMKilled", "메모리 초과 · 137", BAD)],
}
for cx, items in REASONS.items():
    d.path(f"M {cx} {CY+BH//2+6} L {cx} {ZONE_Y+18}", RULE, 1.2, dash="4 5")
    for i, (name, sub, c) in enumerate(items):
        y = ZONE_Y + 34 + i * (RH + 8)
        d.box(cx - RW // 2, y, RW, RH, PAPER2, RULE, 1.0, 5)
        d.t(cx - RW // 2 + 12, y + 17, ddx.fit(name, 11, RW - 24, name), 11, c, MONO, "start", 600)
        d.t(cx - RW // 2 + 12, y + 32, ddx.fit(sub, 10, RW - 24, name), 10, SOFT, KR, "start")

d.t(36, 604, "kubectl get 의 STATUS 칸에 뜨는 이름이 대부분 이 reason 이다 — state 이름이 아니다.",
     12, MUTED, KR, "start")
d.t(36, 624, "Terminated 는 이름일 뿐 실패가 아니다 — 성공·실패는 exitCode 와 reason 이 정하고, "
             "reason 목록은 대표값이다.", 12, MUTED, KR, "start")
d.legend(672, [("시작 대기", WARN), ("정상", OK), ("실패", BAD),
               ("이름이 뜻을 정하지 않는 자리", ACC)])
d.save("06-01-state-reason-map.svg")
print("ok state-reason-map")
