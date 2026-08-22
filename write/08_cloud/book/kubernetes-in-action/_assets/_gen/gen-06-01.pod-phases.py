# 06-01 §2 — Pod 는 생애의 어느 순간이든 다섯 phase 중 하나에 있다
# 본문: "Pod 는 생애의 어느 순간이든 다섯 phase 중 하나에 있습니다" + Pending → Running →
#       Succeeded/Failed 의 일반적 흐름. Unknown 은 흐름 위의 한 칸이 아니라 kubelet 보고가
#       끊길 때 어느 phase에서든 일어나는 일이다.
# 타입 스펙: type-state.md — 관례형(§2 공식 없음)이라 stride 를 4의 배수로 고정한다.
#           시작은 채운 점 r=6, 끝은 고리 점(바깥 r=8 윤곽 + 안 r=5 채움), 상자는 rx=8.
#           안티패턴 "From any state 를 모든 상태에서 그리기" 를 피해 Unknown 은 화살표를
#           흩뿌리지 않고 `* 어느 phase에 있든` 주석 한 줄로 흐름 밖에 둔다.
# 연결선은 저장소 관례대로 직각으로만 꺾는다 — 이 책 149 장이 그 방식이고 dd-lint 가 그것을 강제한다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO
import ddx

W, H = 1000, 624
d = D(W, H, "KUBERNETES IN ACTION · 06-01",
      "Pod 는 어느 순간이든 다섯 phase 중 하나에 있다",
      "Pending 에서 시작해 Running 을 거쳐 Succeeded 또는 Failed 로 끝난다. Unknown 은 흐름 위의 "
      "한 칸이 아니라 kubelet 보고가 끊길 때 어느 phase에서든 일어나는 일이다.",
      lead="Pending → Running → Succeeded 또는 Failed · Unknown 은 흐름 밖에 있다")

BW, BH = 176, 88
CY = 264
PEND, RUN = (216, CY), (488, CY)
SUCC, FAIL = (792, 196), (792, 332)
UNKN = (792, 464)
SPINE = 624

def state(cx, cy, name, sub, tag, c, focal=False):
    x, y = cx - BW // 2, cy - BH // 2
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{BW}" height="{BH}" rx="8" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y, BW, BH, PAPER2, c, 1.1, 8)
    d.t(cx, cy - 18, name, 14, ACC if focal else c, MONO, "middle", 600)
    d.t(cx, cy + 4, ddx.fit(sub, 11, BW - 16, f"{name} sub"), 11, MUTED, KR)
    d.t(cx, cy + 26, ddx.fit(tag, 10, BW - 14, f"{name} tag"), 10, SOFT, KR)

ddx.band(d, 104, 568, "phase 는 한 단어 요약이다 — 정밀한 판단은 conditions 와 컨테이너 state 로 내려간다")

# 시작점 — 채운 점
d.o.append(f'<circle cx="56" cy="{CY}" r="6" fill="{INK}"/>')
d.path(f"M 66 {CY} L 120 {CY}", MUTED, 1.5, m="ar")
d.t(90, CY - 16, "오브젝트 생성", 11, MUTED, KR)

state(*PEND, "Pending", "노드 배정·이미지 pull", "컨테이너가 시작될 때까지", INFO)
state(*RUN, "Running", "모든 컨테이너 생성됨", "최소 하나가 실행·재시작 중", INFO, focal=True)
state(*SUCC, "Succeeded", "모든 컨테이너 성공 종료", "무한정 돌 의도가 아닌 Pod", OK)
state(*FAIL, "Failed", "하나 이상 실패로 종료", "무한정 돌 의도가 아닌 Pod", BAD)

d.path(f"M {PEND[0]+BW//2+6} {CY} L {RUN[0]-BW//2-8} {CY}", MUTED, 1.5, m="ar")
d.t(352, CY - 16, "주 컨테이너 시작", 11, MUTED, KR)

# 부채꼴 — 중립 줄기 + 도착 상태 색을 쓴 팔
d.path(f"M {RUN[0]+BW//2+6} {CY} L {SPINE} {CY}", MUTED, 1.4)
d.path(f"M {SPINE} {SUCC[1]} L {SPINE} {FAIL[1]}", MUTED, 1.4)
for (cx, cy), c, mk, lab, ly in ((SUCC, OK, "ok", "모두 성공", 180),
                                 (FAIL, BAD, "bad", "하나라도 실패", 352)):
    d.path(f"M {SPINE} {cy} L {cx-BW//2-6} {cy}", c, 1.5, m=mk)
    d.t(661, ly, lab, 11, c, KR)
    d.path(f"M {cx+BW//2+6} {cy} L {cx+BW//2+40} {cy}", c, 1.4, m=mk)
    d.o.append(f'<circle cx="932" cy="{cy}" r="8" fill="none" stroke="{c}" stroke-width="1.4"/>')
    d.o.append(f'<circle cx="932" cy="{cy}" r="5" fill="{c}"/>')

# Unknown — 흐름 위의 칸이 아니라 어느 phase에서든 일어나는 일
d.o.append(f'<rect x="48" y="404" width="904" height="120" rx="8" '
           f'fill="{WARN}06" stroke="{WARN}" stroke-width="1.2" stroke-dasharray="7 6"/>')
ddx.ring_label(d, 48, 404, "흐름 밖 — 어느 phase에서든 일어난다", 11, WARN, off=16)
d.chip(176, UNKN[1], "* 어느 phase에 있든", WARN, 11)
d.path(f"M 270 {UNKN[1]} L {UNKN[0]-BW//2-6} {UNKN[1]}", WARN, 1.4, m="warn")
d.t(484, UNKN[1] - 16, "kubelet 이 API 서버 보고를 멈추면", 11, WARN, KR)
state(*UNKN, "Unknown", "kubelet 보고 두절", "노드 장애·네트워크 단절", WARN)

d.t(36, 548, "phase 는 엄밀한 상태 머신이 아니라 한 단어 요약이다 — Succeeded·Failed 는 "
             "무한정 돌 의도가 아닌 Pod 에만 해당한다", 12, MUTED, KR, "start")
d.legend(584, [("도달 중", INFO), ("성공 종료", OK), ("실패 종료", BAD),
               ("보고 두절", WARN), ("본문이 짚는 자리", ACC)])
d.save("06-01-pod-phases.svg")
print("ok pod-phases")
