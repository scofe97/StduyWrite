# 02-01 §2 — 호출자의 uid 를 커널에 묻고 entry 와 대조하는 한 번의 요청.
# 타입 스펙: type-sequence — 프로세스·agent·커널 세 레인 사이를 시간 순으로 오가는 메시지가
#           본체다. 같은 요청에서 uid 가 다르면 마지막 응답만 갈린다는 점이 논점이라 시퀀스를 쓴다.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, BAD, OK, KR, MONO

W, H = 880, 548
d = Seq(W, H, "LAMPSON LAB · 02-01 §2",
        "호출자는 요청이 아니라 커널이 알려 준다",
        "agent 는 소켓 반대편 프로세스의 uid 를 커널에 묻고 entry 와 맞춘다. 같은 요청에서 uid 가 달라지면 응답만 갈린다.",
        "요청에는 신원이 없고, uid 는 프로세스가 고를 수 없다")

d.lanes([("프로세스", "deployer · uid 1001"), ("spire-agent", "Workload API"), ("커널", "소켓 반대편")], y0=104, lane_w=210)
d.rails(498)

d.msg("프로세스", "spire-agent", "FetchX509SVID", 190, MUTED, "ar", sub="신원을 적는 칸이 없다")
d.msg("spire-agent", "커널", "호출자 uid?", 240, ACC, "acc", sub="소켓 반대편 프로세스")
d.msg("커널", "spire-agent", "uid 1001", 288, MUTED, "ar")
d.selfmsg("spire-agent", "entry 대조", 336, MUTED, sub="unix:uid:1001")
d.msg("spire-agent", "프로세스", "SVID + 개인키", 384, OK, "ok", sub="spiffe://lab/client/deployer")

d.line(24, 424, W - 24, 424, "rgba(191,192,192,0.22)", 0.8, "4 4")
d.t(W / 2, 446, "같은 요청을 intruder(uid 1004)가 하면", 11, SOFT, KR, "middle")
d.msg("spire-agent", "프로세스", "PermissionDenied", 484, BAD, "bad", sub="no identity issued")

d.t(24, 530, "응답이 갈리는 곳은 entry 표 한 곳이다 — uid 1004 의 행이 없다", 12, ACC, KR, "start", 600)
d.save("02-01.workload-attest.svg")
