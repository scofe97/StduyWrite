# 10-01.toolchain-choice — go.mod 의 go 줄이 설치된 Go 보다 새로울 때 무엇으로 빌드하나
# 본문 요구(10-01 §3 「go 지시어로 빌드할 Go 버전을 다룹니다」): Go 1.20 이하가 설치돼 있으면 새 go 줄을 무시하고 설치된 버전으로 빌드한다.
#           Go 1.21 이상이면 GOTOOLCHAIN(설정돼 있으면 toolchain 지시어보다 우선)에 따라 갈린다. local 은 설치된 Go 만 써서 오류로 멈추고,
#           특정 버전은 그 버전으로 바꾸되 go 줄보다 낮으면(1.21 이상) local 처럼 멈추고, 기본 auto 는 go 줄이 요구한 버전을 내려받아 빌드한다.
#           local 의 동작은 원문이 아니라 노트의 go1.25.1 실행과 공식 툴체인 문서를 따른다(본문 원문 정오).
# 타입 스펙: type-flowchart — 09-01.error-choice 와 같은 골격(시작 타원, 판단 마름모, 결과 사각, 끝 타원).
#           예는 오른쪽 결과로, 아니오는 아래로. stride 세로 96, 판단 열 중심 x 256, 결과 열 x 536.
#           coral 은 오류로 멈추는 local 결과 하나.
# 사실 출처: Learning Go 2판 10장 「Use the go Directive to Manage Go Build Versions」, go1.25.1 로컬 실행(2026-09-27) —
#           GOTOOLCHAIN=local 과 GOTOOLCHAIN=go1.25.1 모두 go 1.26.0 모듈에서 go.mod requires go >= 1.26.0 (running go 1.25.1).
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, PAPER2, KR, MONO

W, H = 984, 596
CX, RX, RW, RH = 256, 536, 400, 48
DW, DH = 344, 60
START_Y, STRIDE = 112, 96
Q_Y = [START_Y + 88 + i * STRIDE for i in range(3)]     # 200 296 392
END_Y = Q_Y[-1] + DH // 2 + 48


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def diamond(cx, cy, text):
    pts = f"{cx},{cy - DH // 2} {cx + DW // 2},{cy} {cx},{cy + DH // 2} {cx - DW // 2},{cy}"
    d.o.append(f'<polygon points="{pts}" fill="{PAPER2}" stroke="rgba(191,192,192,0.22)" stroke-width="0.9"/>')
    d.t(cx, cy + 5, text, 13, INK, kr(text), "middle", 600)


def result(y, main, sub, c):
    d.tone(RX, y - RH // 2, RW, RH, c, 6, "10", 1.0 if c != ACC else 1.4)
    d.t(RX + 16, y - 2, main, 14, c, kr(main), "start", 600)
    d.t(RX + 16, y + 16, sub, 12, MUTED, kr(sub), "start")


d = D(W, H, "FLOWCHART · 10-01 §3",
      "go 줄이 더 새로우면 무엇으로 빌드할까",
      "go.mod 의 go 줄이 설치된 Go 보다 새 버전을 요구할 때의 판단 순서. Go 1.20 이하가 설치돼 있으면 그 줄을 무시하고 설치된 버전으로 빌드한다. "
      "1.21 이상이면 GOTOOLCHAIN 을 본다. local 이면 설치된 Go 만 쓰므로 오류로 멈춘다. 특정 버전이면 그 버전으로 바꾸는데, 그 버전도 go 줄보다 낮으면 같은 오류로 멈춘다. "
      "기본값 auto 는 go 줄이 요구한 버전을 내려받아 빌드한다.",
      lead="local 과 특정 버전은 toolchain 줄보다 우선하고, 기본 auto 는 toolchain 줄도 따릅니다. 두 오류 경로는 노트가 실행으로 확인했습니다.")

d.o.append(f'<rect x="{CX - 144}" y="{START_Y}" width="288" height="40" rx="20" fill="{PAPER2}" stroke="rgba(191,192,192,0.22)" stroke-width="0.9"/>')
d.t(CX, START_Y + 25, "go 줄이 설치된 Go 보다 새로움", 13, INK, KR, "middle", 600)
d.arrow([(CX, START_Y + 40), (CX, Q_Y[0] - DH // 2)], SOFT, "soft", 1.2)

qs = [("설치된 Go 가 1.20 이하?", ("go 줄을 무시하고 빌드", "go 1.N 두 자리 줄일 때", WARN)),
      ("GOTOOLCHAIN=local?", ("오류로 멈춤", "go.mod requires go >= 1.26.0", ACC)),
      ("GOTOOLCHAIN=go1.x.y 같은 버전?", ("그 버전으로 바꿔 빌드", "go 줄보다 낮으면 오류로 멈춤", INFO))]
for i, (q, (m, s, c)) in enumerate(qs):
    y = Q_Y[i]
    diamond(CX, y, q)
    d.arrow([(CX + DW // 2, y), (RX, y)], SOFT, "soft", 1.2)
    d.t(CX + DW // 2 + 32, y - 8, "예", 12, MUTED, KR, "middle")
    result(y, m, s, c)
    nxt = Q_Y[i + 1] - DH // 2 if i < 2 else END_Y
    d.arrow([(CX, y + DH // 2), (CX, nxt)], SOFT, "soft", 1.2)
    d.t(CX + 12, y + DH // 2 + 22, "아니오", 12, MUTED, KR, "start")

d.o.append(f'<rect x="{CX - 132}" y="{END_Y}" width="264" height="44" rx="20" fill="{OK}14" stroke="{OK}" stroke-width="1.2"/>')
d.t(CX, END_Y + 28, "auto: 요구한 버전을 받아 빌드", 13, OK, KR, "middle", 600)
d.t(CX + 148, END_Y + 28, "Go 1.21 이후의 기본 동작", 12, MUTED, KR, "start")

d.legend(540, [("1.20 이하의 동작", WARN), ("특정 버전", INFO), ("기본 auto", OK), ("오류로 멈춤", ACC)])
d.save("10-01.toolchain-choice.svg")
print("ok 10-01 toolchain-choice")
