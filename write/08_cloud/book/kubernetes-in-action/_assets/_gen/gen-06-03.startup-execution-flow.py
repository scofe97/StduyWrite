# 06-03 §5 — 컨테이너 실행 단계 (이미지 pull → PostStart → probe → 재시작)
# 본문: "컨테이너별로 이미지 pull → 컨테이너 시작(PostStart hook 병렬 실행) → startup probe → liveness probe 순서"
#       "startup probe 를 정의했다면 성공한 뒤에야 liveness 로 넘어가고, 정의하지 않았다면 곧장 liveness 를 시작"
#       "failureThreshold 도달 시 컨테이너 종료 · restartPolicy(Always/OnFailure 재시작, Never 는 Terminated)"
# 타입 스펙: type-flowchart.md — 타원(시작/끝), 사각형(단계), 마름모(startup probe · restartPolicy 판정), 점(합류).
#           startup probe 관문이 liveness 감시 시작을 가르는 핵심 분기라 그 마름모만 focal.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO
import ddx

W, H = 1000, 816
d = D(W, H, "KUBERNETES IN ACTION · 06-03",
      "컨테이너 실행 — startup probe 성공 뒤 liveness 감시",
      "이미지 pull 후 컨테이너가 시작되며 PostStart hook 이 병렬로 돈다. startup probe 가 있으면 성공까지 "
      "liveness 를 유예하고, failureThreshold 도달 시 restartPolicy 에 따라 재시작하거나 Terminated 로 남는다.",
      lead="init 컨테이너 완료 뒤 일반 컨테이너마다 진행 · 선언 순서가 시작 순서를 보장하지 않음")

ddx.band(d, 104, 756, "컨테이너별 시작·감시·재시작 분기 (Always/OnFailure → 재시작 · Never → Terminated)")

def oval(cx, cy, w, h, txt, c):
    d.o.append(f'<rect x="{cx-w//2}" y="{cy-h//2}" width="{w}" height="{h}" rx="{h//2}" '
               f'fill="{c}14" stroke="{c}" stroke-width="1.2"/>')
    d.t(cx, cy + 5, ddx.fit(txt, 13, w - 20, txt), 13, c, KR, "middle", 600)

def step(cx, cy, w, h, title, sub, c):
    d.box(cx - w // 2, cy - h // 2, w, h, PAPER2, c, 1.1, 6)
    d.t(cx, cy - 8, ddx.fit(title, 13, w - 16, title), 13, c, KR, "middle", 600)
    d.t(cx, cy + 14, ddx.fit(sub, 11, w - 16, sub), 11, MUTED, KR)

PULL = (460, 168, 220, 44)
START = (460, 248, 340, 56)
SP_DIA = (460, 340, 120, 38)
SP_WAIT = (776, 340, 260, 56)
MERGE = (460, 424)
LIVE = (460, 492, 300, 56)
TERM = (460, 588, 260, 52)
RP_DIA = (460, 680, 120, 38)
DEAD = (800, 680, 220, 44)

oval(*PULL, "이미지 pull", INFO)
d.path(f"M {PULL[0]} {PULL[1]+22+4} L {PULL[0]} {START[1]-28-6}", MUTED, 1.5, m="ar")

step(*START, "컨테이너 시작 · PostStart 병렬", "kubelet 은 hook 종료까지 시작 관리 대기", INFO)
d.path(f"M {START[0]} {START[1]+28+4} L {START[0]} {SP_DIA[1]-SP_DIA[3]-6}", MUTED, 1.5, m="ar")

# Diamond 1: startup probe defined?
dx, dy = SP_DIA[2], SP_DIA[3]
d.o.append(f'<path d="M {SP_DIA[0]} {SP_DIA[1]-dy} L {SP_DIA[0]+dx} {SP_DIA[1]} L {SP_DIA[0]} {SP_DIA[1]+dy} '
           f'L {SP_DIA[0]-dx} {SP_DIA[1]} Z" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(SP_DIA[0], SP_DIA[1] + 5, "startup probe 정의?", 12, ACC, KR, "middle", 600)

# Yes -> startup probe wait -> merge dot
d.path(f"M {SP_DIA[0]+dx+4} {SP_DIA[1]} L {SP_WAIT[0]-130-6} {SP_DIA[1]}", OK, 1.5, m="ok")
d.chip(612, SP_DIA[1], "예", OK, 11)
step(*SP_WAIT, "startup probe 대기", "성공까지 liveness 실행 유예", OK)
d.path(f"M {SP_WAIT[0]} {SP_WAIT[1]+28+4} L {SP_WAIT[0]} {MERGE[1]} L {MERGE[0]+10} {MERGE[1]}", OK, 1.5, m="ok")

# No -> merge dot
d.path(f"M {SP_DIA[0]} {SP_DIA[1]+dy+4} L {SP_DIA[0]} {MERGE[1]-10}", MUTED, 1.5, m="ar")
d.chip(396, 396, "아니오", MUTED, 11)
d.o.append(f'<circle cx="{MERGE[0]}" cy="{MERGE[1]}" r="5" fill="{INK}"/>')

# Merge -> liveness probe
d.path(f"M {MERGE[0]} {MERGE[1]+6} L {MERGE[0]} {LIVE[1]-28-6}", OK, 1.5, m="ok")
step(*LIVE, "liveness probe 주기적 감시", "성공 유지 시 컨테이너 실행 지속", OK)

# Self loop: 성공 유지 (right side of LIVE)
lx = LIVE[0] + LIVE[2] // 2
d.path(f"M {lx+4} {LIVE[1]-12} L {lx+52} {LIVE[1]-12} L {lx+52} {LIVE[1]+12} L {lx+10} {LIVE[1]+12}", OK, 1.4, m="ok")
d.t(lx + 62, LIVE[1] + 4, "성공 유지", 11, OK, KR, "start")

# liveness -> failureThreshold -> terminated
d.path(f"M {LIVE[0]} {LIVE[1]+28+4} L {LIVE[0]} {TERM[1]-26-6}", BAD, 1.5, m="bad")
d.t(LIVE[0] + 12, 542, "failureThreshold 도달", 11, BAD, KR, "start")
step(*TERM, "컨테이너 종료", "재시작 정책 판정으로 이동", BAD)
d.path(f"M {TERM[0]} {TERM[1]+26+4} L {TERM[0]} {RP_DIA[1]-RP_DIA[3]-6}", MUTED, 1.5, m="ar")

# Diamond 2: restartPolicy?
rx, ry = RP_DIA[2], RP_DIA[3]
d.o.append(f'<path d="M {RP_DIA[0]} {RP_DIA[1]-ry} L {RP_DIA[0]+rx} {RP_DIA[1]} L {RP_DIA[0]} {RP_DIA[1]+ry} '
           f'L {RP_DIA[0]-rx} {RP_DIA[1]} Z" fill="{PAPER2}" stroke="{WARN}" stroke-width="1.2"/>')
d.t(RP_DIA[0], RP_DIA[1] + 5, "restartPolicy 허용?", 12, WARN, KR, "middle", 600)

# Always / OnFailure -> left-margin retry loop back to PULL
d.path(f"M {RP_DIA[0]-rx-4} {RP_DIA[1]} L 112 {RP_DIA[1]} L 112 {PULL[1]} L {PULL[0]-110-8} {PULL[1]}",
       INFO, 1.5, m="info", dash="6 5")
d.chip(224, RP_DIA[1], "Always · OnFailure", INFO, 11)

# Never -> Terminated
d.path(f"M {RP_DIA[0]+rx+4} {RP_DIA[1]} L {DEAD[0]-110-6} {RP_DIA[1]}", WARN, 1.5, m="warn")
d.chip(634, RP_DIA[1], "Never", WARN, 11)
oval(*DEAD, "Terminated 유지", WARN)

d.t(36, 738, "예외: restartPolicy 가 Never 일 때 PostStart 실패 시 Pod 상태는 Completed 표시",
     12, MUTED, KR, "start")
d.legend(772, [("시작 · 재시작", INFO), ("startup 관문", ACC), ("정상 감시", OK),
               ("실패 종료", BAD), ("재시작 안 함", WARN)])
d.save("06-03-startup-execution-flow.svg")
print("ok startup-execution-flow")
