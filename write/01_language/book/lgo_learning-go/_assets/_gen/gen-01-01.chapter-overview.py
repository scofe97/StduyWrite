# 01-01.chapter-overview — go mod init 한 번, 그 뒤로 fmt → vet → build 를 make 가 묶는다
# 본문 요구(01-01 「학습 목표」 지도 문단): "모듈을 한 번 만들고, 그 뒤로는 포맷·검사·빌드를 늘 같은 순서로
#           돌린다. 단계마다 무엇을 실행하고 무엇이 남는지를 같은 자리에 둔다" — 단계마다 같은 슬롯이 반복되는 형태다.
# 타입 스펙: type-process — lanes(명령·결과) × steps(모듈·포맷·검사·빌드). §2 공식의 구조
#           (label_col 140 · step_slot · lane_h · node 는 lane 안 8px 여백)를 따르되, 스타일 계약의 한글 13px
#           하한 때문에 step_slot_w 112 → 204, node_w 100 → 188 로 키웠다. viewBox 984 는 계약 범위 안이다.
# 사실 출처: Learning Go 2판 1장 「Making a Go Module」「go build」「go fmt」「go vet」「Makefiles」,
#           go1.25.1 darwin/arm64 로컬 실행(2026-09-27).
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, KR, MONO

LABEL_W, SLOT, PAD = 140, 204, 28
W = LABEL_W + 4 * SLOT + PAD        # 984
HEAD, LANE_H = 128, 84
NODE_W, NODE_H = 188, 68
H = 476


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def cx(j):
    return LABEL_W + 8 + j * SLOT + NODE_W // 2


def top(k):
    return HEAD + k * LANE_H


d = D(W, H, "PROCESS · 01-01 OVERVIEW",
      "모듈은 한 번, 그 뒤로는 fmt → vet → build",
      "Learning Go 1장의 작업 순서를 네 단계로 나눈 지도. go mod init 으로 모듈을 한 번 만들고, "
      "그 뒤로는 go fmt 가 포맷을 고치고 go vet 이 컴파일되는 버그를 잡고 go build 가 단일 바이너리를 만든다. "
      "Makefile 의 make 한 번이 뒤의 세 단계를 이 순서로 묶는다. 맨 아래 칩은 그 단계를 다루는 절이다.",
      lead="단계마다 위 칸이 실행할 명령, 아래 칸이 그 명령이 남기거나 잡는 것입니다.")

steps = ("1 모듈", "2 포맷", "3 검사", "4 빌드")
lanes = ("명령", "결과")
cmds = ("go mod init", "go fmt ./...", "go vet ./...", "go build")
cmd_subs = ("hello_world · 한 번", "빌드 전 · 커밋 전", "빌드 전", "이름은 모듈 이름")
outs = ("go.mod", "탭 들여쓰기 · 빈 줄 정리", "자리표시자 인자 누락", "hello_world")
out_subs = ("모듈 이름 · Go 버전 · 의존성", "중괄호 위치는 못 고침", "컴파일은 통과한 버그", "VM 없는 단일 바이너리")
tones = (INFO, OK, WARN, INFO)

for j, st in enumerate(steps):
    d.t(cx(j), 112, st, 14, MUTED, KR, "middle", 600)
for k, name in enumerate(lanes):
    d.line(LABEL_W, top(k), W - PAD, top(k), RULE, 0.8)
    d.t(24, top(k) + LANE_H // 2 + 5, name, 13, MUTED, KR, "start", 600)
d.line(LABEL_W, top(2), W - PAD, top(2), RULE, 0.8)
d.line(LABEL_W, HEAD, LABEL_W, top(2), RULE, 0.8)

for j in range(4):
    x = cx(j) - NODE_W // 2
    y0 = top(0) + 8
    d.box(x, y0, NODE_W, NODE_H)
    d.t(cx(j), y0 + 30, cmds[j], 13, INK, kr(cmds[j]), "middle", 600)
    d.t(cx(j), y0 + 52, cmd_subs[j], 12, MUTED, kr(cmd_subs[j]), "middle")
    d.arrow([(cx(j), y0 + NODE_H), (cx(j), top(1) + 8)], SOFT, "soft", 1.2)
    y1 = top(1) + 8
    d.tone(x, y1, NODE_W, NODE_H, tones[j], 6, "10", 1.0)
    d.t(cx(j), y1 + 30, outs[j], 13, tones[j], kr(outs[j]), "middle", 600)
    d.t(cx(j), y1 + 52, out_subs[j], 12, MUTED, kr(out_subs[j]), "middle")
    if j < 3:
        ya = y0 + NODE_H // 2
        d.arrow([(cx(j) + NODE_W // 2, ya), (cx(j + 1) - NODE_W // 2, ya)], SOFT, "soft", 1.2)

# make 가 묶는 구간 — 2~4 단계 아래 괄호
bx1, bx2, by = cx(1) - NODE_W // 2, cx(3) + NODE_W // 2, 328
d.line(bx1, by - 16, bx1, by, ACC, 1.4)
d.line(bx2, by - 16, bx2, by, ACC, 1.4)
d.line(bx1, by, bx2, by, ACC, 1.4)
d.t((bx1 + bx2) / 2, by + 24, "make · fmt → vet → build", 14, ACC, MONO, "middle", 600)

for j, sec in enumerate(("§2", "§4", "§5", "§3")):
    d.chip(cx(j), 392, sec, MUTED, 12)

d.legend(420, [("남는 파일", INFO), ("자동으로 고침", OK), ("잡아서 알림", WARN), ("make 가 묶는 순서", ACC)])
d.save("01-01.chapter-overview.svg")
print("ok chapter-overview")
