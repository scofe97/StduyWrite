# 타입 스펙: type-data-flow — 열은 다섯 번의 명령, 행은 터미널 2(명령)·counter_table(맵)·터미널 1(폴링). 값이 열마다 변한다.
# 사실 출처: 추출본 src/ebpf2.txt 417~446행(Terminal 1/2 출력 표·sudo ls 의 execve 둘), 예제 저장소 chapter2/hello-map.py.
#   표의 명령 순서는 ls · ls · sudo ls · ls · sudo ls, 마지막 맵은 501→5, 0→2.
# 레이아웃 공식: label_col_w=120 · step_slot_w=152 · lane_h=104 · header_h=132 · node 128×72.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 920, 520
LABEL_W, SLOT, LANE_H, HEAD_H, NW, NH = 120, 152, 104, 132, 128, 72
d = D(W, H, "LEARNING EBPF · 02-01 §4", "명령 다섯 번이 UID 별 횟수가 된다",
      "터미널 2 에서 ls 가 세 번, sudo ls 가 두 번 실행된다. ls 는 UID 501 로 한 번, sudo ls 는 UID 501 의 sudo 와 UID 0 의 ls 로 두 번 execve 를 부른다. 그 결과 counter_table 은 501 이 5, 0 이 2 가 되고 터미널 1 의 루프가 2초마다 읽는다.",
      "sudo ls 는 UID 501 과 UID 0 에 하나씩 셉니다")

def cx(j): return LABEL_W + j*SLOT + SLOT/2
def top(k): return HEAD_H + k*LANE_H

# 레인 구분선과 라벨
for k, (a, b) in enumerate((("터미널 2", "명령"), ("맵", "counter_table"), ("터미널 1", "2초 폴링"))):
    y = top(k)
    d.line(24, y, W - 24, y, RULE, 0.8)
    d.t(LABEL_W/2 + 12, y + LANE_H/2 - 2, a, 12, MUTED, KR, "middle", 600)
    d.t(LABEL_W/2 + 12, y + LANE_H/2 + 14, b, 11, SOFT, MONO if b.isascii() else KR)
d.line(24, top(3), W - 24, top(3), RULE, 0.8)
d.line(LABEL_W, HEAD_H, LABEL_W, top(3), RULE, 0.8)
for j in range(5):
    d.chip(cx(j), 112, f"명령 {j+1}", MUTED, 11)

cmds = [("ls", ["execve · UID 501"]), ("ls", ["execve · UID 501"]),
        ("sudo ls", ["sudo · UID 501", "ls · UID 0"]), ("ls", ["execve · UID 501"]),
        ("sudo ls", ["sudo · UID 501", "ls · UID 0"])]
maps = [[("501", "1")], [("501", "2")], [("501", "3"), ("0", "1")], [("501", "4"), ("0", "1")], [("501", "5"), ("0", "2")]]
NY0, NY1 = top(0) + 16, top(1) + 16

# 화살표 먼저
for j in range(5):
    c = ACC if j == 2 else MUTED
    d.arrow([(cx(j), NY0 + NH + 4), (cx(j), NY1 - 4)], c, "acc" if j == 2 else "ar", 1.5)
for j in range(4):
    d.arrow([(cx(j) + NW/2 + 4, NY1 + NH/2), (cx(j+1) - NW/2 - 4, NY1 + NH/2)], MUTED, "ar", 1.3)
d.arrow([(cx(4), NY1 + NH + 4), (cx(4), top(2) + 12)], OK, "ok", 1.5)

for j, (cmd, subs) in enumerate(cmds):
    x = cx(j) - NW/2
    foc = j == 2
    if foc: d.tone(x, NY0, NW, NH, ACC, 6, "14", 1.4)
    else: d.box(x, NY0, NW, NH, PAPER2, RULE, 1.0)
    d.t(cx(j), NY0 + 24, cmd, 14, ACC if foc else INK, MONO, "middle", 600)
    for i, s in enumerate(subs):
        d.t(cx(j), NY0 + 44 + i*16, s, 11, INFO if "UID 0" in s else MUTED, MONO)
for j, rows in enumerate(maps):
    x = cx(j) - NW/2
    foc = j == 2
    if foc: d.tone(x, NY1, NW, NH, ACC, 6, "14", 1.4)
    else: d.box(x, NY1, NW, NH, PAPER2, RULE, 1.0)
    for i, (k, v) in enumerate(rows):
        c = INFO if k == "0" else INK
        d.t(cx(j), NY1 + 30 + i*22 if len(rows) > 1 else NY1 + 42, f"{k} → {v}", 14, c, MONO, "middle", 600)

x = cx(3) - NW/2; w = cx(4) + NW/2 - x
d.tone(x, top(2) + 12, w, 60, OK, 6, "14", 1.3)
d.t(x + w/2, top(2) + 36, "ID 501: 5   ID 0: 2", 14, OK, MONO, "middle", 600)
d.t(x + w/2, top(2) + 58, "2초마다 읽은 결과", 11, MUTED, KR)

d.legend(H - 56, [("root(UID 0) 항목", INFO), ("root 항목이 처음 생김", ACC), ("폴링 결과", OK)])
d.save("02-01.uid-counter.svg")
