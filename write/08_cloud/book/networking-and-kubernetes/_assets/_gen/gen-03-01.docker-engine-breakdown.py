# 03-01.docker-engine-breakdown — runC 는 떠나고 shim 이 남는다
# 본문 요구: 세 구간 — 위임 / 생성 / runC 소멸·shim 존속
# 타입 스펙: type-sequence.md — 레인의 '끝나는 지점'이 요점이므로 runC 레일을 중간에서 끊고
#           shim 레일만 끝까지 잇는다. 존속하는 막대 하나가 이 도식의 focal.
import dd, ddx
from dd import D, Seq, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 700
d = Seq(W, H, "docker ENGINE · runC LEAVES, shim STAYS",
        "runC 는 컨테이너를 띄우고 떠나고, containerd-shim 이 부모로 남는다",
        "runC 의 레일은 가운데에서 끊기고 shim 의 레일만 끝까지 이어진다. 그것이 컨테이너의 부모가 누구인지를 말한다.",
        lead="runC 레일은 가운데에서 끊기고 shim 레일만 끝까지 간다")

LX = ddx.lanes(d, [("dockerd", "요청을 받는다"), ("containerd-shim", "부모로 남는다"),
                   ("runC", "만들고 떠난다"), ("컨테이너", "프로세스")], y0=104, lane_w=196)
DK, SH, RC, PR = (int(LX[k]) for k in ("dockerd", "containerd-shim", "runC", "컨테이너"))
SEGS = [(164, 268, "① dockerd → containerd 위임"),
        (284, 428, "② 컨테이너 생성"),
        (444, 572, "③ runC 는 떠나고 shim 은 남는다")]
Y_END = 596
for a, b, lab in SEGS: ddx.band(d, a, b, lab)
# 레일을 직접 그린다 — runC 만 기동 완료 지점에서 끊는다.
# 덮어 가리면 띠 배경과 색이 어긋나 어두운 막대로 보인다.
RC_END = 500
for x in (DK, SH, PR):
    d.line(x, d.lane_top + 6, x, Y_END, RULE, 1.0, "3 6")
d.line(RC, d.lane_top + 6, RC, RC_END, RULE, 1.0, "3 6")
d.line(RC - 14, RC_END, RC + 14, RC_END, BAD, 1.8)
d.t(RC, RC_END + 22, "여기서 종료", 11, BAD, KR)
# shim 은 끝까지 산다
d.o.append(f'<rect x="{SH-4}" y="200" width="8" height="{Y_END-200}" rx="3" '
           f'fill="{ACC}33" stroke="{ACC}" stroke-width="1.0"/>')

def msg(a, b, y, label, c, mk, dash=None):
    dirn = 1 if b > a else -1
    d.path(f"M {a+10*dirn} {y} L {b-12*dirn} {y}", c, 1.5, m=mk, dash=dash)
    d.t((a + b) // 2, y - 12, label, 11, c, KR, "middle", 600)

msg(DK, SH, 226, "containerd 경유 · shim 기동", INFO, "info")
msg(SH, RC, 336, "컨테이너 생성 지시", INFO, "info")
msg(RC, PR, 392, "cgroup·namespace 생성", INFO, "info")
msg(RC, SH, 480, "기동 완료 후 종료", MUTED, "ar", "6 5")
msg(SH, PR, 552, "부모로 남아 stdio 유지", ACC, "acc")

d.t(36, 616, "컨테이너의 부모는 runC 가 아니라 shim 이다 — dockerd 를 재시작해도 컨테이너가 "
             "살아 있는 이유가 이 막대 하나다", 12, MUTED, KR, "start")
d.legend(Y_END + 44, [("호출", INFO), ("끝까지 남는 부모", ACC), ("여기서 종료", BAD)])
d.save("03-01.docker-engine-breakdown.svg")
print("ok docker-engine-breakdown")
