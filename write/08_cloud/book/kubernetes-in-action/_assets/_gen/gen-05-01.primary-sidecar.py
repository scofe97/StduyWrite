# 05-01 §5 — 사이드카는 주 컨테이너를 보완한다
# 본문: "주(primary) 프로세스 하나와 그 동작을 보완하는 프로세스 하나 이상으로 이뤄질 때만
#        적절합니다 ... Pod 는 사이드카를 여럿 둘 수 있습니다."
#       예 둘 — 프로토콜 변환 프록시(HTTPS → HTTP)와 콘텐츠 전달 에이전트(볼륨 공유).
#       "사이드카는 특정 메인 컨테이너 하나에 종속돼, 메인이 3개로 늘면 사이드카도 정확히 3개"
# 타입 스펙: type-nested.md — Pod 라는 경계 안에 무엇이 들어가는가가 요점이라 경계 링.
#           옛 판은 빈 상자 둘만 그려 사이드카가 *무엇으로* 보완하는지를 못 보여줬다.
#           보완의 통로 둘(localhost · 공유 볼륨)이 05-01 §3 의 공유·격리와 그대로 이어진다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO
import ddx

W, H = 1000, 596
d = D(W, H, "KUBERNETES IN ACTION · 05-01",
      "사이드카는 두 통로로 주 컨테이너를 보완한다",
      "Network 를 공유하니 localhost 로 넘길 수 있고, Mount 는 격리라 파일은 공유 볼륨을 "
      "걸어야 오간다. 코드를 고치지 않고 기능을 붙이는 것이 이 패턴의 값이다.",
      lead="사이드카는 메인과 1:1 로 늘어난다 — 따로 늘리고 싶어지면 별도 Pod 다")

RING = (56, 196, 888, 252)
MAIN = (250, 322)
SIDE_A, SIDE_B = (700, 262), (700, 384)
MW, MH = 220, 116
SW, SH = 300, 92

ddx.band(d, 104, 540, "코드를 못 고치는 레거시일수록 프로세스를 하나 더 붙이는 쪽이 싸고 빠르다")

rx, ry, rw, rh = RING
d.o.append(f'<rect x="{rx}" y="{ry}" width="{rw}" height="{rh}" rx="8" '
           f'fill="{INFO}06" stroke="{INFO}" stroke-width="1.2" stroke-dasharray="7 6"/>')
ddx.ring_label(d, rx, ry, "Pod — 한 단위로 스케줄되고 함께 늘어난다", 11, INFO, off=16)

d.o.append(f'<rect x="{MAIN[0]-MW//2}" y="{MAIN[1]-MH//2}" width="{MW}" height="{MH}" rx="6" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(MAIN[0], MAIN[1] - 20, "주 컨테이너", 14, ACC, KR, "middle", 600)
d.t(MAIN[0], MAIN[1] + 4, "주 애플리케이션 프로세스", 11, MUTED, KR)
d.t(MAIN[0], MAIN[1] + 28, "코드를 건드리지 않는다", 10, SOFT, KR)

def sidecar(cx, cy, title, sub, tag):
    d.box(cx - SW // 2, cy - SH // 2, SW, SH, PAPER2, OK, 1.1, 6)
    d.t(cx, cy - 16, ddx.fit(title, 13, SW - 18, title), 13, OK, KR, "middle", 600)
    d.t(cx, cy + 6, ddx.fit(sub, 11, SW - 16, title), 11, MUTED, KR)
    d.t(cx, cy + 28, ddx.fit(tag, 10, SW - 14, title), 10, SOFT, KR)

sidecar(*SIDE_A, "리버스 프록시", "HTTPS 를 받아 HTTP 로 바꾼다", "레거시 앱에 TLS 를 붙인다")
sidecar(*SIDE_B, "콘텐츠 에이전트", "주기적으로 내려받아 webroot 에 쓴다", "웹 서버는 서빙만 한다")

# 보완의 통로 둘 — 꺾는 열을 갈라 세로 구간이 겹치지 않게 한다
d.path(f"M {SIDE_A[0]-SW//2-6} {SIDE_A[1]} L 480 {SIDE_A[1]} L 480 {MAIN[1]-20} "
       f"L {MAIN[0]+MW//2+8} {MAIN[1]-20}", OK, 1.5, m="ok")
d.t(426, MAIN[1] - 32, "localhost:<포트>", 11, OK, MONO)
d.path(f"M {SIDE_B[0]-SW//2-6} {SIDE_B[1]} L 424 {SIDE_B[1]} L 424 {MAIN[1]+20} "
       f"L {MAIN[0]+MW//2+8} {MAIN[1]+20}", OK, 1.5, m="ok")
d.t(388, MAIN[1] + 40, "공유 볼륨", 11, OK, KR)

d.t(36, 512, "Network 공유가 첫 통로를 열고, Mount 격리가 둘째 통로에 볼륨을 요구한다 — "
             "§3 의 공유·격리 표가 그대로 이 패턴의 근거다", 12, MUTED, KR, "start")
d.legend(556, [("Pod 경계", INFO), ("주 컨테이너", ACC), ("보완하는 쪽과 그 통로", OK)])
d.save("05-01-primary-sidecar.svg")
print("ok primary-sidecar")
